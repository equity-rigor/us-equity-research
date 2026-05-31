# Live Tracking — Phase 2 Forward Calibration Spec

Executes Phase 2 of `design/remediation-plan.md`. Follows the backtest
(`design/backtest-methodology.md`); Track B (post-cutoff true-OOS) is the bridge —
live tracking *is* Track B accruing in real time. Authored 2026-05-31 (overnight T3).

## Why live, after backtest

The score earns the right to imply predictive validity only with a track record
against realized outcomes. The backtest cannot supply that cleanly for an LLM
framework (parametric leakage; the only clean sample is post-cutoff, which is
forward). So the absolute "does the view make money" claim is delegated here, to a
forward record that is leakage-free by construction (the outcome postdates every
decision). The framework already emits dated, falsifiable predictions, so the only
missing pieces are *capturing* them and *resolving* them.

## (a) Forecast registry

Persist every memo's structured prediction at write time, immutable and timestamped.

Record schema (`forecast_registry/<ticker>_<run_id>.json`):
- `run_id`, `ticker`, `as_of_date` (decision date), `model_snapshot` (the
  framework×model pair — outcomes validate a pair, not "the framework"),
  `schema_version`, `claimed_score`.
- `horizon_months`, `decision_date`, `resolution_date = decision_date + horizon`.
- `recommendation`: `rating`, `expected_return`, `price_target`, `spot_at_decision`.
- `scenario_distribution`: the 5 `{scenario: probability, target, return}` rows.
- `triggers`: each what-would-reverse with `{direction, threshold, unit, observable,
  expected_date}` (already in the memo, lifted verbatim).
- `independent_estimate` (once Sprint 3c lands): the blind estimate + implied variance.
- `frozen_sha256`: hash of the record, so resolution cannot be back-edited to fit.

Write-time hook: the orchestrator appends the record at the end of Phase 3, before
the memo is "published." A memo with no registry record is not eligible for the
calibrated score (it opted out of measurement).

## (b) Outcome-resolution daemon

A scheduled task (the mechanism this project already uses) that runs daily and, for
every registry record whose `resolution_date` or any `trigger.expected_date` has
passed, pulls the realized value and scores the prediction. Resolution requires a
price/fundamental feed (remediation Fork B) — the same feed Tracks B/C need.

Per-record scores written to `outcomes/<run_id>.json`:
- `realized_return` over the horizon (factor-neutralized for the alpha view; raw for
  the directional view), `realized_price`, `realized_scenario` (bucketed).
- `directional_hit` (sign of `expected_return` vs realized), `brier` (multiclass on
  the scenario distribution), `pt_abs_pct_error`.
- `trigger_resolution[]`: for each trigger, `fired` (did the observable cross the
  threshold by its date) and `memo_reacted` (was there a re-underwrite/rating change
  logged when it fired) — this scores the *discipline*, not just the call.
- `model_snapshot` carried through, so calibration can be sliced by model.

The daemon is append-only and never edits a frozen forecast; if the feed is
unavailable it marks `pending` and retries, so a missing feed degrades to "not yet
resolved," never to a silent skip.

## (c) Calibration

Once N is adequate, turn resolved outcomes into a calibrated signal:
- **Reliability diagram + Brier decomposition** (reliability / resolution /
  uncertainty) on the scenario probabilities — are 70%-probability calls right ~70%
  of the time? Miscalibration is the headline diagnostic.
- **Hit rate vs base rate**, and **realized-return vs claimed-score** rank
  correlation (does a higher score actually rank-predict higher forward return).
- **Regression of realized outcome on memo features/gates** to learn which
  components predict — this is what eventually *replaces* the asserted 6–10 with a
  calibrated one (remediation Phase 5), and what tells you whether, e.g., G20's
  surviving-attack or Sprint 3c's independent-estimate variance carries real signal.
- **Partition** by analyst, sector, regime, and model snapshot; report per-slice so
  a single good regime can't launder a bad process.

## (d) Honest limits

- **N accrues only with calendar time.** A 12-month-horizon record resolves in 12
  months. No calibrated score for several quarters; anyone promising sooner is
  reconstructing point-in-time data with leakage.
- **Overlapping horizons** induce serial correlation → use block/embargo-aware error
  bars (the Track-C helpers), not naive t-stats.
- **Regime non-stationarity**: a record built in one regime mis-calibrates the next.
- **Survivorship**: only written names get scored; track the funnel (what was
  screened-out) to avoid a flattering denominator.
- **Model drift**: a track record validates a framework×model pair. A model upgrade
  partially resets it — `model_snapshot` on every record makes the reset auditable;
  treat a model change as a re-baseline trigger, not a continuation.

## (e) Governance

Pre-register the scoring rules (what counts as a hit, the horizon, the
factor-neutralization) before resolution, hash them, and never edit mid-flight. The
resolver and the calibration reviewer are not the memo author (reviewer != builder).
The registry is immutable; resolution is append-only; both are diffable so a PM can
audit any score back to its frozen forecast.

## Relationship to the backtest

Track B in `design/backtest-methodology.md` and this spec are the same data path:
post-cutoff decisions resolved forward. The backtest's ablation (Track A) decides
*whether to rebuild*; live tracking decides *whether the rebuilt thing actually
works*, and is the only source that can ever justify the absolute claim a single
score implies. Stand up the registry now (cheap, no feed) so the clock starts; wire
the resolver when Fork B (feed) is decided.

## Cross-references
- `design/remediation-plan.md` — Phase 2 (this) and Phase 5 (score recomposition).
- `design/backtest-methodology.md` — Track B is this, accruing; the Track-C error-bar
  helpers apply to overlapping-horizon outcomes.
- `design/sprint-3c-context.md` — the independent_estimate field this registry stores.
- `backtest/harness/metrics.py` / `metrics_ic.py` — Brier / rank-IC reused by the resolver.
