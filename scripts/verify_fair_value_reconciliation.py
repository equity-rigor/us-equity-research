#!/usr/bin/env python3
"""
verify_fair_value_reconciliation.py — Gate G21 (fair-value reconciliation).

Added in v0.7.0 (judgment layer). Encodes Lesson 1 of the de-bias work:
a memo must compute BOTH an independent fair value (what it is worth,
built without reference to price) AND a market-regime value (where it
trades given the current multiple regime, e.g. the public consensus PT),
and the 12-month base price target must be a convergence-weighted blend
of the two — NOT silently spot-anchored.

G21 is self-gating: n_a when the `valuation_parallel` block is absent
(so it does not disturb grandfathered pre-v0.7.0 memos). When present it
checks, on the structured memo JSON:

  (a) Required fields present and numeric: independent_fair_value_usd,
      market_regime_value_usd, current_price_usd, twelve_month_base_pt_usd,
      and a non-empty independent_fair_value_basis (proving the fair value
      was built independently, not copied from price/consensus).
  (b) Reconciliation: if the 12-month base PT diverges from the
      independent fair value by more than 15%, the memo MUST explicitly
      justify the gap as a timing/regime call — convergence_assumption
      non-empty AND convergence_speed in {fast, moderate, slow, n_a}.
      Divergence <= 15% passes automatically (base is anchored to FV).
  (c) Consistency: if recommendation.price_target_usd is present it must
      equal twelve_month_base_pt_usd within $0.51 (the base PT the memo
      headlines must be the same number the parallel block blends to).

Usage:
    python scripts/verify_fair_value_reconciliation.py --memo-json <memo.json> [--memo-md <path>]

Exit codes: 0 = pass / n_a; non-zero = fail.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GATE = "G21"
_SPEED_ENUM = {"fast", "moderate", "slow", "n_a"}


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def verify(payload: dict) -> int:
    vp = payload.get("valuation_parallel")
    if not isinstance(vp, dict):
        print(f"gate_id: {GATE}\nstatus: n_a\nreason: no valuation_parallel block (pre-v0.7.0 / judgment layer not applicable)")
        return 0

    fv = _num(vp.get("independent_fair_value_usd"))
    regime = _num(vp.get("market_regime_value_usd"))
    price = _num(vp.get("current_price_usd"))
    base = _num(vp.get("twelve_month_base_pt_usd"))
    basis = (vp.get("independent_fair_value_basis") or "").strip()

    missing = [k for k, v in [
        ("independent_fair_value_usd", fv), ("market_regime_value_usd", regime),
        ("current_price_usd", price), ("twelve_month_base_pt_usd", base),
    ] if v is None]
    if missing:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: valuation_parallel missing/non-numeric fields: {', '.join(missing)}")
        return 22
    if len(basis) < 12:
        print(f"gate_id: {GATE}\nstatus: fail\nfailure_reason: independent_fair_value_basis empty/too short — fair value must be built independently of price, and the basis must be stated")
        return 23

    # (b) reconciliation / convergence discipline
    divergence = abs(base / fv - 1.0) if fv else 0.0
    if divergence > 0.15:
        conv_note = (vp.get("convergence_assumption") or "").strip()
        conv_speed = vp.get("convergence_speed")
        if len(conv_note) < 12 or conv_speed not in _SPEED_ENUM:
            print(
                f"gate_id: {GATE}\nstatus: fail\n"
                f"failure_reason: base PT ${base:.2f} diverges {divergence*100:.1f}% from independent fair value ${fv:.2f} (>15%) "
                f"but the gap is not justified as a timing/regime call — convergence_assumption and convergence_speed in "
                f"{{fast,moderate,slow,n_a}} are required.\nconvergence_speed: {conv_speed!r}"
            )
            return 24

    # (c) consistency with the headline PT
    rec_pt = _num((payload.get("recommendation") or {}).get("price_target_usd"))
    if rec_pt is not None and abs(rec_pt - base) > 0.51:
        print(
            f"gate_id: {GATE}\nstatus: fail\n"
            f"failure_reason: recommendation.price_target_usd ${rec_pt:.2f} != valuation_parallel.twelve_month_base_pt_usd ${base:.2f} "
            f"(the headline base PT must equal the blended base)"
        )
        return 25

    gap_px = (price / fv - 1.0) * 100 if fv else 0.0
    print(
        f"gate_id: {GATE}\nstatus: pass\n"
        f"independent_fair_value_usd: {fv:.2f}\nmarket_regime_value_usd: {regime:.2f}\n"
        f"twelve_month_base_pt_usd: {base:.2f}\nprice_vs_fair_value_pct: {gap_px:+.1f}\n"
        f"base_vs_fair_value_pct: {(base/fv-1)*100:+.1f}\nconvergence_speed: {vp.get('convergence_speed')}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Verify G21 — fair-value reconciliation (judgment layer).")
    p.add_argument("--memo-json", required=True, type=Path)
    p.add_argument("--memo-md", required=False, type=Path, default=None, help="(unused; uniform calling contract)")
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
