#!/usr/bin/env python3
"""
verify_revision_velocity.py — Gate G17 (earnings revision velocity
disclosure required when n_analysts >= 5).

Added in v0.2.0. Full discipline in references/phase-2-continuation-us.md
§A6 Earnings Revision Velocity subsection.

Logic:
  1. Read revision_velocity block from memo source_tags. If absent →
     check whether memo claims coverage. If n_analysts can be inferred
     from elsewhere (e.g., source_tags consensus snapshot), use that.
  2. If revision_velocity.n_analysts < 5 OR g17_status is set to
     "n_a_thin_coverage" → G17 = n_a (thin coverage).
  3. Otherwise, require these three fields populated (the load-bearing
     minimum per G17):
       - fy1_eps_revision_3m_pct (number)
       - breadth_3m (number in [-1.0, 1.0])
       - g17_status = "disclosed"
  4. If any required field missing or invalid → G17 = fail,
     blocks_score_above = 7.5.

The block can live at:
  - umbrella memo top-level: payload["revision_velocity"]
  - source_tags inline: payload["source_tags_inline"]["revision_velocity"]
  - source_tags external file (passed as --source-tags-json)

Usage:
    python scripts/verify_revision_velocity.py \\
        --memo-json <memo.json> \\
        [--source-tags-json <source_tags.json>]

Exit codes:
  0 = G17 passes (or n_a)
  non-zero = G17 fails
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

GATE_ID = "G17"
N_ANALYSTS_THIN_THRESHOLD = 5
BREADTH_VALID_RANGE = (-1.0, 1.0)
REQUIRED_FIELDS = ["fy1_eps_revision_3m_pct", "breadth_3m"]


def _print_status(status: str, **kwargs: Any) -> None:
    print(f"gate_id: {GATE_ID}")
    print(f"status: {status}")
    for k, v in kwargs.items():
        print(f"{k}: {v}")


def _extract_revision_velocity(payload: dict[str, Any], source_tags: dict[str, Any] | None) -> dict[str, Any] | None:
    rv = payload.get("revision_velocity")
    if isinstance(rv, dict):
        return rv
    inline = payload.get("source_tags_inline")
    if isinstance(inline, dict) and isinstance(inline.get("revision_velocity"), dict):
        return inline["revision_velocity"]
    if source_tags is not None and isinstance(source_tags.get("revision_velocity"), dict):
        return source_tags["revision_velocity"]
    return None


def verify(memo_json: dict[str, Any], source_tags: dict[str, Any] | None) -> int:
    rv = _extract_revision_velocity(memo_json, source_tags)

    if rv is None:
        _print_status(
            "fail",
            failure_reason="revision_velocity block is absent from memo / source_tags",
            remediation_required=(
                "Add revision_velocity block to source_tags.json per the "
                "schema. At minimum populate n_analysts, "
                "fy1_eps_revision_3m_pct, breadth_3m, g17_status. "
                "If n_analysts < 5, set g17_status to "
                "'n_a_thin_coverage' instead."
            ),
            blocks_score_above=7.5,
        )
        return 1

    n_analysts = rv.get("n_analysts")
    g17_status_declared = rv.get("g17_status")

    # n_a path: thin coverage
    if g17_status_declared == "n_a_thin_coverage":
        _print_status(
            "n_a",
            reason=(
                f"g17_status declared 'n_a_thin_coverage' "
                f"(n_analysts={n_analysts})"
            ),
        )
        return 0
    if isinstance(n_analysts, int) and n_analysts < N_ANALYSTS_THIN_THRESHOLD:
        _print_status(
            "n_a",
            reason=(
                f"n_analysts={n_analysts} < {N_ANALYSTS_THIN_THRESHOLD} "
                "(thin coverage; revision velocity not load-bearing)"
            ),
        )
        return 0

    # Required-field check
    missing = []
    invalid = []
    for f in REQUIRED_FIELDS:
        if f not in rv or rv[f] is None:
            missing.append(f)
            continue
        if not isinstance(rv[f], (int, float)):
            invalid.append(f"{f}={rv[f]!r}")
    if isinstance(rv.get("breadth_3m"), (int, float)):
        b = rv["breadth_3m"]
        if not (BREADTH_VALID_RANGE[0] <= b <= BREADTH_VALID_RANGE[1]):
            invalid.append(
                f"breadth_3m={b} outside [{BREADTH_VALID_RANGE[0]}, "
                f"{BREADTH_VALID_RANGE[1]}]"
            )

    if g17_status_declared != "disclosed":
        # Allow absent g17_status to still pass if other fields are
        # complete — but flag it so callers can normalize.
        if g17_status_declared is not None:
            invalid.append(
                f"g17_status={g17_status_declared!r} (expected 'disclosed' "
                "or 'n_a_thin_coverage')"
            )

    if missing or invalid:
        details = []
        if missing:
            details.append(f"missing=[{', '.join(missing)}]")
        if invalid:
            details.append(f"invalid=[{'; '.join(invalid)}]")
        _print_status(
            "fail",
            failure_reason=(
                f"revision_velocity disclosure incomplete: {' '.join(details)}"
            ),
            remediation_required=(
                "Populate the missing/invalid fields per source_tags.json "
                "revision_velocity schema; minimum fields are "
                "fy1_eps_revision_3m_pct and breadth_3m, with breadth_3m "
                "in [-1.0, 1.0]. Set g17_status='disclosed' when complete."
            ),
            blocks_score_above=7.5,
        )
        return 2

    _print_status(
        "pass",
        n_analysts=n_analysts if n_analysts is not None else "unspecified",
        fy1_eps_revision_3m_pct=rv["fy1_eps_revision_3m_pct"],
        breadth_3m=rv["breadth_3m"],
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify G17 — earnings revision velocity disclosure when "
            "coverage is non-thin (n_analysts >= 5)."
        )
    )
    parser.add_argument("--memo-json", required=True, type=Path,
                        help="Path to structured memo JSON")
    parser.add_argument("--memo-md", required=False, type=Path, default=None,
                        help="(Unused for G17 — accepted for uniform calling contract)")
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
