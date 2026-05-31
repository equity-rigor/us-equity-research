# Sprint 3c Context — Consensus-Independent Estimator (the Phase-1 keystone)

DRAFT for review (Hongyi). Authored 2026-05-31 as the execution spec for Phase 1 of
`design/remediation-plan.md` — the single highest-leverage fix from the v0.4.0
critical review. Companion to `design/sprint-3b-context.md` (isolation provenance,
the precondition) and `design/backtest-methodology.md` (the H3 contrast is built to
measure exactly this change). Same contract style as 3b; nothing scheduled here.

## Why 3c is the keystone

The review's core finding: the framework defines edge as `your_number − consensus_number`
and has **no consensus-independent estimate anywhere**, so "edge" is undefinable,
correlated-wrong (you and the Street wrong together) is undetectable by construction,
and G20's ≥8pp differentiation requirement actively rewards manufactured deviation.
Empirically, every showcase memo's base EPS is the Street median.

3c fixes this at the generation layer, and it does so by reusing the machinery
Sprint 3a/3b already built — but **constructively, not destructively**. Sprint 3a
spawns R-v2 as an isolated subagent to *attack* variances. 3c spawns an isolated
subagent to *build the load-bearing number from primitives* with no sight of the
Street figure, then computes the variance after the estimate is locked. The same
isolation contract, the same provenance manifest (3b), pointed at construction.

This is cheap (no new data feed; reuses existing infra) and it is the precondition
for an honest score (it makes the "no edge" outcome expressible) and for the
backtest's H3 hypothesis. Build it first.

## What 3c delivers (one sentence)

A memo that wants to claim a non-Hold rating above the consensus-anchored ceiling
must carry an **independent estimate** of at least one load-bearing driver, built by
an isolated subagent blind to consensus, whose implied variance reconciles with the
declared `consensus_variance` — or it takes the respectable **no-edge** path.

## Versioning

- Plugin **v0.4.0 → v0.5.0** (minor; additive schema + one new gate + graduated
  enforcement). This is the same bump `remediation-plan.md` Phase 5 anticipates.
- `memo.json` gains an optional `independent_estimate` block; `schema_version` enum
  extends to include `"0.5.0"`. Additive — v0.1.0–v0.4.0 memos validate unchanged.
- New gate **G21** (independent-estimate-backed variance). `verification_gates.json`
  `gate_id` enum extends to G21; `gates` array `maxItems` 20 → 21. This is the first
  gate-count change since v0.3.0 — it forces the doc-count reconciliation (overnight
  queue T7 / review Issue 5 debt), so do that sweep as part of this sprint.
- Manifest stays the 3b shape; the estimator's isolation is recorded in the 3b
  `adversarial_isolation` block, generalized to `isolation_events` with a
  `role ∈ {attacker, estimator}` discriminator (additive).

## Universal constraints (inherit from 3a/3b — unchanged)

Additive-only schema with enum grandfathering; pydantic optional-import shim in any
new verifier; committed `test_*.py` shipped in the same commit as every verifier
change; heredoc-to-file commit messages; no inline `#` in shell blocks; Path A
(local commit, no push); alt-index git workaround on the mounted repo; red-team
voice. Run pytest via `/tmp/pylibs`, `--basetemp=/tmp/...` (the `/sessions` overlay
is full).

## Items

### Item 1 — schema: the `independent_estimate` block

Add to `schemas/memo.json` an optional top-level object `independent_estimate`,
`additionalProperties:false`:

- `target_line_item` (string, required) — what was estimated (e.g. "FY27 datacenter
  revenue", "FY27 NIM", "FY27 production × realization").
- `estimate_value` (number, required) and `unit` (string).
- `basis` (string) — for EPS-type estimates, explicitly `"GAAP"` or `"non_GAAP"`
  (this is the anti-NVDA-denominator field; G18-ext checks the headline multiple's
  basis matches this).
- `drivers` (array, minItems 1) of `{name, value, unit, source_ref, base_rate_band}` —
  the primitive decomposition the estimate was built from. `base_rate_band` is the
  historical analog range for that driver (the substrate for the base-rate attack).
- `consensus_value` (number) and `implied_variance_pct` (number) — filled by the
  orchestrator *after* the blind estimate is locked: `(estimate − consensus)/consensus`.
- `isolation` (object): `{subagent_dispatch_id, estimator_model, context_isolation:bool,
  inputs_excluded:[...]}` — reuses the 3b provenance shape; `inputs_excluded` MUST list
  `["consensus_eps","street_pt","sell_side_notes"]` at minimum.
- `outcome ∈ {edge_supported, no_edge, driver_base_rate_failed}` — the estimator's
  verdict. `no_edge` is a success state, not a penalty.

Bump `schema_version` enum to include `0.5.0`; document-level metadata `schema_version`
→ `0.5.0` in memo.json only (per the v0.4.0 convention). Grandfather: prove a v0.4.0
memo validates clean against the 0.5.0 schema.

### Item 2 — reference: `independent-estimator-us.md`

New `us-equity-research/references/independent-estimator-us.md` (~200 lines), the
constructive twin of `r-v2-isolated-attack-us.md`:

- *Spawn contract.* Orchestrator dispatches the estimator via Task tool,
  `description="independent estimator — blind build"`, before the consensus_variance
  set is finalized. The prompt contains ONLY: the sector primitive template, the raw
  driver inputs (units, prices, capacity, balances × spread × credit, etc.), the
  relevant point-in-time filings, and the output schema. It MUST NOT contain: the
  consensus EPS/PT, sell-side notes, the bull/bear narrative, or any number derived
  from the Street.
- *Per-sector primitive templates.* Semis: units × ASP × attach × GM. Banks: avg
  balances × NIM × efficiency × NCO. E&P: production × realization × lifting cost.
  Each template lists the primitives the estimator must source independently.
- *Driver base-rate band.* For each driver, the estimator builds the historical
  analog distribution from primary sources (prior-cycle filings) and records the band.
  A driver outside its band without a specific structural reason → `driver_base_rate_failed`.
- *The reconcile.* The orchestrator computes `implied_variance` only after the blind
  estimate returns, then checks it against the analyst's declared `consensus_variance`.
  Three cases: (a) they agree → genuine, independently-grounded edge; (b) blind
  estimate ≈ consensus → `no_edge` (the honest path; see Item 4); (c) they disagree
  in direction → a flag the analyst must resolve (the analyst's variance may be the
  manufactured one).
- *Bounded context* (~30–50K tokens, mirroring R-v2) and *independent source reads*
  logged to the manifest.

### Item 3 — gate G21: independent-estimate-backed variance

New `scripts/verify_independent_estimate.py` (pydantic shim; stdlib-only logic):

- n_a if rating == Hold, or headline self-labeled "consensus-anchored", or
  schema_version < 0.5.0 (grandfathered), or memo carries `independent_estimate.outcome
  == "no_edge"` (the honest exit passes cleanly — it is not an overclaim).
- For a non-Hold memo at schema 0.5.0 claiming a score above the consensus-anchored
  ceiling: require `independent_estimate` present with `isolation.context_isolation ==
  true`, `inputs_excluded` covering the consensus fields, ≥1 driver with a
  `base_rate_band`, and `implied_variance_pct` reconciling (same sign, within a
  tolerance band) with at least one load-bearing `consensus_variance`. Fail otherwise
  with `blocks_score_above` at the consensus-anchored ceiling.
- Smoke test ≥6 branches: Hold n_a; no_edge pass; v0.4.0 grandfather skip; non-Hold
  0.5.0 with reconciling isolated estimate → pass; with estimate but isolation=false →
  fail; with estimate whose implied variance contradicts the declared variance → fail.

### Item 4 — the no-edge terminal state

Make `no_edge` a first-class, non-penalized outcome end-to-end: the rating taxonomy
gains/`recommendation.rating` accepts `"NoEdge"` (or reuse Hold with an explicit
`no_edge_reason`), G15/G20/G21 treat it as a clean pass (not a 7.0 penalty), and the
rubric documents it as a *success*. This removes the structural incentive that pushes
every memo toward a manufactured rateable view (review Issue 5).

### Item 5 — EPS-basis cross-consistency (the NVDA denominator bug)

Extend `verify_quant_cross_doc_consistency.py` (G18) OR add a focused check: the EPS
used in the headline `PT = EPS × multiple` must carry the same basis (GAAP /
non-GAAP) as the reconciliation bridge's labeled EPS, and the multiple must be the
matching basis. This catches the verified NVDA defect (headline "$6.50 non-GAAP" ×
40 while the bridge labels $6.50 GAAP and non-GAAP $6.65). Ship with a test.

### Item 6 — orchestrator wiring + wrap

`us-equity-research/SKILL.md`: add the estimator dispatch to Phase 2 (before the
variance set locks) and the no-edge path to the rating logic. Bump both plugin.json
to 0.5.0, CHANGELOG, README (gate count → 21, graduated rigor + independent estimate
documented). Run pytest; tag v0.5.0 LOCALLY (Path A). Reconcile all stale gate
counts as part of this (ties to overnight T7).

## Acceptance criteria

1. A non-Hold memo above the consensus-anchored ceiling cannot pass G21 without an
   isolated, base-rate-anchored independent estimate whose implied variance reconciles
   with the declared variance. `no_edge` passes cleanly.
2. The NVDA-class GAAP/non-GAAP denominator inconsistency fails Item 5's check.
3. v0.1.0–v0.4.0 memos validate and gate-run unchanged (grandfathered).
4. Every verifier change ships with a committed test; full pytest green before the
   v0.5.0 tag.
5. The harness H3 contrast (`full` vs `consensus_relative_only`) now has a real
   treatment to measure: `full` = estimator on, `consensus_relative_only` = estimator
   off.

## Honest limits

The independent estimate **narrows but does not eliminate** correlated-wrong: if the
analyst and the Street share a wrong *driver* assumption, only the base-rate attack
on that driver catches it, and only when history is informative — which it is least
at genuine regime breaks, the exact moments edge matters most. And like 3b, the
isolation is provenance-reconciled, not runtime-attested: a determined operator can
still fabricate a consistent `independent_estimate` block. 3c raises the cost of
faking edge from "shade consensus by 8pp" to "fabricate a blind driver build with a
defensible base-rate band that reconciles to a manifest" — materially harder, not
impossible.

## Cross-references
- `design/remediation-plan.md` — Phase 1, which this executes.
- `design/sprint-3b-context.md` — isolation provenance; G21 reuses its manifest block.
- `design/backtest-methodology.md` — H3 measures this change's value.
- `us-equity-research/references/r-v2-isolated-attack-us.md` — the destructive twin
  whose isolation contract Item 2 mirrors constructively.
