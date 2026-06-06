#!/usr/bin/env python3
"""
verify_what_would_reverse.py — Phase C gate G9 verifier.

For every entry in `what_would_reverse[]`, verify:
  1. `numerical_threshold` contains at least one digit (regex \\d)
  2. `numerical_threshold` carries a quantitative marker:
       %, B, M, bps, $, or a comparator (>, <, >=, <=, ≥, ≤)
  3. `observable_via` is a non-empty string

Owns bug B09: numerical_threshold = "if hyperscaler capex weakens
materially" with unit="" — no digit, no denominator.

Usage:
    python scripts/verify_what_would_reverse.py --memo-json <memo.json> [--memo-md <path>]

Exit codes:
    0 = pass; 1 = fail; 2 = usage / IO / shape error.

Self-contained: stdlib + pydantic v2 minimal slice.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

GATE_ID = "G9"
DIGIT_RE = re.compile(r"\d")
QUANT_MARKERS = ("%", "B", "M", "bps", "$", ">", "<", "≥", "≤")


class Trigger(BaseModel):
    model_config = ConfigDict(extra="ignore")
    direction: str | None = None
    numerical_threshold: str
    unit: str | None = None
    observable_via: str


def _locate_triggers(payload: dict[str, Any]) -> list[dict[str, Any]]:
    triggers = payload.get("what_would_reverse")
    if not isinstance(triggers, list):
        raise KeyError("what_would_reverse[] not found at top-level of memo JSON")
    return triggers


def _check_trigger(idx: int, raw: dict[str, Any]) -> dict[str, Any] | None:
    try:
        t = Trigger.model_validate(raw)
    except ValidationError as exc:
        return {
            "index": idx,
            "label": raw.get("direction", "<unknown>"),
            "threshold": str(raw.get("numerical_threshold", "")),
            "missing": f"schema: {exc.errors()[0]['msg']}",
        }
    threshold = t.numerical_threshold.strip()
    obs_via = t.observable_via.strip()
    missing: list[str] = []
    if not DIGIT_RE.search(threshold):
        missing.append("no digit in numerical_threshold")
    if not any(m in threshold for m in QUANT_MARKERS):
        missing.append("no quantitative marker (%, B, M, bps, $, >, <, ≥, ≤)")
    if not obs_via:
        missing.append("empty observable_via")
    if missing:
        return {
            "index": idx,
            "label": t.direction or "<unspecified>",
            "threshold": threshold,
            "missing": "; ".join(missing),
        }
    return None


def verify(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        f for f in (_check_trigger(i, r) for i, r in enumerate(_locate_triggers(payload)))
        if f is not None
    ]


def _emit_failure(failures: list[dict[str, Any]]) -> None:
    first = failures[0]
    print(f"gate_id: {GATE_ID}")
    print("status: fail")
    print(
        f'failure_reason: what_would_reverse[{first["index"]}] '
        f'(direction={first["label"]}) numerical_threshold '
        f'"{first["threshold"]}" lacks {first["missing"]}'
    )
    print(
        f'remediation_required: what_would_reverse[{first["index"]}]'
        ".numerical_threshold + .unit — rewrite with explicit number "
        "and denominator per references/what-would-reverse-us.md"
    )
    if len(failures) > 1:
        print(f"additional_failures: {len(failures) - 1}")
        for extra in failures[1:]:
            print(f'  - [{extra["index"]}] {extra["label"]}: "{extra["threshold"]}" — {extra["missing"]}')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify G9 — what_would_reverse triggers have numerical denominators."
    )
    parser.add_argument("--memo-json", required=True, type=Path,
                        help="Path to structured memo JSON")
    parser.add_argument("--memo-md", required=False, type=Path, default=None,
                        help="(Unused; uniform calling contract)")
    args = parser.parse_args(argv)

    if not args.memo_json.is_file():
        print(f"verify_what_would_reverse.py: file not found: {args.memo_json}", file=sys.stderr)
        return 2
    try:
        payload = json.loads(args.memo_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"verify_what_would_reverse.py: cannot read JSON: {exc}", file=sys.stderr)
        return 2

    try:
        failures = verify(payload)
    except KeyError as exc:
        print(f"gate_id: {GATE_ID}\nstatus: fail\nfailure_reason: {exc}")
        return 2

    if failures:
        _emit_failure(failures)
        return 1

    print(
        f"gate_id: {GATE_ID} status: pass "
        f"({len(_locate_triggers(payload))} triggers verified with numerical denominators)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
