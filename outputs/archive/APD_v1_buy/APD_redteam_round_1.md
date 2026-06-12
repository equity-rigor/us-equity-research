# APD (Air Products) IC Memo — PM Red-Team, Round 1

**Date:** 2026-06-09 · **Target:** ≥8.5 (D20 default) · **Verdict: PASS — 8.8 / 10** · **Bottleneck: B-view (the variance is forward/predictive) + B2/B3 (segment op-margin analog)**

This is a red-team, not a cheerleader. The APD memo is **mechanically clean — all 19 applicable gates pass; G16 n_a** — and, uniquely versus a Hold, it carries a **defended non-consensus Buy** that clears the two hardest gates: G15 (consensus variance) and **G20 (view defensibility)**. That makes it a structurally *stronger* deliverable than a gate-clean Hold, because the view itself survived a structured attack. It clears 8.5 comfortably. It does not reach 9.0 because the load-bearing variance is **forward/predictive** (the FY2027 FCF inflection has not yet printed) and the segment layer is an operating-margin analog.

---

## Step 1 — Mechanical gate sweep (G1–G20)

| Gate | Name | Status | Note |
|---|---|---|---|
| G1 | EPS × multiple multiplicativity | **pass** | 5 scenarios multiply within ±0.5% (12.50×16.0=200.00 … 16.00×28.0=448.00) |
| G2 | Segment GM reconciliation | **pass** | weighted 23.72% vs 23.72% (op-margin analog; APD *reports* segment operating income — better-grounded than a pure construct) |
| G3 | SOTP monotonicity | **pass** | NI≤OP≤GP≤Rev holds all 3 segments |
| G4 | Scenario probabilities = 1.00 | **pass** | 0.10/0.22/0.40/0.20/0.08 |
| G5 | Bear/bull EPS bridge reconciles | **pass** | strong_bear −2.00, bear −1.00, bull +0.75, strong_bull +1.50 — exact |
| G6 | Source tag at first use | **pass** | revenue/ADV/beta/share categories tagged |
| G7 | Headline conditionality | **pass** | source_conditional; top-3 include S3 guide + S4 valuation → conditional required & present |
| G8 | GM taxonomy box | **pass** | T1–T5, op-margin analog labeled |
| G9 | What-would-reverse numerical | **pass** | 7 triggers w/ denominators (impairment ≥$1B, EPS <$13.50, capex >$4.5B…) |
| G10 | Anchor weighting impact table | **pass** | weighting_sensitivity present |
| G11 | Non-GAAP→GAAP reconciliation | **pass** | explicit GAAP-loss → adjusted-EPS bridge table in §4 |
| G12 | SBC treatment in FCF | **pass** | OCF−capex; SBC ~0.6% rev, flagged immaterial |
| G13 | Barra factor exposure | **pass** | 7 factors w/ z-scores |
| G14 | Capacity / ADV / days-to-exit | **pass** | ADV $340M; 10/20/30% = 3.5/1.8/1.2 days |
| **G15** | **Consensus variance** | **pass** | **non-Hold Buy → variance required & supplied:** V1 multiple re-rate, sizing 2.4pp (=20×60×20/10000), S1/S2/S3 evidence |
| G16 | Bank metrics | **n/a** | non-bank (Materials / Industrial Gases) |
| G17 | Revision velocity | **pass** | n=23; FY1 EPS +3.5% 3m; two guidance raises |
| G18 | Quant cross-doc consistency | **pass** | MD factor z-scores match JSON within ±0.2 |
| G19 | Provenance manifest | **pass** | SHA-256 verified; 16 web calls, 15 agents, 20 outputs hashed |
| **G20** | **View defensibility** | **pass** | **(a)** +25.8% PT-implied vs +16.2% consensus = **9.65pp differentiation** (≥8); **(b)** V1 carries S1 + S2 evidence; **(c)** adjudication_trail variance_attack on V1 (base_rate_sanity → modified) |

**Zero gate failures, including the two gates that grade view quality.** A Hold gets G15/G20 for free as n_a; this Buy *earned* them.

---

## Step 2 — Rubric scorecard (B1–B14 + view)

| Bug | Dimension | Score | Comment |
|---|---|---:|---|
| B1 | EPS × multiple | 9.5 | Exact |
| B2 | Segment GM reconcile | 8.0 | Op-margin analog, but built on APD's *reported* segment operating income (Americas 29.6%, Asia 26.0%, Europe 28.3% + Corporate reconciler) — more grounded than a pure construct |
| B3 | SOTP monotonicity | 8.3 | Monotonic; segment multiples reasonable for IG |
| B4 | GM taxonomy box | 9.0 | T1–T5; op-margin analog explicitly labeled (no GAAP GM in industrial gas) |
| B5 | Headline conditionality | 9.0 | Source-conditional with explicit if/then triggers |
| B6 | Bear EPS bridge | 9.0 | Soft/clean/strong; reconcile exactly |
| B7 | What-would-reverse | 9.5 | 7 numerical triggers, each with an observable (8-K, capex guide, Yara FID) |
| B8 | Cross-version consistency | 8.5 | Net debt $15.84B vs the company's 2.2x recourse-adjusted basis explicitly reconciled; PT $355 vs Street $328 owned in §6 |
| B9 | A0 tail map | 8.8 | 6 tails (4 bear + 2 bull), shifts conserve to zero |
| B10 | Position sizing | 9.0 | 5 mandates + Kelly + long-APD/short-LIN pair w/ beta hedge |
| B11 | Non-GAAP/GAAP reconcile | 9.0 | Explicit GAAP-loss → adjusted bridge table |
| B12 | SBC in FCF | 9.0 | OCF−capex; SBC immaterial; the *real* flag (debt-funded dividend) surfaced |
| B13 | Factor exposure | 9.0 | 7 Barra tags + rationale (Value+Quality+Low-Vol) |
| B14 | Capacity / ADV | 9.0 | Days-to-exit at 10/20/30% |
| **View** | **G15+G20 defensibility** | **8.8** | The differentiator: a genuine non-consensus Buy (+10pp above Street), S1/S2-anchored, surviving a base-rate attack. **Residual ceiling: the variance is forward** — the FCF inflection is sourced and mechanical but not yet realized; conviction is appropriately capped at 0.20× and the rating is source-conditional. |

**Weighted overall: 8.8/10.** Band: **8.5–9.0 (IC-grade hardness), upper end** — the G20-defended view lifts it above a comparable gate-clean Hold.

**What's genuinely good:** the memo takes a real, sized, above-Street view and then *attacks its own view* on the record (the adjudication-trail base-rate attack, outcome "modified" with the probability trimmed 65→60 and the re-rate capped at half-gap). That is exactly the discipline G20 exists to force — and it correctly identifies the load-bearing variable (the FY2027 FCF inflection) rather than hand-waving "Linde discount = upside."

---

## Step 3 — Residual ceiling (why 8.8, not 9.2)

1. **The variance is predictive, not yet realized (the honest cap).** V1 rests on capex guidance ($7.0B→$4.0B) and two beats — strong primary-source signals, but the FY2027 FCF positive print is still forward. Until the FY26 Q4 capex/FCF guide (Nov-2026) confirms, conviction is rightly 0.20× and the headline source-conditional. *No fix — this is the genuine state of the thesis; pretending otherwise would be the bug.*
2. **B2/B3 op-margin analog** — industrial gas has no GAAP gross margin; the segment layer uses reported segment *operating* income as the analog (labeled). Already more grounded than the Holds' modeled splits.
3. **Polish (B8):** could add one line reconciling the FY24 GAAP $17.18 (gain-inflated) vs adjusted $12.43 in §4 — minor.

**The memo is IC-ready at 8.8 and comfortably clears the 8.5 bar.** Unlike a Hold, it stakes a defended directional view and survives the view-quality gates. No edit changes the Buy call or the +18.7% probability-weighted return.

*Gate logs: `outputs/APD_verification_gates.json` · Manifest (SHA-verified): `outputs/APD_manifest.json`. Deliverable PDF: `outputs/APD_IC_memo.pdf`.*
