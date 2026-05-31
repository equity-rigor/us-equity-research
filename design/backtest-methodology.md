# Backtest Methodology — Validating the Research Framework

Institutional-grade historical validation design. Precedes live tracking (`design/remediation-plan.md` Phase 2). Authored 2026-05-31.

This is the rigor that gates the rebuild: until the framework's central claim — *that its output predicts forward risk-adjusted returns better than consensus and factors* — survives a leakage-honest backtest, the rebuild is building on an unvalidated premise. The deliverable here is the methodology, pre-registered, not the result.

---

## 0. The core problem, stated first

Backtesting a quant signal is a solved craft. Backtesting an **LLM-driven** research framework is not, because of one dominant threat that does not exist in classical backtests:

> **The model has the future in its weights.** Ask the system to research NVDA "as of 2024-06-01" and the model already knows, parametrically, how NVDA performed through its training cutoff. Point-in-time *input* data does not fix this — the leakage is in the model's memory, not the prompt.

Every design choice below is dominated by this. A backtest that does not measure and bound leakage is not conservative-but-imperfect; it is **invalid** — it will report spurious skill that is recall, and greenlight a rebuild that fails live. The methodology is therefore organized around isolating the framework's *incremental, causal* contribution from the model's *latent knowledge*.

A second, framework-specific constraint compounds it: each deep-dive memo is expensive (~2 hours of orchestrated agent execution, hundreds of tool calls). Sample size is costly, so the design must be **sample-efficient** (paired/within-name comparisons) rather than relying on large N.

---

## 1. What we are testing — pre-registered hypotheses

Pre-registration is mandatory: fix hypotheses, universe, horizons, metrics, and decision thresholds *before* looking at outcomes, to avoid the dredging that makes most strategy backtests fiction. Register the document hash.

| ID | Hypothesis | Primary metric | Null |
|----|-----------|----------------|------|
| H1 | The composite score rank-predicts forward factor-neutral return | Rank-IC, decile spread IR | IC = 0 |
| H2 | The framework's *structure* adds value over the raw model view | Δ(decision quality), gated vs ungated, paired | Δ = 0 |
| H3 | The **consensus-independent estimate's** variance predicts returns better than the **consensus-relative** variance | ΔIC (independent − relative) | ΔIC = 0 |
| H4 | Surviving (isolated, base-rate-defensible) variances predict more than unsurvived ones | IC by survival bucket | equal |
| H5 | What-would-reverse trigger discipline reduces drawdown / improves timing | trigger-conditioned MDD, capture ratio | no effect |

H2 and H3 are the load-bearing tests — they validate the *methodology*, which is leakage-robust (see §3), and H3 directly validates the Phase-1 keystone before it is built broadly. H1 is the headline claim but the *weakest* design (most leakage-exposed); it is reported with the widest error bars.

---

## 2. The dominant threat: LLM training-data leakage — layered defense

No single control is sufficient; defense is layered and the residual leakage is *measured*, not assumed away.

1. **Point-in-time (PIT) input isolation.** Feed only as-of-date artifacts (filings, prices, consensus snapshots, transcripts dated ≤ decision date). Necessary, not sufficient.
2. **Model-cutoff gating (the clean control).** A decision is *clean* only if the outcome horizon lies **entirely after the test model's training cutoff**. To validate 2024 decisions cleanly you need a model snapshot whose cutoff precedes 2024. Maintain a **model-snapshot registry** (model id ↔ cutoff date) and run each backtest window on the latest snapshot whose cutoff predates the window. Without older snapshots, the clean sample is only the post-current-cutoff period — which is small and bleeds into live tracking.
3. **Leakage audit / measurement (run on every window).** Quantify the bias rather than wish it away:
   - *Direct-recall probe:* ask the blinded model for the outcome (price 12m hence, beat/miss); its accuracy estimates the leakage ceiling for that window.
   - *Blinded−unblinded delta:* run the framework with the name anonymized/redacted (sector + financials, no identifiers) vs identified; the performance gap is a leakage estimate. Anonymization is imperfect (the model may re-identify), so the probe is also a re-identification test.
   - *Counterfactual perturbation:* feed a fictional but plausible alternate history; if "skill" persists on counterfactual inputs, it is reasoning; if it collapses, the real-data result was recall.
4. **Discard or down-weight contaminated cases** by measured leakage; report results both raw and leakage-adjusted, with the adjustment method pre-registered.

The honest consequence: the cleanest evidence (H2/H3 ablations and post-cutoff OOS) will be *small-N or leakage-robust by construction*; the large-N historical evidence (H1 PIT) is *contaminated and bounded, not trusted absolutely*. The methodology makes that trade explicit instead of hiding it.

---

## 3. Three-track design

No single track is sufficient; the conclusion rests on their agreement.

**Track A — Ablation (the workhorse; leakage-robust).** Hold the model and the information set fixed; vary only the framework's structure: {full framework} vs {no gates} vs {consensus-relative only, no independent estimate} vs {raw model view}. Measure the *incremental* effect on out-of-sample decision quality via paired, within-name comparisons. Leakage is approximately common-mode across arms and **differences out** — the estimand is the methodology's causal contribution, which is exactly what we are deciding whether to rebuild. Most sample-efficient (paired design), least leakage-exposed. This is the load-bearing track.

**Track B — Post-cutoff true-OOS (the absolute claim; clean but small).** Decisions whose entire outcome horizon postdates the test model's cutoff. Genuinely out-of-sample; no parametric leakage. Tiny N by construction and it grows only with calendar time — it is the bridge to live tracking. Used for the absolute "does the score predict returns" claim, with honest small-N error bars (bootstrap CIs, not asymptotic).

**Track C — Leakage-audited PIT historical (breadth; contaminated).** The large stratified historical sample, run PIT, with §2 leakage measurement applied and results reported raw and leakage-adjusted. Provides breadth/power for IC decay and regime analysis; never trusted as an absolute skill estimate. Its role is to *agree or disagree* with A and B, not to stand alone.

Decision rests on **convergence**: a rebuild is justified only if Track A shows positive incremental value, Track B is directionally consistent (not contradicting), and Track C's leakage-adjusted result does not collapse to zero.

---

## 4. Data spec — bitemporal PIT spine + model registry

- **Bitemporal store** (valid-time and knowledge-time) so every query reconstructs exactly what was knowable as-of date D: filings (EDGAR, by filing date), prices/returns (split/div-adjusted, PIT), **consensus snapshots dated as-of** (the #1 look-ahead in fundamental backtests — never use a restated consensus), transcripts, borrow rate/utilization, factor returns.
- **Survivorship-free universe:** PIT index constituents including delisted/acquired/bankrupt names with their terminal returns. Omitting them is the classic alpha-inflation bug.
- **Model-snapshot registry:** model id ↔ training cutoff ↔ availability, so §2.2 gating is enforceable and so results are stamped with the (framework × model) pair they validate (see §9 model-drift).
- **Corporate-action and restatement handling:** use first-reported (PIT) fundamentals for the decision, GAAP-restated for nothing in-sample.

Forks dependency: Track A needs only filings + the model (no live feed) — runnable under "Claude-only." Tracks B/C and all return metrics need the price/factor/borrow feeds (`remediation-plan.md` Fork B). If Fork B = no feeds, only Track A is executable, and only on non-return proxies — a materially weaker but still informative backtest.

---

## 5. Sample construction & power

- **Universe:** pre-registered, e.g. Russell 1000 PIT constituents, stratified by sector, size, and **regime** (rate regime, vol regime, cross-sectional dispersion regime) so results are not a single-regime artifact.
- **Selection:** stratified random sample, *not* cherry-picked names. The current 5 showcase memos are not a sample — they are anecdotes and have zero evidentiary weight for H1.
- **Power:** fundamental deep-dives are costly, so classical N is small. Mitigation: Track A's paired design (variance-reducing), block bootstrap for CIs, and reporting *effect size with CI* rather than binary significance. Pre-compute the minimum detectable effect at the affordable N; if it exceeds plausible alpha, say so up front rather than running an underpowered test.

---

## 6. Labels, nulls, neutralization

- **Label:** forward H-month return (H = the memo's stated horizon, primary 12m), **factor-neutralized** — residual after regressing out market + size/value/momentum/quality (and sector) — so we measure *alpha*, not factor beta a cheap ETF would have captured. Also: Brier score on the 5-scenario probabilities; realized vs PT error; trigger-fire timing.
- **Nulls / benchmarks (a backtest without the right null is theater):**
  1. **Consensus** (sell-side PT-implied return / consensus EPS revision) — the framework must beat *just following the Street*.
  2. **Factor model** — does residual alpha survive factor neutralization?
  3. **Score permutation** — shuffle scores across names; does true IC exceed the permutation distribution?
  4. **Raw model view** (Track A) — does structure beat the un-gated model?
- **Costs:** all return metrics net of transaction cost, market impact at the tested participation rate, and **borrow** on shorts. Gross alpha that dies after costs/borrow is not alpha.

---

## 7. Metrics & overfitting controls

**Performance:** Rank-IC (Spearman, score vs forward residual return) and its t-stat with **Newey–West** SEs (overlapping horizons induce serial correlation); **IC decay curve** and half-life (edge decay); decile **long/short spread** portfolio IR; hit rate vs base rate; calibration via reliability diagram + Brier decomposition; capture ratios for H5.

**Overfitting / multiple-testing controls (non-negotiable for credibility):**
- **Purged k-fold cross-validation with embargo** (López de Prado): purge training labels that overlap a test horizon and embargo the post-test window, to kill leakage through overlapping/serially-correlated labels.
- **Deflated Sharpe Ratio** — adjust any reported SR/IR for the number of configurations tried and non-normality; the naive SR of the best of many trials is upward-biased.
- **Probability of Backtest Overfitting (PBO)** via combinatorially-symmetric CV — report it; a high PBO kills the result regardless of in-sample IR.
- **Multiple-testing correction** (Benjamini–Hochberg) across the 20 gates + composite + sub-signals; testing 20 gates guarantees a spurious "winner" uncorrected.
- **Block bootstrap** CIs throughout (not asymptotic, given small N and serial correlation).

---

## 8. Protocol (step-by-step)

1. Pre-register hypotheses, universe, horizons, metrics, thresholds; hash and commit the registration.
2. Build the bitemporal PIT spine and the model-snapshot registry; validate as-of reconstruction on spot checks.
3. Draw the stratified survivorship-free sample; freeze it.
4. For each name/date: run the §2 leakage audit (record direct-recall, blinded−unblinded delta, counterfactual).
5. Track A: run the ablation arms on the frozen sample; compute paired Δ.
6. Track B: run the post-cutoff clean subset.
7. Track C: run the PIT historical sample; apply leakage adjustment.
8. Compute metrics (§6–7) with all overfitting controls; bootstrap CIs.
9. Apply the §10 decision rule. Report raw and leakage-adjusted, by regime, with PBO and DSR.
10. Archive everything for reproduction and for the model-drift re-run (§9).

---

## 9. Destruction analysis (when this backtest is invalid; kill criteria)

The user asked for it on the *signal*; here it is on the *backtest itself* — the conditions under which our own validation is not to be trusted.

- **Leakage ceiling breached.** If the direct-recall probe shows the model predicts outcomes well even blinded, the leakage ceiling is near the measured skill and H1 is uninterpretable. *Kill:* report Track A/B only; do not claim absolute skill.
- **Model drift.** A backtest validates a specific **(framework × model) pair**. A model upgrade (e.g., opus-4-8 → successor) partially invalidates it; latent knowledge, calibration, and reasoning all shift. *Kill/trigger:* any model change forces a re-run of at least Track A before the rebuild's validation carries over. This is a standing model-risk governance control, not a one-time check.
- **Regime non-stationarity.** Alpha concentrated in one regime (e.g., only the 2023–24 AI melt-up) does not generalize. *Kill:* require positive IC in ≥2 of 3 pre-registered regimes, else scope the claim to the regime.
- **Underpowered N.** If the minimum detectable effect (§5) exceeds plausible alpha, a null is uninformative, not exculpatory. *Kill:* do not interpret a null as "no harm"; state the power limit.
- **Capacity / crowding.** A score-sorted L/S book has a capacity ceiling (universe liquidity, borrow on the short leg). Report alpha vs participation/AUM; alpha that exists only at negligible size is not deployable. The short leg's borrow and squeeze risk cap capacity asymmetrically.
- **Survivorship / consensus look-ahead reintroduced.** Any restated-consensus or delisting-omission bug silently inflates results; spot-audit the spine.
- **PBO high / DSR ≤ 0.** Either kills the result outright.

---

## 10. Decision rule & deployment runbook (what greenlights the rebuild)

Pre-registered, conjunctive:

1. **Track A (incremental value): required.** Paired Δ in decision quality > 0 with bootstrap CI excluding 0, net of costs. This is the gate — if structure adds nothing over the raw model, the rebuild is not justified on these grounds.
2. **Track B (absolute, clean): directionally consistent**, not contradicting A (small N tolerated; sign and CI overlap).
3. **Track C (breadth): leakage-adjusted IC does not collapse to 0**; positive in ≥2 regimes.
4. **Overfitting gates:** PBO < 0.5 and Deflated Sharpe > 0 on the headline portfolio.
5. **H3 specifically positive** (independent-estimate variance beats consensus-relative) → greenlights the Phase-1 keystone *first*, since it is both validated and cheap.

If 1–4 pass: proceed to the rebuild, sized to the *measured* effect (not the in-sample max). If 1 fails: do not rebuild for alpha — scope the framework honestly as a process/competence tool (the cheap Fork-A branch) and rely on live tracking only. Governance: independent sign-off on the pre-registration and on the leakage audit before results are read; the reviewer is not the builder.

---

## 11. Honest verdict — what a backtest can and cannot establish here

A backtest of an LLM research framework **cannot** cleanly establish "the model picks stocks well" — leakage makes the absolute skill estimate unreliable, and the only fully clean sample (post-cutoff) is small and *is* live tracking under another name. What it **can** establish, and what we should actually decide on, is **causal and incremental**: does the framework's *structure* — gates, the independent estimate, survival-tested variances, trigger discipline — improve decisions over the raw model on the same information, leakage differenced out (Track A)? That question is answerable now, is the right question for a *rebuild* decision, and is leakage-robust. So the methodology deliberately demotes the seductive H1 ("our score predicts returns") to a wide-error-bar supporting role and elevates H2/H3 (the ablation) to the decision gate. That inversion is the institutional-grade move: validate the thing you can validate cleanly, and let live tracking earn the absolute claim over time.

---

## Cross-references
- `design/remediation-plan.md` — Phase 2 (live tracking) follows this; Fork B (feeds) gates Tracks B/C.
- `design/framework-critical-review.md` — Issue 1 (unbacktested score) is what this answers.
- `us-equity-research/references/r-v2-isolated-attack-us.md` — the isolation machinery whose constructive twin (the independent estimate) H3 validates.
