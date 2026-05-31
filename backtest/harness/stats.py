"""Paired-difference statistics for the Track A ablation.

The estimand is the within-case difference (treatment - baseline) on a decision-
quality metric, so common-mode leakage cancels. A moving-block bootstrap
preserves serial correlation across as-of-ordered cases (overlapping horizons
induce autocorrelation); optional leakage weights down-weight differentially-
contaminated cases. Pure stdlib so it runs on a bare interpreter.

Nothing here knows about the framework or the data — it operates on plain lists
of per-case metric values, which is what keeps the statistics honest and unit-
testable in isolation.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class BootstrapCI:
    point: float
    low: float
    high: float
    n: int
    n_boot: int
    block_size: int
    alpha: float


def paired_differences(treatment: list[float], baseline: list[float]) -> list[float]:
    if len(treatment) != len(baseline):
        raise ValueError("treatment and baseline must be equal length (paired design)")
    if not treatment:
        raise ValueError("empty input")
    return [float(t) - float(b) for t, b in zip(treatment, baseline)]


def weighted_mean(values: list[float], weights: list[float] | None = None) -> float:
    if not values:
        raise ValueError("empty values")
    if weights is None:
        return sum(values) / len(values)
    if len(weights) != len(values):
        raise ValueError("weights length mismatch")
    wsum = sum(weights)
    if wsum <= 0:
        raise ValueError("weights must sum to > 0")
    return sum(v * w for v, w in zip(values, weights)) / wsum


def leakage_weights(leakage_scores: list[float], floor: float = 0.05) -> list[float]:
    """w_i = max(floor, 1 - leakage_score_i). Not normalized (weighted_mean
    normalizes). The floor keeps a heavily-contaminated case from getting zero
    weight, which would silently drop sample."""
    return [max(floor, 1.0 - float(s)) for s in leakage_scores]


def _moving_block_indices(n: int, block_size: int, rng: random.Random) -> list[int]:
    """Circular moving-block resample of indices, length n."""
    bs = max(1, block_size)
    idx: list[int] = []
    while len(idx) < n:
        start = rng.randrange(0, n)
        idx.extend((start + k) % n for k in range(bs))
    return idx[:n]


def moving_block_bootstrap_ci(
    values: list[float],
    *,
    n_boot: int = 2000,
    block_size: int = 1,
    alpha: float = 0.05,
    weights: list[float] | None = None,
    seed: int = 12345,
) -> BootstrapCI:
    """Percentile CI for the (optionally weighted) mean via moving-block bootstrap.

    block_size=1 reduces to the iid bootstrap. The point estimate is the
    (weighted) sample mean; the interval is the [alpha/2, 1-alpha/2] percentiles
    of the bootstrap distribution of the (weighted) mean.
    """
    n = len(values)
    if n == 0:
        raise ValueError("empty values")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0,1)")
    rng = random.Random(seed)
    point = weighted_mean(values, weights)
    boots: list[float] = []
    for _ in range(n_boot):
        idx = _moving_block_indices(n, block_size, rng)
        sample = [values[i] for i in idx]
        w = [weights[i] for i in idx] if weights is not None else None
        boots.append(weighted_mean(sample, w))
    boots.sort()
    lo_i = int((alpha / 2.0) * n_boot)
    hi_i = int((1.0 - alpha / 2.0) * n_boot) - 1
    lo_i = max(0, min(n_boot - 1, lo_i))
    hi_i = max(0, min(n_boot - 1, hi_i))
    return BootstrapCI(
        point=point, low=boots[lo_i], high=boots[hi_i],
        n=n, n_boot=n_boot, block_size=block_size, alpha=alpha,
    )


def decision_gate(ci: BootstrapCI, direction: str = "greater") -> bool:
    """Pre-registered gate: the contrast is significant in the hypothesized
    direction iff the CI excludes zero on the correct side.

    direction='greater' (higher metric is better): require ci.low > 0.
    direction='less'    (lower metric is better):  require ci.high < 0.
    """
    if direction == "greater":
        return ci.low > 0.0
    if direction == "less":
        return ci.high < 0.0
    raise ValueError("direction must be 'greater' or 'less'")
