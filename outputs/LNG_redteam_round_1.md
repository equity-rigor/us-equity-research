# LNG (Cheniere) IC Memo — PM Red-Team, Round 1

**Date:** 2026-06-09 · **Target:** ≥8.5 (D20 default) · **Verdict: PASS — 8.6 / 10** · **Bottleneck: B2/B3 (segment inputs modeled) + B11 (GAAP→Adj-EBITDA bridge is prose)**

This is a red-team, not a cheerleader. The memo is **mechanically clean — all 19 applicable gates pass; G15/G16/G20 n_a** — and structurally complete (T1–T5 taxonomy, layered bear/bull bridges, A0 tail map with zero-sum shifts, 5-mandate sizing, three-method reconcile, 7 Barra factor tags, capacity/ADV, source-conditional headline, 7 numerically-denominated triggers, honest below-Street edge). It clears 8.5. It does **not** reach 9.0 because three things are gate-passing-but-soft: the segment GM/SOTP inputs are analyst constructs (Cheniere discloses neither segment GM nor segment GP/OP/NI), the earnings-quality story (GAAP→Adj-EBITDA hedge wedge) is narrative-only, and the A0 standing catalog is thin (4 tails vs the ~6 D12 wants).

---

## Step 1 — Mechanical gate sweep (G1–G20)

| Gate | Name | Status | Note |
|---|---|---|---|
| G1 | EPS × multiple multiplicativity | **pass** | 5 scenarios multiply within ±0.5% (17.00×8.5=144.00 … 22.00×17.0=374.00) |
| G2 | Segment GM reconciliation | **pass** | weighted 35.206% vs 35.21% (<1bp) — *but see B2* |
| G3 | SOTP monotonicity | **pass** | NI≤OP≤GP≤Rev holds all 3 segments — *but see B3* |
| G4 | Scenario probabilities = 1.00 | **pass** | 0.10/0.22/0.38/0.22/0.08 |
| G5 | Bear/bull EPS bridge reconciles | **pass** | strong_bear −2.51, bear −1.01, bull +0.99, strong_bull +2.49 — all exact |
| G6 | Source tag at first use | **pass** | v0.3.0 strict; revenue/ADV/beta/share categories all tagged |
| G7 | Headline conditionality | **pass** | source_conditional; top-3 anchors include S3 guides → conditional required & present |
| G8 | GM taxonomy box | **pass** | T1–T5 with LNG energy-margin adaptation |
| G9 | What-would-reverse numerical | **pass** | 7 triggers w/ denominators (JKM<$5/3Q, EBITDA<$7.0B, fee≤$2.00…) |
| G10 | Anchor weighting impact table | **pass** | weighting_sensitivity present |
| G11 | Non-GAAP→GAAP reconciliation | **pass** | flag present + parallel marker — *but no explicit bridge table; see B11* |
| G12 | SBC treatment in FCF | **pass** | OCF−capex; SBC ~0.8% rev, flagged immaterial |
| G13 | Barra factor exposure | **pass** | 7 factors w/ z-scores |
| G14 | Capacity / ADV / days-to-exit | **pass** | ADV $470M; 10/20/30% = 2.7/1.3/0.9 days |
| G15 | Consensus variance | **n/a** | rating=Hold (1 load-bearing downward variance declared anyway) |
| G16 | Bank metrics | **n/a** | non-bank (Energy/LNG) |
| G17 | Revision velocity | **pass** | n=23; FY1 EPS +4.0% 3m; breadth +0.4; guidance raised |
| G18 | Quant cross-doc consistency | **pass** | MD factor z-scores match JSON within ±0.2 |
| G19 | Provenance manifest | **pass** | SHA-256 verified; 16 web calls, 15 agents, 20 outputs hashed |
| G20 | View defensibility | **n/a** | Hold (base PT $253.63 is ~16% below Street median $304.50) |

**Zero gate failures.** Mechanical floor cleared → ≥7.5 by construction; structures present → ≥8.5.

---

## Step 2 — Rubric scorecard (B1–B14)

| Bug | Dimension | Score | Comment |
|---|---|---:|---|
| B1 | EPS × multiple | 9.5 | Exact; prices are outputs of EPS×P/E, not reverse-engineered |
| **B2** | **Segment GM reconcile** | **7.0** | **Passes G2, but all 3 LTM segment margins are S5-modeled.** Cheniere discloses neither segment GM nor a clean GAAP segment P&L; splits constructed to reconcile to a modeled consolidated. Arithmetically honest (labeled S5) but not filing-sourced. |
| **B3** | **SOTP monotonicity** | **7.5** | **Passes G3, but segment GP/OP/NI are modeled-to-be-monotonic**, not built from disclosed segment P&L. Directionally fine; not 10-K-derived. |
| B4 | GM taxonomy box | 9.0 | T1–T5; LNG/energy-margin adaptation explicitly labeled |
| B5 | Headline conditionality | 9.0 | Source-conditional with if/then triggers; matches the S3-guide anchors |
| B6 | Bear EPS bridge | 9.0 | Soft/clean/strong layers; reconcile exactly both tails |
| B7 | What-would-reverse | 9.5 | 7 triggers, all numerical, each with an observable (JKM curve, guide, 8-K fee) |
| B8 | Cross-version consistency | 8.5 | Net debt $21.7B (consolidated) vs $26.5B (EV-implied incl CQP NCI) **explicitly reconciled** in §12 + metadata; base PT $253.63 vs Street $304.50 owned in §6/§9. Good discipline. |
| **B9** | **A0 tail map** | **7.5** | Shifts conserve to zero (✓), bull tail present (✓), but **only 4 tails** — D12 wants ~6 standing (recession ✓, Fed ✓, glut ✓ + a regulatory/policy standing tail and a sanctions/tariff line are thin/absent). |
| B10 | Position sizing | 9.0 | 5 mandates + Kelly + long-VG/short-LNG pair w/ beta hedge |
| **B11** | **Non-GAAP/GAAP reconcile** | **7.5** | Flag + parallel marker present (G11 ✓), hedge-MtM driver explained in prose, **but no explicit line-item GAAP-NI → Consolidated-Adj-EBITDA → DCF bridge table** — and for this name that wedge (Q1'26 −$3.5B GAAP vs +$2.3B EBITDA) is the entire earnings-quality story. |
| B12 | SBC in FCF | 9.0 | OCF−capex defined; SBC ~0.8% rev flagged immaterial |
| B13 | Factor exposure | 9.0 | 7 Barra tags + rationale (Quality/Size/Growth tilt) |
| B14 | Capacity / ADV | 9.0 | Days-to-exit at 10/20/30% participation; highly liquid |

**Weighted overall: 8.6/10.** Band: **8.5–9.0 (IC-grade hardness).** B2/B3/B11 cluster at ~7.5 and define the ceiling; B9 is next.

**What's genuinely good (the things PMs usually kill memos for, handled here):** the memo *refuses to manufacture edge*. It declares exactly one load-bearing variance (FY2027 EBITDA durability + multiple, downward, ~58%, S1/S3-evidenced), labels it two-tailed, and lands **Hold at +4.9% against a +27% Street** — a real below-consensus PT ($253.63 vs $304.50) defended three ways (comps 10.2x, DCF $225, midstream-band bear floor). That is the opposite of consensus reproduction, and it correctly identifies the load-bearing assumption (multiple durability into the supply wave, not near-term estimates — which are *rising*).

---

## Step 3 — Push from 8.6 → ~9.0 (ordered by score-gain-per-effort)

### Fix 1 (low effort, high gain) — B11: add the explicit GAAP → Adj-EBITDA → DCF bridge table
**Why:** the ASC 815 hedge wedge IS the earnings-quality thesis; it deserves a table, not a sentence. **File:** `LNG_IC_memo.md` §4. Add a Reg-G-style bridge (GAAP NI + unrealized derivative MtM + D&A + interest + tax → Consolidated Adj EBITDA; less maintenance capex/interest/taxes/distributions-to-NCI → DCF). **Re-verify:** `verify_non_gaap.py`. **Impact: B11 7.5→9.0.**

### Fix 2 (low-medium) — B9: complete the A0 standing-tail catalog
**Why:** only 4 tails. **File:** `LNG_structured.json` → `tail_risks`. Add 2 standing tails — a **DOE/FERC export-policy reversal** (regulatory) and a **tariff/trade-war gas-demand** line — shifts conserving to zero. **Re-verify:** G10. **Impact: B9 7.5→8.8.**

### Fix 3 (medium) — B2/B3: relabel the segment basis as the Consolidated-Adj-EBITDA-margin analog (the LNG equivalent of banks' NIM per D24)
**Why:** make explicit that, like an IPP/bank, Cheniere's "segment margin" is an EBITDA-margin analog, not a GAAP GM — and tie the SOTP to disclosed segment/platform economics where possible. Keeps S5 labeling honest but removes the "fabricated to reconcile" smell. **Re-verify:** `verify_segment_gm.py`, `verify_sotp_monotonicity.py`. **Impact: B2 7.0→8.0, B3 7.5→8.3.**

**Projected post-fix score: ~8.9–9.0.** No fix changes the Hold call, the +4.9% expected return, or the two-sided risk.

---

## Honest bottom line
The memo is **IC-defensible today at 8.6** — it would survive an IC discussion. Its real strength is discipline: it doesn't fake edge, takes a defensible ~16%-below-Street PT, correctly names the load-bearing variable (multiple durability into the biggest LNG supply wave in history, *not* estimates), and is transparent about what's modeled (everything S5-tagged, net-debt bases reconciled). Its real weakness is intrinsic to the name: a pure-play LNG exporter forces segment-level *constructs* to satisfy gates designed for disclosed-GM industrials, and the one table that would most reward the reader — the GAAP→Adj-EBITDA→DCF bridge — is prose. Fixes 1–3 push it to ~9.0.

*Gate logs: `outputs/LNG_verification_gates.json` · Manifest (SHA-verified): `outputs/LNG_manifest.json`. Round 1 of N.*
