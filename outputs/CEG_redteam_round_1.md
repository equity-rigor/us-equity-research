# CEG (Constellation Energy) IC Memo — PM Red-Team, Round 1

**Date:** 2026-06-11 · **Target:** ≥8.5 (D20 default) · **Verdict: PASS — 8.7 / 10** · **Bottleneck: B2/B3 (segment energy-margin modeled) + the open-book/hedge disclosure gap**

This is a red-team, not a cheerleader. The memo is **mechanically clean — all 19 applicable gates pass; G15/G16/G20 n_a** — and structurally complete (T1–T5 taxonomy, layered bridges, 6-tail A0 map with zero-sum shifts, 5-mandate sizing, three-method reconcile, 7 Barra factor tags, capacity/ADV, source-conditional headline, 7 numerically-denominated triggers, GAAP/non-GAAP bridge, declared downward variance). It clears 8.5. It does not reach 9.0 because (a) CEG discloses geographic segments by capacity, not energy margin, so the GM/SOTP layer is modeled, and (b) the load-bearing bear lever — the open out-year book's sensitivity to PJM capacity reversion — rests on hedge ratios CEG does not disclose at this granularity.

---

## Step 1 — Mechanical gate sweep (G1–G20)

| Gate | Name | Status | Note |
|---|---|---|---|
| G1 | EPS × multiple multiplicativity | **pass** | 5 scenarios multiply within ±0.5% (12.00×14.0=168.00 … 15.50×25.0=387.50) |
| G2 | Segment GM reconciliation | **pass** | weighted 23.75% vs 23.75% — *but modeled, see B2* |
| G3 | SOTP monotonicity | **pass** | NI≤OP≤GP≤Rev holds all 3 segments — *but see B3* |
| G4 | Scenario probabilities = 1.00 | **pass** | 0.12/0.25/0.36/0.20/0.07 |
| G5 | Bear/bull EPS bridge reconciles | **pass** | strong_bear −1.50, bear −0.75, bull +1.00, strong_bull +2.00 — exact |
| G6 | Source tag at first use | **pass** | revenue/ADV/beta/capacity categories tagged (GW figures sourced in JSON) |
| G7 | Headline conditionality | **pass** | source_conditional; top-3 include the S3 FY2026 guide → conditional required & present |
| G8 | GM taxonomy box | **pass** | T1–T5, IPP energy-margin adaptation |
| G9 | What-would-reverse numerical | **pass** | 7 triggers w/ denominators (EPS <$13.0, BRA <$250, synergies <$2/sh) |
| G10 | Anchor weighting impact table | **pass** | weighting_sensitivity present |
| G11 | Non-GAAP→GAAP reconciliation | **pass** | GAAP-EPS vs Adjusted-Operating-EPS parallel in §4 |
| G12 | SBC treatment in FCF | **pass** | OCF−capex; SBC ~0.3% rev; the real flag (hedge-collateral OCF swing) surfaced |
| G13 | Barra factor exposure | **pass** | 7 factors w/ z-scores |
| G14 | Capacity / ADV / days-to-exit | **pass** | ADV $1.0B; 10/20/30% = 2.0/1.0/0.7 days |
| G15 | Consensus variance | **n/a** | rating=Hold (1 load-bearing downward variance declared anyway, sizing 2.16pp) |
| G16 | Bank metrics | **n/a** | non-bank (Utilities/IPP) |
| G17 | Revision velocity | **pass** | n=21; PTs net −8% 3mo; EPS flat (guidance reaffirmed) |
| G18 | Quant cross-doc consistency | **pass** | MD factor z-scores match JSON within ±0.2 |
| G19 | Provenance manifest | **pass** | SHA-256 verified; 16 web calls, 15 agents, 20 outputs hashed |
| G20 | View defensibility | **n/a** | Hold (base PT $256.50 is ~30% below the stale Street median $367) |

**Zero gate failures.** Mechanical floor cleared → ≥7.5; structures present → ≥8.5.

---

## Step 2 — Rubric scorecard (B1–B14)

| Bug | Dimension | Score | Comment |
|---|---|---:|---|
| B1 | EPS × multiple | 9.5 | Exact |
| **B2** | **Segment GM reconcile** | **7.0** | **Passes G2, but the 4 LTM segment margins are S5-modeled** — CEG reports geographic segments by *capacity* and Adjusted Operating Earnings, not segment energy margin. Honest (S5-tagged) but constructed. |
| **B3** | **SOTP monotonicity** | **7.5** | **Passes G3, but segment GP/OP/NI are modeled-to-be-monotonic**, not from a disclosed segment P&L. The nuclear-vs-gas multiple split (11x/8x) is the analytically important part and is defensible. |
| B4 | GM taxonomy box | 9.0 | T1–T5; IPP energy-margin adaptation labeled |
| B5 | Headline conditionality | 9.0 | Source-conditional with explicit if/then triggers |
| B6 | Bear EPS bridge | 9.0 | Soft/clean/strong; reconcile exactly both tails |
| B7 | What-would-reverse | 9.5 | 7 numerical triggers, each with an observable (BRA report, guide, 8-K) |
| B8 | Cross-version consistency | 8.5 | Net debt EV-implied $21.15B vs standalone $5.3B + Calpine debt explicitly reconciled (§12 + metadata); base PT $256.50 vs stale Street $367 owned in §6/§8 |
| B9 | A0 tail map | 8.8 | 6 tails (4 bear + 2 bull), shifts conserve to zero |
| B10 | Position sizing | 9.0 | 5 mandates + Kelly + long-VST/short-CEG pair w/ beta hedge |
| B11 | Non-GAAP/GAAP reconcile | 9.0 | GAAP-EPS ↔ Adjusted-Operating-EPS parallel; MtM driver explained |
| B12 | SBC in FCF | 9.0 | OCF−capex; SBC immaterial; the hedge-collateral OCF swing surfaced as the real flag |
| B13 | Factor exposure | 9.0 | 7 Barra tags + rationale (Size/Liquidity/Growth, negative Momentum) |
| B14 | Capacity / ADV | 9.0 | Days-to-exit at 10/20/30%; most liquid in the cohort |

**Weighted overall: 8.7/10.** Band: **8.5–9.0 (IC-grade hardness).** B2/B3 cluster at ~7.5 (intrinsic to an IPP that discloses capacity, not margin); B9 next.

**What's genuinely good:** the memo is **internally consistent with the prior VST work** — it treats CEG as the premium *short* leg of the long-VST/short-CEG pair and lands a Hold that is honestly ~30% below a *stale, being-cut* Street PT, correctly identifying that the de-rate is already ~40% done (so Hold, not Sell) while naming the load-bearing variable (premium durability on PJM-capacity-at-cap cyclical-peak earnings, gated by FERC EL25-49). It declares one sized downward variance and refuses the premium-permanence framing.

---

## Step 3 — Residual ceiling (why 8.7, not 9.2)

1. **B2/B3 — modeled segment layer (intrinsic).** CEG reports geographic segments by MW capacity and headlines Adjusted Operating EPS, not a segment energy margin — so the GM/SOTP reconciliation uses an S5-tagged energy-margin analog. Honest, but not filing-derived. *No clean fix without disclosure CEG doesn't provide.*
2. **Open-book / hedge-ratio gap.** The bear's central lever — the out-year book's exposure to PJM capacity reverting from the cap — depends on hedge ratios CEG does not disclose at this granularity; the EBITDA sensitivity is modeled (flagged in §12). A 10-Q hedge-disclosure slide would tighten it.
3. **Polish (B8):** could add one line reconciling FY24 GAAP $11.89 (favorable MtM) vs adjusted $8.67 directly in §4 — minor.

**The memo is IC-ready at 8.7 and comfortably clears the 8.5 bar.** No edit changes the Hold call, the +3.0% probability-weighted return, or the two-sided risk; the actionable expression remains the long-VST / short-CEG premium-compression pair and a sub-$200 / new-PPA re-entry.

*Gate logs: `outputs/CEG_verification_gates.json` · Manifest (SHA-verified): `outputs/CEG_manifest.json`. Deliverable PDF: `outputs/CEG_IC_memo.pdf`.*
