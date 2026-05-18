#!/usr/bin/env python3
"""
verify_weighting_sensitivity.py — Gate G10 (anchor weighting impact table present).

Owns bug B10 (NVDA v0 fixture): `weighting_sensitivity` block deleted from
`scenarios_inline`, removing the ±10pp shift impact table that Phase 4 IC
defense requires.

Usage:
    python scripts/verify_weighting_sensitivity.py --memo-json <memo.json> [--memo-md <path>]

Accepts either:
  - a full structured memo (schemas/memo.json shape) — block at
    `scenarios_inline.weighting_sensitivity`, OR
  - a standalone scenarios.json (schemas/scenarios.json) — block at
    top-level `weighting_sensitivity`.

Exit codes:
  0 = G10 passes (weighting_sensitivity present with required sub-fields)
  non-zero = G10 fails (absent OR empty OR required sub-fields missing/null)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class _StrongTailPlus10(BaseModel):
    strong_bear: float
    strong_bull: float


class _WeightingSensitivity(BaseModel):
    base_minus_10_to_bear: float
    base_minus_10_to_bull: float
    strong_tail_plus_10: _StrongTailPlus10 | None = Field(default=None)


def _extract_block(payload: dict[str, Any]) -> tuple[Any, str]:
    """Locate weighting_sensitivity in either umbrella memo or standalone scenarios.json.

    Returns (block_or_None, source_path_for_error_messages).
    """
    inline = payload.get("scenarios_inline")
    if isinstance(inline, dict):
        return inline.get("weighting_sensitivity"), "scenarios_inline.weighting_sensitivity"
    return payload.get("weighting_sensitivity"), "weighting_sensitivity"


def _print_fail(reason: str, path: str) -> None:
    print("gate_id: G10")
    print("status: fail")
    print(f"failure_reason: {reason}")
    print(f"remediation_required: {path} — populate with base±10pp shift impacts per references/five-scenario-framework-us.md §5.2")


def verify(payload: dict[str, Any]) -> int:
    """Return 0 on pass, non-zero on fail. Prints structured G10 evidence."""
    block, path = _extract_block(payload)

    if block is None:
        _print_fail(f"{path} block is missing; required for anchor weighting impact table", path)
        return 1

    if not isinstance(block, dict):
        _print_fail(f"{path} must be an object, got {type(block).__name__}", path)
        return 2

    if len(block) == 0:
        _print_fail(f"{path} is empty; required: base_minus_10_to_bear and base_minus_10_to_bull", path)
        return 3

    missing = [k for k in ("base_minus_10_to_bear", "base_minus_10_to_bull")
               if k not in block or block[k] is None]
    if missing:
        _print_fail(f"{path} missing required sub-field(s): {', '.join(missing)}", path)
        return 4

    stp10 = block.get("strong_tail_plus_10")
    if stp10 is not None:
        if not isinstance(stp10, dict):
            _print_fail(f"{path}.strong_tail_plus_10 must be an object, got {type(stp10).__name__}", path)
            return 5
        sub_missing = [k for k in ("strong_bear", "strong_bull")
                       if k not in stp10 or stp10[k] is None]
        if sub_missing:
            _print_fail(f"{path}.strong_tail_plus_10 missing sub-field(s): {', '.join(sub_missing)}", path)
            return 6

    try:
        _WeightingSensitivity(**block)
    except ValidationError as exc:
        _print_fail(f"{path} shape invalid: {exc.errors()[0]['msg']}", path)
        return 7

    print("gate_id: G10")
    print("status: pass")
    print(f"weighting_sensitivity_path: {path}")
    print(f"base_minus_10_to_bear: {block['base_minus_10_to_bear']}")
    print(f"base_minus_10_to_bull: {block['base_minus_10_to_bull']}")
    if stp10 is not None:
        print(f"strong_tail_plus_10.strong_bear: {stp10['strong_bear']}")
        print(f"strong_tail_plus_10.strong_bull: {stp10['strong_bull']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify G10 — anchor weighting impact table present.")
    parser.add_argument("--memo-json", required=True, type=Path,
                        help="Path to structured memo JSON or standalone scenarios.json")
    parser.add_argument("--memo-md", required=False, type=Path, default=None,
                        help="(Unused; accepted for uniform calling contract)")
    args = parser.parse_args(argv)

    try:
        payload = json.loads(args.memo_json.read_text())
    except FileNotFoundError:
        print(f"gate_id: G10\nstatus: fail\nfailure_reason: file not found: {args.memo_json}")
        return 8
    except json.JSONDecodeError as exc:
        print(f"gate_id: G10\nstatus: fail\nfailure_reason: invalid JSON: {exc}")
        return 9

    return verify(payload)


if __name__ == "__main__":
    sys.exit(main())
