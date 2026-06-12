# VST IC Memo — PM Red-Team, Round 1

**Date:** 2026-06-09 · **Target:** ≥8.5 (D20 default) · **Verdict: PASS — 8.6 / 10** · **Bottleneck: B2/B3 (segment inputs are modeled, not disclosed)**

This is a red-team, not a cheerleader. The memo is **mechanically clean — all 20 gates pass or n/a** — and structurally complete (taxonomy, layered bridges, A0, 5-mandate sizing, three-method reconcile, factor tags, capacity, conditional headline, numerical triggers, honest edge attribution). It clears 8.5. It does **not** reach 9.0 because three things are gate-passing-but-soft: the segment GM/SOTP inputs are analyst constructs chosen to reconcile, the largest forensic table in the whole thesis (the GAAP→Adj-EBITDA hedge wedge) is narrative-only, and the A0 tail catalog is thin.

---

## Step 1 — Mechanical gate sweep (G1–G20)

| Gate | Name | Status | Note |
|---|---|---|---|
| G1 | EPS × multiple multiplicativity | **pass** | 5 scenarios multiply within ±0.5% |
| G2 | Segment GM reconciliation | **pass** | weighted = 28.715% vs 28.72% (0.5bp) — *but see B2* |
| G3 | SOTP monotonicity | **pass** | NI≤OP≤GP≤Rev holds all 4 segments — *but see B3* |
| G4 | Scenario probabilities = 1.00 | **pass** | 0.10/0.22/0.38/0.22/0.08 |
| G5 | Bear/bull EPS bridge reconciles | **pass** | all bridges sum to base±step exactly |
| G6 | Source tag at first use | **pass** | v0.3.0 strict mode, all categories |
| G7 | Headline conditionality | **pass** | source-conditional; matches anchor mix |
| G8 | GM taxonomy box | **pass** | T1–T5 with IPP energy-margin adaptation |
| G9 | What-would-reverse numerical | **pass** | 7 triggers w/ denominators |
| G10 | Anchor weighting impact table | **pass** | weighting_sensitivity present |
| G11 | Non-GAAP→GAAP reconciliation | **pass** | flag present — *but no explicit table; see B11* |
| G12 | SBC treatment in FCF | **pass** | OCF−capex; SBC immaterial, flagged |
| G13 | Barra factor exposure | **pass** | 7 factors w/ z-scores |
| G14 | Capacity / ADV / days-to-exit | **pass** | ADV $793M; 10/20/30% participation |
| G15 | Consensus variance | **n/a** | rating=Hold → consensus-anchored valid (1 load-bearing downward variance also declared) |
| G16 | Bank metrics | **n/a** | non-bank |
| G17 | Revision velocity | **pass** | n=17; FY1 EPS +4.3% 3m; breadth +0.3 |
| G18 | Quant cross-doc consistency | **pass** | — |
| G19 | Provenance manifest | **pass** | SHA-256 verified; ≥12 calls, ≥15 agents |
| G20 | View defensibility | **n/a** | Hold is not a non-consensus *rating* (but see B8 note — base PT is 33% below Street) |

**Zero gate failures.** Mechanical floor cleared → memo is ≥7.5 by construction; structures present → ≥8.5.

---

## Step 2 — Rubric scorecard (B1–B14)

| Bug | Dimension | Score | Comment |
|---|---|---:|---|
| B1 | EPS × multiple | 9.5 | Exact; prices are outputs of EPS×P/E |
| **B2** | **Segment GM reconcile** | **7.0** | **Passes G2, but all 4 LTM segment GM inputs are S5-modeled.** VST discloses segment *Adjusted EBITDA*, not GM; the revenue/GM splits were constructed to reconcile. Arithmetically honest (labeled S5) but not sourced. |
| **B3** | **SOTP monotonicity** | **7.5** | **Passes G3, but segment GP/OP/NI are modeled-to-be-monotonic**, not built bottom-up from disclosed segment P&L (which VST doesn't publish at GP/OP/NI granularity). Directionally fine; not filing-derived. |
| B4 | GM taxonomy box | 9.0 | T1–T5 present; IPP adaptation explicitly labeled (good) |
| B5 | Headline conditionality | 9.0 | Source-conditional with if/then triggers; matches anchors |
| B6 | Bear EPS bridge | 9.0 | Soft/clean/strong layers; reconcile exactly |
| B7 | What-would-reverse | 9.5 | 7 triggers, all numerical (<$250/MW-day, <$7.0B, >$2.8B/6mo…) |
| B8 | Cross-version consistency | 8.0 | Net debt cited $16.4B (FY25) and $19.3B (Q1'26/comps) — both contextualized but **basis not explicitly reconciled in one place**; base PT $153 sits **33% below sell-side median $230** with no sentence owning that gap |
| **B9** | **A0 tail map** | **7.5** | Shifts conserve to zero (✓) and a bull tail is present (✓), but **only 4 tails** — the D12 standing catalog wants ~6 standing macro tails (Fed +200bp, NBER recession, broad risk-off) + idiosyncratic + bull. Catalog is thin |
| B10 | Position sizing | 9.0 | 5 mandates + Kelly + pair-trade hedge ratio |
| **B11** | **Non-GAAP/GAAP reconcile** | **7.5** | Flag present (G11 ✓) and the hedge-MTM driver is explained in prose, **but there is no explicit line-item GAAP-NI → Adj-EBITDA bridge table** — and for this name the wedge is the entire earnings-quality story (Adj EBITDA = 6.3× GAAP NI; delta 300% of NI). The single most important table is narrative-only |
| B12 | SBC in FCF | 9.0 | Defined OCF−capex; SBC immaterial, flagged; offset ratio shown |
| B13 | Factor exposure | 9.0 | 7 Barra tags + rationale |
| B14 | Capacity / ADV | 9.0 | Days-to-exit at 10/20/30% participation |

**Weighted overall: 8.6/10.** Band: **8.5–9.0 (IC-grade hardness).** Three soft spots (B2, B3, B11) cluster at ~7.5 and define the ceiling; B9 is the next.

**What's genuinely good (not flattery — these are the things PMs usually kill memos for, and they're handled):** the memo *refuses to manufacture edge*. It declares exactly one load-bearing variance (2028 open-book, downward, ~60%, S1/gov-evidenced), labels everything else consensus-anchored, and lands Hold honestly at +2.6%. It also takes a real *non-consensus PT* (base $153 vs Street $230) and defends it three ways (DCF $107, private-market 7.5×, the de-rate thesis). That is the opposite of consensus reproduction.

---

## Step 3 — Push from 8.6 → 9.0 (ordered by score-gain-per-effort)

> Per the rubric, I do **not** modify the original memo — these are the edits for you to approve. Each cites the file + section and a before/after.

### Fix 1 (highest gain) — B2/B3: replace modeled segment inputs with disclosed segment Adjusted EBITDA
**Why:** A sharp PM will catch that G2/G3 pass on fabricated-to-reconcile inputs. VST *does* disclose segment Adjusted EBITDA (FY25: East $2,282M, Texas $1,834M, Retail $1,622M, West $244M, Corp/Asset-Closure negative). Reframe the GM taxonomy + G2 reconciliation on **Adjusted-EBITDA margin** (the IPP analog, exactly as banks use NIM per D24), tag S1/S2, and add an explicit **"Corporate / Asset Closure" reconciling row** so Σsegment → consolidated ties to *reported* numbers, not constructed ones.
- **File:** `VST_structured.json` → `financials.ltm.segments` (swap `gm_pct` S5 constructs for disclosed segment Adj-EBITDA-margin, S1) + `valuation.methods[SOTP].key_assumptions` (drive segment value off disclosed segment EBITDA × multiple, keep monotonic chain) + `gm_taxonomy.entries` (relabel T1/T2 as Adj-EBITDA-margin analog).
- **Re-verify:** `verify_segment_gm.py`, `verify_sotp_monotonicity.py`. **Score impact: B2 7.0→9.0, B3 7.5→9.0.**

### Fix 2 (low effort, high gain) — B11: add the explicit GAAP→Adj-EBITDA bridge table
**Why:** The hedge-MTM wedge IS the thesis on earnings quality; it deserves a table, not a sentence.
- **File:** `VST_IC_memo.md` §4, immediately after the financials table. Add:
  > GAAP NI $944M **+** unrealized hedge MTM $808M **+** transition/merger & non-cash comp **−** nuclear decommissioning trust income **−** other = **Ongoing Adj EBITDA $5,912M** (S2: VST FY25 8-K Reg-G reconciliation). Delta = 300% of GAAP NI (5y avg) — flagged per forensic_flags.
- **Re-verify:** `verify_non_gaap.py` (already passes; this strengthens B11). **Score impact: B11 7.5→9.0.**

### Fix 3 (low-medium effort) — B9: complete the A0 standing-tail catalog
**Why:** Only 4 tails; D12 wants the full standing set so the PM sees correlated-book risk.
- **File:** `VST_structured.json` → `tail_risks`. Add 2 standing macro tails — **Fed +200bp** and **NBER recession / broad risk-off** (both bear, high-beta name) — each with shifts conserving to zero. Keep the 3 existing bear + 1 bull.
- **Re-verify:** `verify_weighting_sensitivity.py` / G10. **Score impact: B9 7.5→8.8.**

### Fix 4 (trivial, polish) — B8: own the two number bases
- **File:** `VST_IC_memo.md` §3/§4. Add one line: *"Net debt $16.4B at FY25 year-end vs $19.3B at Q1'26 (Cogentrix pre-funding); the comps EV bridge uses the current $19.3B."* And in §1/§2 add: *"Our base PT $153 is ~33% below the sell-side median $230 — the Hold reflects +2.6% to **our** lower target; we are fading the Street's +50% upside, not endorsing it."*
- **Score impact: B8 8.0→9.0.**

**Projected post-fix score: ~9.0.** Fixes 1+2 alone (the two that matter) lift the bottleneck cluster and would put the memo at ~8.9.

---

## Honest bottom line
The memo is **IC-defensible today at 8.6** — it would survive an IC discussion. Its real intellectual strength is discipline: it doesn't fake edge, it takes a defensible below-Street PT, and it's transparent about what's modeled (everything S5-tagged). Its real weakness is that an IPP forces segment-level *constructs* to satisfy G2/G3 (gates designed for industrials with disclosed GM), and the one table that would most reward the reader — the hedge-MTM bridge — is prose. Fix those two and it's a 9.0. **No fix changes the Hold call; the +2.6% expected return and the two-sided risk are robust to all four edits.**

*Gate logs: `outputs/VST_verification_gates.json` · Manifest (SHA-verified): `outputs/VST_manifest.json`. Round 1 of N; original memo unmodified per red-team protocol.*
