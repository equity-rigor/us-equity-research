#!/usr/bin/env python3
"""Gate G3 — SOTP monotonicity verification.

For every segment in the SOTP valuation method, verify NI <= OP <= GP <= Revenue
within rounding tolerance (delta <= $10M absolute AND <= 0.5% relative).
Any inversion exceeding both bounds is a hard fail. N/A if no SOTP method present.

Usage:
    python scripts/verify_sotp_monotonicity.py <memo.json>
    python scripts/verify_sotp_monotonicity.py --memo-json <path> [--memo-md <path>]

Exit 0 = pass or N/A; non-zero = fail.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError

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


def verify(memo: dict[str, Any]) -> tuple[int, list[str]]:
    sotp = _find_sotp_method(memo)
    if sotp is None:
        return (0, ["gate_id: G3", "status: n_a", "reason: No SOTP method in valuation.methods[]"])
    segments = _collect_segments(sotp)
    if not segments:
        return (0, ["gate_id: G3", "status: n_a", "reason: SOTP present but no segment rows"])

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
        return (0, ["gate_id: G3", "status: pass", f"segments_checked: {len(segments)}"])
    msgs = [
        "gate_id: G3",
        "status: fail",
        f"failure_reason: {failures[0]}",
        "remediation_required: valuation.methods[SOTP].key_assumptions",
    ]
    msgs.extend(f"additional_failure: {x}" for x in failures[1:])
    return (1, msgs)


def _parse_args(argv: list[str]) -> Path:
    p = argparse.ArgumentParser(description="Verify SOTP monotonicity (G3).")
    p.add_argument("memo_json", nargs="?", help="Path to memo JSON (positional)")
    p.add_argument("--memo-json", dest="memo_json_flag", help="Path to memo JSON (flag form)")
    p.add_argument("--memo-md", dest="memo_md", help="Path to memo Markdown (unused by G3)")
    a = p.parse_args(argv)
    path_str = a.memo_json or a.memo_json_flag
    if not path_str:
        p.error("memo JSON path required (positional or --memo-json)")
    return Path(path_str)


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
