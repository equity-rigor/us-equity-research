#!/usr/bin/env python3
"""
verify_source_tier_public.py — Gate G23 (source-tier public boundary).

Added in v0.7.0 (judgment layer). Encodes the compliance boundary that
the framework is practised on PURELY-PUBLIC information: every S1-S5
citation must resolve to a publicly accessible source. Entitlement-
restricted research (client-only sell-side notes, expert-network
transcripts under NDA, subscription-only feeds, anything marked
no-redistribution or no-AI-input) is OUT OF FRAMEWORK SCOPE — it may be
used only as a personal, non-persisted, localized cross-check, never as
a committed memo anchor.

Public sell-side SIGNALS are fine: aggregated consensus median/dispersion,
publicly-reported price targets and rating distributions, public PT
history. What G23 forbids is committing the proprietary NOTE itself
(or its restricted contents) as a citation.

G23 checks, on the source_tags JSON (and optionally the memo MD):

  (a) Every citation in all_citations[] and top_anchors[].citation must
      NOT declare access_tier="restricted" or public_access=false.
  (b) No citation `ref`/`source_type` may contain a high-confidence
      entitlement marker (client-only, no-redistribution, proprietary
      research, "expressly authorized", "destroy the document", named
      restricted research desks used as a primary citation, etc.).
  (c) (optional) if --memo-md given, the same markers must not appear in
      a citation context in the memo body.

n_a only when no source_tags file is supplied. Otherwise it runs.

Usage:
    python scripts/verify_source_tier_public.py --source-tags-json <tags.json> [--memo-json <m>] [--memo-md <md>]

Exit codes: 0 = pass / n_a; non-zero = fail.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GATE = "G23"

# High-confidence markers that a source is entitlement-restricted / non-public.
# Firm-agnostic by design: the test is the no-redistribution / client-only STATUS,
# not who published it. (Public sell-side SIGNALS via aggregators are fine and S4.)
_RESTRICTED = re.compile(
    r"(client[\-\s]?only|not\s+for\s+redistribution|do\s+not\s+redistribute|"
    r"no[\-\s]redistribution|proprietary\s+research|expressly\s+authorized|"
    r"destroy\s+the\s+document|subscription[\-\s]?only|subscriber[\-\s]?only|"
    r"entitled\s+recipients?|restricted\s+research|"
    r"broker\s+research\s+note|sell[\-\s]side\s+(?:note|research)\b)",
    re.IGNORECASE,
)


def _iter_citations(tags: dict):
    for c in tags.get("all_citations", []) or []:
        if isinstance(c, dict):
            yield c
    for a in tags.get("top_anchors", []) or []:
        if isinstance(a, dict) and isinstance(a.get("citation"), dict):
            yield a["citation"]


def verify_tags(tags: dict, memo_md_text: str | None) -> int:
    offenders = []
    n = 0
    for c in _iter_citations(tags):
        n += 1
        ref = str(c.get("ref", ""))
        stype = str(c.get("source_type", ""))
        if c.get("access_tier") == "restricted" or c.get("public_access") is False:
            offenders.append(f"access_tier/public_access flags non-public: {ref[:80]!r}")
            continue
        hay = f"{stype} :: {ref}"
        m = _RESTRICTED.search(hay)
        if m:
            offenders.append(f"restricted marker '{m.group(0)}' in citation: {ref[:80]!r}")

    if memo_md_text:
        # only flag markers that appear next to a source tag like "(S4: ... <marker> ...)"
        for m in re.finditer(r"\(S[1-5][^)]*\)", memo_md_text):
            if _RESTRICTED.search(m.group(0)):
                offenders.append(f"restricted marker in memo citation: {m.group(0)[:80]!r}")

    if offenders:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: {len(offenders)} citation(s) resolve to entitlement-restricted / non-public sources — framework anchors must be publicly accessible")
        for o in offenders[:6]:
            print(f"  - {o}")
        return 22

    print(f"gate_id: {GATE}\nstatus: pass\ncitations_checked: {n}\nnote: all citations resolve to publicly accessible sources")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Verify G23 — source-tier public boundary (judgment layer).")
    p.add_argument("--source-tags-json", required=False, type=Path, default=None)
    p.add_argument("--memo-json", required=False, type=Path, default=None,
                   help="If source_tags not given, the memo's inline source_tags_inline block is used")
    p.add_argument("--memo-md", required=False, type=Path, default=None)
    args = p.parse_args(argv)

    tags = None
    if args.source_tags_json and args.source_tags_json.exists():
        try:
            tags = json.loads(args.source_tags_json.read_text())
        except json.JSONDecodeError as exc:
            print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: invalid JSON: {exc}")
            return 21
    elif args.memo_json and args.memo_json.exists():
        try:
            tags = (json.loads(args.memo_json.read_text()) or {}).get("source_tags_inline")
        except json.JSONDecodeError as exc:
            print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: invalid JSON: {exc}")
            return 21

    if not isinstance(tags, dict):
        print(f"gate_id: {GATE}\nstatus: n_a\nreason: no source_tags supplied")
        return 0

    md_text = None
    if args.memo_md and args.memo_md.exists():
        md_text = args.memo_md.read_text(errors="ignore")

    return verify_tags(tags, md_text)


if __name__ == "__main__":
    sys.exit(main())
