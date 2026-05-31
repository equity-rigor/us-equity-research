# FrameworkRunner Integration Design

How to implement `backtest/harness/components.py:FrameworkRunner` against the real
`us-equity-research` orchestration, so the Track A ablation produces a *real* signal.
This is the first wiring point and the only one that needs no data feed (Track A
runs Claude-only on decision-quality proxies). Design only — no live invocation here.
Authored 2026-05-31 (overnight T6).

## Contract recap

`FrameworkRunner.run(case, arm, bundle) -> Decision`. One call per (case, arm). The
`arm` string selects *how much of the framework's structure is active* on the same
inputs; everything else (model, PIT bundle) is held fixed. The returned `Decision`
carries `rating, expected_return, price_target, spot, scenario_probabilities` — the
fields the metrics consume.

## The four arms — what each toggles

The arms must differ ONLY in structure, never in information or model, or the ablation
is confounded.

- **`full`** — the complete pipeline: Phase 1–3 specialists, A-Consensus, R-v2
  isolated attack, the independent estimator (once Sprint 3c lands), and the full
  verification-gate pass. The production behavior.
- **`no_gates`** — identical research and synthesis, but the Phase-4 verification
  gates are NOT enforced (the memo is produced but gate failures do not cap/alter the
  rating or sizing). Isolates "do the gates change the decision."
- **`consensus_relative_only`** — the estimator is OFF: variances are defined only
  relative to consensus (the current v0.4.0 behavior). This is the baseline the
  Sprint 3c independent estimate is measured against (backtest H3).
- **`raw_model`** — a single-prompt view: hand the model the same PIT bundle and ask
  for rating + expected return + PT + a 5-scenario distribution, with no phases, no
  specialist agents, no gates. The null that asks "does any of the scaffolding beat
  just asking the model."

Implementation: a single `arm_config` flag threaded into the orchestrator that gates
(a) which phases/agents run, (b) whether the estimator is dispatched, (c) whether the
gate pass is enforcing. Keep one code path; the flag turns pieces on/off. Do not fork
the orchestrator per arm (divergent code paths reintroduce confounds).

## PIT input injection

The orchestration must consume the `bundle` (point-in-time filings, prices, as-of
consensus snapshot) and be **prevented from fetching anything dated after
`case.as_of_date`**. Concretely: run with web tools disabled and all inputs supplied
from the bundle, OR with a fetch shim that rejects post-as-of documents. This is
necessary but NOT sufficient against leakage (the model's parametric memory still
leaks) — Track A tolerates that because leakage is common-mode across arms and
differences out; the PIT discipline still matters so the arms see identical, clean
inputs.

## Parsing the Decision

The orchestration already emits a structured `<ticker>_structured.json` conforming to
`schemas/memo.json`. The adapter parses from it:
- `rating` ← `recommendation.rating`
- `expected_return` ← `recommendation.upside_downside_pct` / 100 (or the
  probability-weighted scenario return)
- `price_target` ← `recommendation.price_target` (base case)
- `spot` ← `current_price_usd`
- `scenario_probabilities` ← the `scenarios[]` block, `{scenario: probability}`
Validate the parse (probabilities sum ~1; numbers present); on a malformed memo,
raise rather than silently coerce — a parse failure is data, not a zero.

## Decision caching

Each `full`-arm run is ~2 hours of orchestrated execution and hundreds of tool calls;
four arms per case multiplies that. Cache by `(case_id, arm, model_snapshot,
bundle_hash)` so re-runs and resumes are free, and so a crashed batch resumes without
re-paying. The cache key MUST include the model snapshot and bundle hash — a different
model or different inputs is a different decision.

## Model-snapshot pinning

Record the exact model id + training cutoff on every run; a Track A result validates a
specific *(framework × model)* pair (see `design/backtest-methodology.md` §9 model
drift). Pin one model across all arms within a run, and stamp it into the results so a
later model upgrade triggers re-validation rather than silently carrying over.

## Cost / latency envelope

Order-of-magnitude: `full` ≈ 2h and several hundred tool calls; `consensus_relative_
only` ≈ similar minus the estimator; `no_gates` ≈ similar minus the gate pass;
`raw_model` ≈ minutes. A 30-name Track A sample × 4 arms is dominated by the heavy
arms — budget accordingly, lean on caching and parallel dispatch, and start with a
small stratified pilot (10–15 names) to size the effect before scaling. This cost is
exactly why Track A's paired design (variance-reducing) matters: it extracts the most
signal per expensive run.

## What this design deliberately does NOT do

- It does not invoke the orchestration (that is the implementation task).
- It does not add a data feed; realized-return labels (Tracks B/C) remain gated on
  remediation Fork B. Track A here scores decision-quality proxies, not alpha.
- It does not change the framework's runtime behavior — the `arm_config` flag is the
  only addition, and `full` must be byte-for-byte the production path.

## Cross-references
- `backtest/harness/components.py` — the `FrameworkRunner` interface this implements.
- `design/backtest-methodology.md` — Track A (the estimand), §9 (model drift).
- `design/sprint-3c-context.md` — the estimator that distinguishes `full` from
  `consensus_relative_only`.
