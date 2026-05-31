"""Decision-quality metrics, computed on (Decision, Outcome).

Under Claude-only (no return feed) these run on mock/proxy outcomes; swap the
LabelProvider for a real forward factor-neutral return feed (remediation Fork B)
to get realized-alpha metrics. Each metric declares its polarity so the gate
picks the correct CI side.
"""
from __future__ import annotations

from .models import Decision, Outcome


def _sign(x: float) -> int:
    return (x > 0) - (x < 0)


def directional_accuracy(decision: Decision, outcome: Outcome) -> float:
    """1.0 if the sign of the expected return matches the realized sign (and the
    call was non-flat), else 0.0."""
    s = _sign(decision.expected_return)
    return 1.0 if s != 0 and s == _sign(outcome.realized_return) else 0.0


def multiclass_brier(scenario_probabilities: dict[str, float], realized_scenario: str) -> float:
    """Multiclass Brier score: sum over scenarios of (p - y)^2, y=1 for the
    realized scenario. Lower is better; 0 is perfect."""
    classes = set(scenario_probabilities) | {realized_scenario}
    total = 0.0
    for c in classes:
        p = float(scenario_probabilities.get(c, 0.0))
        y = 1.0 if c == realized_scenario else 0.0
        total += (p - y) ** 2
    return total


def pt_abs_pct_error(price_target: float, realized_price: float) -> float:
    """|PT - realized| / |realized|. Lower is better."""
    if realized_price == 0:
        return float("inf")
    return abs(price_target - realized_price) / abs(realized_price)


# Polarity per metric so the decision gate picks the correct CI side.
METRIC_POLARITY = {
    "directional_accuracy": "higher_better",
    "brier": "lower_better",
    "pt_abs_pct_error": "lower_better",
}

PRIMARY = "directional_accuracy"


def components(decision: Decision, outcome: Outcome) -> dict[str, float]:
    return {
        "directional_accuracy": directional_accuracy(decision, outcome),
        "brier": multiclass_brier(decision.scenario_probabilities, outcome.realized_scenario),
        "pt_abs_pct_error": pt_abs_pct_error(decision.price_target, outcome.realized_price),
    }


def primary_quality(decision: Decision, outcome: Outcome, primary: str = PRIMARY) -> float:
    return components(decision, outcome)[primary]
