#!/usr/bin/env python3
"""
verify_quant_cross_doc_consistency.py — Gate G18 (quant overlay
cross-document consistency).

Added in v0.3.0. Full discipline in
us-equity-ic-rigor/references/quant-overlay-us.md §'Honest framing'.

Closes the audit finding that, in pre-v0.3.0 Plugin 2 reference files,
the same NVDA name carried different Barra z-scores across documents
(Momentum +1.8 in quant-overlay-us.md, +2.3 in position-sizing-us.md).
G18 catches the same disease at memo runtime: when the analyst (or LLM)
quotes a factor z-score in Markdown prose that diverges from the
structured `quant_overlay.factor_tags` block in memo.json, G18 fails.

Logic:
  1. Read memo JSON; extract quant_overlay.factor_tags. If missing,
     return n_a (G13 separately enforces factor_tags presence —
     don't double-fail).
  2. Scan memo Markdown for narrative references to the 7 canonical
     Barra factors: Value, Quality, Momentum, Growth, Size, Low-Vol,
     Liquidity. Pattern: factor name + optional whitespace + sign
     (+/-/Unicode minus) + decimal number.
  3. For each Markdown match, compare to the structured value within
     ±0.2 tolerance. Tolerance reflects "narrative may round to one
     decimal" while still catching real drift (+1.8 vs +2.3 = 0.5
     gap, well outside tolerance).
  4. If any mismatch found, fail with offending factor + Markdown value
     + structured value + delta.
  5. If structured block exists but no Markdown references found,
     return pass with note (narrative did not quote factor numbers —
     internally consistent by default).

Usage:
    python scripts/verify_quant_cross_doc_consistency.py \\
        --memo-json <memo.json> --memo-md <memo.md>

Exit codes:
  0 = G18 passes (or n_a)
  non-zero = G18 fails
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, NamedTuple

GATE_ID = "G18"
TOLERANCE = 0.2

# Canonical Barra factor names. Keys match memo.json
# definitions/quant_overlay.factor_tags property names.
CANONICAL_FACTORS = {
    "value": ["value"],
    "quality": ["quality"],
    "momentum": ["momentum"],
    "growth": ["growth"],
    "size": ["size"],
    "low_vol": ["low-vol", "low_vol", "low vol", "lowvol"],
    "liquidity": ["liquidity"],
}

# Build a regex that matches: <factor display name> + whitespace +
# (+/-/Unicode minus) + decimal number.
# Handles "Momentum +1.8", "Value −1.5", "Low-Vol +0.2", "Low Vol +0.2"
# and the common variation patterns. Case-insensitive.
_FACTOR_DISPLAY_PATTERNS = []
for canonical, aliases in CANONICAL_FACTORS.items():
    for alias in aliases:
        escaped = re.escape(alias)
        _FACTOR_DISPLAY_PATTERNS.append((canonical, escaped))

# One mega-regex that captures (factor_alias_index, sign_char, number).
# We compile per-factor to keep capture groups simple.
_PER_FACTOR_RE = {
    canonical: re.compile(
        # Negative lookbehind to avoid matching mid-word "Value" inside
        # "Devalue" etc. — require word boundary or punctuation.
        r"(?<![A-Za-z])(?:" + "|".join(re.escape(a) for a in aliases) + r")\b"
        r"\s*([+\-−])\s*"
        r"(\d+(?:\.\d+)?)",
        re.IGNORECASE,
    )
    for canonical, aliases in CANONICAL_FACTORS.items()
}


class _Mismatch(NamedTuple):
    factor: str
    markdown_value: float
    structured_value: float
    delta: float
    markdown_excerpt: str
    line_no: int


def _print_status(status: str, **kwargs: Any) -> None:
    print(f"gate_id: {GATE_ID}")
    print(f"status: {status}")
    for k, v in kwargs.items():
        print(f"{k}: {v}")


def _normalize_sign(sign_char: str) -> int:
    if sign_char in ("-", "−"):
        return -1
    return 1


def _line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks so we don't match values in code samples."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("\n")
            continue
        out.append("\n" if in_fence else line)
    return "".join(out)


def _extract_factor_tags(memo_json: dict[str, Any]) -> dict[str, float] | None:
    """Find factor_tags across the umbrella memo or quant_overlay sub-object."""
    qo = memo_json.get("quant_overlay")
    if isinstance(qo, dict) and isinstance(qo.get("factor_tags"), dict):
        return {
            k.lower(): float(v) for k, v in qo["factor_tags"].items() if isinstance(v, (int, float))
        }
    if isinstance(memo_json.get("factor_tags"), dict):
        return {
            k.lower(): float(v)
            for k, v in memo_json["factor_tags"].items()
            if isinstance(v, (int, float))
        }
    return None


def _scan_markdown(memo_md: str) -> list[tuple[str, float, str, int]]:
    """Return list of (factor_canonical, signed_value, excerpt, line_no)."""
    cleaned = _strip_code_blocks(memo_md)
    findings: list[tuple[str, float, str, int]] = []
    for canonical, pat in _PER_FACTOR_RE.items():
        for m in pat.finditer(cleaned):
            try:
                value = _normalize_sign(m.group(1)) * float(m.group(2))
            except (ValueError, IndexError):
                continue
            start = max(0, m.start() - 40)
            end = min(len(cleaned), m.end() + 40)
            excerpt = cleaned[start:end].replace("\n", " ").strip()
            findings.append((canonical, value, excerpt, _line_of_offset(cleaned, m.start())))
    return findings


def verify(memo_json: dict[str, Any], memo_md: str) -> int:
    factor_tags = _extract_factor_tags(memo_json)
    if factor_tags is None:
        _print_status(
            "n_a",
            reason="quant_overlay.factor_tags absent (G13 handles presence separately)",
        )
        return 0

    md_findings = _scan_markdown(memo_md)
    if not md_findings:
        _print_status(
            "pass",
            reason="no Markdown factor references found; consistency trivially holds",
            structured_factors=",".join(sorted(factor_tags.keys())),
        )
        return 0

    mismatches: list[_Mismatch] = []
    matched_factor_set: set[str] = set()
    for canonical, md_value, excerpt, line_no in md_findings:
        struct_value = factor_tags.get(canonical)
        if struct_value is None:
            mismatches.append(
                _Mismatch(
                    factor=canonical,
                    markdown_value=md_value,
                    structured_value=float("nan"),
                    delta=float("nan"),
                    markdown_excerpt=excerpt,
                    line_no=line_no,
                )
            )
            continue
        matched_factor_set.add(canonical)
        delta = abs(md_value - struct_value)
        if delta > TOLERANCE:
            mismatches.append(
                _Mismatch(
                    factor=canonical,
                    markdown_value=md_value,
                    structured_value=struct_value,
                    delta=delta,
                    markdown_excerpt=excerpt,
                    line_no=line_no,
                )
            )

    if mismatches:
        first = mismatches[0]
        if first.structured_value != first.structured_value:  # NaN check
            reason = (
                f"Markdown references factor '{first.factor}' "
                f"({first.markdown_value:+.2f}) but structured "
                "factor_tags does not contain this factor"
            )
        else:
            reason = (
                f"Markdown '{first.factor} {first.markdown_value:+.2f}' "
                f"(line ~{first.line_no}) diverges from structured "
                f"factor_tags.{first.factor} = {first.structured_value:+.2f} "
                f"by {first.delta:.2f} (tolerance {TOLERANCE:.2f})"
            )
        _print_status(
            "fail",
            failure_reason=reason,
            remediation_required=(
                "Reconcile Markdown narrative factor z-scores with structured "
                "quant_overlay.factor_tags block per quant-overlay-us.md "
                "§'Honest framing'. Within ±0.2 tolerance. "
                "If both are wrong (guessed values), fix the canonical "
                "structured block first, then have the Markdown re-read it."
            ),
            offending_factor=first.factor,
            markdown_value=f"{first.markdown_value:+.2f}",
            structured_value=(
                f"{first.structured_value:+.2f}"
                if first.structured_value == first.structured_value
                else "absent"
            ),
            offending_line=first.line_no,
            markdown_excerpt=first.markdown_excerpt[:120],
            blocks_score_above=7.5,
        )
        if len(mismatches) > 1:
            print(f"additional_mismatches: {len(mismatches) - 1}")
            for m in mismatches[1:]:
                if m.structured_value == m.structured_value:
                    print(
                        f"  {m.factor}: md={m.markdown_value:+.2f} "
                        f"vs struct={m.structured_value:+.2f} "
                        f"(delta {m.delta:.2f}, line {m.line_no})"
                    )
                else:
                    print(
                        f"  {m.factor}: md={m.markdown_value:+.2f} "
                        f"vs struct=absent (line {m.line_no})"
                    )
        return 1

    _print_status(
        "pass",
        markdown_factor_references=len(md_findings),
        factors_compared=",".join(sorted(matched_factor_set)),
        tolerance=f"±{TOLERANCE:.2f}",
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify G18 — quant overlay cross-document consistency "
            "between memo.json factor_tags and Markdown narrative."
        )
    )
    parser.add_argument("--memo-json", required=True, type=Path)
    parser.add_argument("--memo-md", required=True, type=Path)
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

    return verify(memo_json, memo_md)


if __name__ == "__main__":
    sys.exit(main())
