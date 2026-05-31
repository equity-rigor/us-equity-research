"""Information-coefficient and factor-neutralization metrics (pure stdlib).

Used by Track C and by the live-tracking resolver: rank IC (does the score rank-
predict forward return), factor-neutral residualization (measure alpha, not factor
beta), and the IC-decay curve (edge decay over horizon).
"""
from __future__ import annotations

import math


def _ranks(xs: list[float]) -> list[float]:
    """1-based ranks with average ranks for ties."""
    n = len(xs)
    order = sorted(range(n), key=lambda i: xs[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for kk in range(i, j + 1):
            ranks[order[kk]] = avg
        i = j + 1
    return ranks


def _pearson(a: list[float], b: list[float]) -> float:
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if va <= 0 or vb <= 0:
        return 0.0
    return cov / math.sqrt(va * vb)


def spearman_rank_ic(scores: list[float], forward_returns: list[float]) -> float:
    """Spearman rank IC in [-1, 1]."""
    if len(scores) != len(forward_returns) or len(scores) < 2:
        raise ValueError("need equal-length vectors of length >= 2")
    return _pearson(_ranks(scores), _ranks(forward_returns))


def _solve(matrix: list[list[float]], vec: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting for a small square system."""
    n = len(matrix)
    a = [row[:] + [vec[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(a[r][col]))
        a[col], a[piv] = a[piv], a[col]
        if abs(a[col][col]) < 1e-15:
            continue
        for r in range(n):
            if r != col:
                f = a[r][col] / a[col][col]
                for c in range(col, n + 1):
                    a[r][c] -= f * a[col][c]
    return [a[i][n] / a[i][i] if abs(a[i][i]) > 1e-15 else 0.0 for i in range(n)]


def ols_residualize(y: list[float], X: list[list[float]], ridge: float = 1e-9) -> list[float]:
    """Residuals of y after OLS on X (an intercept is added). A tiny ridge keeps the
    normal equations solvable under collinearity."""
    n = len(y)
    if n == 0 or len(X) != n:
        raise ValueError("X must have one row per y observation")
    design = [[1.0] + [float(v) for v in row] for row in X]
    p = len(design[0])
    ata = [[sum(design[r][i] * design[r][j] for r in range(n)) for j in range(p)] for i in range(p)]
    for i in range(p):
        ata[i][i] += ridge
    aty = [sum(design[r][i] * y[r] for r in range(n)) for i in range(p)]
    beta = _solve(ata, aty)
    return [y[r] - sum(design[r][i] * beta[i] for i in range(p)) for r in range(n)]


def factor_neutral_returns(returns: list[float], factor_exposures: list[list[float]]) -> list[float]:
    """Residual returns after regressing out the factor exposures (one exposure row
    per observation). This is the alpha the score should be judged on."""
    return ols_residualize(returns, factor_exposures)


def ic_decay(scores: list[float], returns_by_horizon: dict[int, list[float]]) -> dict[int, float]:
    """Rank IC at each horizon — the edge-decay curve."""
    return {h: spearman_rank_ic(scores, returns_by_horizon[h]) for h in sorted(returns_by_horizon)}
