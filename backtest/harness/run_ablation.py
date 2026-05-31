"""Track A ablation orchestrator: components -> per-case decisions -> metrics ->
paired-Δ statistics -> gate. Defaults to Mock components so the full pipeline
runs with no external dependencies; pass real components to go live.

Run (from the backtest/ directory):
    python -m harness.run_ablation --sample config/sample.example.json --out /tmp/ablation.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import metrics as M
from . import stats as S
from .components import (
    ARMS, CONTRASTS,
    FrameworkRunner, LabelProvider, LeakageProbe, PITProvider,
    MockFrameworkRunner, MockLabelProvider, MockLeakageProbe, MockPITProvider,
)
from .models import ArmResult, Case, ContrastResult


def load_sample(path: str | Path) -> tuple[list[Case], dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cases = [Case(**c) for c in data["cases"]]
    return cases, data.get("meta", {})


def run(
    cases: list[Case],
    *,
    pit: PITProvider | None = None,
    labels: LabelProvider | None = None,
    runner: FrameworkRunner | None = None,
    leakage: LeakageProbe | None = None,
    primary: str = M.PRIMARY,
    arms: tuple[str, ...] = ARMS,
    contrasts: tuple[tuple[str, str, str], ...] = CONTRASTS,
    n_boot: int = 2000,
    block_size: int = 1,
    alpha: float = 0.05,
    seed: int = 12345,
) -> dict[str, Any]:
    """Execute the ablation and return a structured results report.

    Components default to the deterministic Mocks. `MockFrameworkRunner` needs the
    same `MockLabelProvider` instance to share the latent signal, so they are
    constructed together when both are omitted.
    """
    if labels is None:
        labels = MockLabelProvider()
    if runner is None:
        runner = MockFrameworkRunner(labels if isinstance(labels, MockLabelProvider) else MockLabelProvider())
    pit = pit or MockPITProvider()
    leakage = leakage or MockLeakageProbe()

    if primary not in M.METRIC_POLARITY:
        raise ValueError(f"unknown primary metric: {primary}")

    # Order by as-of date so the moving-block bootstrap's block structure is
    # meaningful (overlapping-horizon autocorrelation is time-ordered).
    cases = sorted(cases, key=lambda c: c.as_of_date)
    case_ids = [c.case_id for c in cases]

    bundles = {c.case_id: pit.bundle(c) for c in cases}
    outcomes = {c.case_id: labels.outcome(c) for c in cases}
    leak = {c.case_id: leakage.assess(c, bundles[c.case_id]) for c in cases}

    arm_results: dict[str, ArmResult] = {}
    for arm in arms:
        per_q: dict[str, float] = {}
        per_comp: dict[str, dict[str, float]] = {}
        for c in cases:
            decision = runner.run(c, arm, bundles[c.case_id])
            comp = M.components(decision, outcomes[c.case_id])
            per_comp[c.case_id] = comp
            per_q[c.case_id] = comp[primary]
        arm_results[arm] = ArmResult(arm=arm, per_case_quality=per_q, per_case_components=per_comp)

    direction = "greater" if M.METRIC_POLARITY[primary] == "higher_better" else "less"
    leak_scores = [leak[cid].leakage_score for cid in case_ids]
    weights = S.leakage_weights(leak_scores)

    contrast_results: list[ContrastResult] = []
    for treatment, baseline, hypothesis in contrasts:
        tvals = [arm_results[treatment].per_case_quality[cid] for cid in case_ids]
        bvals = [arm_results[baseline].per_case_quality[cid] for cid in case_ids]
        diffs = S.paired_differences(tvals, bvals)
        ci = S.moving_block_bootstrap_ci(
            diffs, n_boot=n_boot, block_size=block_size, alpha=alpha, seed=seed)
        ci_w = S.moving_block_bootstrap_ci(
            diffs, n_boot=n_boot, block_size=block_size, alpha=alpha, weights=weights, seed=seed)
        # Gate on the leakage-adjusted interval (the conservative choice).
        gate = S.decision_gate(ci_w, direction=direction)
        contrast_results.append(ContrastResult(
            treatment_arm=treatment, baseline_arm=baseline, hypothesis=hypothesis,
            n=len(diffs),
            mean_delta=ci.point, ci_low=ci.low, ci_high=ci.high,
            leakage_adjusted_mean_delta=ci_w.point,
            leakage_adjusted_ci_low=ci_w.low, leakage_adjusted_ci_high=ci_w.high,
            gate_pass=gate,
        ))

    return {
        "primary_metric": primary,
        "metric_direction": direction,
        "n_cases": len(cases),
        "mean_leakage_score": (sum(leak_scores) / len(leak_scores)) if leak_scores else 0.0,
        "bootstrap": {"n_boot": n_boot, "block_size": block_size, "alpha": alpha, "seed": seed},
        "contrasts": [cr.__dict__ for cr in contrast_results],
        "caveat": "Mock components produce synthetic fixtures, not real estimates. See backtest/README.md.",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Track A ablation backtest (scaffold; Mock components by default).")
    p.add_argument("--sample", required=True, type=Path)
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--primary", default=M.PRIMARY, choices=sorted(M.METRIC_POLARITY))
    p.add_argument("--n-boot", type=int, default=2000)
    p.add_argument("--block-size", type=int, default=1)
    p.add_argument("--alpha", type=float, default=0.05)
    args = p.parse_args(argv)

    cases, _meta = load_sample(args.sample)
    report = run(cases, primary=args.primary, n_boot=args.n_boot,
                 block_size=args.block_size, alpha=args.alpha)
    text = json.dumps(report, indent=2)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
