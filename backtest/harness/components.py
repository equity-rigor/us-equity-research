"""Pluggable components: data providers, the framework runner (ablation arms),
and the leakage probe — abstract interfaces plus deterministic Mock impls.

STUB BOUNDARY. The Mock* classes exist only to exercise the pipeline and the
statistics end-to-end with no external dependencies. Going to production means
replacing them, one interface at a time:

  PITProvider     -> EDGAR + bitemporal spine (point-in-time filings, prices,
                     as-of consensus snapshots).
  LabelProvider   -> forward factor-neutral return feed (remediation Fork B).
  FrameworkRunner -> the real us-equity-research orchestration, one call per
                     ablation arm, with the arm toggling which structure is on.
  LeakageProbe    -> real direct-recall / blinded-minus-unblinded / counterfactual
                     probes (design/backtest-methodology.md §2).

No Mock output is a real estimate. Each is a deterministic synthetic fixture
seeded by case_id (+ arm) so the harness is reproducible and the tests are
stable. The MockFrameworkRunner deliberately encodes a *synthetic* effect
(full > consensus_relative_only > no_gates ~ raw_model) so the pipeline has a
known signal to recover; this is NOT a claim about the real framework.
"""
from __future__ import annotations

import hashlib
import math
import random
from abc import ABC, abstractmethod

from .models import Case, Decision, LeakageReport, Outcome, PITBundle

# The four ablation arms (design/backtest-methodology.md Track A).
ARMS = ("full", "no_gates", "consensus_relative_only", "raw_model")

# Pre-registered contrasts: (treatment, baseline, hypothesis).
CONTRASTS = (
    ("full", "raw_model", "H2_structure_vs_raw_model"),
    ("full", "consensus_relative_only", "H3_independent_estimate_value"),
    ("full", "no_gates", "gates_value"),
)

_SCENARIOS = ("strong_bear", "bear", "base", "bull", "strong_bull")


def _seed(*parts: object) -> int:
    h = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return int(h[:8], 16)


# --- Abstract interfaces (the production wiring points) -------------------

class PITProvider(ABC):
    @abstractmethod
    def bundle(self, case: Case) -> PITBundle: ...


class LabelProvider(ABC):
    @abstractmethod
    def outcome(self, case: Case) -> Outcome: ...


class FrameworkRunner(ABC):
    @abstractmethod
    def run(self, case: Case, arm: str, bundle: PITBundle) -> Decision: ...


class LeakageProbe(ABC):
    @abstractmethod
    def assess(self, case: Case, bundle: PITBundle) -> LeakageReport: ...


# --- Deterministic Mock implementations (scaffold only) -------------------

class MockPITProvider(PITProvider):
    def bundle(self, case: Case) -> PITBundle:
        return PITBundle(case_id=case.case_id, as_of_date=case.as_of_date,
                         artifacts={"note": "MOCK point-in-time bundle"})


class MockLabelProvider(LabelProvider):
    """Deterministic synthetic outcomes. A latent 'true' forward return per case
    drives realized_return; the MockFrameworkRunner's arms recover that latent
    signal with arm-specific fidelity so the ablation has an effect to detect."""

    def __init__(self, scenarios: tuple[str, ...] = _SCENARIOS):
        self.scenarios = scenarios

    def latent_return(self, case: Case) -> float:
        return random.Random(_seed("latent", case.case_id)).gauss(0.0, 0.25)

    def outcome(self, case: Case) -> Outcome:
        true_ret = self.latent_return(case)
        realized = true_ret + random.Random(_seed("outcome", case.case_id)).gauss(0.0, 0.05)
        spot = 100.0
        # Bucket the realized return into a scenario class.
        k = len(self.scenarios)
        idx = max(0, min(k - 1, int((realized + 0.5) * k)))
        return Outcome(
            case_id=case.case_id,
            realized_return=realized,
            realized_price=spot * (1.0 + realized),
            realized_scenario=self.scenarios[idx],
        )


def _scenario_probs(est: float, rng: random.Random) -> dict[str, float]:
    """A crude gaussian bump over the scenario ladder centered on the estimate."""
    k = len(_SCENARIOS)
    center = (est + 0.5) * (k - 1)
    raw = [math.exp(-0.5 * ((i - center) / 1.0) ** 2) for i in range(k)]
    s = sum(raw)
    return {_SCENARIOS[i]: raw[i] / s for i in range(k)}


class MockFrameworkRunner(FrameworkRunner):
    """Each arm estimates the latent return with arm-specific fidelity and noise.
    Encodes a synthetic effect ordering full > consensus_relative_only >
    no_gates ~ raw_model. Fixture only — not a statement about the real system."""

    ARM_FIDELITY = {"full": 0.65, "consensus_relative_only": 0.50, "no_gates": 0.40, "raw_model": 0.40}
    ARM_NOISE = {"full": 0.10, "consensus_relative_only": 0.14, "no_gates": 0.18, "raw_model": 0.18}

    def __init__(self, labels: MockLabelProvider):
        self.labels = labels

    def run(self, case: Case, arm: str, bundle: PITBundle) -> Decision:
        true_ret = self.labels.latent_return(case)
        rng = random.Random(_seed("decision", case.case_id, arm))
        fid = self.ARM_FIDELITY.get(arm, 0.40)
        noise = self.ARM_NOISE.get(arm, 0.18)
        est = fid * true_ret + rng.gauss(0.0, noise)
        spot = 100.0
        rating = "Buy" if est > 0.05 else ("Sell" if est < -0.05 else "Hold")
        return Decision(
            case_id=case.case_id, arm=arm, rating=rating,
            expected_return=est, price_target=spot * (1.0 + est), spot=spot,
            scenario_probabilities=_scenario_probs(est, rng),
        )


class MockLeakageProbe(LeakageProbe):
    def assess(self, case: Case, bundle: PITBundle) -> LeakageReport:
        rng = random.Random(_seed("leak", case.case_id))
        return LeakageReport(
            case_id=case.case_id,
            direct_recall_accuracy=min(1.0, max(0.0, rng.uniform(0.0, 0.6))),
            blinded_unblinded_delta=max(0.0, rng.gauss(0.05, 0.05)),
            counterfactual_persistence=min(1.0, max(0.0, rng.uniform(0.0, 0.5))),
        )
