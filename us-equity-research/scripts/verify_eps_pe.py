#!/usr/bin/env python3
"""
verify_eps_pe.py — Phase C gate G1 verifier (EPS × multiple multiplicativity).

For every scenario row in the 5-scenario block, verify:
    abs(eps * multiple - target_price) / abs(target_price) <= 0.005   (±0.5%)

Owns bug B01 (base.target_price corrupted 190 -> 200).

Usage:
    python scripts/verify_eps_pe.py --memo-json <path/to/memo.json> [--memo-md <path>]

Exit codes:
    0 — gate passes
    1 — gate fails (at least one scenario violates tolerance)
    2 — usage / IO error

Reads either:
    - a full memo JSON with `scenarios_inline.scenarios[...]`, or
    - a standalone scenarios.json with top-level `scenarios[...]`.

Self-contained per Phase-C pre-stagger discipline: stdlib + pydantic v2 only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError

GATE_ID = "G1"
TOL_PCT = 0.005  # 0.5% relative tolerance per gate definition


class Scenario(BaseModel):
    """Minimal slice of a scenario row required for G1."""

    model_config = ConfigDict(extra="ignore")

    id: str
    probability: float | None = None
    eps: float
    multiple: float
    target_price: float = Field(..., ge=0)


def locate_scenarios(payload: dict) -> list[dict]:
    """Return the scenario list, supporting both memo and standalone shapes."""
    if isinstance(payload.get("scenarios_inline"), dict):
        inline = payload["scenarios_inline"]
        if isinstance(inline.get("scenarios"), list):
            return inline["scenarios"]
    if isinstance(payload.get("scenarios"), list):
        return payload["scenarios"]
    raise KeyError(
        "Could not locate scenarios: expected `scenarios_inline.scenarios` "
        "or top-level `scenarios`."
    )


def verify(scenarios_raw: list[dict]) -> list[dict]:
    """Return list of failure dicts; empty list means gate passes."""
    failures: list[dict] = []
    for raw in scenarios_raw:
        try:
            s = Scenario.model_validate(raw)
        except ValidationError as e:
            failures.append(
                {
                    "scenario_id": raw.get("id", "<unknown>"),
                    "kind": "schema",
                    "detail": str(e),
                }
            )
            continue

        computed = s.eps * s.multiple
        if s.target_price == 0:
            # Avoid division by zero — flag as failure if computed nonzero.
            if abs(computed) > 1e-9:
                failures.append(
                    {
                        "scenario_id": s.id,
                        "kind": "math",
                        "eps": s.eps,
                        "multiple": s.multiple,
                        "target_price": s.target_price,
                        "computed": computed,
                        "delta_pct": float("inf"),
                    }
                )
            continue

        rel_delta = abs(computed - s.target_price) / abs(s.target_price)
        if rel_delta > TOL_PCT:
            failures.append(
                {
                    "scenario_id": s.id,
                    "kind": "math",
                    "eps": s.eps,
                    "multiple": s.multiple,
                    "target_price": s.target_price,
                    "computed": computed,
                    "delta_pct": rel_delta * 100.0,
                }
            )
    return failures


def emit_failure(failures: list[dict]) -> None:
    """Structured error output matching schemas/verification_gates.json evidence."""
    first = failures[0]
    print(f"gate_id: {GATE_ID}")
    print("status: fail")
    if first["kind"] == "math":
        reason = (
            f'Scenario "{first["scenario_id"]}" target_price='
            f"{first['target_price']:.2f} disagrees with EPS×multiple="
            f"{first['computed']:.2f} by {first['delta_pct']:.3f}% "
            f"(tolerance ±{TOL_PCT * 100:.1f}%)"
        )
    else:
        reason = f'Scenario "{first["scenario_id"]}" failed schema validation: {first["detail"]}'
    print(f"failure_reason: {reason}")
    print(
        f"remediation_required: scenarios_inline.scenarios"
        f"[id={first['scenario_id']}].target_price OR eps/multiple"
    )
    if len(failures) > 1:
        print(f"additional_failures: {len(failures) - 1}")
        for extra in failures[1:]:
            if extra["kind"] == "math":
                print(
                    f"  - {extra['scenario_id']}: "
                    f"eps*mult={extra['computed']:.2f} vs "
                    f"target_price={extra['target_price']:.2f} "
                    f"({extra['delta_pct']:.3f}%)"
                )
            else:
                print(f"  - {extra['scenario_id']}: schema error")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__ or "Verify G1 — EPS × multiple multiplicativity."
    )
    parser.add_argument("--memo-json", required=True, help="Path to structured memo JSON")
    parser.add_argument(
        "--memo-md",
        required=False,
        default=None,
        help="Path to memo Markdown (unused; accepted for uniform calling contract)",
    )
    args = parser.parse_args(argv)

    path = Path(args.memo_json)
    if not path.is_file():
        print(f"verify_eps_pe.py: file not found: {path}", file=sys.stderr)
        return 2

    try:
        with path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"verify_eps_pe.py: cannot read JSON: {exc}", file=sys.stderr)
        return 2

    try:
        scenarios_raw = locate_scenarios(payload)
    except KeyError as exc:
        print(f"verify_eps_pe.py: {exc}", file=sys.stderr)
        return 2

    failures = verify(scenarios_raw)
    if failures:
        emit_failure(failures)
        return 1

    print(
        f"gate_id: {GATE_ID} status: pass "
        f"({len(scenarios_raw)} scenarios verified within ±{TOL_PCT * 100:.1f}%)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
