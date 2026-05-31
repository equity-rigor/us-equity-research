"""Tests for the Track-C overfitting controls (pure stdlib; runs bare)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BACKTEST_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKTEST_DIR))

from harness import stats_trackc as TC  # noqa: E402


# --- deflated Sharpe ratio ---

def test_dsr_in_unit_interval():
    v = TC.deflated_sharpe_ratio(0.3, n_trials=10, n_obs=120)
    assert 0.0 <= v <= 1.0


def test_dsr_monotone_increasing_in_observed_sr():
    lo = TC.deflated_sharpe_ratio(0.1, n_trials=10, n_obs=120)
    hi = TC.deflated_sharpe_ratio(0.5, n_trials=10, n_obs=120)
    assert hi > lo


def test_dsr_decreasing_in_n_trials():
    few = TC.deflated_sharpe_ratio(0.3, n_trials=2, n_obs=120)
    many = TC.deflated_sharpe_ratio(0.3, n_trials=200, n_obs=120)
    assert many < few  # more trials -> higher null bar -> lower DSR


def test_expected_max_sharpe_grows_with_trials():
    assert TC.expected_max_sharpe(2, 120) < TC.expected_max_sharpe(100, 120)
    assert TC.expected_max_sharpe(1, 120) == 0.0


def test_dsr_rejects_short_track():
    with pytest.raises(ValueError):
        TC.deflated_sharpe_ratio(0.3, n_trials=10, n_obs=1)


# --- purged k-fold ---

def test_purged_kfold_partitions_test_indices():
    folds = TC.purged_kfold_indices(20, k=5, embargo=2)
    assert len(folds) == 5
    all_test = sorted(i for _, test in folds for i in test)
    assert all_test == list(range(20))  # test folds partition the range


def test_purged_kfold_train_test_disjoint_and_embargoed():
    n, embargo = 30, 3
    for train, test in TC.purged_kfold_indices(n, k=5, embargo=embargo):
        assert set(train).isdisjoint(test)
        ts, te = min(test), max(test) + 1
        # no train index falls within the embargo band around the test fold
        for i in train:
            assert not (ts - embargo <= i < te + embargo)


def test_purged_kfold_bad_k():
    with pytest.raises(ValueError):
        TC.purged_kfold_indices(10, k=1)


# --- probability of backtest overfitting ---

def test_pbo_skilled_is_zero():
    # config 0 dominates in every block -> IS winner is also OOS winner -> PBO 0.
    skilled = [[1, 1, 1, 1], [0, 0, 0, 0]]
    assert TC.probability_of_backtest_overfitting(skilled) == 0.0


def test_pbo_overfit_is_one():
    # IS winner is consistently the OOS loser across all splits -> PBO 1.
    overfit = [[5, 5, 1, 1], [1, 1, 5, 5]]
    assert TC.probability_of_backtest_overfitting(overfit) == 1.0


def test_pbo_in_unit_interval():
    m = [[3, 1, 4, 1, 5, 9], [2, 7, 1, 8, 2, 8], [1, 4, 1, 5, 9, 2]]
    v = TC.probability_of_backtest_overfitting(m)
    assert 0.0 <= v <= 1.0


def test_pbo_rejects_degenerate():
    with pytest.raises(ValueError):
        TC.probability_of_backtest_overfitting([[1, 2, 3]])  # one config
