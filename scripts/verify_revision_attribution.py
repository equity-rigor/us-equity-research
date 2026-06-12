#!/usr/bin/env python3
"""
verify_revision_attribution.py — Gate G22 (revision attribution).

Added in v0.7.0 (judgment layer). Encodes Lesson 2 of the de-bias work:
when a target price is revised, the change must be DECOMPOSED into how
much came from new estimates (verifiable), how much from the multiple
(judgment), and how much from a methodology switch. A revision driven
mostly by the multiple or a methodology change — rather than by new
estimates — is an anchoring/judgment flag and must be labelled as such,
not presented as if new facts moved the number.

G22 is self-gating: n_a when `valuation.revision_bridge` (or top-level
`revision_bridge`) is absent — i.e. it only binds on rebuilds/revisions.
When present it checks, on the structured memo JSON:

  (a) Shape: prior_price_target_usd, new_price_target_usd numeric;
      components is a non-empty list, each with driver in
      {estimate, multiple, methodology, other}, numeric delta_usd, and a
      non-empty rationale.
  (b) Arithmetic: sum(component.delta_usd) reconciles to
      (new_price_target_usd - prior_price_target_usd) within max($1, 1%).
  (c) Judgment honesty: judgment_share_pct (share of the ABSOLUTE move
      attributable to multiple + methodology) must be present and match
      the components within 3pp; and if judgment_share_pct > 50 the memo
      must carry a non-empty judgment_flag note (acknowledging that the
      revision is judgment-led, hence lower-confidence) — this is the
      anti-anchoring discipline.

Usage:
    python scripts/verify_revision_attribution.py --memo-json <memo.json> [--memo-md <path>]

Exit codes: 0 = pass / n_a; non-zero = fail.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GATE = "G22"
_DRIVER_ENUM = {"estimate", "multiple", "methodology", "other"}


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def verify(payload: dict) -> int:
    rb = (payload.get("valuation") or {}).get("revision_bridge")
    if rb is None:
        rb = payload.get("revision_bridge")
    if not isinstance(rb, dict):
        print(f"gate_id: {GATE}\nstatus: n_a\nreason: no revision_bridge (not a revision/rebuild memo)")
        return 0

    prior = _num(rb.get("prior_price_target_usd"))
    new = _num(rb.get("new_price_target_usd"))
    comps = rb.get("components")
    if prior is None or new is None:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: revision_bridge missing numeric prior_price_target_usd / new_price_target_usd")
        return 22
    if not isinstance(comps, list) or not comps:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: revision_bridge.components must be a non-empty list")
        return 23

    total = 0.0
    judgment_abs = 0.0
    all_abs = 0.0
    for i, c in enumerate(comps):
        if not isinstance(c, dict):
            print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: component[{i}] is not an object")
            return 24
        d = _num(c.get("delta_usd"))
        drv = c.get("driver")
        rat = (c.get("rationale") or "").strip()
        if d is None or drv not in _DRIVER_ENUM or len(rat) < 6:
            print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: component[{i}] needs numeric delta_usd, driver in {sorted(_DRIVER_ENUM)}, and a rationale (got driver={drv!r})")
            return 25
        total += d
        all_abs += abs(d)
        if drv in ("multiple", "methodology"):
            judgment_abs += abs(d)

    tol = max(1.0, 0.01 * abs(new))
    if abs(total - (new - prior)) > tol:
        print(
            f"gate_id: {GATE}\nstatus: fail\n"
            f"failure_reason: components sum {total:+.2f} != (new - prior) {(new - prior):+.2f} (tol ${tol:.2f}) — the attribution must reconcile"
        )
        return 26

    computed_share = (judgment_abs / all_abs * 100.0) if all_abs else 0.0
    declared_share = _num(rb.get("judgment_share_pct"))
    if declared_share is None:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: revision_bridge.judgment_share_pct required (share of |move| from multiple+methodology); computed {computed_share:.0f}%")
        return 27
    if abs(declared_share - computed_share) > 3.0:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: declared judgment_share_pct {declared_share:.0f}% != computed {computed_share:.0f}% (tol 3pp)")
        return 28

    if computed_share > 50.0:
        flag = (rb.get("judgment_flag") or "").strip()
        if len(flag) < 12:
            print(
                f"gate_id: {GATE}\nstatus: fail\n"
                f"failure_reason: {computed_share:.0f}% of the revision is multiple+methodology (judgment), not new estimates — "
                f"a non-empty judgment_flag (acknowledging the revision is judgment-led / lower-confidence) is required"
            )
            return 29

    print(
        f"gate_id: {GATE}\nstatus: pass\n"
        f"prior_pt: {prior:.2f}\nnew_pt: {new:.2f}\ntotal_move: {(new-prior):+.2f}\n"
        f"judgment_share_pct: {computed_share:.0f}\n"
        f"note: {'judgment-led (flagged)' if computed_share > 50 else 'estimate-led'}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Verify G22 — revision attribution (judgment layer).")
    p.add_argument("--memo-json", required=True, type=Path)
    p.add_argument("--memo-md", required=False, type=Path, default=None, help="(unused)")
    p.add_argument("--source-tags-json", required=False, type=Path, default=None, help="(unused)")
    args = p.parse_args(argv)
    try:
        payload = json.loads(args.memo_json.read_text())
    except FileNotFoundError:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: file not found: {args.memo_json}")
        return 20
    except json.JSONDecodeError as exc:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: invalid JSON: {exc}")
        return 21
    return verify(payload)


if __name__ == "__main__":
    sys.exit(main())
