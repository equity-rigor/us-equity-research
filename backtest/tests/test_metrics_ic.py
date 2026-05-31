"""Tests for IC + factor-neutralization metrics (pure stdlib; runs bare)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BACKTEST_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKTEST_DIR))

from harness import metrics_ic as IC  # noqa: E402


def test_rank_ic_perfectly_aligned():
    assert IC.spearman_rank_ic([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)


def test_rank_ic_perfectly_reversed():
    assert IC.spearman_rank_ic([1, 2, 3, 4], [40, 30, 20, 10]) == pytest.approx(-1.0)


def test_rank_ic_known_intermediate():
    # ranks [1,2,3,4] vs [3,4,1,2] -> Pearson on ranks = -0.6
    assert IC.spearman_rank_ic([1, 2, 3, 4], [3, 4, 1, 2]) == pytest.approx(-0.6)


def test_rank_ic_handles_ties():
    v = IC.spearman_rank_ic([1, 1, 2, 2], [5, 6, 7, 8])
    assert -1.0 <= v <= 1.0


def test_rank_ic_length_guard():
    with pytest.raises(ValueError):
        IC.spearman_rank_ic([1, 2], [1])


def test_residualize_exact_linear_is_zero():
    resid = IC.ols_residualize([2, 4, 6, 8], [[1], [2], [3], [4]])  # y = 2x
    assert max(abs(r) for r in resid) < 1e-6


def test_residualize_collinear_is_stable_and_small():
    # two identical columns -> singular without the ridge; must not crash and y is in span
    resid = IC.ols_residualize([2, 4, 6, 8], [[1, 1], [2, 2], [3, 3], [4, 4]])
    assert max(abs(r) for r in resid) < 1e-2


def test_factor_neutral_removes_exposure():
    returns = [2, 4, 6, 8]
    exposures = [[1], [2], [3], [4]]  # returns == 2 * exposure
    resid = IC.factor_neutral_returns(returns, exposures)
    assert max(abs(r) for r in resid) < 1e-6


def test_ic_decay_per_horizon():
    decay = IC.ic_decay([1, 2, 3, 4], {1: [10, 20, 30, 40], 2: [40, 30, 20, 10]})
    assert decay[1] == pytest.approx(1.0)
    assert decay[2] == pytest.approx(-1.0)
    assert sorted(decay.keys()) == [1, 2]
