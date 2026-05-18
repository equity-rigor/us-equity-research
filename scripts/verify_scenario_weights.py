#!/usr/bin/env python3
"""
verify_scenario_weights.py — Gate G4 (scenario probabilities sum to 1.00 ±0.01).

Owns bug B04 (NVDA v0 fixture): base probability silently reduced 0.50 → 0.45,
making the 5-scenario distribution sum to 0.95.

Usage:
    python scripts/verify_scenario_weights.py --memo-json <memo.json> [--memo-md <path>]

Accepts either:
  - a full structured memo (schemas/memo.json shape) — scenarios at
    `scenarios_inline.scenarios[]`, OR
  - a standalone scenarios.json (schemas/scenarios.json) — scenarios at
    top-level `scenarios[]`.

Exit codes:
  0 = G4 passes
  non-zero = G4 fails (also covers shape / integrity adjacencies that would
             make a sum-check meaningless: wrong cardinality, missing IDs)

Adjacent G4-integrity checks (kept narrow on purpose; cross-sensitivity to
B01-B03, B05-B14 must remain zero):
  - exactly 5 scenarios
  - IDs are exactly {strong_bear, bear, base, bull, strong_bull}
These pass on clean.json and on every other B0N fixture in nvda_v0, so they
do not introduce cross-sensitivity. The probability-sum check is what fires
on B04.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError

PROB_SUM_TARGET = 1.00
PROB_SUM_TOL = 0.01
REQUIRED_IDS = {"strong_bear", "bear", "base", "bull", "strong_bull"}


class _Scenario(BaseModel):
    id: str
    probability: float = Field(ge=0.0, le=1.0)


def _extract_scenarios(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Locate scenarios array in either umbrella memo or standalone scenarios.json."""
    inline = payload.get("scenarios_inline")
    if isinstance(inline, dict) and isinstance(inline.get("scenarios"), list):
        return inline["scenarios"]
    if isinstance(payload.get("scenarios"), list):
        return payload["scenarios"]
    raise KeyError(
        "scenarios array not found at scenarios_inline.scenarios[] "
        "or top-level scenarios[]"
    )


def _print_fail(reason: str, *, delta: float | None = None) -> None:
    print("gate_id: G4")
    print("status: fail")
    print(f"failure_reason: {reason}")
    if delta is not None:
        print(f"observed_delta: {delta:.4f}")
    print("remediation_required: scenarios_inline.scenarios[].probability")


def verify(payload: dict[str, Any]) -> int:
    """Return 0 on pass, non-zero on fail. Prints structured G4 evidence."""
    try:
        raw_scenarios = _extract_scenarios(payload)
    except KeyError as exc:
        _print_fail(str(exc))
        return 2

    # Integrity adjacency: exactly 5 scenarios.
    if len(raw_scenarios) != 5:
        _print_fail(
            f"expected exactly 5 scenarios, found {len(raw_scenarios)}"
        )
        return 3

    # Parse with pydantic for type-safety.
    try:
        scenarios = [_Scenario(**s) for s in raw_scenarios]
    except ValidationError as exc:
        _print_fail(f"scenario shape invalid: {exc.errors()[0]['msg']}")
        return 4

    # Integrity adjacency: required IDs all present, no extras, no dupes.
    observed_ids = [s.id for s in scenarios]
    if len(set(observed_ids)) != len(observed_ids):
        _print_fail(f"duplicate scenario ids: {observed_ids}")
        return 5
    if set(observed_ids) != REQUIRED_IDS:
        missing = REQUIRED_IDS - set(observed_ids)
        extra = set(observed_ids) - REQUIRED_IDS
        _print_fail(
            f"scenario id set != {{strong_bear,bear,base,bull,strong_bull}}; "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )
        return 6

    # The actual G4 check: probability sum within tolerance.
    p_sum = sum(s.probability for s in scenarios)
    delta = p_sum - PROB_SUM_TARGET
    if abs(delta) > PROB_SUM_TOL:
        _print_fail(
            f"Scenario probabilities sum to {p_sum:.4f}, expected "
            f"{PROB_SUM_TARGET:.2f} ± {PROB_SUM_TOL:.2f} "
            f"(delta {delta:+.4f})",
            delta=delta,
        )
        return 1

    print("gate_id: G4")
    print("status: pass")
    print(f"probability_sum: {p_sum:.4f}")
    print(f"tolerance: {PROB_SUM_TARGET:.2f} ± {PROB_SUM_TOL:.2f}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify G4 — scenario weights sum to 1.00 ±0.01.")
    parser.add_argument("--memo-json", required=True, type=Path,
                        help="Path to structured memo JSON or standalone scenarios.json")
    parser.add_argument("--memo-md", required=False, type=Path, default=None,
                        help="(Unused; accepted for uniform calling contract)")
    args = parser.parse_args(argv)

    try:
        payload = json.loads(args.memo_json.read_text())
    except FileNotFoundError:
        print(f"gate_id: G4\nstatus: fail\nfailure_reason: file not found: {args.memo_json}")
        return 7
    except json.JSONDecodeError as exc:
        print(f"gate_id: G4\nstatus: fail\nfailure_reason: invalid JSON: {exc}")
        return 8

    return verify(payload)


if __name__ == "__main__":
    sys.exit(main())
