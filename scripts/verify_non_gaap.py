#!/usr/bin/env python3
"""
verify_non_gaap.py — Phase D gate G11 (non-GAAP / GAAP reconciliation present).
Cross-layer JSON ↔ Markdown verifier. Owns bug B11.

G11 contract (per `references/forensic-accounting-checklist-us.md` Item 5 and
`schemas/verification_gates.json` G11):
  - Primary: `forensic_flags.non_gaap_reconciliation_present` must be true.
  - Cross-layer: if the JSON flag is true, Markdown should show a GAAP/non-GAAP
    parallel/reconciliation paragraph (see PARALLEL_MARKERS). A JSON-false flag
    fails regardless of MD content (structured flag is authoritative on the
    bear side). B11 corrupts both layers consistently.
  - Enhanced scrutiny (informational, NOT a gate fail): when reconciliation
    present AND `non_gaap_to_gaap_delta_pct_ni_5y_avg > 25` we surface an
    alert in the pass output.

Usage:
    python scripts/verify_non_gaap.py --memo-json <path> [--memo-md <path>]

If --memo-md is omitted, looks for a sibling .md to memo.json. Exit codes:
0 = pass, 1 = fail, 2 = usage/IO/schema error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError

GATE_ID = "G11"
DELTA_SCRUTINY_THRESHOLD_PCT = 25.0  # >25% sustained → forensic alert.

# Marker phrases for GAAP/non-GAAP reconciliation *narrative* discussion
# (NOT lone S-tag citation strings like "S2: ... non-GAAP reconciliation",
# which appear in B11.md too). Case-insensitive. What B11 removes is the
# parallel-disclosure narrative; the table-source citations still mention
# "non-GAAP reconciliation" so we cannot rely on that phrase alone.
PARALLEL_MARKERS = (
    "gaap/non-gaap parallel",
    "gaap / non-gaap parallel",
    "non-gaap/gaap parallel",
    "non-gaap / gaap parallel",
    "gaap equivalent",
    "bridges to gaap",
    "bridge to gaap",
    "gaap-to-non-gaap delta",
    "non-gaap-to-gaap delta",
    "gaap to non-gaap delta",
    "reconciliation: present",
    "reconciliation present",
)

REMEDIATION = (
    "remediation_required: clean.md §6.0 — restore GAAP/non-GAAP parallel "
    "paragraph; forensic_flags.non_gaap_reconciliation_present → true "
    "(per references/forensic-accounting-checklist-us.md Item 5)"
)


# ----- Minimal pydantic slices ----------------------------------------------


class _ForensicFlags(BaseModel):
    model_config = ConfigDict(extra="ignore")
    non_gaap_reconciliation_present: Optional[bool] = None
    non_gaap_to_gaap_delta_pct_ni_5y_avg: Optional[float] = None


class _Memo(BaseModel):
    model_config = ConfigDict(extra="ignore")
    forensic_flags: _ForensicFlags


# ----- Helpers ---------------------------------------------------------------


def _emit_fail(reason: str, *, extras: Optional[dict] = None) -> None:
    print(f"gate_id: {GATE_ID}\nstatus: fail\nfailure_reason: {reason}")
    if extras:
        for k, v in extras.items():
            print(f"{k}: {v}")
    print(REMEDIATION)


def _has_parallel_marker(md_text: str) -> bool:
    if not md_text:
        return False
    lower = md_text.lower()
    return any(marker in lower for marker in PARALLEL_MARKERS)


def _has_non_gaap_citation(md_text: str) -> bool:
    """True if the memo cites any non-GAAP number (case-insensitive)."""
    if not md_text:
        return False
    return bool(re.search(r"non[-\s]?gaap", md_text, flags=re.IGNORECASE))


# ----- Core verification -----------------------------------------------------


def verify(memo_raw: dict, md_text: str) -> int:
    """Return 0 on pass, non-zero on fail. Prints structured G11 evidence."""
    try:
        memo = _Memo.model_validate(memo_raw)
    except ValidationError as exc:
        _emit_fail(
            f"memo JSON missing required structure for G11: {exc.errors()[0]['msg']}"
        )
        return 2

    ff = memo.forensic_flags
    flag_present = ff.non_gaap_reconciliation_present
    delta_pct = ff.non_gaap_to_gaap_delta_pct_ni_5y_avg

    md_has_parallel = _has_parallel_marker(md_text)
    md_cites_non_gaap = _has_non_gaap_citation(md_text)

    # Case 1: JSON flag missing entirely → can't verify; if non-GAAP cited,
    # this is a structural fail.
    if flag_present is None:
        if md_cites_non_gaap:
            _emit_fail(
                "forensic_flags.non_gaap_reconciliation_present is absent "
                "from JSON; memo cites non-GAAP numbers so this gate cannot "
                "be verified silently.",
                extras={"md_cites_non_gaap": "true"},
            )
            return 1
        # No non-GAAP citation and no flag → G11 is n_a.
        print(f"gate_id: {GATE_ID}\nstatus: pass")
        print("note: G11 n/a — no non-GAAP measures cited in memo")
        return 0

    # Case 2: JSON flag is False → primary B11 detection vector.
    if flag_present is False:
        # Strong corroborated fail when MD also lacks parallel marker.
        if not md_has_parallel:
            _emit_fail(
                "forensic_flags.non_gaap_reconciliation_present=false AND "
                "no GAAP/non-GAAP parallel/reconciliation paragraph found in "
                "rendered Markdown (corroborated absence — Reg G + Item 10(e) "
                "discipline broken).",
                extras={
                    "json_flag": "false",
                    "md_parallel_marker_found": "false",
                    "md_cites_non_gaap": "true" if md_cites_non_gaap else "false",
                },
            )
            return 1
        # Cross-layer inconsistency: JSON says no, MD has the marker → still
        # fails (bear side: the structured forensic flag is the authoritative
        # source for the verification gate).
        _emit_fail(
            "forensic_flags.non_gaap_reconciliation_present=false but MD "
            "appears to discuss a GAAP/non-GAAP parallel — cross-layer "
            "inconsistency on the bear side; structured flag must be true "
            "when reconciliation is in fact disclosed.",
            extras={
                "json_flag": "false",
                "md_parallel_marker_found": "true",
            },
        )
        return 1

    # Case 3: JSON flag is True.
    # Warn (informational) if MD lacks parallel marker but cites non-GAAP.
    # Do NOT fail — schema treats JSON as authoritative when flag is true;
    # the MD-side absence may be due to render-template variance.
    pass_notes = ["json_flag: true"]
    if md_cites_non_gaap and not md_has_parallel:
        pass_notes.append(
            "warn: MD cites non-GAAP but no parallel-marker phrase detected "
            "(informational; JSON flag authoritative)"
        )
    elif md_has_parallel:
        pass_notes.append("md_parallel_marker_found: true")

    # Enhanced scrutiny: delta > 25% sustained.
    if delta_pct is not None and delta_pct > DELTA_SCRUTINY_THRESHOLD_PCT:
        pass_notes.append(
            f"forensic_alert: non_gaap_to_gaap_delta_pct_ni_5y_avg="
            f"{delta_pct:.1f}% > {DELTA_SCRUTINY_THRESHOLD_PCT:.0f}% — "
            "enhanced scrutiny signal (gate still passes; surface for IC)"
        )

    print(f"gate_id: {GATE_ID}\nstatus: pass")
    for note in pass_notes:
        print(note)
    return 0


# ----- CLI -------------------------------------------------------------------


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify G11 — non-GAAP / GAAP reconciliation present.",
    )
    parser.add_argument(
        "--memo-json", required=True, type=Path,
        help="Path to structured memo JSON",
    )
    parser.add_argument(
        "--memo-md", required=False, type=Path, default=None,
        help="Path to rendered Markdown memo (default: sibling .md to memo_json)",
    )
    args = parser.parse_args(argv)

    if not args.memo_json.is_file():
        print(
            f"gate_id: {GATE_ID}\nstatus: fail\n"
            f"failure_reason: memo JSON not found: {args.memo_json}",
            file=sys.stderr,
        )
        return 2

    try:
        memo_raw = json.loads(args.memo_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(
            f"gate_id: {GATE_ID}\nstatus: fail\n"
            f"failure_reason: invalid JSON in {args.memo_json}: {exc}",
            file=sys.stderr,
        )
        return 2

    # Resolve MD path: explicit flag wins; otherwise sibling .md.
    md_path = (
        args.memo_md if args.memo_md is not None
        else args.memo_json.with_suffix(".md")
    )
    md_text = ""
    if md_path.is_file():
        md_text = md_path.read_text(encoding="utf-8")
    # If MD not found, we run JSON-only — Case 2/3 still work, Case 1 still
    # handles the structural-missing-flag fail correctly.

    return verify(memo_raw, md_text)


if __name__ == "__main__":
    sys.exit(main())
