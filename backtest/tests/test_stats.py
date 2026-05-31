"""Tests for the ablation statistics — the part that must be correct.

Pure stdlib; runs on a bare interpreter (no pydantic/numpy).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BACKTEST_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKTEST_DIR))

from harness import stats as S  # noqa: E402


def test_paired_differences_basic():
    assert S.paired_differences([1.0, 2.0, 3.0], [0.5, 0.5, 0.5]) == [0.5, 1.5, 2.5]


def test_paired_differences_length_mismatch():
    with pytest.raises(ValueError):
        S.paired_differences([1.0, 2.0], [1.0])


def test_weighted_mean_unweighted_equals_mean():
    assert S.weighted_mean([2.0, 4.0, 6.0]) == 4.0


def test_weighted_mean_weights_shift_toward_high_weight():
    # weight the 10.0 heavily -> mean pulled toward 10.
    m = S.weighted_mean([0.0, 10.0], [1.0, 9.0])
    assert m == pytest.approx(9.0)


def test_weighted_mean_rejects_nonpositive_weights():
    with pytest.raises(ValueError):
        S.weighted_mean([1.0, 2.0], [0.0, 0.0])


def test_leakage_weights_monotone_and_floored():
    w = S.leakage_weights([0.0, 0.5, 1.0], floor=0.05)
    assert w[0] == pytest.approx(1.0)
    assert w[1] == pytest.approx(0.5)
    assert w[2] == pytest.approx(0.05)  # floored, not 0


def test_bootstrap_point_equals_sample_mean():
    vals = [0.1, 0.2, 0.3, 0.4, 0.5]
    ci = S.moving_block_bootstrap_ci(vals, n_boot=500, seed=1)
    assert ci.point == pytest.approx(sum(vals) / len(vals))
    assert ci.low <= ci.point <= ci.high


def test_bootstrap_strong_positive_excludes_zero():
    # tight cluster around +1.0 -> 95% CI should be well above 0.
    vals = [0.9, 1.0, 1.1, 0.95, 1.05, 1.0, 0.98, 1.02]
    ci = S.moving_block_bootstrap_ci(vals, n_boot=3000, seed=7)
    assert ci.low > 0.0
    assert S.decision_gate(ci, "greater") is True


def test_bootstrap_null_includes_zero():
    # symmetric around 0 -> CI should straddle 0, gate fails.
    vals = [-1.0, 1.0, -0.8, 0.8, -1.2, 1.2, -0.9, 0.9, -1.1, 1.1]
    ci = S.moving_block_bootstrap_ci(vals, n_boot=3000, seed=11)
    assert ci.low < 0.0 < ci.high
    assert S.decision_gate(ci, "greater") is False


def test_bootstrap_deterministic_given_seed():
    vals = [0.1, -0.2, 0.3, 0.05, 0.2, -0.1, 0.15]
    a = S.moving_block_bootstrap_ci(vals, n_boot=1000, seed=42)
    b = S.moving_block_bootstrap_ci(vals, n_boot=1000, seed=42)
    assert (a.point, a.low, a.high) == (b.point, b.low, b.high)


def test_block_size_preserves_n():
    vals = [float(i) for i in range(20)]
    ci = S.moving_block_bootstrap_ci(vals, n_boot=200, block_size=5, seed=3)
    assert ci.n == 20


def test_decision_gate_less_direction():
    # lower-is-better metric: a strongly negative Δ should pass 'less'.
    vals = [-0.5, -0.6, -0.55, -0.45, -0.5, -0.52]
    ci = S.moving_block_bootstrap_ci(vals, n_boot=2000, seed=5)
    assert ci.high < 0.0
    assert S.decision_gate(ci, "less") is True
    assert S.decision_gate(ci, "greater") is False


def test_decision_gate_bad_direction():
    ci = S.moving_block_bootstrap_ci([0.1, 0.2], n_boot=100, seed=1)
    with pytest.raises(ValueError):
        S.decision_gate(ci, "sideways")
