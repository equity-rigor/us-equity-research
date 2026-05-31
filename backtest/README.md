# Track A Ablation Backtest Harness (scaffold)

Executes the leakage-robust **ablation** track of `design/backtest-methodology.md`:
hold the model and the information set fixed, vary only the framework's structure
across arms, and measure paired within-case differences in decision quality.
Because leakage is approximately common-mode across arms, it **differences out** —
so the estimand is the framework structure's *causal, incremental* contribution,
which is the question a rebuild decision actually turns on.

## What is real vs stubbed

Real and tested:
- `harness/stats.py` — paired differences, moving-block bootstrap CI, leakage
  weighting, decision gate.
- `harness/metrics.py` — decision-quality metrics + polarity.
- `harness/preregister.py` — canonical hash / freeze / verify of the config.
- `harness/run_ablation.py` — the end-to-end pipeline.

Stubbed (deterministic Mocks; the production wiring points):
- `PITProvider` → EDGAR + bitemporal point-in-time spine (filings, prices,
  **as-of** consensus snapshots).
- `LabelProvider` → forward factor-neutral return feed (`design/remediation-plan.md`
  Fork B). Until this is real, only proxy outcomes exist.
- `FrameworkRunner` → the real `us-equity-research` orchestration, one call per
  arm, the arm toggling which structure is on (`full` / `no_gates` /
  `consensus_relative_only` / `raw_model`).
- `LeakageProbe` → real direct-recall / blinded-minus-unblinded / counterfactual
  probes (`design/backtest-methodology.md` §2).

**The Mock outputs are synthetic fixtures, not estimates.** The MockFrameworkRunner
deliberately encodes a synthetic effect (`full > consensus_relative_only >
no_gates ~ raw_model`) so the pipeline has a known signal to recover and the smoke
test can assert the machinery works. None of it says anything about the real
framework's skill.

## Run the demo (no dependencies)

From this directory:

    python -m harness.run_ablation --sample config/sample.example.json --out /tmp/ablation.json

Prints a results report: per registered contrast, the paired mean Δ on the primary
metric, the bootstrap CI, the leakage-adjusted Δ + CI, and the gate decision.

## Tests

    python -m pytest backtest/tests -q

`test_stats.py` covers the statistics (the part that must be correct);
`test_pipeline_smoke.py` runs the full pipeline on Mock components and checks it
recovers the synthetic effect with well-formed output.

## Wiring to production (order of operations)

1. Replace `FrameworkRunner` with the real orchestration — this is the only piece
   needed for a Claude-only Track A on proxy outcomes.
2. Replace `LeakageProbe` with the real probes; gate on the leakage-adjusted CI.
3. Replace `PITProvider` with the bitemporal spine; enforce model-cutoff gating.
4. Replace `LabelProvider` once Fork B (return feed) is decided — this turns proxy
   decision-quality into realized factor-neutral alpha and unlocks Tracks B/C.

Pre-register first (`harness/preregister.freeze`), then never edit the config
mid-run. Governance: independent sign-off on the registration and the leakage
audit before results are read; the reviewer is not the builder.
