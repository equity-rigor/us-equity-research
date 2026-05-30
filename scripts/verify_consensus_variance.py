#!/usr/bin/env python3
"""
verify_consensus_variance.py — Gate G15 (consensus variance declared for
non-Hold rated memos OR memo self-labeled "consensus-anchored" in headline).

Added in v0.2.0. Full discipline in references/consensus-variance-us.md.

Logic:
  1. If memo recommendation.rating is "Hold" → G15 = n_a (consensus-
     anchored Hold is a valid rating, no variance required).
  2. If memo Markdown headline contains "consensus-anchored" (case-
     insensitive) → G15 = n_a (memo has self-labeled honestly).
  3. If memo source_tags has revision_velocity.n_analysts < 5 → G15 = n_a
     (thin coverage — no meaningful consensus baseline).
  4. Otherwise, memo must have ≥1 entry in consensus_variance block with:
     - sizing_impact_pp ≥ 2.0 (load-bearing)
     - ≥1 evidence_ref at s_level ∈ {S1, S2, S3} (not all-S4/S5)
     If absent or all-decorative or all-weak-evidence → G15 = fail,
     blocks_score_above = 7.0.

The consensus_variance block can live at one of:
  - umbrella memo top-level: payload["consensus_variance"]
  - source_tags inline: payload["source_tags_inline"]["consensus_variance"]
  - source_tags external file: payload["source_tags_ref"] pointing to a
    file that contains consensus_variance — caller passes that file as
    --memo-json directly, or as --source-tags-json sibling.

Usage:
    python scripts/verify_consensus_variance.py \\
        --memo-json <memo.json or structured.json> \\
        --memo-md <memo.md> \\
        [--source-tags-json <source_tags.json>]

Exit codes:
  0 = G15 passes (or n_a)
  non-zero = G15 fails
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

GATE_ID = "G15"
SIZING_LOAD_BEARING_PP = 2.0
PRIMARY_S_LEVELS = {"S1", "S2", "S3"}
HOLD_RATINGS = {"Hold"}
CONSENSUS_ANCHORED_PATTERN = re.compile(r"consensus[\s\-]anchored", re.IGNORECASE)
# v0.3.0 — derived-value recomputation tolerance per audit Issue #3.
# The formula in consensus-variance-us.md:
#   sizing_impact_pp = magnitude_pct * probability_pct * sensitivity_pct / 10000
# (since each factor is in %, multiplying three % values and dividing by
# 10000 converts to percentage points: 20% × 60% × 8% = 0.96pp)
SIZING_RECOMPUTE_TOLERANCE_PP = 0.1


def _print_status(status: str, **kwargs: Any) -> None:
    print(f"gate_id: {GATE_ID}")
    print(f"status: {status}")
    for k, v in kwargs.items():
        print(f"{k}: {v}")


def _extract_consensus_variance(payload: dict[str, Any], source_tags: dict[str, Any] | None) -> list[dict[str, Any]] | None:
    """Locate consensus_variance array across the three accepted locations."""
    if isinstance(payload.get("consensus_variance"), list):
        return payload["consensus_variance"]
    inline = payload.get("source_tags_inline")
    if isinstance(inline, dict) and isinstance(inline.get("consensus_variance"), list):
        return inline["consensus_variance"]
    if source_tags is not None and isinstance(source_tags.get("consensus_variance"), list):
        return source_tags["consensus_variance"]
    return None


def _extract_n_analysts(payload: dict[str, Any], source_tags: dict[str, Any] | None) -> int | None:
    """Locate revision_velocity.n_analysts across accepted locations."""
    rv = payload.get("revision_velocity")
    if not isinstance(rv, dict):
        inline = payload.get("source_tags_inline")
        if isinstance(inline, dict):
            rv = inline.get("revision_velocity")
    if not isinstance(rv, dict) and source_tags is not None:
        rv = source_tags.get("revision_velocity")
    if isinstance(rv, dict) and isinstance(rv.get("n_analysts"), int):
        return rv["n_analysts"]
    return None


def _is_load_bearing(variance: dict[str, Any]) -> bool:
    sizing = variance.get("sizing_impact_pp")
    if not isinstance(sizing, (int, float)):
        return False
    if abs(sizing) < SIZING_LOAD_BEARING_PP:
        return False
    refs = variance.get("evidence_refs") or []
    for ref in refs:
        if isinstance(ref, dict) and ref.get("s_level") in PRIMARY_S_LEVELS:
            return True
    return False


def verify(memo_json: dict[str, Any], memo_md: str, source_tags: dict[str, Any] | None) -> int:
    rating = (memo_json.get("recommendation") or {}).get("rating")

    # Branch 1: Hold rating = n_a
    if rating in HOLD_RATINGS:
        _print_status("n_a", reason=f"rating={rating} (consensus-anchored Hold is a valid rating)")
        return 0

    # Branch 2: explicit "consensus-anchored" self-label in Markdown headline
    # Restrict the scan to the first ~50 lines (headline / recommendation
    # section) to avoid false positives in deeper body prose.
    headline_window = "\n".join(memo_md.splitlines()[:50])
    if CONSENSUS_ANCHORED_PATTERN.search(headline_window):
        _print_status("n_a", reason="headline self-labeled 'consensus-anchored'")
        return 0

    # Branch 3: thin coverage
    n_analysts = _extract_n_analysts(memo_json, source_tags)
    if isinstance(n_analysts, int) and n_analysts < 5:
        _print_status("n_a", reason=f"n_analysts={n_analysts} < 5 (no meaningful consensus baseline)")
        return 0

    # Branch 4: actual gate check
    variances = _extract_consensus_variance(memo_json, source_tags)
    if variances is None or len(variances) == 0:
        _print_status(
            "fail",
            failure_reason=(
                f"rating={rating} requires consensus_variance block with "
                "load-bearing entries per G15, but block is absent or empty"
            ),
            remediation_required=(
                "Add consensus_variance entries to source_tags.json per "
                "consensus-variance-us.md, OR self-label headline as "
                "'consensus-anchored' and lower rating to Hold."
            ),
            blocks_score_above=7.0,
        )
        return 1

    load_bearing = [v for v in variances if _is_load_bearing(v)]
    if len(load_bearing) == 0:
        decorative_count = len(variances)
        _print_status(
            "fail",
            failure_reason=(
                f"rating={rating} requires ≥1 load-bearing variance "
                f"(sizing_impact_pp ≥ {SIZING_LOAD_BEARING_PP} AND ≥1 "
                "evidence_ref at S1-S3); found "
                f"{decorative_count} declared but 0 load-bearing"
            ),
            remediation_required=(
                "Either size up the variance with stronger evidence to "
                "reach load-bearing threshold, or self-label headline as "
                "'consensus-anchored' and lower rating to Hold."
            ),
            blocks_score_above=7.0,
        )
        return 2

    # Branch 5 (v0.3.0): derived-value recomputation.
    # For each variance with magnitude_pct, probability_right_pct, and
    # scenario_sensitivity_pct all populated, recompute
    # sizing_impact_pp = magnitude × probability × sensitivity / 10000
    # and verify the declared value matches within ±0.1pp. Catches
    # the audit-flagged failure mode where authors write internally
    # inconsistent variance math (declared sizing_impact_pp != formula).
    for idx, v in enumerate(variances):
        magnitude = v.get("magnitude_pct")
        prob = v.get("probability_right_pct")
        sens = v.get("scenario_sensitivity_pct")
        declared = v.get("sizing_impact_pp")
        if not all(isinstance(x, (int, float)) for x in (magnitude, prob, sens, declared)):
            continue  # Optional fields missing — skip recomputation.
        expected = (abs(magnitude) * prob * sens) / 10000.0
        # Signed sizing: variance with positive magnitude shifts scenario
        # probability up; negative magnitude shifts down. Take absolute
        # value of magnitude for the recomputation (sign carried in
        # the declared value).
        if abs(abs(declared) - expected) > SIZING_RECOMPUTE_TOLERANCE_PP:
            vid = v.get("variance_id") or v.get("line_item") or f"index_{idx}"
            _print_status(
                "fail",
                failure_reason=(
                    f"variance {vid!r} declares sizing_impact_pp="
                    f"{declared:.3f} but recomputed from "
                    f"magnitude_pct={magnitude} × probability_right_pct="
                    f"{prob} × scenario_sensitivity_pct={sens} / 10000 = "
                    f"{expected:.3f} (tolerance ±{SIZING_RECOMPUTE_TOLERANCE_PP}pp). "
                    "Internal inconsistency in variance math."
                ),
                remediation_required=(
                    "Either correct the declared sizing_impact_pp to match "
                    "the formula, OR adjust magnitude / probability / "
                    "sensitivity inputs to reflect the intended scenario "
                    "shift. Per consensus-variance-us.md: sizing_impact_pp = "
                    "magnitude_pct × probability_right_pct × "
                    "scenario_sensitivity_pct / 10000."
                ),
                offending_variance=vid,
                declared_sizing_impact_pp=f"{declared:.3f}",
                recomputed_sizing_impact_pp=f"{expected:.3f}",
                delta_pp=f"{abs(abs(declared) - expected):.3f}",
                blocks_score_above=7.0,
            )
            return 3

    types_declared = sorted({v.get("type", "?") for v in load_bearing})
    total_sizing = sum(
        abs(v.get("sizing_impact_pp", 0.0))
        for v in load_bearing
        if isinstance(v.get("sizing_impact_pp"), (int, float))
    )
    _print_status(
        "pass",
        rating=rating,
        load_bearing_count=len(load_bearing),
        types_declared=",".join(types_declared),
        total_sizing_impact_pp=f"{total_sizing:.2f}",
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify G15 — consensus variance declared for non-Hold "
            "memos or memo self-labeled 'consensus-anchored'."
        )
    )
    parser.add_argument("--memo-json", required=True, type=Path,
                        help="Path to structured memo JSON")
    parser.add_argument("--memo-md", required=True, type=Path,
                        help="Path to memo Markdown (for headline self-label scan)")
    parser.add_argument("--source-tags-json", required=False, type=Path, default=None,
                        help="(Optional) standalone source_tags.json sibling file")
    args = parser.parse_args(argv)

    for p, label in [(args.memo_json, "memo JSON"), (args.memo_md, "memo Markdown")]:
        if not p.is_file():
            _print_status("fail", failure_reason=f"file not found: {p} ({label})")
            return 6

    try:
        memo_json = json.loads(args.memo_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _print_status("fail", failure_reason=f"cannot parse memo JSON: {exc}")
        return 7

    try:
        memo_md = args.memo_md.read_text(encoding="utf-8")
    except OSError as exc:
        _print_status("fail", failure_reason=f"cannot read memo Markdown: {exc}")
        return 7

    source_tags: dict[str, Any] | None = None
    if args.source_tags_json is not None:
        try:
            source_tags = json.loads(args.source_tags_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            _print_status("fail", failure_reason=f"cannot parse source_tags JSON: {exc}")
            return 7

    return verify(memo_json, memo_md, source_tags)


if __name__ == "__main__":
    sys.exit(main())
