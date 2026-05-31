"""End-to-end smoke test: the pipeline runs on Mock components and recovers the
synthetic effect the MockFrameworkRunner encodes (full arm > raw_model). This
validates the wiring + statistics, not the real framework.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BACKTEST_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKTEST_DIR))

from harness import preregister as P  # noqa: E402
from harness.models import Case  # noqa: E402
from harness.run_ablation import load_sample, run  # noqa: E402

REPO_ROOT = BACKTEST_DIR.parent
SAMPLE = BACKTEST_DIR / "config" / "sample.example.json"


def _synthetic_cases(n: int = 80) -> list[Case]:
    cases = []
    for i in range(n):
        # spread as-of dates across 2022-2024 so ordering/blocking is meaningful
        year = 2022 + (i % 3)
        month = (i % 12) + 1
        cases.append(Case(
            case_id=f"s{i:03d}",
            ticker=f"T{i:03d}",
            as_of_date=f"{year}-{month:02d}-15",
            horizon_months=12,
        ))
    return cases


def _contrast(report, treatment, baseline):
    for c in report["contrasts"]:
        if c["treatment_arm"] == treatment and c["baseline_arm"] == baseline:
            return c
    raise AssertionError(f"contrast {treatment} vs {baseline} not found")


def test_pipeline_runs_and_is_well_formed():
    report = run(_synthetic_cases(40), n_boot=500)
    assert report["n_cases"] == 40
    assert len(report["contrasts"]) == 3
    for c in report["contrasts"]:
        assert c["n"] == 40
        for k in ("mean_delta", "ci_low", "ci_high",
                  "leakage_adjusted_mean_delta", "leakage_adjusted_ci_low", "leakage_adjusted_ci_high"):
            assert isinstance(c[k], float)
        assert c["ci_low"] <= c["mean_delta"] <= c["ci_high"]
        assert isinstance(c["gate_pass"], bool)
    assert 0.0 <= report["mean_leakage_score"] <= 1.0


def test_recovers_synthetic_effect_directional():
    # full encodes higher fidelity than raw_model -> positive directional Δ.
    report = run(_synthetic_cases(80), n_boot=1000)
    h2 = _contrast(report, "full", "raw_model")
    assert h2["mean_delta"] > 0.0


def test_recovers_synthetic_effect_continuous():
    # On a lower-is-better metric, full should have LOWER PT error than raw_model.
    report = run(_synthetic_cases(80), primary="pt_abs_pct_error", n_boot=1000)
    assert report["metric_direction"] == "less"
    h2 = _contrast(report, "full", "raw_model")
    assert h2["mean_delta"] < 0.0


def test_independent_estimate_contrast_present():
    # H3: full vs consensus_relative_only is registered and computed.
    report = run(_synthetic_cases(40), n_boot=300)
    h3 = _contrast(report, "full", "consensus_relative_only")
    assert h3["hypothesis"] == "H3_independent_estimate_value"
    assert h3["n"] == 40


def test_example_sample_loads_and_runs():
    cases, meta = load_sample(SAMPLE)
    assert len(cases) >= 8
    report = run(cases, n_boot=300)
    assert report["n_cases"] == len(cases)


def test_determinism():
    a = run(_synthetic_cases(30), n_boot=400)
    b = run(_synthetic_cases(30), n_boot=400)
    assert a["contrasts"][0]["mean_delta"] == b["contrasts"][0]["mean_delta"]
    assert a["contrasts"][0]["leakage_adjusted_ci_low"] == b["contrasts"][0]["leakage_adjusted_ci_low"]


def test_preregistration_freeze_verify_roundtrip(tmp_path):
    config = {"primary_metric": "directional_accuracy", "arms": ["full", "raw_model"]}
    frozen = tmp_path / "prereg.json"
    digest = P.freeze(config, frozen)
    assert len(digest) == 64
    assert P.verify(config, frozen) is True
    # any drift in the config breaks verification
    mutated = dict(config, primary_metric="brier")
    assert P.verify(mutated, frozen) is False
