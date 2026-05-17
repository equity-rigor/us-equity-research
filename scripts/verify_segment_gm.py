#!/usr/bin/env python3
"""verify_segment_gm.py — Phase C gate G2 verifier (segment GM reconciliation).

Computes weighted_gm = Σ(seg_revenue × seg_GM) / Σ(seg_revenue) for the
current-period segment breakdown (financials.ltm.segments, falling back to
historical segments only if no LTM block is present) and verifies it agrees
with the period's consolidated gross_margin_pct within ±50bp.

Owns bug B02 (financials.ltm.segments[Datacenter].gm_pct 76.5 → 80.0 drives
weighted GM 74.88% → 78.02% vs reported 75.00% → 302bp delta).

Scope is LTM-only because historical-period segment rows in schemas/memo.json
are illustrative and frequently partial; enforcing G2 on them yields false
positives. GM fields are percent points (75.0 == 75.00%), so 50bp == 0.50pp.

Usage:  python scripts/verify_segment_gm.py <path/to/memo.json>
Exit:   0 = pass / n_a; 1 = fail; 2 = usage / IO error.

Self-contained per Phase-C pre-stagger discipline: stdlib + pydantic v2 only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError

GATE_ID = "G2"
TOL_BP = 50.0
TOL_PP = TOL_BP / 100.0  # 50bp == 0.50 percent points


class Segment(BaseModel):
    """Minimal slice of a segment row required for G2."""

    model_config = ConfigDict(extra="ignore")

    name: str
    revenue_usd_m: float
    gm_pct: float


class FinancialPeriod(BaseModel):
    """Minimal slice of a financial period required for G2."""

    model_config = ConfigDict(extra="ignore")

    period: str
    period_type: Optional[str] = None
    revenue_usd_m: Optional[float] = None
    gross_margin_pct: Optional[float] = None
    segments: Optional[list[Segment]] = None


def _collect_periods(payload: dict) -> list[FinancialPeriod]:
    """Return [LTM] if LTM has segments; else fall back to historical periods
    that have segments (covers single-period memos without an LTM block).

    Historical-period segment rows are skipped whenever an LTM with segments
    is present, because historicals are illustrative/partial and not the
    canonical target of G2."""
    financials = payload.get("financials") or {}
    periods: list[FinancialPeriod] = []

    ltm = financials.get("ltm")
    if isinstance(ltm, dict) and ltm.get("segments"):
        try:
            periods.append(FinancialPeriod.model_validate(ltm))
            return periods
        except ValidationError:
            # Malformed LTM — fall through to historicals.
            pass

    hist = financials.get("historical")
    if isinstance(hist, list):
        for raw in hist:
            if not (isinstance(raw, dict) and raw.get("segments")):
                continue
            try:
                periods.append(FinancialPeriod.model_validate(raw))
            except ValidationError:
                continue
    return periods


def _is_reconcilable(period: FinancialPeriod) -> bool:
    """Reconcilable iff period has gross_margin_pct and non-empty segments
    with strictly positive total revenue."""
    if period.gross_margin_pct is None or not period.segments:
        return False
    seg_total = sum(s.revenue_usd_m for s in period.segments)
    return seg_total > 0


def _weighted_gm(period: FinancialPeriod) -> float:
    """Compute Σ(rev × gm) / Σ(rev) in percent points."""
    segs = period.segments or []
    total_rev = sum(s.revenue_usd_m for s in segs)
    if total_rev == 0:
        return 0.0
    total_gp = sum(s.revenue_usd_m * s.gm_pct for s in segs)
    return total_gp / total_rev


def verify(payload: dict) -> tuple[list[dict], int]:
    """Return (failures, periods_checked); empty failures means gate passes."""
    failures: list[dict] = []
    periods_checked = 0
    for period in _collect_periods(payload):
        if not _is_reconcilable(period):
            continue
        periods_checked += 1
        weighted = _weighted_gm(period)
        reported = period.gross_margin_pct  # type: ignore[assignment]
        delta_pp = abs(weighted - reported)
        if delta_pp > TOL_PP:
            failures.append(
                {
                    "period": period.period,
                    "weighted_gm_pct": weighted,
                    "reported_gm_pct": reported,
                    "delta_bp": delta_pp * 100.0,
                    "segments": [
                        {"name": s.name, "rev": s.revenue_usd_m, "gm_pct": s.gm_pct}
                        for s in (period.segments or [])
                    ],
                }
            )
    return failures, periods_checked


def emit_failure(failures: list[dict]) -> None:
    """Structured error output matching schemas/verification_gates.json evidence."""
    first = failures[0]
    print(f"gate_id: {GATE_ID}")
    print("status: fail")
    reason = (
        f'Period "{first["period"]}" segment-weighted GM '
        f'{first["weighted_gm_pct"]:.2f}% diverges from consolidated GM '
        f'{first["reported_gm_pct"]:.2f}% by {first["delta_bp"]:.1f}bp '
        f'(tolerance ±{TOL_BP:.0f}bp)'
    )
    print(f"failure_reason: {reason}")
    print(
        f'remediation_required: financials.{first["period"]}.segments[].gm_pct '
        f"OR financials.{first['period']}.gross_margin_pct"
    )
    print(f"segments_checked: {len(first['segments'])}")
    for s in first["segments"]:
        print(
            f"  - {s['name']}: revenue=${s['rev']:.0f}M × GM={s['gm_pct']:.2f}%"
        )
    if len(failures) > 1:
        print(f"additional_failures: {len(failures) - 1}")
        for extra in failures[1:]:
            print(
                f"  - {extra['period']}: weighted={extra['weighted_gm_pct']:.2f}% "
                f"vs reported={extra['reported_gm_pct']:.2f}% "
                f"({extra['delta_bp']:.1f}bp)"
            )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "Usage: python scripts/verify_segment_gm.py <path/to/memo.json>",
            file=sys.stderr,
        )
        return 2

    path = Path(argv[1])
    if not path.is_file():
        print(f"verify_segment_gm.py: file not found: {path}", file=sys.stderr)
        return 2

    try:
        with path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"verify_segment_gm.py: cannot read JSON: {exc}", file=sys.stderr)
        return 2

    failures, periods_checked = verify(payload)
    if failures:
        emit_failure(failures)
        return 1

    print(
        f"gate_id: {GATE_ID} status: pass "
        f"({periods_checked} period(s) reconciled within ±{TOL_BP:.0f}bp)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
