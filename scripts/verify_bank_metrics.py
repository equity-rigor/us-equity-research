#!/usr/bin/env python3
"""
verify_bank_metrics.py — Gate G16 (bank-specific AOCI bridge + CET1 walk +
NIM trajectory + stress capital context required for Banks-sector memos).

Added in v0.2.0. Full discipline in references/phase-1-deep-dive-us.md
§FS-Banks Augmentation.

Logic:
  1. Read memo sector_gics and industry_gics. If neither matches the
     Banks/Insurance/BDC keyword set → G16 = n_a (non-bank sector).
  2. Otherwise, the bank_metrics block must be present and must contain
     all four required disclosure groups:
       (a) AOCI bridge: afs_book_value_usd_b, afs_fair_value_usd_b,
           aoci_mark_usd_b, htm_book_value_usd_b, htm_fair_value_usd_b,
           tbvps_mtm_usd
       (b) CET1 walk: cet1_ratio_pct, required_cet1_pct
       (c) NIM trajectory: nim_latest_pct, nim_5y_trajectory (≥5 values),
           deposit_beta_cumulative_cycle_pct
       (d) Stress capital: scb_pct, capital_return_capacity_usd_b,
           ccar_dfast_severely_adverse_cet1_trough_pct (latter optional
           for Category IV / below-$100B, which gets a softer pass)
  3. If any of (a)-(d) is missing for a Banks sector → G16 = fail,
     blocks_score_above = 7.0.

The bank_metrics block can live at:
  - umbrella memo top-level: payload["bank_metrics"]
  - source_tags inline: payload["source_tags_inline"]["bank_metrics"]
  - source_tags external file (passed as --source-tags-json)

Usage:
    python scripts/verify_bank_metrics.py \\
        --memo-json <memo.json> \\
        [--source-tags-json <source_tags.json>]

Exit codes:
  0 = G16 passes (or n_a)
  non-zero = G16 fails
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

GATE_ID = "G16"

# Sector / industry keyword set that triggers bank discipline.
# Match is case-insensitive substring.
BANK_KEYWORDS = (
    "bank",
    "banks",
    "depository",
    "broker",
    "broker-dealer",
    "investment banking",
    "diversified financials",
    "regional financ",
    "insurance",
    "life insurance",
    "p&c",
    "property and casualty",
    "reinsurance",
    "bdc",
    "business development",
)

# Required field groups. Field names match schemas/source_tags.json
# bank_metrics block.
REQUIRED_AOCI_BRIDGE = [
    "afs_book_value_usd_b",
    "afs_fair_value_usd_b",
    "aoci_mark_usd_b",
    "htm_book_value_usd_b",
    "htm_fair_value_usd_b",
    "tbvps_mtm_usd",
]
REQUIRED_CET1_WALK = ["cet1_ratio_pct", "required_cet1_pct"]
REQUIRED_NIM = [
    "nim_latest_pct",
    "nim_5y_trajectory",
    "deposit_beta_cumulative_cycle_pct",
]
REQUIRED_STRESS_CAPITAL_FULL = [
    "scb_pct",
    "capital_return_capacity_usd_b",
    "ccar_dfast_severely_adverse_cet1_trough_pct",
]
REQUIRED_STRESS_CAPITAL_CATEGORY_IV = [
    "scb_pct",
    "capital_return_capacity_usd_b",
    # CCAR/DFAST trough optional for Cat IV / below-$100B
]


def _print_status(status: str, **kwargs: Any) -> None:
    print(f"gate_id: {GATE_ID}")
    print(f"status: {status}")
    for k, v in kwargs.items():
        print(f"{k}: {v}")


def _sector_is_bank(memo_json: dict[str, Any]) -> bool:
    fields = [memo_json.get("sector_gics", ""), memo_json.get("industry_gics", "")]
    blob = " ".join(str(f).lower() for f in fields if f)
    return any(kw in blob for kw in BANK_KEYWORDS)


def _extract_bank_metrics(payload: dict[str, Any], source_tags: dict[str, Any] | None) -> dict[str, Any] | None:
    bm = payload.get("bank_metrics")
    if isinstance(bm, dict):
        return bm
    inline = payload.get("source_tags_inline")
    if isinstance(inline, dict) and isinstance(inline.get("bank_metrics"), dict):
        return inline["bank_metrics"]
    if source_tags is not None and isinstance(source_tags.get("bank_metrics"), dict):
        return source_tags["bank_metrics"]
    return None


def _field_present(bm: dict[str, Any], key: str) -> bool:
    """A field is considered present if the value is non-None and (for arrays) non-empty."""
    if key not in bm:
        return False
    v = bm[key]
    if v is None:
        return False
    if isinstance(v, list):
        return len(v) >= (5 if key == "nim_5y_trajectory" else 1)
    return True


def _check_group(bm: dict[str, Any], group: list[str], label: str) -> list[str]:
    """Return list of missing field names for the group."""
    return [f for f in group if not _field_present(bm, f)]


def verify(memo_json: dict[str, Any], source_tags: dict[str, Any] | None) -> int:
    if not _sector_is_bank(memo_json):
        _print_status(
            "n_a",
            reason=(
                f"sector_gics={memo_json.get('sector_gics', '?')!r} / "
                f"industry_gics={memo_json.get('industry_gics', '?')!r} "
                "— not in {Banks, Insurance, BDC, Broker-Dealer}"
            ),
        )
        return 0

    bm = _extract_bank_metrics(memo_json, source_tags)
    if bm is None:
        _print_status(
            "fail",
            failure_reason="sector is Banks but bank_metrics block is absent",
            remediation_required=(
                "Add bank_metrics block per source_tags.json schema with "
                "AOCI bridge / CET1 walk / NIM trajectory / stress capital "
                "context per phase-1-deep-dive-us.md FS-Banks Augmentation."
            ),
            blocks_score_above=7.0,
        )
        return 1

    category = (bm.get("bank_category") or "").upper()
    stress_required = (
        REQUIRED_STRESS_CAPITAL_CATEGORY_IV
        if category in {"IV", "BELOW_100B"}
        else REQUIRED_STRESS_CAPITAL_FULL
    )

    missing_aoci = _check_group(bm, REQUIRED_AOCI_BRIDGE, "AOCI bridge")
    missing_cet1 = _check_group(bm, REQUIRED_CET1_WALK, "CET1 walk")
    missing_nim = _check_group(bm, REQUIRED_NIM, "NIM trajectory")
    missing_stress = _check_group(bm, stress_required, "Stress capital")

    all_missing = {
        "AOCI_bridge": missing_aoci,
        "CET1_walk": missing_cet1,
        "NIM_trajectory": missing_nim,
        "stress_capital": missing_stress,
    }
    failing_groups = [g for g, m in all_missing.items() if m]

    if failing_groups:
        details = "; ".join(
            f"{g} missing [{', '.join(all_missing[g])}]" for g in failing_groups
        )
        _print_status(
            "fail",
            failure_reason=(
                f"sector is Banks (category={category or 'unspecified'}), "
                "but bank_metrics is missing required field(s): " + details
            ),
            remediation_required=(
                "Populate missing fields per source_tags.json bank_metrics "
                "block + phase-1-deep-dive-us.md §FS-Banks Augmentation. "
                "All four groups (AOCI bridge / CET1 walk / NIM / stress capital) "
                "must be complete for G16 to pass."
            ),
            blocks_score_above=7.0,
        )
        return 2

    _print_status(
        "pass",
        sector_gics=memo_json.get("sector_gics", ""),
        bank_category=category,
        groups_verified="AOCI_bridge, CET1_walk, NIM_trajectory, stress_capital",
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify G16 — bank discipline required for Banks-sector memos."
        )
    )
    parser.add_argument("--memo-json", required=True, type=Path,
                        help="Path to structured memo JSON")
    parser.add_argument("--memo-md", required=False, type=Path, default=None,
                        help="(Unused for G16 — accepted for uniform calling contract)")
    parser.add_argument("--source-tags-json", required=False, type=Path, default=None,
                        help="(Optional) standalone source_tags.json sibling file")
    args = parser.parse_args(argv)

    if not args.memo_json.is_file():
        _print_status("fail", failure_reason=f"file not found: {args.memo_json}")
        return 6

    try:
        memo_json = json.loads(args.memo_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _print_status("fail", failure_reason=f"cannot parse memo JSON: {exc}")
        return 7

    source_tags: dict[str, Any] | None = None
    if args.source_tags_json is not None:
        try:
            source_tags = json.loads(args.source_tags_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            _print_status("fail", failure_reason=f"cannot parse source_tags JSON: {exc}")
            return 7

    return verify(memo_json, source_tags)


if __name__ == "__main__":
    sys.exit(main())
