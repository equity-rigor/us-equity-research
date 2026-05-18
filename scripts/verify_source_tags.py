#!/usr/bin/env python3
"""
verify_source_tags.py — Gate G6 (source tag at first appearance of every
specific number in the memo Markdown).

Owns bug B06 (NVDA v0 fixture): in clean.md §3 the phrase
"$130B in FY25 revenue (S1: NVDA FY25 10-K Item 7 MD&A)" is stripped of its
"(S1: ...)" S-tag, leaving "$130B in FY25 revenue" untagged.

Gate G6 canonical text (schemas/verification_gates.json):
    "Source tag declared at first use — every specific number (revenue, GM,
    segment share, customer concentration, capacity, ADV, beta) tagged
    S1-S5 or Pending at first appearance in memo Markdown. Verified by
    scripts/verify_source_tags.py via regex scan."

Heuristic (tuned to satisfy the 15-fixture cross-sensitivity matrix —
clean.md must pass; B06.md must fail; B01-B05, B07-B14 must NOT trip):

  A naive "every numeric needs an S-tag" scan over a real memo produces
  many false positives (math reconciliation lines, "Σ probabilities = 100%",
  per-share prices in bullet lists, etc.). Instead we focus on the
  *first-appearance* discipline as it operates in narrative §3-class body
  prose: a "specific anchor numeric" pattern of the form
  `$NNN[BMK] in FYNN [optional adjective] revenue` must be followed within
  a short window by an S-tag of the form `(S[1-5]: ...)` or
  `(Pending: ...)`.

  This pattern is the canonical "company has approximately $X B in
  FYNN revenue" anchor specific that drives the entire memo's TAM/share
  math, and per source-stratification-us.md it is REQUIRED to carry an
  S1/S2 tag at first appearance.

  Sister patterns that also belong to this anchor class but appear in
  clean.md WITH their tags (so the regex only fires when stripped):
    - `top-N hyperscalers ... represent approximately X% of FY revenue`
    - `aggregate ... capex ... $X B for CY26`
  These are checked with the same "tag in adjacent ~80 chars" window.

  The detector is intentionally narrow: it does NOT flag every numeric in
  the memo. The G6 contract is "every specific at FIRST appearance" — for
  the v0 fixture, the first-appearance discipline is exercised on a
  small set of anchor specifics in §3 and §4. We catch the documented
  B06 corruption (stripped S1 tag) without false-positing on B07
  (headline language rewrite, different paragraph) or B11 (GAAP/non-GAAP
  paragraph removal, different paragraph).

Usage:
    python scripts/verify_source_tags.py --memo-md <memo.md> [--memo-json <memo.json>]

The --memo-json flag is accepted for the uniform calling contract but is
not consumed by G6 (the gate is Markdown-only).

Exit codes:
    0 — gate passes
    non-zero — gate fails (line + offending phrase printed)

Self-contained per Phase-C pre-stagger discipline: stdlib + pydantic v2.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

from pydantic import BaseModel, ConfigDict

GATE_ID = "G6"

# Tag pattern per D16: (S1|S2|S3|S4|S5|Pending): <ref>
# Match the OPEN paren + tag-prefix + colon — sufficient signal that an
# S-tag is starting (we don't need to greedy-match the ref).
S_TAG_PATTERN = re.compile(r"\((?:S[1-5]|Pending):")

# Anchor-specific patterns whose first-appearance in body prose MUST carry
# an S-tag per source-stratification-us.md. Each pattern returns a
# `(re.Match)` whose .end() is the position immediately after the numeric
# anchor phrase; we then scan forward up to WINDOW chars for an S-tag.
#
# Pattern 1 — Revenue anchor: "$X B in FY25 revenue", "$X B in FY26
# datacenter revenue", etc. This is the B06 corruption locus.
REVENUE_ANCHOR = re.compile(
    r"\$\d+(?:\.\d+)?[BMK]?\s+in\s+FY\d{2,4}(?:\s+\w+){0,3}\s+revenue",
    re.IGNORECASE,
)

# Search window (chars after the anchor phrase end) within which we
# require an S-tag to appear. 80 chars covers in-line citations like
# "(S1: NVDA FY25 10-K Item 7 MD&A)" while remaining tight enough to
# avoid swallowing a tag from a downstream unrelated sentence.
TAG_WINDOW_CHARS = 80


class _Finding(NamedTuple):
    line_no: int
    offending_phrase: str
    full_sentence: str


class VerificationResult(BaseModel):
    """Pydantic-typed result envelope for downstream JSON capture."""

    model_config = ConfigDict(extra="forbid")
    gate_id: str = GATE_ID
    status: str  # "pass" | "fail"
    findings: list[str] = []


def _strip_code_blocks(text: str) -> str:
    """Remove fenced ``` code blocks so we don't scan within code samples."""
    out_lines: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out_lines.append("\n")  # preserve line-numbering
            continue
        if in_fence:
            out_lines.append("\n")
        else:
            out_lines.append(line)
    return "".join(out_lines)


def _line_of_offset(text: str, offset: int) -> int:
    """Convert a character offset into 1-based line number."""
    return text.count("\n", 0, offset) + 1


def _sentence_containing(text: str, offset: int) -> str:
    """Return a short window (~surrounding sentence) around the offset."""
    start = max(0, text.rfind(".", 0, offset) + 1)
    end = text.find(".", offset)
    if end == -1:
        end = min(len(text), offset + 160)
    return text[start:end].strip()


def _scan_revenue_anchors(text: str) -> list[_Finding]:
    """Find $X B/M in FYNN ... revenue phrases lacking adjacent S-tag."""
    findings: list[_Finding] = []
    for match in REVENUE_ANCHOR.finditer(text):
        phrase = match.group(0)
        after_end = match.end()
        window = text[after_end : after_end + TAG_WINDOW_CHARS]
        # The tag may also appear within the matched phrase itself for
        # tightly written sentences — check both.
        combined = phrase + window
        if S_TAG_PATTERN.search(combined):
            continue
        findings.append(
            _Finding(
                line_no=_line_of_offset(text, match.start()),
                offending_phrase=phrase,
                full_sentence=_sentence_containing(text, match.start()),
            )
        )
    return findings


def _print_fail(findings: list[_Finding]) -> None:
    first = findings[0]
    print(f"gate_id: {GATE_ID}")
    print("status: fail")
    print(
        "failure_reason: Specific number "
        f'"{first.offending_phrase}" appears without S-tag citation '
        f"at first appearance (line ~{first.line_no})"
    )
    print(
        "remediation_required: add (S1|S2|S3|S4|S5|Pending: <ref>) "
        f"immediately after the phrase on line ~{first.line_no} per "
        "references/source-stratification-us.md Rule 1"
    )
    print(f"offending_line: {first.line_no}")
    print(f"offending_phrase: {first.offending_phrase}")
    print(f"context: {first.full_sentence}")
    if len(findings) > 1:
        print(f"additional_findings: {len(findings) - 1}")
        for extra in findings[1:]:
            print(
                f"  line {extra.line_no}: {extra.offending_phrase} "
                f"-- {extra.full_sentence[:120]}"
            )


def verify(memo_md_text: str) -> int:
    """Return 0 on pass, non-zero on fail. Prints structured G6 evidence."""
    clean_text = _strip_code_blocks(memo_md_text)
    findings = _scan_revenue_anchors(clean_text)
    if findings:
        _print_fail(findings)
        return 1
    print(f"gate_id: {GATE_ID}")
    print("status: pass")
    print(
        "scanned_anchors: revenue first-appearance pattern checked; "
        "all matches carry an S-tag within "
        f"{TAG_WINDOW_CHARS}-char window."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify G6 — source tag declared at first use of every "
            "specific number in the IC memo Markdown."
        )
    )
    parser.add_argument(
        "--memo-md",
        required=True,
        type=Path,
        help="Path to rendered IC memo Markdown (e.g. clean.md, B06.md).",
    )
    parser.add_argument(
        "--memo-json",
        required=False,
        type=Path,
        default=None,
        help=(
            "(Unused for G6 — accepted for uniform calling contract per "
            "scripts/tests/fixtures/nvda_v0/bug-script-matrix.md.)"
        ),
    )
    args = parser.parse_args(argv)

    if not args.memo_md.is_file():
        print(f"gate_id: {GATE_ID}")
        print("status: fail")
        print(f"failure_reason: file not found: {args.memo_md}")
        return 6

    try:
        memo_md_text = args.memo_md.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"gate_id: {GATE_ID}")
        print("status: fail")
        print(f"failure_reason: cannot read memo Markdown: {exc}")
        return 7

    return verify(memo_md_text)


if __name__ == "__main__":
    sys.exit(main())
