#!/usr/bin/env python3
"""
test_verify_revision_velocity.py — Direct tests for G17.

Sprint 4 Item 4 final closure. Pass / fail / n_a / grandfathered fixtures
covering the revision-velocity gate per scripts/verify_revision_velocity.py
and references/phase-2-continuation-us.md §A6.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_revision_velocity.py"


def _run(memo: dict, tmp_path: Path) -> subprocess.CompletedProcess:
    mj = tmp_path / "memo.json"
    mj.write_text(json.dumps(memo), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(mj)],
        capture_output=True,
        text=True,
    )


def _parse_status(stdout: str) -> str:
    for line in stdout.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def _base_memo(schema_version: str = "0.5.0") -> dict:
    return {
        "schema_version": schema_version,
        "ticker": "TEST",
        "as_of_date": "2026-06-06",
        "model_cutoff_date": "2026-01-01",
        "current_price_usd": 100.0,
        "revision_velocity": {
            "n_analysts": 18,
            "fy1_eps_revision_3m_pct": -4.5,
            "breadth_3m": -0.4,
            "g17_status": "disclosed",
        },
    }


# -----------------------------------------------------------------------------
# Pass case
# -----------------------------------------------------------------------------


def test_g17_pass_with_full_disclosure(tmp_path: Path):
    proc = _run(_base_memo(), tmp_path)
    assert proc.returncode == 0, f"expected pass, got: {proc.stdout}\n{proc.stderr}"
    assert _parse_status(proc.stdout) == "pass"


def test_g17_pass_positive_breadth(tmp_path: Path):
    memo = _base_memo()
    memo["revision_velocity"]["fy1_eps_revision_3m_pct"] = 8.0
    memo["revision_velocity"]["breadth_3m"] = 0.7
    proc = _run(memo, tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "pass"


def test_g17_pass_zero_revision(tmp_path: Path):
    memo = _base_memo()
    memo["revision_velocity"]["fy1_eps_revision_3m_pct"] = 0.0
    memo["revision_velocity"]["breadth_3m"] = 0.0
    proc = _run(memo, tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "pass"


# -----------------------------------------------------------------------------
# Fail cases
# -----------------------------------------------------------------------------


def test_g17_fail_missing_fy1_eps_revision(tmp_path: Path):
    memo = _base_memo()
    del memo["revision_velocity"]["fy1_eps_revision_3m_pct"]
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g17_fail_missing_breadth(tmp_path: Path):
    memo = _base_memo()
    del memo["revision_velocity"]["breadth_3m"]
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g17_fail_breadth_out_of_range_positive(tmp_path: Path):
    memo = _base_memo()
    memo["revision_velocity"]["breadth_3m"] = 1.5  # > 1.0 max
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g17_fail_breadth_out_of_range_negative(tmp_path: Path):
    memo = _base_memo()
    memo["revision_velocity"]["breadth_3m"] = -1.5  # < -1.0 min
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g17_fail_missing_revision_velocity_block_entirely(tmp_path: Path):
    memo = _base_memo()
    del memo["revision_velocity"]
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


# -----------------------------------------------------------------------------
# N/A cases
# -----------------------------------------------------------------------------


def test_g17_na_thin_coverage_n_analysts_below_5(tmp_path: Path):
    memo = _base_memo()
    memo["revision_velocity"]["n_analysts"] = 3
    # The revision fields can be absent or invalid — n_a from thin coverage trumps.
    del memo["revision_velocity"]["fy1_eps_revision_3m_pct"]
    proc = _run(memo, tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "n_a"


def test_g17_na_explicit_status_flag(tmp_path: Path):
    memo = _base_memo()
    memo["revision_velocity"]["g17_status"] = "n_a_thin_coverage"
    proc = _run(memo, tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "n_a"


# -----------------------------------------------------------------------------
# Grandfathered
# -----------------------------------------------------------------------------


def test_g17_grandfathered_v0_1(tmp_path: Path):
    memo = _base_memo(schema_version="0.1.0")
    # Strip revision_velocity — v0.1.0 predates G17.
    del memo["revision_velocity"]
    proc = _run(memo, tmp_path)
    assert proc.returncode == 0
    status = _parse_status(proc.stdout)
    assert status in {"skipped", "n_a", "pass"}, (
        f"v0.1.0 should be grandfathered, got {status}: {proc.stdout}"
    )
