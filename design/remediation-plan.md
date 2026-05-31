# Remediation Program — Addressing the v0.4.0 Critical Review

Companion to `design/framework-critical-review.md` (the diagnosis) and `design/sprint-3b-context.md` (the isolation-provenance sprint, which becomes one tile in this larger program). Authored 2026-05-31.

This is how a senior L/S PM and an agent build-team would actually plan the fix — not a feature backlog. The defining move is that **you do not start with code.** Two strategic decisions gate everything; until they are made, every sprint is polishing the editor. The plan below states them first, then sequences the build by dependency, and red-teams itself at the end.

---

## Decision 0 — the two strategic forks (resolve before any building)

**Fork A — Scope: single-name diligence tool, or portfolio system?** The framework is an excellent deep-dive engine. Issues 3 and 4 (no L/S risk, no origination, no book layer) are not bugs in a diligence tool — they are category mismatches. A senior PM forces the call: either (a) **scope it honestly** as a high-conviction deep-dive tool for a handful of names and stop implying portfolio-grade output, or (b) **commit to building the portfolio half** (origination → risk → construction → monitoring), which is a larger program than the research engine itself. Most of the cost below lives in (b). Choosing (a) is legitimate and cheap; pretending (a) is (b) is what the review penalizes.

**Fork B — Data: stay "Claude-only / no live feeds," or take market data?** Issues 3 and 6 (shorts unpriced, factor exposures asserted, sizing decorative) are *unfixable* without three feeds: a **price/returns history** (for covariance and realized vol), a **borrow feed** (rate, utilization, days-to-cover), and **factor returns** (to estimate exposures by regression rather than assertion). The framework's founding "Claude-only, no live feeds" constraint is directly incompatible with real risk management. The PM must decide: take the feeds (and accept the operational/cost/governance burden), or accept that all risk numbers are illustrative and label them as such. There is no third option where asserted Barra z-scores become trustworthy.

Everything downstream is conditioned on these two answers. The plan assumes the ambitious branch (A=portfolio, B=take feeds) and flags what collapses under the conservative branch.

---

## Division of labor — senior analyst vs agent system

| Owned by the senior analyst (judgment) | Owned by the agent system (execution) |
|----------------------------------------|----------------------------------------|
| The two forks above; model-risk governance | Isolated independent estimation (Sprint 3a infra) |
| Which primitives drive each name; the analog set for base rates | Driver decomposition, base-rate computation from filings |
| Overriding the model with a documented reason | Gate verification, cross-document consistency checks |
| Borrow/squeeze read on a specific crowded short | Borrow/utilization pull, days-to-cover math |
| Final sizing under the book's risk budget | Covariance build, contribution-to-risk, candidate sizes |
| What "no edge" means for a given mandate | Outcome resolution, calibration accrual (scheduled daemon) |

The principle: the agent builds the *evidence and the arithmetic*; the analyst owns the *judgment and the override*. The current framework inverts this in one dangerous place — it lets the agent emit a judgment-flavored 6–10 score the analyst then defers to. The recomposition (Phase 5) fixes that.

---

## The phased program

Ordering is by dependency and leverage, not by issue number. Cheap keystones first; long-pole data accrual started in parallel; the expensive risk build gated on Fork B.

### Phase 1 — Consensus-independent estimator (the keystone). Fixes Issues 2, 5, and the floor of 1.

**Hypothesis.** "Edge" is currently undefinable because every number is anchored to consensus. If one load-bearing forecast is built from primitives *without sight of the Street number*, then variance becomes real (independent_estimate − consensus), correlated-wrong becomes inspectable (the drivers are explicit and stress-testable), and the honest "no edge" outcome becomes expressible.

**Design / agent architecture.** Add an **Independent Estimator** agent, spawned with the *same isolation machinery Sprint 3a built for R-v2* — but constructive, not destructive. It receives only the raw driver primitives (units, price, attach, mix, capacity, balances × spread × credit for banks), the relevant filings, and the methodology; it MUST NOT receive the consensus EPS, the Street PT, the sell-side notes, or the bull narrative. It returns a number and its driver bridge. The orchestrator then computes the variance against consensus *after* the estimate is locked. Reuse `attacker_context_isolation` provenance (manifest 0.4.0, Sprint 3b) so the isolation is verifiable, not self-reported.

**Data spec.** Primitive drivers per sector (semis: units × ASP × attach × GM; banks: avg balances × NIM × efficiency × NCO; E&P: production × realization × lifting cost). Point-in-time filings only. No consensus fields in the estimator's context.

**Validation.** The estimate's *drivers* are attacked on base rates (reuse R-v2's `base_rate_sanity`): is each driver inside its historical analog distribution? A variance survives only if it is both independent (built blind) and base-rate-defensible.

**Destruction.** (i) Hidden anchoring — if the primitives handed in are themselves Street-derived, independence is fake; mitigation is strict primitive sourcing + the isolation gate. (ii) Garbage-in — a blind estimate can be confidently wrong; that is *fine and the point* — it surfaces as a large, base-rate-failing variance the analyst must own, rather than a laundered consensus. (iii) It does not catch correlated-wrong when the analyst and Street share a *driver* assumption (e.g., everyone wrong on AI attach rate); only the base-rate attack on that driver can, and only if history is a guide.

**Also in Phase 1 (cheap, ride along):** a **"no differentiated view" terminal state** that is a respectable success output (not a 7.0 penalty), fired when the independent estimate ≈ consensus and no driver stresses to an edge; and **correctness/cross-consistency gates** that catch the form-not-content failures the review found — e.g., the headline EPS basis (GAAP vs non-GAAP) must equal the basis in the reconciliation bridge (this is the NVDA `$6.50` denominator bug; extend the G18 quant-cross-doc verifier).

### Phase 2 — Forecast registry + outcome resolver + calibration. Fixes Issue 1. **Start now; matures over quarters.**

**Hypothesis.** A score earns the right to imply predictive validity only by accumulating a track record against realized outcomes. The framework already emits dated, machine-readable forecasts (scenario probabilities, PT, what-would-reverse triggers with dates) — so the track record is buildable; it just is not being captured.

**Design / agent architecture.** (i) **Forecast registry** — persist every memo's structured prediction at write time (scenario distribution, PT, horizon, trigger dates). (ii) **Outcome-resolution daemon** — a *scheduled task* (the capability already in use) that at each horizon/trigger date pulls the realized value and scores the prediction: Brier score on the 5-scenario probabilities, directional hit/miss, realized return vs PT, and whether each what-would-reverse trigger fired and whether the memo reacted. (iii) **Calibration model** — once N is adequate, regress realized outcomes on memo features/gates to learn which actually predict, replacing the asserted 6–10.

**Data spec.** Realized prices/EPS/segment actuals at horizon (needs Fork B's feed). Per-analyst and per-memo-type partitioning.

**Validation.** Reliability diagrams (are 70%-probability calls right 70% of the time), Brier decomposition, hit-rate vs base rate.

**Destruction.** This is the honest long pole. (i) N is small and accrues slowly — no calibrated score for several quarters; you cannot retro-backtest because the memos did not exist historically (point-in-time reconstruction is possible but expensive and leakage-prone). (ii) Regime dependence — a track record built in one regime mis-calibrates the next. (iii) Survivorship — only written names get scored. **Interim honest move:** until calibration matures, *stop emitting a single number that implies predictive validity* (Phase 5) rather than pretend.

### Phase 3 — L/S risk layer. Fixes Issues 3 and 6. **Gated on Fork B = take feeds.**

**Hypothesis.** Sizing is decorative because there is no covariance, no borrow in the numerator, and no book context. Real risk-budgeted sizing requires a returns covariance and a borrow feed; with them, the universal 0.125 fudge can be retired.

**Design / agent architecture.**
- **Borrow into E[R]:** subtract `stock_loan_rate_bps` + a squeeze-risk premium from short expected return *before* Kelly. (Trivial code, large correctness gain.)
- **Factor/covariance model:** estimate exposures by rolling regression of name returns on factor proxies (Value/Momentum/Quality/Size/LowVol ETFs or vendor factor returns) instead of asserting z-scores; build a sample/shrinkage covariance from price history. A real Barra/Axioma feed is better; the proxy is the Claude-only-compatible floor and is *approximate, not decorative* — label it so.
- **Risk-budgeted sizing:** replace Kelly×0.125 with contribution-to-tracking-error budgeting — size the name so its *marginal* contribution to book vol/factor risk fits the budget, given current holdings. Negative-edge names → no position or a short, stated honestly (this directly kills the "negative Kelly → benchmark weight" incoherence).
- **Short-specialist agent** (the missing function the review flagged): owns borrow availability/cost, days-to-cover, utilization/crowding, and asymmetric (capped-upside/left-tailed) payoff modeling; applies a different sizing cap.
- **Book object:** a portfolio-state object (holdings, sizes, exposures, P&L) that the sizing and monitoring layers read.

**Data spec.** Daily returns history (covariance, realized vol), factor returns, borrow rate/utilization, short interest/days-to-cover.

**Validation.** Backtest the sizing policy on historical book states (ex-ante risk vs realized); verify factor-neutral pairs actually neutralize out-of-sample.

**Destruction.** Proxy factor exposures are noisy and unstable; sample covariance is non-stationary (shrinkage helps, not cures). Under Fork B = no feeds, this entire phase collapses to "label the numbers illustrative" — the conservative branch cannot have real L/S risk, full stop.

### Phase 4 — Portfolio process. Fixes Issue 4. (Only under Fork A = portfolio.)

- **Origination funnel:** a cheap, wide **screening agent** (factor / revision / event / anomaly screens) that ranks a candidate watchlist; the expensive deep-dive runs *only* on the top of the funnel. Different cost profile by design (cheap-wide → expensive-deep).
- **Tiered rigor:** explicit tiers — *screen* (minutes), *quick-look* (~15 min, gate subset), *full IC* (the current ~2-hour, 19-agent process). Most names live at screen/quick-look; full deep-dive only for sizing decisions. This is what makes a 60–120 name book tractable.
- **Position-aware monitoring:** the what-would-reverse triggers feed a monitoring daemon (scheduled task) that fires *weighted by position size* and routes a re-underwrite when a held name's trigger trips.

**Destruction.** The deep-dive remains expensive even tiered; agent cost/latency is the real ceiling on book scale. Screening quality is its own alpha problem — a weak screen just moves the consensus problem upstream.

### Phase 5 — Recompose the score. Fixes the root of Issue 1.

Retire the single 6–10. Emit a **vector**: `mechanical_integrity` (pass/fail — the honest, already-good G1–G6 floor), `edge_independence` (did an isolated estimate produce a base-rate-defensible variance — Phase 1), and `calibration` (the analyst's / memo-type's track record — Phase 2, blank until it matures). A PM reads three honest signals instead of one misleading one. Gated on Phases 1–2.

---

## Sequencing and dependencies

```
Decision 0 (forks A & B) ──┬─> Phase 1 (independent estimator)  ── keystone, ~1 sprint, cheap
                           │      └─ enables ─> no-edge exit, correctness gates, Phase 5
                           ├─> Phase 2 (registry + resolver)    ── START NOW, matures over quarters
                           └─(Fork B)─> Phase 3 (L/S risk)      ── large build, gated on feeds
                                          └─(Fork A)─> Phase 4 (portfolio process)
Phase 1 + Phase 2 ──> Phase 5 (recompose score)
Sprint 3b (isolation provenance) ──> precondition for Phase 1's verifiable isolation
```

Critical path: **Decision 0 → Sprint 3b (isolation provenance) → Phase 1 (independent estimator).** That is the cheapest sequence that makes "edge" mean something. Phase 2 runs in parallel from day one because it only pays off with elapsed time. Phase 3 is the expensive half and should not start until Fork B is decided yes.

**Concrete next sprint (3c):** the Independent Estimator + no-edge exit + the EPS-basis cross-consistency gate. It reuses Sprint 3a/3b isolation machinery, needs no new data feed, and is the single highest-leverage change — it converts the framework from "scores deviation from consensus" to "tests whether an independent build supports a deviation at all."

---

## Honest limits of this plan (red-team on the remediation itself)

1. **The binding constraint is Fork B, not engineering.** Without price/borrow/factor feeds, Issues 3 and 6 can only be made *less dishonest* (label numbers illustrative), not *fixed*. No amount of agent cleverness substitutes for a covariance matrix.
2. **Calibration cannot be rushed.** A predictive score needs quarters-to-years of forward outcomes; anyone promising a backtested score sooner is reconstructing point-in-time data with leakage. The interim deliverable is *honest decomposition*, not a magic number.
3. **The independent estimator narrows but does not eliminate correlated-wrong.** If the analyst and the Street share a wrong *driver* assumption, only the base-rate attack catches it, and only when history is informative — which it is not at genuine regime breaks (the exact moments edge matters most).
4. **This roughly doubles the system.** The portfolio half (origination, risk, construction, monitoring) is a larger build than the existing research engine. Fork A = "scope honestly as a deep-dive tool" is a legitimate, much cheaper answer, and a disciplined PM should price it seriously rather than defaulting to the ambitious branch.
5. **Anti-gaming is adversarial and never finished.** Moving from presence-gates to the independent estimator raises the cost of gaming; it does not end it. Expect to keep red-teaming the estimator the way Sprint 3a red-teamed R-v2.

---

## Cross-references

- `design/framework-critical-review.md` — the six core issues this program addresses.
- `design/sprint-3b-context.md` — isolation provenance; precondition for Phase 1's verifiable independence.
- `us-equity-research/references/r-v2-isolated-attack-us.md` — the isolation machinery Phase 1 reuses constructively.
- `us-equity-ic-rigor/references/position-sizing-us.md`, `quant-overlay-us.md` — what Phase 3 replaces.
