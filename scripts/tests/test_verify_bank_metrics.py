#!/usr/bin/env python3
"""
test_verify_bank_metrics.py — Direct tests for G16.

Sprint 4 Item 4 final closure. Pass / fail / n_a / grandfathered fixtures
covering the bank-discipline gate per scripts/verify_bank_metrics.py and
references/phase-1-deep-dive-us.md §FS-Banks Augmentation.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_bank_metrics.py"


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


def _base_bank_memo(schema_version: str = "0.5.0") -> dict:
    """Banks-sector memo with all 4 required disclosure groups populated.

    The bank_metrics block is FLAT per the verifier's REQUIRED_* field lists —
    all field names live at bank_metrics.<field>, not in nested sub-objects.
    """
    return {
        "schema_version": schema_version,
        "ticker": "JPM",
        "as_of_date": "2026-06-06",
        "model_cutoff_date": "2026-01-01",
        "current_price_usd": 300.0,
        "sector_gics": "Financials",
        "industry_gics": "Diversified Banks",
        "bank_metrics": {
            # AOCI bridge
            "afs_book_value_usd_b": 350.0,
            "afs_fair_value_usd_b": 330.0,
            "aoci_mark_usd_b": -20.0,
            "htm_book_value_usd_b": 280.0,
            "htm_fair_value_usd_b": 260.0,
            "tbvps_mtm_usd": 75.0,
            # CET1 walk — required_cet1 = 4.5 + 2.5 + scb + gsib_surcharge per v0.3.0 recompute
            # = 4.5 + 2.5 + 3.3 + 0 (no G-SIB surcharge in this fixture) = 10.3
            "cet1_ratio_pct": 15.2,
            "required_cet1_pct": 10.3,
            # NIM trajectory
            "nim_latest_pct": 2.65,
            "nim_5y_trajectory": [2.05, 2.10, 2.15, 2.40, 2.65],
            "deposit_beta_cumulative_cycle_pct": 45.0,
            # Stress capital
            "scb_pct": 3.3,
            "capital_return_capacity_usd_b": 28.0,
            "ccar_dfast_severely_adverse_cet1_trough_pct": 11.4,
        },
    }


_AOCI_FIELDS = [
    "afs_book_value_usd_b",
    "afs_fair_value_usd_b",
    "aoci_mark_usd_b",
    "htm_book_value_usd_b",
    "htm_fair_value_usd_b",
    "tbvps_mtm_usd",
]
_CET1_FIELDS = ["cet1_ratio_pct", "required_cet1_pct"]
_NIM_FIELDS = ["nim_latest_pct", "nim_5y_trajectory", "deposit_beta_cumulative_cycle_pct"]
_STRESS_FIELDS = [
    "scb_pct",
    "capital_return_capacity_usd_b",
    "ccar_dfast_severely_adverse_cet1_trough_pct",
]


def _strip_group(memo: dict, fields: list[str]) -> dict:
    for f in fields:
        memo["bank_metrics"].pop(f, None)
    return memo


# -----------------------------------------------------------------------------
# Pass case
# -----------------------------------------------------------------------------


def test_g16_pass_complete_bank_disclosures(tmp_path: Path):
    proc = _run(_base_bank_memo(), tmp_path)
    assert proc.returncode == 0, f"expected pass, got: {proc.stdout}\n{proc.stderr}"
    assert _parse_status(proc.stdout) == "pass"


# -----------------------------------------------------------------------------
# Fail cases — missing each required group
# -----------------------------------------------------------------------------


def test_g16_fail_missing_aoci_bridge(tmp_path: Path):
    memo = _strip_group(_base_bank_memo(), _AOCI_FIELDS)
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g16_fail_missing_cet1_walk(tmp_path: Path):
    memo = _strip_group(_base_bank_memo(), _CET1_FIELDS)
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g16_fail_missing_nim_trajectory(tmp_path: Path):
    memo = _strip_group(_base_bank_memo(), _NIM_FIELDS)
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g16_fail_missing_stress_capital(tmp_path: Path):
    memo = _strip_group(_base_bank_memo(), _STRESS_FIELDS)
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g16_fail_missing_bank_metrics_block_entirely(tmp_path: Path):
    memo = _base_bank_memo()
    del memo["bank_metrics"]
    proc = _run(memo, tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


# -----------------------------------------------------------------------------
# N/A cases — non-bank sectors
# -----------------------------------------------------------------------------


def test_g16_na_information_technology_sector(tmp_path: Path):
    memo = _base_bank_memo()
    memo["sector_gics"] = "Information Technology"
    memo["industry_gics"] = "Semiconductors"
    # Even with no bank_metrics, non-bank sector → n_a
    del memo["bank_metrics"]
    proc = _run(memo, tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "n_a"


def test_g16_na_consumer_discretionary(tmp_path: Path):
    memo = _base_bank_memo()
    memo["sector_gics"] = "Consumer Discretionary"
    memo["industry_gics"] = "Internet & Direct Marketing Retail"
    del memo["bank_metrics"]
    proc = _run(memo, tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "n_a"


# -----------------------------------------------------------------------------
# Grandfathered
# -----------------------------------------------------------------------------


def test_g16_grandfathered_v0_1(tmp_path: Path):
    memo = _base_bank_memo(schema_version="0.1.0")
    # Strip bank_metrics — v0.1.0 predates G16 so this must be skipped.
    del memo["bank_metrics"]
    proc = _run(memo, tmp_path)
    assert proc.returncode == 0
    status = _parse_status(proc.stdout)
    assert status in {"skipped", "n_a", "pass"}, (
        f"v0.1.0 should be grandfathered, got {status}: {proc.stdout}"
    )
