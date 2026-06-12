# Judgment Discipline (v0.7.0 layer) — US

The 20 mechanical gates (G1–G20) verify the **arithmetic**: the math ties, every number is sourced, scenarios sum to 1.00, the bear bridge reconciles. They verify **zero judgment**. But a rating is made by two judgment calls — the **base anchor** and the **multiple** — and updated by a third act: **how you revise**. That is where bias enters and where the original framework was silent. The v0.7.0 judgment layer (gates G21–G23 + the disciplines below) sits on top of the mechanical gates.

> **One line for the top of both SKILLs:** *Gates verify the arithmetic; they do not verify the judgment. The base anchor and the multiple are where the call is made — decompose them, tag them verifiable-or-assumed, and re-derive them; never adopt them from price or from another analyst's conclusion.*

## Lesson 1 — Two values in parallel; blend by convergence (G21)
Compute **both**: (B) an **independent fair value** — DCF + NAV/SOTP + normalized-earnings × a justified through-cycle multiple, built **without reference to price**; and (A) a **market-regime value** — the public consensus PT, which embeds the current-multiple regime. The **gap between price and B is the mispricing signal** (gap < ~8% → fairly valued/Hold; large gap → Buy/Sell sized by the gap). The 12-month base PT is a **convergence-weighted blend**, not either pole: anchor toward fair value, weighted by convergence speed — FAST if catalyst-driven (print/guide/FID), SLOW if momentum/regime-persistent. **G21**: when `valuation_parallel` is present, the base PT must reconcile to the independent fair value within 15% or the gap must be explicitly justified as a timing/regime call (`convergence_assumption` + `convergence_speed`). Schema: top-level `valuation_parallel`.

## Lesson 2 — Decompose every revision (G22)
When a target moves, split the move into **Δestimate (verifiable) / Δmultiple (judgment) / Δmethodology (judgment)**. A revision should come mostly from *estimates*. When it comes mostly from the *multiple* or a *methodology switch*, it is judgment-led — trust it **less**, and label it. **G22**: when `valuation.revision_bridge` is present, components must reconcile to (new − prior); `judgment_share_pct` (share of |move| from multiple + methodology) must match the components; and if it exceeds 50%, a `judgment_flag` is required. *Methodology-switch PT jumps (e.g. SoTP→P/E tripling a target) and PT-chases-price history are the canonical tells.* Schema: `valuation.revision_bridge`.

## Lesson 3 — Tag each input verifiable vs. assumed; name the load-bearing one
Normalized EPS is **buildable bottom-up and tends to converge** across analysts (verifiable). The multiple is a **judgment that diverges** (assumed). The disagreement almost always lives in the assumed input — surface it so the debate is about the right thing. Schema: per-method `input_attribution: {verifiable, assumed, load_bearing_input}`.

## Lesson 4 — For any "structural re-rate / this-time-is-different" thesis: base rate + mechanism + observable
Don't argue the headline PT. (i) Check the **base rate** of that *class* of claim ("memory de-cyclicalized → higher multiple" was argued at the 2017–18 top and reset in 2019 and 2023). (ii) Trace it to its **single load-bearing mechanism** (e.g. long-term fixed-price agreements holding through a 50–70% spot crash — fragile; out-of-the-money offtake gets renegotiated). (iii) Name the **falsifiable public observable + date** that confirms or breaks it. Test *that*, not the conclusion. Schema: `structural_thesis_tests[]: {thesis, base_rate, load_bearing_mechanism, discriminating_observable, observe_by, verdict}`.

## Lesson 5 — Public sell-side *signals* only; never the proprietary note (enforced by G23)
Ingest **public** sell-side signals — aggregated consensus median/dispersion, publicly-reported PTs, public rating distributions, public PT history (the "PT chases price" pattern is visible from it). **Re-derive the multiple/PT yourself**; never adopt another analyst's conclusion. A desk reaching *Neutral* despite IB conflicts is more credible than one reaching *Buy*. **Entitlement-restricted research (client-only sell-side notes, NDA expert calls, subscription feeds, anything marked no-redistribution / no-AI-input) is OUT OF FRAMEWORK SCOPE** — usable only as a personal, non-persisted, **localized cross-check**, never a committed anchor. See Lesson 5b.

## Lesson 5b — Source-tier public boundary (G23)
Every S1–S5 citation must resolve to a **publicly accessible** source. This is what makes a call reproducible and auditable. **G23** scans `source_tags` for entitlement markers (client-only, no-redistribution, proprietary research, named restricted desks used as a primary citation, or an explicit `access_tier: restricted` / `public_access: false`) and fails the memo if any citation is non-public. The nonpublic layer is the analyst's personal overlay; it sits on top, nuances conviction privately, and **never enters the repo**.

## Lesson 6 — Conviction is a separate, downgradeable axis; the anchoring check is bidirectional
Track **rating and conviction independently**. New public counter-evidence lowers conviction even when it does not flip the rating. And the anchoring discipline runs on your **own** revisions in **both** directions — over-revising toward the bulls (importing their conclusions) is the same bias as the original spot-anchoring, just flipped. Schema: `conviction_axis: {rating, conviction, conviction_drivers_for, conviction_drivers_against, self_anchoring_check, downgradeable_note}`.

## Lesson 7 — Cyclicals: normalized EPS + P/B, never peak × forward multiple
A deep cyclical at a peak looks "cheap" on peak-EPS × the current multiple — that *inverts* the call (the most-overvalued name screens cheapest). For `is_cyclical: true` names, the base must be valued on **mid-cycle / normalized EPS** with a **price-to-book cross-check**, never peak EPS. (Extends the D8 sector branch.)

---
### Gate summary (v0.7.0)
- **G21 — fair-value reconciliation** (`scripts/verify_fair_value_reconciliation.py`): self-gating on `valuation_parallel`; base PT reconciles to independent fair value or justifies the gap as timing.
- **G22 — revision attribution** (`scripts/verify_revision_attribution.py`): self-gating on `valuation.revision_bridge`; the move decomposes to estimate/multiple/methodology, reconciles, and flags judgment-led revisions (>50% multiple+methodology).
- **G23 — source-tier public boundary** (`scripts/verify_source_tier_public.py`): every citation resolves to a public source; entitlement-restricted research is rejected.

All three are **additive and self-gating** — `n_a` when their block is absent — so they layer cleanly over the grandfathered 20-gate set without disturbing it. Run via `scripts/run_all_gates.sh TICKER` (now 22 lines).
