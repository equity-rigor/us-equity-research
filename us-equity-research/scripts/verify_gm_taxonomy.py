#!/usr/bin/env python3
"""
verify_gm_taxonomy.py — Gate G8 (GM taxonomy box exists with 5 GM types).

Owns bug B08 (NVDA v0): `gm_taxonomy.entries = []`.

Pass conditions:
  a) `gm_taxonomy.entries` is non-empty
  b) All 5 GM types are represented across entries:
     T1_consolidated, T2_segment, T3_sub_segment, T4_analyst_modeled, T5_marginal

Usage:
    python scripts/verify_gm_taxonomy.py --memo-json <memo.json> [--memo-md <path>]

Optional flag --memo-md is accepted (uniform calling contract) but unused.

Exit codes: 0 = pass; non-zero = fail.

Self-contained: stdlib + pydantic v2 only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

GATE_ID = "G8"
REQUIRED_TYPES = (
    "T1_consolidated",
    "T2_segment",
    "T3_sub_segment",
    "T4_analyst_modeled",
    "T5_marginal",
)


class _Entry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: str


def _locate_taxonomy(payload: dict[str, Any]) -> dict[str, Any]:
    """Return gm_taxonomy block from full memo or standalone shape."""
    gmt = payload.get("gm_taxonomy")
    if isinstance(gmt, dict):
        return gmt
    if isinstance(payload.get("entries"), list):
        return payload
    raise KeyError(
        "gm_taxonomy block not found: expected top-level `gm_taxonomy` with `entries[]`."
    )


def _fail(reason: str, *, remediation: str | None = None) -> None:
    print(f"gate_id: {GATE_ID}")
    print("status: fail")
    print(f"failure_reason: {reason}")
    print(
        "remediation_required: "
        + (remediation or "gm_taxonomy.entries[] — populate per references/gm-taxonomy-us.md")
    )


def verify(payload: dict[str, Any]) -> int:
    try:
        taxonomy = _locate_taxonomy(payload)
    except KeyError as exc:
        _fail(str(exc))
        return 2

    entries_raw = taxonomy.get("entries")
    if not isinstance(entries_raw, list):
        _fail("gm_taxonomy.entries must be a list of taxonomy entries")
        return 3

    # Condition (a): non-empty.
    if len(entries_raw) == 0:
        _fail("gm_taxonomy.entries is empty; required: at least 1 entry covering T1-T5 types")
        return 1

    # Parse entries; collect observed `type` values.
    observed: set[str] = set()
    for idx, raw in enumerate(entries_raw):
        try:
            entry = _Entry.model_validate(raw)
        except ValidationError as exc:
            _fail(f"gm_taxonomy.entries[{idx}] shape invalid: {exc.errors()[0]['msg']}")
            return 4
        observed.add(entry.type)

    # Condition (b): all 5 GM types represented.
    missing = [t for t in REQUIRED_TYPES if t not in observed]
    if missing:
        _fail(
            f"gm_taxonomy.entries missing required GM types: "
            f"{', '.join(missing)} (have: {sorted(observed)})"
        )
        return 5

    print(f"gate_id: {GATE_ID}")
    print("status: pass")
    print(f"entries_count: {len(entries_raw)} (all 5 types T1-T5 present)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify G8 — GM taxonomy box has entries spanning T1-T5."
    )
    parser.add_argument("--memo-json", required=True, type=Path, help="Structured memo JSON path.")
    parser.add_argument(
        "--memo-md",
        required=False,
        type=Path,
        default=None,
        help="(Unused; accepted for uniform calling contract.)",
    )
    args = parser.parse_args(argv)

    if not args.memo_json.is_file():
        print(f"gate_id: {GATE_ID}\nstatus: fail\nfailure_reason: file not found: {args.memo_json}")
        return 6

    try:
        payload = json.loads(args.memo_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"gate_id: {GATE_ID}\nstatus: fail\nfailure_reason: invalid JSON: {exc}")
        return 7

    return verify(payload)


if __name__ == "__main__":
    sys.exit(main())
