#!/usr/bin/env python3
"""Gate G3 — SOTP monotonicity verification.

For every segment in the SOTP valuation method, verify NI <= OP <= GP <= Revenue
within rounding tolerance (delta <= $10M absolute AND <= 0.5% relative).
Any inversion exceeding both bounds is a hard fail. N/A if no SOTP method present.

Usage:
    python scripts/verify_sotp_monotonicity.py --memo-json <path> [--memo-md <path>]

Exit 0 = pass or N/A; non-zero = fail.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from pydantic import BaseModel, Field, ValidationError
except ModuleNotFoundError:
    # Stdlib-only fallback for environments without pydantic.
    # Production has pydantic; this branch keeps regression tests runnable.
    class ValidationError(Exception):  # type: ignore[no-redef]
        pass
    def Field(default=None, **_kwargs):  # type: ignore[no-redef]
        return default
    class BaseModel:  # type: ignore[no-redef]
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

# Inversion forgiven only if BOTH: delta<=$10M AND delta<=0.5% of larger.
ABS_TOL_USD_M = 10.0
REL_TOL = 0.005


class SOTPSegment(BaseModel):
    name: str
    revenue: float | None = Field(default=None)
    gp: float | None = Field(default=None)
    op: float | None = Field(default=None)
    ni: float | None = Field(default=None)


def _coerce_float(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _extract_segment(name: str, payload: Any) -> SOTPSegment | None:
    """Build a SOTPSegment from a key_assumptions entry, or None if not segment-shaped."""
    if not isinstance(payload, dict):
        return None

    def _find(*needles: str) -> float | None:
        for k, v in payload.items():
            kl = k.lower()
            if all(n in kl for n in needles):
                f = _coerce_float(v)
                if f is not None:
                    return f
        return None

    revenue = _find("revenue")
    gp = _find("segment_gp")
    op = _find("segment_op")
    ni = _find("segment_ni")
    # Require >=2 of the monotonicity fields to treat this as a segment row.
    if sum(x is not None for x in (revenue, gp, op, ni)) < 2:
        return None
    return SOTPSegment(name=name, revenue=revenue, gp=gp, op=op, ni=ni)


def _find_sotp_method(memo: dict[str, Any]) -> dict[str, Any] | None:
    methods = (memo.get("valuation") or {}).get("methods")
    if not isinstance(methods, list):
        return None
    for m in methods:
        if isinstance(m, dict) and m.get("method") == "SOTP":
            return m
    return None


def _collect_segments(sotp: dict[str, Any]) -> list[SOTPSegment]:
    ka = sotp.get("key_assumptions")
    if not isinstance(ka, dict):
        return []
    return [s for name, p in ka.items() if (s := _extract_segment(name, p)) is not None]


def _inversion_fails(higher: float, lower: float) -> tuple[bool, float, float]:
    """higher should be >= lower; return (is_fail, delta, relative)."""
    delta = lower - higher
    if delta <= 0:
        return (False, delta, 0.0)
    denom = max(abs(higher), abs(lower), 1e-9)
    rel = delta / denom
    if delta <= ABS_TOL_USD_M and rel <= REL_TOL:
        return (False, delta, rel)
    return (True, delta, rel)


def _collect_segments_strict(sotp: dict[str, Any]) -> tuple[list[SOTPSegment], list[str]]:
    """v0.3.0 strict mode: require complete segment shape.

    A segment is complete if it has EITHER:
      (a) Industrial: Revenue + GP + OP + NI (all 4)
      (b) Banks per D24: PPNR + Pre-Tax + NI (all 3)
    Partial segments are excluded and listed in warnings. If the
    resulting verified set is empty, G3 fails per audit Issue #3(c).
    """
    ka = sotp.get("key_assumptions")
    if not isinstance(ka, dict):
        return ([], ["key_assumptions missing or not a dict"])
    segments: list[SOTPSegment] = []
    warnings: list[str] = []
    for name, p in ka.items():
        if not isinstance(p, dict):
            continue
        def _find(substr: str) -> float | None:
            for k, v in p.items():
                if substr in str(k).lower():
                    return _coerce_float(v)
            return None
        rev = _find("revenue")
        gp = _find("segment_gp")
        op = _find("segment_op")
        ni = _find("segment_ni")
        ppnr = _find("ppnr")
        pretax = _find("pre_tax") if _find("pre_tax") is not None else _find("pretax")
        industrial_complete = all(x is not None for x in (rev, gp, op, ni))
        banks_complete = all(x is not None for x in (ppnr, pretax, ni))
        if industrial_complete:
            segments.append(SOTPSegment(name=name, revenue=rev, gp=gp, op=op, ni=ni))
        elif banks_complete:
            # D24 banks mapping: PPNR -> Pre-Tax -> NI replaces
            # Revenue -> GP -> OP -> NI. PPNR occupies the top two
            # rungs of the industrial chain so existing monotonicity
            # logic carries through.
            segments.append(SOTPSegment(
                name=name,
                revenue=ppnr,
                gp=ppnr,
                op=pretax,
                ni=ni,
            ))
        else:
            present = [
                lbl for lbl, v in (
                    ("Revenue", rev), ("GP", gp), ("OP", op), ("NI", ni),
                    ("PPNR", ppnr), ("Pre-Tax", pretax),
                ) if v is not None
            ]
            warnings.append(
                f'segment "{name}" has incomplete shape (only [{", ".join(present) or "none"}] present); '
                "v0.3.0 requires industrial [Revenue, GP, OP, NI] OR banks [PPNR, Pre-Tax, NI] complete"
            )
    return (segments, warnings)


def _run_monotonicity(segments: list[SOTPSegment], prefix_msgs: list[str]) -> tuple[int, list[str]]:
    failures: list[str] = []
    for seg in segments:
        chain = [("Revenue", seg.revenue), ("GP", seg.gp), ("OP", seg.op), ("NI", seg.ni)]
        for i in range(len(chain) - 1):
            hl, hv = chain[i]
            ll, lv = chain[i + 1]
            if hv is None or lv is None:
                continue
            fail, delta, rel = _inversion_fails(hv, lv)
            if fail:
                failures.append(
                    f'SOTP segment "{seg.name}" violates monotonicity: '
                    f"{ll}=${lv:,.0f}M > {hl}=${hv:,.0f}M "
                    f"(delta ${delta:,.0f}M, {rel * 100:.2f}%)"
                )
    if not failures:
        msgs = ["gate_id: G3", "status: pass", f"segments_checked: {len(segments)}"]
        msgs.extend(prefix_msgs)
        return (0, msgs)
    msgs = [
        "gate_id: G3",
        "status: fail",
        f"failure_reason: {failures[0]}",
        "remediation_required: valuation.methods[SOTP].key_assumptions",
    ]
    msgs.extend(f"additional_failure: {x}" for x in failures[1:])
    msgs.extend(prefix_msgs)
    return (1, msgs)


def verify(memo: dict[str, Any]) -> tuple[int, list[str]]:
    schema_version = memo.get("schema_version", "0.1.0")
    sotp = _find_sotp_method(memo)
    if sotp is None:
        return (0, ["gate_id: G3", "status: n_a", "reason: No SOTP method in valuation.methods[]"])

    # v0.3.0+: strict segment-shape enforcement per audit Issue #3(c).
    # Pre-v0.3.0 memos keep the lenient _collect_segments behavior for
    # backwards compatibility (grandfather rule).
    if schema_version == "0.3.0":
        segments, shape_warnings = _collect_segments_strict(sotp)
        if not segments:
            reason = (
                "SOTP present but no complete segment rows (v0.3.0 strict). "
                "Every segment must declare the full industrial chain "
                "[Revenue, GP, OP, NI] OR the full banks chain per D24 "
                "[PPNR, Pre-Tax, NI]. Pre-v0.3.0 memos passed n_a here "
                "silently — v0.3.0 fails to close the audit-flagged gap "
                "(verify_sotp_monotonicity covered ~half its stated scope)."
            )
            if shape_warnings:
                reason += " Incomplete segments: " + "; ".join(shape_warnings[:3])
                if len(shape_warnings) > 3:
                    reason += f" (+{len(shape_warnings) - 3} more)"
            return (1, [
                "gate_id: G3",
                "status: fail",
                f"failure_reason: {reason}",
                "remediation_required: populate the full monotonicity ladder for every SOTP segment per memo.json definitions/sotp_segment",
                "blocks_score_above: 7.0",
            ])
        prefix: list[str] = []
        if shape_warnings:
            prefix.append(
                f"warning: {len(shape_warnings)} segment(s) excluded for "
                "incomplete shape: " + "; ".join(shape_warnings[:3])
            )
        return _run_monotonicity(segments, prefix)

    # Pre-v0.3.0 legacy path: lenient _collect_segments + lenient n_a.
    segments = _collect_segments(sotp)
    if not segments:
        return (0, ["gate_id: G3", "status: n_a", "reason: SOTP present but no segment rows (pre-v0.3.0 lenient grandfathered)"])
    return _run_monotonicity(segments, prefix_msgs=[])


def _parse_args(argv: list[str]) -> Path:
    p = argparse.ArgumentParser(description="Verify SOTP monotonicity (G3).")
    p.add_argument("--memo-json", required=True, help="Path to structured memo JSON")
    p.add_argument("--memo-md", required=False, default=None,
                   help="Path to memo Markdown (unused by G3; accepted for uniform calling contract)")
    a = p.parse_args(argv)
    return Path(a.memo_json)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    memo_path = _parse_args(argv)
    if not memo_path.exists():
        print(f"gate_id: G3\nstatus: fail\nfailure_reason: memo JSON not found at {memo_path}", file=sys.stderr)
        return 2
    try:
        memo = json.loads(memo_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"gate_id: G3\nstatus: fail\nfailure_reason: cannot parse memo JSON: {e}", file=sys.stderr)
        return 2
    try:
        exit_code, msgs = verify(memo)
    except ValidationError as e:
        print(f"gate_id: G3\nstatus: fail\nfailure_reason: schema validation error: {e}", file=sys.stderr)
        return 2
    stream = sys.stdout if exit_code == 0 else sys.stderr
    for line in msgs:
        print(line, file=stream)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
