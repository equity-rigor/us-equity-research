"""
Tests for scripts/verify_revision_attribution.py (Gate G22, v0.7.0 judgment layer).

Invariants:
  1. n_a (exit 0) when no revision_bridge (self-gating).
  2. pass when components reconcile and judgment_share is estimate-led (<50%).
  3. pass when judgment-led (>50%) AND a judgment_flag is present.
  4. fail when judgment-led (>50%) and the judgment_flag is missing.
  5. fail when components do not reconcile to (new - prior).
  6. fail when declared judgment_share_pct disagrees with the components.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_revision_attribution.py"


def _run(payload: dict, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    p = tmp_path / "memo.json"
    p.write_text(json.dumps(payload))
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(p)],
        capture_output=True, text=True,
    )


def _bridge(prior, new, comps, share, flag=None):
    rb = {"prior_price_target_usd": prior, "new_price_target_usd": new,
          "components": comps, "judgment_share_pct": share}
    if flag is not None:
        rb["judgment_flag"] = flag
    return {"valuation": {"revision_bridge": rb}}


def test_no_block_is_na(tmp_path):
    r = _run({"valuation": {}}, tmp_path)
    assert r.returncode == 0 and "status: n_a" in r.stdout


def test_estimate_led_passes(tmp_path):
    comps = [
        {"driver": "estimate", "delta_usd": 16.0, "rationale": "FY27 EPS raised on new bookings"},
        {"driver": "multiple", "delta_usd": 4.0, "rationale": "modest re-rate"},
    ]
    r = _run(_bridge(100.0, 120.0, comps, 20.0), tmp_path)
    assert r.returncode == 0 and "status: pass" in r.stdout


def test_judgment_led_with_flag_passes(tmp_path):
    comps = [
        {"driver": "estimate", "delta_usd": 0.0, "rationale": "EPS unchanged"},
        {"driver": "methodology", "delta_usd": -84.73, "rationale": "re-anchored to fair value"},
        {"driver": "multiple", "delta_usd": -42.0, "rationale": "cyclical de-rate"},
    ]
    r = _run(_bridge(828.73, 702.0, comps, 100.0,
                     flag="100% methodology+multiple — judgment-led de-bias, not new info"), tmp_path)
    assert r.returncode == 0 and "status: pass" in r.stdout


def test_judgment_led_without_flag_fails(tmp_path):
    comps = [
        {"driver": "estimate", "delta_usd": 0.0, "rationale": "EPS unchanged"},
        {"driver": "multiple", "delta_usd": -126.73, "rationale": "multiple re-rate"},
    ]
    r = _run(_bridge(828.73, 702.0, comps, 100.0), tmp_path)  # no flag
    assert r.returncode != 0 and "status: fail" in r.stdout


def test_non_reconciling_fails(tmp_path):
    comps = [{"driver": "estimate", "delta_usd": 5.0, "rationale": "x"}]
    r = _run(_bridge(100.0, 120.0, comps, 0.0), tmp_path)  # 5 != 20
    assert r.returncode != 0 and "status: fail" in r.stdout


def test_wrong_declared_share_fails(tmp_path):
    comps = [
        {"driver": "estimate", "delta_usd": 0.0, "rationale": "EPS unchanged"},
        {"driver": "multiple", "delta_usd": 20.0, "rationale": "re-rate"},
    ]
    r = _run(_bridge(100.0, 120.0, comps, 10.0,
                     flag="judgment-led"), tmp_path)  # computed 100, declared 10
    assert r.returncode != 0 and "status: fail" in r.stdout
