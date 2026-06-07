#!/usr/bin/env python3
"""verify_bear_bridge.py — Gate G5.

For every non-base scenario in `scenarios_inline.scenarios[]`, verify that
the sum of `eps_bridge[].delta_eps` equals `scenario.eps - base_eps` within
±0.01 absolute (signed delta_eps: negative for bear adjustments, positive
for bull).

CLI (per S-C-N invocation contract used across Phase C/D):
    python scripts/verify_bear_bridge.py --memo-json <path> [--memo-md <path>]

Exit codes:
    0 — gate passes
    non-zero — gate fails (structured stdout per verification_gates.json)

Standalone, no shared helpers. Pydantic v2 minimal slice.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

GATE_ID = "G5"
TOLERANCE = 0.01  # absolute $/share tolerance per task spec


# --------------------------- Pydantic v2 slice ---------------------------


class EpsBridgeStep(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str
    delta_eps: float
    layer: str | None = None
    source_tag: str | None = None


class Scenario(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    eps: float
    eps_bridge: list[EpsBridgeStep] = Field(default_factory=list)


class ScenariosInline(BaseModel):
    model_config = ConfigDict(extra="ignore")
    base_eps: float
    scenarios: list[Scenario]


# --------------------------- Verification logic ---------------------------


def verify(memo_json_path: Path) -> int:
    """Return 0 on pass, non-zero on fail. Prints structured stdout."""
    try:
        with memo_json_path.open() as fh:
            raw = json.load(fh)
    except FileNotFoundError:
        print(
            f"gate_id: {GATE_ID}\nstatus: fail\nfailure_reason: memo JSON not found at {memo_json_path}\nremediation_required: provide --memo-json path"
        )
        return 2
    except json.JSONDecodeError as exc:
        print(
            f"gate_id: {GATE_ID}\nstatus: fail\nfailure_reason: memo JSON invalid: {exc}\nremediation_required: fix JSON syntax"
        )
        return 2

    inline_raw = raw.get("scenarios_inline")
    if inline_raw is None:
        # Gate is n_a if scenarios_inline absent — treat as pass so cross-sensitivity stays clean.
        print(f"gate_id: {GATE_ID}\nstatus: n_a\nfailure_reason: scenarios_inline block absent")
        return 0

    try:
        inline = ScenariosInline.model_validate(inline_raw)
    except Exception as exc:  # pydantic ValidationError
        print(
            f"gate_id: {GATE_ID}\nstatus: fail\nfailure_reason: scenarios_inline failed schema validation: {exc}\nremediation_required: scenarios_inline shape per schemas/scenarios.json"
        )
        return 3

    base_eps = inline.base_eps
    failures: list[str] = []

    for scenario in inline.scenarios:
        if scenario.id == "base":
            # Base scenario bridge is empty by convention; skip.
            continue
        bridge_sum = sum(step.delta_eps for step in scenario.eps_bridge)
        expected_delta = scenario.eps - base_eps
        residual = bridge_sum - expected_delta
        if abs(residual) > TOLERANCE:
            failures.append(
                f'Scenario "{scenario.id}" bridge deltas sum to {bridge_sum:+.4f}, '
                f"expected {expected_delta:+.4f} (= scenario.eps {scenario.eps:.4f} "
                f"- base_eps {base_eps:.4f}); residual {residual:+.4f} exceeds ±{TOLERANCE}"
            )

    if failures:
        print(f"gate_id: {GATE_ID}")
        print("status: fail")
        # Emit first failure as the canonical failure_reason.
        print(f"failure_reason: {failures[0]}")
        if len(failures) > 1:
            for extra in failures[1:]:
                print(f"additional_failure: {extra}")
        print(
            "remediation_required: scenarios_inline.scenarios[].eps_bridge[] — re-derive delta_eps so Σ = scenario.eps − base_eps"
        )
        return 1

    print(f"gate_id: {GATE_ID}")
    print("status: pass")
    print(f"checked_scenarios: {len([s for s in inline.scenarios if s.id != 'base'])}")
    print(f"tolerance_abs: {TOLERANCE}")
    return 0


# --------------------------- CLI plumbing ---------------------------


def parse_args(argv: list[str]) -> Path:
    parser = argparse.ArgumentParser(
        description="Verify gate G5 (bear/bull EPS bridge reconciles to base_eps).",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--memo-json", required=True, type=Path, help="Path to structured memo JSON"
    )
    parser.add_argument(
        "--memo-md",
        required=False,
        type=Path,
        default=None,
        help="Accepted for uniform invocation contract; unused (G5 is JSON-only).",
    )
    args = parser.parse_args(argv)
    return args.memo_json


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    memo_json_path = parse_args(argv)
    return verify(memo_json_path)


if __name__ == "__main__":
    sys.exit(main())
