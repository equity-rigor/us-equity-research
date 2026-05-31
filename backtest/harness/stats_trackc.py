"""Track-C overfitting controls (design/backtest-methodology.md §7).

Pure stdlib. Three institutional guards against backtest overfitting:
  - deflated_sharpe_ratio: Bailey & Lopez de Prado DSR — probability the true SR
    exceeds the inflated null maximum, deflating for the number of trials and for
    non-normality (skew/kurtosis) of returns.
  - purged_kfold_indices: time-ordered k-fold with a purge+embargo band around each
    test fold, so overlapping-horizon labels cannot leak across the split.
  - probability_of_backtest_overfitting: CSCV PBO — fraction of combinatorial
    in-sample/out-of-sample splits where the in-sample-best config lands below the
    out-of-sample median.
"""
from __future__ import annotations

import math
from itertools import combinations

_GAMMA = 0.5772156649015329  # Euler-Mascheroni


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_ppf(p: float) -> float:
    """Inverse standard-normal CDF (Acklam's rational approximation)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= phigh:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def expected_max_sharpe(n_trials: int, n_obs: int) -> float:
    """Expected maximum per-observation Sharpe across n_trials independent null
    strategies. Under the null SR=0, an estimated SR over T obs has SE ~ 1/sqrt(T-1);
    the expected max of N draws scales that by the Gumbel-tail factor."""
    if n_obs < 2:
        raise ValueError("n_obs must be >= 2")
    if n_trials <= 1:
        return 0.0
    sr_sigma = math.sqrt(1.0 / (n_obs - 1))
    factor = ((1 - _GAMMA) * _norm_ppf(1 - 1.0 / n_trials)
              + _GAMMA * _norm_ppf(1 - 1.0 / (n_trials * math.e)))
    return sr_sigma * factor


def deflated_sharpe_ratio(observed_sr: float, n_trials: int, n_obs: int,
                          skew: float = 0.0, kurt: float = 3.0) -> float:
    """DSR in [0,1]: probability the true SR > 0 after deflating for the number of
    trials (multiple testing) and non-normality. `observed_sr` is the per-observation
    (non-annualized) Sharpe; kurt is the (non-excess) kurtosis (3 == normal)."""
    if n_obs < 2:
        raise ValueError("n_obs must be >= 2")
    sr0 = expected_max_sharpe(n_trials, n_obs)
    denom = math.sqrt(max(1e-12, 1 - skew * observed_sr + ((kurt - 1) / 4.0) * observed_sr ** 2))
    z = (observed_sr - sr0) * math.sqrt(n_obs - 1) / denom
    return _norm_cdf(z)


def purged_kfold_indices(n: int, k: int, embargo: int = 0) -> list[tuple[list[int], list[int]]]:
    """Time-ordered k-fold splits with a purge+embargo band around each test fold.

    Test folds are contiguous and partition range(n). For each fold, the training set
    excludes the test indices plus an `embargo`-sized band on each side, so a label
    horizon overlapping the test cannot leak into training.
    """
    if k < 2 or k > n:
        raise ValueError("require 2 <= k <= n")
    # contiguous, near-equal fold boundaries
    base, rem = divmod(n, k)
    bounds, start = [], 0
    for i in range(k):
        size = base + (1 if i < rem else 0)
        bounds.append((start, start + size))
        start += size
    folds: list[tuple[list[int], list[int]]] = []
    for (ts, te) in bounds:
        test = list(range(ts, te))
        lo, hi = max(0, ts - embargo), min(n, te + embargo)
        train = [i for i in range(n) if i < lo or i >= hi]
        folds.append((train, test))
    return folds


def probability_of_backtest_overfitting(perf_matrix: list[list[float]]) -> float:
    """CSCV PBO. perf_matrix is n_configs rows x M block-performance columns. Partition
    the M blocks into every IS/OOS half-split; for each, pick the in-sample-best config
    and find its out-of-sample relative rank. PBO is the fraction of splits where that
    rank is below the OOS median (the IS winner is an OOS loser)."""
    n_configs = len(perf_matrix)
    if n_configs < 2:
        raise ValueError("need >= 2 configs")
    m = len(perf_matrix[0])
    if m < 2 or any(len(r) != m for r in perf_matrix):
        raise ValueError("need >= 2 equal-length blocks per config")
    cols = list(range(m))
    half = m // 2
    overfit, total = 0, 0
    for combo in combinations(cols, half):
        is_cols = set(combo)
        oos_cols = [c for c in cols if c not in is_cols]
        if not oos_cols:
            continue
        is_score = [sum(row[c] for c in is_cols) / len(is_cols) for row in perf_matrix]
        oos_score = [sum(row[c] for c in oos_cols) / len(oos_cols) for row in perf_matrix]
        best = max(range(n_configs), key=lambda i: is_score[i])
        beats = sum(1 for i in range(n_configs) if oos_score[best] > oos_score[i])
        w = (beats + 0.5) / n_configs  # relative OOS rank in (0,1); higher == better
        total += 1
        if w < 0.5:
            overfit += 1
    return overfit / total if total else 0.0
