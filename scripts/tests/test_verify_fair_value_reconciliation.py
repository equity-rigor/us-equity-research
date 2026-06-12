"""
Tests for scripts/verify_fair_value_reconciliation.py (Gate G21, v0.7.0 judgment layer).

Invariants:
  1. n_a (exit 0) when no valuation_parallel block (self-gating).
  2. pass when base PT reconciles to fair value within 15%.
  3. pass when base diverges >15% but the gap is justified (convergence_assumption + speed).
  4. fail when base diverges >15% and the gap is NOT justified.
  5. fail when recommendation.price_target_usd != the blended base.
  6. fail when independent_fair_value_basis is missing/empty.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_fair_value_reconciliation.py"


def _run(payload: dict, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    p = tmp_path / "memo.json"
    p.write_text(json.dumps(payload))
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(p)],
        capture_output=True, text=True,
    )


def _vp(base, fv, conv_note="", conv_speed=None):
    return {
        "valuation_parallel": {
            "independent_fair_value_usd": fv,
            "independent_fair_value_basis": "DCF + SOTP + normalized comps, built without reference to price",
            "market_regime_value_usd": fv * 1.4,
            "current_price_usd": fv * 1.5,
            "twelve_month_base_pt_usd": base,
            "convergence_assumption": conv_note,
            "convergence_speed": conv_speed,
        },
        "recommendation": {"price_target_usd": base},
    }


def test_no_block_is_na(tmp_path):
    r = _run({"recommendation": {"price_target_usd": 100}}, tmp_path)
    assert r.returncode == 0 and "status: n_a" in r.stdout


def test_base_within_15pct_passes(tmp_path):
    r = _run(_vp(base=108.0, fv=100.0), tmp_path)
    assert r.returncode == 0 and "status: pass" in r.stdout


def test_divergence_justified_passes(tmp_path):
    r = _run(_vp(base=140.0, fv=100.0,
                 conv_note="cycle still rising; partial 12-month reversion only", conv_speed="slow"), tmp_path)
    assert r.returncode == 0 and "status: pass" in r.stdout


def test_divergence_unjustified_fails(tmp_path):
    r = _run(_vp(base=140.0, fv=100.0, conv_note="", conv_speed="bogus"), tmp_path)
    assert r.returncode != 0 and "status: fail" in r.stdout


def test_headline_pt_mismatch_fails(tmp_path):
    payload = _vp(base=108.0, fv=100.0)
    payload["recommendation"]["price_target_usd"] = 130.0  # != blended base
    r = _run(payload, tmp_path)
    assert r.returncode != 0 and "status: fail" in r.stdout


def test_missing_basis_fails(tmp_path):
    payload = _vp(base=108.0, fv=100.0)
    payload["valuation_parallel"]["independent_fair_value_basis"] = ""
    r = _run(payload, tmp_path)
    assert r.returncode != 0 and "status: fail" in r.stdout
