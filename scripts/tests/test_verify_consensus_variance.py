#!/usr/bin/env python3
"""
test_verify_consensus_variance.py — Direct tests for G15.

Sprint 4 Item 4 final closure. Pass / fail / n_a / grandfathered fixtures
covering the gate's documented logic per scripts/verify_consensus_variance.py
and references/consensus-variance-us.md.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_consensus_variance.py"


def _run(memo: dict, md_text: str, tmp_path: Path) -> subprocess.CompletedProcess:
    mj = tmp_path / "memo.json"
    mj.write_text(json.dumps(memo), encoding="utf-8")
    md = tmp_path / "memo.md"
    md.write_text(md_text, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(mj), "--memo-md", str(md)],
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
        "recommendation": {
            "rating": "Sell",
            "upside_downside_pct": -15.0,
        },
        "revision_velocity": {
            "n_analysts": 15,
            "fy1_eps_revision_3m_pct": -3.0,
            "breadth_3m": -0.5,
            "g17_status": "disclosed",
        },
    }


def _headline_md(text: str = "Headline: Sell on margin compression risk") -> str:
    return f"# Investment Memo\n\n## Headline\n{text}\n"


# -----------------------------------------------------------------------------
# Pass cases
# -----------------------------------------------------------------------------


def test_g15_pass_sell_with_s1_variance(tmp_path: Path):
    memo = _base_memo()
    memo["consensus_variance"] = [
        {
            "type": "margin",
            "sizing_impact_pp": 3.0,
            "evidence_refs": [{"s_level": "S1", "ref": "10-K Item 7A"}],
        }
    ]
    proc = _run(memo, _headline_md(), tmp_path)
    assert proc.returncode == 0, f"expected pass, got: {proc.stdout}\n{proc.stderr}"
    assert _parse_status(proc.stdout) == "pass"


def test_g15_pass_buy_with_s2_variance(tmp_path: Path):
    memo = _base_memo()
    memo["recommendation"]["rating"] = "Buy"
    memo["recommendation"]["upside_downside_pct"] = 18.0
    memo["consensus_variance"] = [
        {
            "type": "revenue",
            "sizing_impact_pp": 2.5,
            "evidence_refs": [{"s_level": "S2", "ref": "10-Q Note 5"}],
        }
    ]
    proc = _run(memo, _headline_md("Headline: Buy on revenue inflection"), tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "pass"


def test_g15_pass_strong_sell_with_s3_variance(tmp_path: Path):
    memo = _base_memo()
    memo["recommendation"]["rating"] = "Strong Sell"
    memo["recommendation"]["upside_downside_pct"] = -25.0
    memo["consensus_variance"] = [
        {
            "type": "scenario_weight",
            "sizing_impact_pp": 4.0,
            "evidence_refs": [{"s_level": "S3", "ref": "FQ2 call transcript"}],
        }
    ]
    proc = _run(memo, _headline_md("Headline: Strong Sell on cycle peak"), tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "pass"


# -----------------------------------------------------------------------------
# N/A cases
# -----------------------------------------------------------------------------


def test_g15_na_hold_rating(tmp_path: Path):
    memo = _base_memo()
    memo["recommendation"]["rating"] = "Hold"
    memo["recommendation"]["upside_downside_pct"] = 2.0
    # No consensus_variance — should still pass as n_a
    proc = _run(memo, _headline_md("Headline: Hold pending clarity"), tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "n_a"


def test_g15_na_consensus_anchored_headline(tmp_path: Path):
    memo = _base_memo()
    # Sell rating but headline self-labels consensus-anchored
    md = "# Memo\n## Headline\nThis is a **consensus-anchored** Sell call.\n"
    proc = _run(memo, md, tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "n_a"


def test_g15_na_thin_coverage(tmp_path: Path):
    memo = _base_memo()
    memo["revision_velocity"]["n_analysts"] = 3
    proc = _run(memo, _headline_md(), tmp_path)
    assert proc.returncode == 0
    assert _parse_status(proc.stdout) == "n_a"


# -----------------------------------------------------------------------------
# Fail cases
# -----------------------------------------------------------------------------


def test_g15_fail_sell_no_variance(tmp_path: Path):
    memo = _base_memo()
    # Sell rating with no consensus_variance at all → fail
    proc = _run(memo, _headline_md(), tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g15_fail_sizing_impact_below_threshold(tmp_path: Path):
    memo = _base_memo()
    memo["consensus_variance"] = [
        {
            "type": "margin",
            "sizing_impact_pp": 1.0,  # below 2.0 load-bearing threshold
            "evidence_refs": [{"s_level": "S1", "ref": "10-K"}],
        }
    ]
    proc = _run(memo, _headline_md(), tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


def test_g15_fail_all_s4_evidence(tmp_path: Path):
    memo = _base_memo()
    memo["consensus_variance"] = [
        {
            "type": "multiple",
            "sizing_impact_pp": 3.0,
            "evidence_refs": [
                {"s_level": "S4", "ref": "FactSet consensus"},
                {"s_level": "S4", "ref": "Visible Alpha"},
            ],
        }
    ]
    proc = _run(memo, _headline_md(), tmp_path)
    assert proc.returncode != 0
    assert _parse_status(proc.stdout) == "fail"


# -----------------------------------------------------------------------------
# Grandfathered
# -----------------------------------------------------------------------------


def test_g15_grandfathered_v0_1(tmp_path: Path):
    memo = _base_memo(schema_version="0.1.0")
    # Sell rating without consensus_variance — would normally fail, but
    # v0.1.0 predates G15 so it must be skipped/grandfathered.
    proc = _run(memo, _headline_md(), tmp_path)
    assert proc.returncode == 0
    status = _parse_status(proc.stdout)
    assert status in {"skipped", "n_a", "pass"}, (
        f"v0.1.0 should be grandfathered (skipped/n_a/pass), got {status}: {proc.stdout}"
    )
