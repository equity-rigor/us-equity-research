#!/usr/bin/env python3
"""
verify_view_defensibility.py — Gate G20 (view defensibility for memos
claiming a rubric score above 8.5).

Added in v0.3.0. Closes the audit Issue #1 (highest severity): the
17-gate verification stack grades structural completeness, not view
quality. A consensus-hugging memo with perfect mechanical execution
scored 9.0+ under v0.2.0. G20 raises the bar by requiring three
conjunctive conditions for any score above 8.5.

Logic:

  1. If memo recommendation.rating == "Hold" → G20 = n_a (Hold rating
     is not a non-consensus claim; no defensibility required).
  2. If memo Markdown headline self-labels "consensus-anchored" → n_a
     (the honest path; rating cap already applied via G15).
  3. If memo n_analysts < 5 (thin coverage) → n_a (no consensus
     baseline to differ from).
  4. Otherwise, all three conditions must hold:

     (a) **Differentiation magnitude.** Headline
         recommendation.upside_downside_pct differs from S4 consensus
         PT-implied return by at least 8.0 absolute percentage points.
         The consensus PT-implied return is computed from
         source_tags.top_anchors or revision_velocity / consensus
         snapshot if a S4-tagged PT median exists in the memo.

     (b) **Evidence strength.** At least one declared consensus_variance
         entry must have ≥1 evidence_ref at S1 or S2 (S3 alone, S4
         alone, S5 alone all insufficient for the strongest evidence
         requirement of the load-bearing variance set). Standard G15
         (v0.2.0) accepted S1-S3 evidence; G20 tightens to require S1
         or S2 specifically on at least one variance — the strongest
         claim must be primary-source-anchored.

     (c) **Survival of structured attack.** The memo's
         adjudication_trail (v0.3.0) must contain at least one entry
         with type='variance_attack', target_variance_id referencing
         a load-bearing variance, attack_type in the 5 canonical
         dimensions (evidence_credibility, triangulation_completeness,
         base_rate_sanity, catalyst_dependency, timing_arbitrage), and
         attack_outcome in {rebutted, modified}. Variance attacks with
         outcome='conceded' do not satisfy G20 because conceded
         variances are removed from the load-bearing set.

  5. v0.1.x and v0.2.0 memos grandfathered (G20 = skipped,
     reason='grandfathered_pre_v0_3').

Caps score at 8.5 on fail (not 7.0 — G20 is rubric-discriminating
not memo-killing).

Usage:
    python scripts/verify_view_defensibility.py \\
        --memo-json <memo.json> --memo-md <memo.md> \\
        [--source-tags-json <source_tags.json>]

Exit codes:
  0 = G20 passes (or n_a or skipped)
  non-zero = G20 fails
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

GATE_ID = "G20"
DIFFERENTIATION_THRESHOLD_PP = 8.0
PRIMARY_S_LEVELS_TIGHTEST = {"S1", "S2"}  # G20 tightens vs G15's S1-S3
CANONICAL_ATTACK_TYPES = {
    "evidence_credibility",
    "triangulation_completeness",
    "base_rate_sanity",
    "catalyst_dependency",
    "timing_arbitrage",
}
SURVIVING_OUTCOMES = {"rebutted", "modified"}
HOLD_RATINGS = {"Hold"}
CONSENSUS_ANCHORED_PATTERN = re.compile(r"consensus[\s\-]anchored", re.IGNORECASE)
N_ANALYSTS_THIN_THRESHOLD = 5
FAIL_CAP = 8.5


def _print_status(status: str, **kwargs: Any) -> None:
    print(f"gate_id: {GATE_ID}")
    print(f"status: {status}")
    for k, v in kwargs.items():
        print(f"{k}: {v}")


def _extract_consensus_variance(payload: dict[str, Any], source_tags: dict[str, Any] | None) -> list[dict[str, Any]]:
    if isinstance(payload.get("consensus_variance"), list):
        return payload["consensus_variance"]
    inline = payload.get("source_tags_inline")
    if isinstance(inline, dict) and isinstance(inline.get("consensus_variance"), list):
        return inline["consensus_variance"]
    if source_tags is not None and isinstance(source_tags.get("consensus_variance"), list):
        return source_tags["consensus_variance"]
    return []


def _extract_n_analysts(payload: dict[str, Any], source_tags: dict[str, Any] | None) -> int | None:
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


def _extract_consensus_pt_implied_return_pct(
    payload: dict[str, Any], source_tags: dict[str, Any] | None
) -> float | None:
    """Look for an S4-tagged PT median among top_anchors or consensus snapshot.

    Returns the consensus-implied return as a percentage (e.g., +12.5 means
    consensus PT is 12.5% above spot). None if no S4 PT median found.
    """
    # Approach 1: top_anchors with claim mentioning 'PT' / 'price target'
    # and an S4 citation containing 'consensus' / 'FactSet' / 'Visible Alpha'.
    candidates: list[dict[str, Any]] = []
    for container in (payload, payload.get("source_tags_inline"), source_tags):
        if not isinstance(container, dict):
            continue
        top_anchors = container.get("top_anchors")
        if isinstance(top_anchors, list):
            candidates.extend(a for a in top_anchors if isinstance(a, dict))

    spot = None
    cur = payload.get("current_price_usd")
    if isinstance(cur, (int, float)):
        spot = float(cur)

    for anchor in candidates:
        claim = str(anchor.get("claim", "")).lower()
        citation = anchor.get("citation") or {}
        if isinstance(citation, dict) and citation.get("s_level") == "S4":
            ref = str(citation.get("ref", "")).lower()
            if "pt" in claim or "price target" in claim or "pt" in ref:
                value = anchor.get("value")
                if isinstance(value, (int, float)) and spot is not None and spot > 0:
                    return ((value - spot) / spot) * 100.0
    # No PT anchor with S4 → cannot compute consensus-implied return.
    return None


def _has_load_bearing_with_s1_or_s2(variances: list[dict[str, Any]]) -> tuple[bool, dict[str, Any] | None]:
    """Find a load-bearing variance with at least one S1 or S2 evidence_ref."""
    for v in variances:
        sizing = v.get("sizing_impact_pp")
        if not isinstance(sizing, (int, float)) or abs(sizing) < 2.0:
            continue
        if not v.get("load_bearing", True):
            continue
        refs = v.get("evidence_refs") or []
        for ref in refs:
            if isinstance(ref, dict) and ref.get("s_level") in PRIMARY_S_LEVELS_TIGHTEST:
                return (True, v)
    return (False, None)


def _attack_survives_for_load_bearing(
    adjudication_trail: list[dict[str, Any]],
    load_bearing_variances: list[dict[str, Any]],
) -> tuple[bool, str]:
    """Verify at least one load-bearing variance has a surviving attack entry."""
    load_bearing_ids = {
        v.get("variance_id") or v.get("line_item")
        for v in load_bearing_variances
    }
    for entry in adjudication_trail:
        if not isinstance(entry, dict):
            continue
        if entry.get("type") != "variance_attack":
            continue
        attack_type = entry.get("attack_type")
        outcome = entry.get("attack_outcome")
        target = entry.get("target_variance_id")
        if (
            attack_type in CANONICAL_ATTACK_TYPES
            and outcome in SURVIVING_OUTCOMES
            and target in load_bearing_ids
        ):
            return (True, str(target))
    return (False, "")


def verify(
    memo_json: dict[str, Any], memo_md: str, source_tags: dict[str, Any] | None
) -> int:
    schema_version = memo_json.get("schema_version", "0.1.0")
    if schema_version != "0.3.0":
        _print_status(
            "skipped",
            reason=f"grandfathered_pre_v0_3 (schema_version={schema_version})",
        )
        return 0

    rating = (memo_json.get("recommendation") or {}).get("rating")
    if rating in HOLD_RATINGS:
        _print_status("n_a", reason=f"rating={rating} (Hold is not a non-consensus claim)")
        return 0

    headline_window = "\n".join(memo_md.splitlines()[:50])
    if CONSENSUS_ANCHORED_PATTERN.search(headline_window):
        _print_status("n_a", reason="headline self-labeled 'consensus-anchored'")
        return 0

    n_analysts = _extract_n_analysts(memo_json, source_tags)
    if isinstance(n_analysts, int) and n_analysts < N_ANALYSTS_THIN_THRESHOLD:
        _print_status(
            "n_a",
            reason=f"n_analysts={n_analysts} < {N_ANALYSTS_THIN_THRESHOLD} (no consensus baseline)",
        )
        return 0

    # Condition (a): differentiation magnitude
    headline_return = (memo_json.get("recommendation") or {}).get("upside_downside_pct")
    consensus_return = _extract_consensus_pt_implied_return_pct(memo_json, source_tags)
    if not isinstance(headline_return, (int, float)):
        _print_status(
            "fail",
            failure_reason=(
                "recommendation.upside_downside_pct absent or non-numeric; "
                "cannot compute differentiation magnitude"
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 1
    if consensus_return is None:
        _print_status(
            "fail",
            failure_reason=(
                "no S4-tagged PT median found in top_anchors; cannot compute "
                "consensus-implied return for differentiation check. Add an "
                "S4 PT median anchor (claim including 'PT' / 'price target', "
                "citation with s_level=S4)."
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 2
    differentiation = abs(headline_return - consensus_return)
    if differentiation < DIFFERENTIATION_THRESHOLD_PP:
        _print_status(
            "fail",
            failure_reason=(
                f"differentiation magnitude {differentiation:.2f}pp below "
                f"G20 threshold {DIFFERENTIATION_THRESHOLD_PP:.1f}pp "
                f"(headline expected return {headline_return:+.2f}% vs "
                f"consensus PT-implied return {consensus_return:+.2f}%). "
                "Memo is too close to consensus to claim score above 8.5. "
                "Either differentiate the headline OR self-label 'consensus-"
                "anchored' and accept the Hold rating ceiling."
            ),
            blocks_score_above=FAIL_CAP,
            headline_expected_return_pct=f"{headline_return:+.2f}",
            consensus_implied_return_pct=f"{consensus_return:+.2f}",
            differentiation_pp=f"{differentiation:.2f}",
        )
        return 3

    # Condition (b): evidence strength
    variances = _extract_consensus_variance(memo_json, source_tags)
    has_s12, exemplar = _has_load_bearing_with_s1_or_s2(variances)
    if not has_s12:
        _print_status(
            "fail",
            failure_reason=(
                "no load-bearing consensus_variance has any evidence_ref at "
                "S1 or S2. G15 (v0.2.0) accepts S1-S3 for any load-bearing "
                "variance; G20 (v0.3.0) tightens to require at least one S1 "
                "or S2 (primary-source) evidence ref on at least one "
                "load-bearing variance — the strongest claim in the memo "
                "must be primary-source-anchored, not weak-secondary."
            ),
            remediation_required=(
                "Strengthen the evidence for at least one load-bearing "
                "variance by citing a 10-K, 10-Q, 8-K, DEF 14A, 20-F, or "
                "Form 4 directly. If no primary-source evidence is "
                "available for any declared variance, the memo cannot "
                "claim score above 8.5 and should be sized down accordingly."
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 4

    # Condition (c): attack survival
    adjudication_trail = memo_json.get("adjudication_trail") or []
    if not isinstance(adjudication_trail, list):
        adjudication_trail = []
    load_bearing = [v for v in variances if v.get("load_bearing", True) and abs(v.get("sizing_impact_pp", 0)) >= 2.0]
    attack_survived, target = _attack_survives_for_load_bearing(
        adjudication_trail, load_bearing
    )
    if not attack_survived:
        _print_status(
            "fail",
            failure_reason=(
                "no adjudication_trail entry of type='variance_attack' "
                "targets a load-bearing variance with attack_type in the "
                "5 canonical dimensions and attack_outcome in {rebutted, "
                "modified}. G20 requires that R-v2 attempted a structured "
                "attack and that the variance survived (or was modified) "
                "with documented reasoning. Generic attacks ('could be "
                "wrong') do not satisfy G20."
            ),
            remediation_required=(
                "Add at least one adjudication_trail entry with "
                "type='variance_attack', target_variance_id pointing to a "
                "load-bearing variance, attack_type in {evidence_credibility, "
                "triangulation_completeness, base_rate_sanity, "
                "catalyst_dependency, timing_arbitrage}, and attack_outcome "
                "in {rebutted, modified}. Discipline in "
                "references/pm-synthesis-adjudication-us.md §R-v2 attack "
                "methodology."
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 5

    _print_status(
        "pass",
        differentiation_pp=f"{differentiation:.2f}",
        load_bearing_variance_with_s1_or_s2=exemplar.get("line_item") if exemplar else None,
        surviving_attack_target=target,
        adjudication_trail_entries=len(adjudication_trail),
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify G20 — view defensibility (differentiation + primary "
            "evidence + surviving attack) for memos claiming rubric > 8.5."
        )
    )
    parser.add_argument("--memo-json", required=True, type=Path)
    parser.add_argument("--memo-md", required=True, type=Path)
    parser.add_argument("--source-tags-json", required=False, type=Path, default=None)
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
            _print_status("fail", failure_reason=f"cannot parse source_tags: {exc}")
            return 7

    return verify(memo_json, memo_md, source_tags)


if __name__ == "__main__":
    sys.exit(main())
