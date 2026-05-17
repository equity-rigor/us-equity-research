#!/usr/bin/env python3
"""
verify_headline_conditionality.py — Phase C gate G7 (headline conditionality
matches anchor strength). Cross-layer JSON↔Markdown verifier.

Owns bug B07 (NVDA v0 fixture): both JSON and Markdown layers corrupted —
`scenarios_inline.headline.conditionality` flipped to "unconditional" while
`top_anchors[0..2]` still contains an S3 anchor (A3 Blackwell ASP). The
clean.md Pattern-A source-conditional language is also stripped from the
§1 headline paragraph and the §2 HEADLINE CONDITIONALITY line.

G7 contract:
  - "Strong" top-3 = every one of top_anchors[0..2].citation.s_level ∈ {S1, S2}
  - "Weak"   top-3 = any of top_anchors[0..2].citation.s_level ∈ {S3, S4, S5, Pending}
  - If weak → `headline.conditionality` MUST be "source_conditional" or
    "range_only" (never "unconditional"), AND the §1 headline paragraph
    must use Pattern A/B/C/D conditional language.
  - If strong → "unconditional" is preferred; "source_conditional" is allowed
    as cautious overstatement (no failure raised).
  - JSON-internal cross-check: `scenarios_inline.headline.conditionality` ==
    `source_tags_inline.headline_conditionality`.
  - MD↔JSON cross-check: the `HEADLINE CONDITIONALITY:` line in §2 of the
    rendered Markdown reports the same value as the JSON.

Pattern A/B/C/D marker phrases (per references/source-stratification-us.md):
  - Pattern A — Source-conditional bias: "source-conditional", "source_conditional"
  - Pattern B — If-then event trigger:   "conditional on", "subject to",
                                         "downgrade to", "upgrade to"
  - Pattern C — Anchored to upcoming filing: "anchored to", "view is anchored",
                                             "re-rate after"
  - Pattern D — Consensus range (S4-anchored): "consensus range",
                                               "scenario-weighted range",
                                               "range anchored"

Usage:
    python scripts/verify_headline_conditionality.py <memo.json> [--memo-md <path>]

If --memo-md is omitted the script looks for a sibling .md at the same
stem as memo.json (e.g. fixtures/nvda_v0/clean.json → clean.md).

Exit codes:
    0 — gate passes
    1 — gate fails (mismatch detected)
    2 — usage / IO / schema error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError

GATE_ID = "G7"
WEAK_S_LEVELS = {"S3", "S4", "S5", "Pending"}
ALLOWED_CONDITIONALITY = {"unconditional", "source_conditional", "range_only"}

# Pattern A/B/C/D marker phrases (case-insensitive).
PATTERN_MARKERS = (
    "source-conditional", "source_conditional",  # Pattern A
    "conditional on", "subject to", "downgrade to", "upgrade to",  # Pattern B
    "anchored to", "view is anchored", "re-rate after",  # Pattern C
    "consensus range", "scenario-weighted range", "range anchored",  # Pattern D
)

REMEDIATION = (
    "remediation_required: scenarios_inline.headline + "
    "source_tags_inline.headline_conditionality + §1 headline paragraph "
    "(restore Pattern A/B/C/D conditional language per "
    "references/source-stratification-us.md)"
)


# ----- Minimal pydantic slices ----------------------------------------------


class _Citation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    s_level: str


class _Anchor(BaseModel):
    model_config = ConfigDict(extra="ignore")
    anchor_id: Optional[str] = None
    citation: _Citation


class _Headline(BaseModel):
    model_config = ConfigDict(extra="ignore")
    conditionality: str
    headline_text: Optional[str] = ""


class _ScenariosInline(BaseModel):
    model_config = ConfigDict(extra="ignore")
    headline: _Headline


class _SourceTagsInline(BaseModel):
    model_config = ConfigDict(extra="ignore")
    top_anchors: list[_Anchor] = Field(min_length=3)
    headline_conditionality: str


class _Memo(BaseModel):
    model_config = ConfigDict(extra="ignore")
    scenarios_inline: _ScenariosInline
    source_tags_inline: _SourceTagsInline


# ----- Helpers ---------------------------------------------------------------


def _emit_fail(reason: str, *, extras: Optional[dict] = None) -> None:
    print(f"gate_id: {GATE_ID}\nstatus: fail\nfailure_reason: {reason}")
    if extras:
        for k, v in extras.items():
            print(f"{k}: {v}")
    print(REMEDIATION)


def _extract_section_1_headline(md_text: str) -> str:
    """First bolded paragraph after the `## §1` header (stops at blank line)."""
    m = re.search(r"##\s+§1\b[^\n]*\n", md_text)
    if not m:
        return ""
    body = md_text[m.end():]
    nxt = re.search(r"\n##\s+§\d", body)
    if nxt:
        body = body[: nxt.start()]
    bold_open = body.find("**")
    if bold_open < 0:
        return ""
    chunk = body[bold_open:]
    para_end = chunk.find("\n\n")
    return chunk.strip() if para_end < 0 else chunk[:para_end].strip()


def _extract_md_conditionality(md_text: str) -> Optional[str]:
    r"""Pull value from the `HEADLINE CONDITIONALITY: \`<val>\`` line in §2."""
    m = re.search(
        r"HEADLINE\s+CONDITIONALITY\*?\*?\s*[:\-]\s*`?([a-z_]+)`?",
        md_text, flags=re.IGNORECASE,
    )
    return m.group(1).strip().lower() if m else None


def _has_pattern_marker(text: str) -> bool:
    if not text:
        return False
    lower = text.lower()
    return any(m in lower for m in PATTERN_MARKERS)


# ----- Core verification -----------------------------------------------------


def verify(memo_raw: dict, md_text: str) -> int:
    """Return 0 on pass, non-zero on fail. Prints structured G7 evidence."""
    try:
        memo = _Memo.model_validate(memo_raw)
    except ValidationError as exc:
        _emit_fail(f"memo JSON missing required structure for G7: {exc.errors()[0]['msg']}")
        return 2

    sti = memo.source_tags_inline
    si_headline = memo.scenarios_inline.headline
    top3 = [a.citation.s_level for a in sti.top_anchors[:3]]
    weak = any(lvl in WEAK_S_LEVELS for lvl in top3)

    json_cond_scen = si_headline.conditionality
    json_cond_st = sti.headline_conditionality

    # Conditionality enum sanity.
    if json_cond_scen not in ALLOWED_CONDITIONALITY:
        _emit_fail(f"scenarios_inline.headline.conditionality has invalid value '{json_cond_scen}'")
        return 2
    if json_cond_st not in ALLOWED_CONDITIONALITY:
        _emit_fail(f"source_tags_inline.headline_conditionality has invalid value '{json_cond_st}'")
        return 2

    # JSON-internal cross-check.
    if json_cond_scen != json_cond_st:
        _emit_fail(
            f"JSON-internal mismatch: scenarios_inline.headline.conditionality"
            f"='{json_cond_scen}' but source_tags_inline.headline_conditionality"
            f"='{json_cond_st}'",
            extras={"top_3_s_levels": ",".join(top3)},
        )
        return 1

    # Primary G7 check: weak top-3 cannot claim unconditional.
    if weak and json_cond_scen == "unconditional":
        _emit_fail(
            f"headline.conditionality='unconditional' but top-3 anchors "
            f"include weak S-level ({','.join(top3)}). Required: "
            f"'source_conditional' (any S3) or 'range_only' (S4/S5 leading) "
            f"with Pattern A/B/C/D language.",
            extras={"top_3_s_levels": ",".join(top3), "json_conditionality": json_cond_scen},
        )
        return 1

    # Markdown headline-language check (only enforced when weak top-3).
    if weak:
        sec1 = _extract_section_1_headline(md_text)
        if not _has_pattern_marker(sec1):
            snip = (sec1 or "<empty>")[:180].replace("\n", " ")
            _emit_fail(
                "§1 headline paragraph lacks Pattern A/B/C/D conditional "
                f"language marker despite weak top-3 anchors ({','.join(top3)})",
                extras={
                    "top_3_s_levels": ",".join(top3),
                    "json_conditionality": json_cond_scen,
                    "md_headline_snippet": snip,
                },
            )
            return 1
        if not _has_pattern_marker(si_headline.headline_text or ""):
            snip = (si_headline.headline_text or "")[:180].replace("\n", " ")
            _emit_fail(
                "scenarios_inline.headline.headline_text lacks Pattern A/B/C/D "
                f"language despite weak top-3 anchors ({','.join(top3)})",
                extras={
                    "top_3_s_levels": ",".join(top3),
                    "json_conditionality": json_cond_scen,
                    "json_headline_snippet": snip,
                },
            )
            return 1

    # MD↔JSON cross-check on §2 HEADLINE CONDITIONALITY line.
    md_cond = _extract_md_conditionality(md_text)
    if md_cond is not None and md_cond != json_cond_scen:
        _emit_fail(
            f"cross-layer mismatch: §2 HEADLINE CONDITIONALITY='{md_cond}' "
            f"but JSON conditionality='{json_cond_scen}'",
            extras={
                "top_3_s_levels": ",".join(top3),
                "md_conditionality": md_cond,
                "json_conditionality": json_cond_scen,
            },
        )
        return 1

    # Pass.
    print(f"gate_id: {GATE_ID}\nstatus: pass")
    print(f"top_3_s_levels: {','.join(top3)}")
    print(f"json_conditionality: {json_cond_scen}")
    print(f"top_3_strength: {'weak' if weak else 'strong'}")
    return 0


# ----- CLI -------------------------------------------------------------------


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify G7 — headline conditionality matches anchor strength.",
    )
    parser.add_argument("memo_json", type=Path, help="Path to structured memo JSON")
    parser.add_argument(
        "--memo-md", type=Path, default=None,
        help="Path to rendered Markdown memo (default: sibling .md to memo_json)",
    )
    args = parser.parse_args(argv)

    if not args.memo_json.is_file():
        print(f"gate_id: {GATE_ID}\nstatus: fail\n"
              f"failure_reason: memo JSON not found: {args.memo_json}", file=sys.stderr)
        return 2

    try:
        memo_raw = json.loads(args.memo_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"gate_id: {GATE_ID}\nstatus: fail\n"
              f"failure_reason: invalid JSON in {args.memo_json}: {exc}", file=sys.stderr)
        return 2

    md_path = args.memo_md if args.memo_md is not None else args.memo_json.with_suffix(".md")
    if not md_path.is_file():
        print(f"gate_id: {GATE_ID}\nstatus: fail\n"
              f"failure_reason: memo Markdown not found: {md_path}", file=sys.stderr)
        return 2

    return verify(memo_raw, md_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    sys.exit(main())
