"""Data contracts every pluggable component speaks. Pure stdlib dataclasses, so
the framework runner, data providers, and feed integrations can be swapped
without touching the pipeline or the statistics.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Case:
    """One backtest unit: a name evaluated as-of a point in time.

    `as_of_date` is the decision date and the point-in-time cutoff — nothing
    knowable only after it may enter the decision. `horizon_months` sets the
    outcome label horizon.
    """
    case_id: str
    ticker: str
    as_of_date: str  # ISO 8601 date
    horizon_months: int = 12
    sector: str = "unknown"
    size_bucket: str = "unknown"
    regime: str = "unknown"


@dataclass
class PITBundle:
    """Point-in-time inputs knowable as-of Case.as_of_date. A real provider
    returns filings, prices, and an as-of consensus snapshot; the scaffold
    carries an opaque payload."""
    case_id: str
    as_of_date: str
    artifacts: dict[str, Any] = field(default_factory=dict)


@dataclass
class Decision:
    """The framework's output for one (case, arm). The forecast fields are what
    the metrics consume."""
    case_id: str
    arm: str
    rating: str  # Buy / Hold / Sell / NoEdge
    expected_return: float  # decimal, e.g. 0.12 == +12%
    price_target: float
    spot: float
    scenario_probabilities: dict[str, float] = field(default_factory=dict)
    triggers: list[Any] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Outcome:
    """Realized result at the horizon. Needs a forward-return feed (remediation
    Fork B) in production; mocked in the scaffold."""
    case_id: str
    realized_return: float  # factor-neutral forward return (decimal)
    realized_price: float
    realized_scenario: str


@dataclass
class LeakageReport:
    """Per-case leakage measurement (design/backtest-methodology.md §2). Higher
    leakage_score == more contaminated by the model's parametric memory of the
    future."""
    case_id: str
    direct_recall_accuracy: float       # [0,1] blinded outcome-recall accuracy
    blinded_unblinded_delta: float      # identified minus anonymized performance
    counterfactual_persistence: float   # [0,1] skill retained on fabricated history

    @property
    def leakage_score(self) -> float:
        # Pre-registered aggregation into [0,1]. Weights are part of the
        # pre-registration; changing them requires re-freezing the config.
        raw = (
            0.5 * self.direct_recall_accuracy
            + 0.3 * max(0.0, self.blinded_unblinded_delta)
            + 0.2 * self.counterfactual_persistence
        )
        return max(0.0, min(1.0, raw))


@dataclass
class ArmResult:
    arm: str
    per_case_quality: dict[str, float]            # case_id -> primary metric value
    per_case_components: dict[str, dict[str, float]]  # case_id -> {component: value}


@dataclass
class ContrastResult:
    """Paired comparison treatment_arm - baseline_arm on the primary metric."""
    treatment_arm: str
    baseline_arm: str
    hypothesis: str
    n: int
    mean_delta: float
    ci_low: float
    ci_high: float
    leakage_adjusted_mean_delta: float
    leakage_adjusted_ci_low: float
    leakage_adjusted_ci_high: float
    gate_pass: bool
