#!/usr/bin/env python3
"""verify_quant_overlay.py — Phase D gates G13 (factor tags) + G14 (capacity).

Owns both gates in a single script per design/file-ownership.md (S-D-4): both
probe the same `quant_overlay` JSON block, so combining them keeps the per-gate
script footprint clean. Each invocation emits TWO independent gate_check
objects (one for G13, one for G14) per schemas/verification_gates.json, and
encodes their independence via distinct exit codes.

Canonical scope authority: us-equity-ic-rigor/references/quant-overlay-us.md
(committed by S-D-1). The G13 scope paragraph and G14 scope paragraph in that
reference define the exact PASS/FAIL semantics enforced here; this script is to
quant-overlay-us.md what verify_segment_gm.py is to gm-taxonomy-us.md.

G13 (Factor exposure stated — Barra):
  PASS iff `quant_overlay.factor_tags` contains all 7 required keys
  (value, quality, momentum, growth, size, low_vol, liquidity), each a
  numeric value in the closed interval [-3.0, +3.0] per schemas/memo.json.
  FAIL if any of the 7 are absent, null, non-numeric, or outside [-3, +3].

G14 (Capacity / ADV / days-to-exit stated):
  PASS iff `quant_overlay.capacity.adv_30d_usd_m` is present, non-null,
  numeric, and strictly positive AND `quant_overlay.capacity.
  days_to_exit_10pct_participation` is present, non-null, numeric, and
  strictly positive. Per quant-overlay-us.md these two fields are the Phase D
  trip-wire; further participation tiers are recommended but do NOT trip G14.

Owns bugs:
  B13 — factor_tags pruned to {value, quality, momentum} → G13 fail only
  B14 — capacity.days_to_exit_10pct_participation removed → G14 fail only

Cross-sensitivity invariant: B13 trips G13 only; B14 trips G14 only; all
other fixtures (clean + B01-B12) leave BOTH gates passing.

Usage:  python scripts/verify_quant_overlay.py --memo-json <path> [--memo-md <path>]

Exit codes:
  0 — both gates pass
  1 — G13 fails, G14 passes
  2 — G13 passes, G14 fails
  3 — both gates fail
  4 — I/O error (file not found / JSON parse error)
  5 — schema error (reserved)

Self-contained: stdlib + pydantic v2 only; NO shared helpers.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

GATE_G13 = "G13"
GATE_G14 = "G14"

REQUIRED_FACTORS = ("value", "quality", "momentum", "growth", "size", "low_vol", "liquidity")
FACTOR_MIN = -3.0
FACTOR_MAX = 3.0

REQUIRED_CAPACITY_FIELDS = ("adv_30d_usd_m", "days_to_exit_10pct_participation")

BLOCKS_SCORE_ABOVE = 8.0
SCRIPT_PATH = "scripts/verify_quant_overlay.py"
SCOPE_AUTHORITY = "us-equity-ic-rigor/references/quant-overlay-us.md"


class FactorTags(BaseModel):
    """Minimal slice — Optional so missing keys surface as None."""

    model_config = ConfigDict(extra="ignore")

    value: Optional[float] = None
    quality: Optional[float] = None
    momentum: Optional[float] = None
    growth: Optional[float] = None
    size: Optional[float] = None
    low_vol: Optional[float] = None
    liquidity: Optional[float] = None


class Capacity(BaseModel):
    """Minimal slice — Optional so missing keys surface as None."""

    model_config = ConfigDict(extra="ignore")

    adv_30d_usd_m: Optional[float] = None
    days_to_exit_10pct_participation: Optional[float] = None
    days_to_exit_20pct_participation: Optional[float] = None
    days_to_exit_30pct_participation: Optional[float] = None
    max_position_constrained_by_adv_pct_nav: Optional[float] = None


def _now_iso() -> str:
    """ISO 8601 timestamp with timezone for gate_check.checked_at."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_finite_number(v: Any) -> bool:
    """True iff v is a real numeric value (excluding bool, NaN, inf)."""
    if isinstance(v, bool):
        return False
    if not isinstance(v, (int, float)):
        return False
    try:
        f = float(v)
    except (TypeError, ValueError):
        return False
    return f == f and f not in (float("inf"), float("-inf"))


def check_g13(quant_overlay: Optional[dict]) -> dict:
    """Evaluate G13 — factor exposure block.

    Returns a gate_check dict per schemas/verification_gates.json. Status is
    'pass' iff all 7 required factors are present, numeric, and in [-3, +3]."""
    gate: dict[str, Any] = {
        "gate_id": GATE_G13,
        "name": "Factor exposure stated (Barra)",
        "status": "pass",
        "checked_at": _now_iso(),
        "category": "quant_overlay",
        "blocks_score_above": BLOCKS_SCORE_ABOVE,
        "evidence": {"verification_script": SCRIPT_PATH},
    }

    if not isinstance(quant_overlay, dict):
        gate["status"] = "fail"
        gate["failure_reason"] = (
            "quant_overlay block missing from memo JSON; cannot evaluate factor_tags"
        )
        gate["remediation_required"] = (
            f"Populate quant_overlay.factor_tags per {SCOPE_AUTHORITY} G13 scope"
        )
        gate["evidence"]["factors_present"] = []
        return gate

    raw_tags = quant_overlay.get("factor_tags")
    if not isinstance(raw_tags, dict):
        gate["status"] = "fail"
        gate["failure_reason"] = (
            "quant_overlay.factor_tags absent or not an object; required: all 7 Barra factors"
        )
        gate["remediation_required"] = (
            f"Populate quant_overlay.factor_tags with all 7 z-scores per {SCOPE_AUTHORITY}"
        )
        gate["evidence"]["factors_present"] = []
        return gate

    tags = FactorTags.model_validate(raw_tags)
    present: list[str] = []
    missing: list[str] = []
    out_of_range: list[tuple[str, float]] = []

    for key in REQUIRED_FACTORS:
        raw_val = raw_tags.get(key)
        validated_val = getattr(tags, key)
        if raw_val is None or validated_val is None:
            missing.append(key)
            continue
        if not _is_finite_number(raw_val):
            out_of_range.append((key, raw_val))
            continue
        fv = float(raw_val)
        if fv < FACTOR_MIN or fv > FACTOR_MAX:
            out_of_range.append((key, fv))
            continue
        present.append(key)

    gate["evidence"]["factors_present"] = present
    gate["evidence"]["factors_required"] = list(REQUIRED_FACTORS)

    if missing or out_of_range:
        gate["status"] = "fail"
        parts: list[str] = []
        if missing:
            parts.append(
                f"missing {len(missing)} of 7 required factors: {', '.join(missing)}"
            )
            gate["evidence"]["factors_missing"] = missing
        if out_of_range:
            oor_str = ", ".join(f"{k}={v}" for k, v in out_of_range)
            parts.append(
                f"{len(out_of_range)} factor(s) outside [{FACTOR_MIN}, {FACTOR_MAX}]: {oor_str}"
            )
            gate["evidence"]["factors_out_of_range"] = [
                {"factor": k, "value": v} for k, v in out_of_range
            ]
        gate["failure_reason"] = "quant_overlay.factor_tags " + "; ".join(parts)
        gate["remediation_required"] = (
            f"quant_overlay.factor_tags — populate all 7 Barra-style z-scores in "
            f"[{FACTOR_MIN}, {FACTOR_MAX}] per {SCOPE_AUTHORITY} G13 scope"
        )
    return gate


def check_g14(quant_overlay: Optional[dict]) -> dict:
    """Evaluate G14 — capacity block.

    Returns a gate_check dict per schemas/verification_gates.json. Status is
    'pass' iff both adv_30d_usd_m and days_to_exit_10pct_participation are
    present, numeric, and strictly positive."""
    gate: dict[str, Any] = {
        "gate_id": GATE_G14,
        "name": "Capacity / ADV / days-to-exit stated",
        "status": "pass",
        "checked_at": _now_iso(),
        "category": "quant_overlay",
        "blocks_score_above": BLOCKS_SCORE_ABOVE,
        "evidence": {"verification_script": SCRIPT_PATH},
    }

    if not isinstance(quant_overlay, dict):
        gate["status"] = "fail"
        gate["failure_reason"] = (
            "quant_overlay block missing from memo JSON; cannot evaluate capacity"
        )
        gate["remediation_required"] = (
            f"Populate quant_overlay.capacity per {SCOPE_AUTHORITY} G14 scope"
        )
        gate["evidence"]["capacity_fields_present"] = []
        return gate

    raw_cap = quant_overlay.get("capacity")
    if not isinstance(raw_cap, dict):
        gate["status"] = "fail"
        gate["failure_reason"] = (
            "quant_overlay.capacity absent or not an object; required: adv_30d_usd_m + "
            "days_to_exit_10pct_participation"
        )
        gate["remediation_required"] = (
            f"Populate quant_overlay.capacity with ADV and days-to-exit per {SCOPE_AUTHORITY}"
        )
        gate["evidence"]["capacity_fields_present"] = []
        return gate

    Capacity.model_validate(raw_cap)  # tolerate extras / missings via Optional slice
    field_status: dict[str, dict[str, Any]] = {}
    failures: list[str] = []

    for key in REQUIRED_CAPACITY_FIELDS:
        raw_val = raw_cap.get(key)
        if raw_val is None:
            failures.append(f'{key} missing or null')
            field_status[key] = {"present": False, "value": None}
            continue
        if not _is_finite_number(raw_val):
            failures.append(f'{key} non-numeric (value={raw_val!r})')
            field_status[key] = {"present": True, "value": raw_val, "numeric": False}
            continue
        fv = float(raw_val)
        if fv <= 0:
            failures.append(f'{key} not strictly positive (value={fv})')
            field_status[key] = {"present": True, "value": fv, "positive": False}
            continue
        field_status[key] = {"present": True, "value": fv, "positive": True}

    gate["evidence"]["capacity_fields_present"] = [
        k for k, s in field_status.items() if s.get("present")
    ]
    gate["evidence"]["capacity_fields_required"] = list(REQUIRED_CAPACITY_FIELDS)

    if failures:
        gate["status"] = "fail"
        gate["failure_reason"] = (
            "quant_overlay.capacity required field check failed: " + "; ".join(failures)
        )
        gate["remediation_required"] = (
            f"quant_overlay.capacity — populate adv_30d_usd_m and "
            f"days_to_exit_10pct_participation (both positive) per {SCOPE_AUTHORITY} G14 scope"
        )
        gate["evidence"]["capacity_field_status"] = field_status
    return gate


def verify(payload: dict) -> dict:
    """Return the full structured output for one memo evaluation."""
    quant_overlay = payload.get("quant_overlay") if isinstance(payload, dict) else None
    g13 = check_g13(quant_overlay)
    g14 = check_g14(quant_overlay)
    both_pass = g13["status"] == "pass" and g14["status"] == "pass"
    return {
        "gates": [g13, g14],
        "overall_pass": both_pass,
        "blocks_score_above": 10.0 if both_pass else BLOCKS_SCORE_ABOVE,
    }


def exit_code_for(output: dict) -> int:
    """Encode G13/G14 independence into a 4-valued exit code."""
    g13_fail = output["gates"][0]["status"] == "fail"
    g14_fail = output["gates"][1]["status"] == "fail"
    if g13_fail and g14_fail:
        return 3
    if g14_fail:
        return 2
    if g13_fail:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify G13 (factor tags) + G14 (capacity) per quant-overlay-us.md."
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
        print(f"verify_quant_overlay.py: file not found: {path}", file=sys.stderr)
        return 4

    try:
        with path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"verify_quant_overlay.py: cannot read JSON: {exc}", file=sys.stderr)
        return 4

    output = verify(payload)
    print(json.dumps(output, indent=2))
    return exit_code_for(output)


if __name__ == "__main__":
    sys.exit(main())
