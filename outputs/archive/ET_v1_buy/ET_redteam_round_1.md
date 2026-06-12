# ET IC Memo — PM Red-Team, Round 1

**Date:** 2026-06-09 · **Target:** ≥8.5 (D20 default) · **Verdict: PASS — 8.6 / 10** · **Bottleneck: B2/B3 (segment inputs modeled, not disclosed) + B11 (no explicit GAAP→Adj-EBITDA / DCF bridge table)**

This is a red-team, not a cheerleader. The memo is **mechanically clean — all 20 gates pass or n/a** — and structurally complete (S1–S5 stratification, five-scenario block with reconciling DCF/unit bridges, three-method valuation, GM taxonomy, A0 tails, 5-mandate sizing, factor tags, capacity, conditional headline, numerical triggers, honest edge attribution). It clears 8.5 comfortably and is the **stronger archetype than a consensus-anchored Hold**: it carries a *genuine, differentiated, S1-evidenced* non-consensus view (Buy at a PT **10.75pp below** the Street) that **survived an adversarial R-v2 attack** (G20 affirmatively passes, not n/a). It does **not** reach 9.0 because three things are gate-passing-but-soft: the segment cash-margin/SOTP inputs are analyst constructs chosen to reconcile, the earnings-quality bridge (GAAP NI → Adj EBITDA → DCF) is narrative-only, and the A0 tail catalog carries 4 of the ~6 D12 standing macro tails.

---

## Step 1 — Mechanical gate sweep (G1–G20)

| Gate | Name | Status | Note |
|---|---|---|---|
| G1 | EPS × multiple multiplicativity | **pass** | 5 scenarios (DCF/unit × P/DCF) multiply within ±0.5% |
| G2 | Segment GM reconciliation | **pass** | weighted = 18.00% vs consolidated 18.0% (0bp) — *but see B2* |
| G3 | SOTP monotonicity | **pass** | NI≤OP≤GP≤Rev holds all 5 segments — *but see B3* |
| G4 | Scenario probabilities = 1.00 | **pass** | 0.08/0.20/0.37/0.27/0.08 |
| G5 | Bear/bull bridge reconciles | **pass** | all DCF/unit bridges sum to base $2.86 ± step exactly |
| G6 | Source tag at first use | **pass** | v0.3.0 strict mode — all 6 categories (incl. capacity MMcf/d, beta) |
| G7 | Headline conditionality | **pass** | top-3 anchors S1/S1/S2 (strong); source-conditional consistent across layers |
| G8 | GM taxonomy box | **pass** | T1–T5 with midstream cash-margin adaptation |
| G9 | What-would-reverse numerical | **pass** | 7 triggers w/ denominators (<4.0x, >$18.6B, <1.5x, <$55/bbl…) |
| G10 | Anchor weighting impact table | **pass** | weighting_sensitivity present (±10pp shifts) |
| G11 | Non-GAAP→GAAP reconciliation | **pass** | flag present + "bridges to GAAP" prose — *but no explicit table; see B11* |
| G12 | SBC treatment in FCF | **pass** | OCF−capex; SBC immaterial (~0.15% rev), not added back |
| G13 | Barra factor exposure | **pass** | 7 factors w/ z-scores (Value +1.4 lead) |
| G14 | Capacity / ADV / days-to-exit | **pass** | ADV $320M; 10/20/30% participation 3.1/1.6/1.0d |
| **G15** | **Consensus variance** | **pass** | **rating=Buy; 1 load-bearing downward MULTIPLE variance, sizing 2.11pp (=18×65×18/10000), S1/S2 evidence, recompute-consistent** |
| G16 | Bank metrics | **n/a** | non-bank (Energy / midstream MLP) |
| G17 | Revision velocity | **pass** | n=22; FY1 EBITDA +4.3% 3m (guidance raise); breadth +0.4 |
| G18 | Quant cross-doc consistency | **pass** | 7 MD factor refs match structured within ±0.2 |
| G19 | Provenance manifest | **pass** | SHA-256 verified (4 files); 20 web calls; 15 agents |
| **G20** | **View defensibility** | **pass** | **diff 10.75pp (headline +12.54% vs consensus PT-implied +23.29%); S1/S2 evidence on V1; surviving variance_attack (base_rate_sanity → modified); graduated 9.0+ n/a on schema 0.3.0** |

**Zero gate failures.** Mechanical floor → ≥7.5 by construction; structures present → ≥8.5; **G15 + G20 passing affirmatively (not n/a) → the view is defensible, not just complete.**

---

## Step 2 — Rubric scorecard (B1–B17)

| Bug | Dimension | Score | Comment |
|---|---|---:|---|
| B1 | EPS × multiple | 9.5 | Exact; prices are outputs of DCF/unit × P/DCF |
| **B2** | **Segment GM reconcile** | **7.0** | **Passes G2, but all 4 LTM segment cash-margin inputs are S5-modeled.** ET discloses segment *Adjusted EBITDA*, not GM; revenue/margin splits were constructed to reconcile to 18.0%. Arithmetically honest (S5-labeled) but not filing-derived. |
| **B3** | **SOTP monotonicity** | **7.5** | **Passes G3, but segment GP/OP/NI are modeled-to-be-monotonic**, not built from disclosed segment P&L (ET doesn't publish GP/OP/NI per segment). Directionally fine; not bottom-up. |
| B4 | GM taxonomy box | 9.0 | T1–T5; fee-based-vs-commodity sub-segment split is the right midstream adaptation |
| B5 | Headline conditionality | 9.0 | Source-conditional with explicit upgrade/downgrade triggers; matches strong anchor mix |
| B6 | Bear/bull bridge | 9.0 | Soft/clean/strong layers; reconcile to $2.86 base exactly |
| B7 | What-would-reverse | 9.5 | 7 triggers, all numerical and observable (10-Q leverage, 8-K, NYMEX curves) |
| **B8** | **Cross-version consistency** | **8.5** | Net debt $69.0B (DCF/comps) vs LT debt $69,317M (S1 10-Q) vs ~$70.2B (aggregator net) — **each contextualized**, and the memo explicitly owns the below-Street gap (−10.75pp, §1/§6). Minor: the three debt bases could be reconciled in one footnote. |
| **B9** | **A0 tail map** | **7.5** | Shifts conserve to zero (✓), bull tail present (✓), but **4 tails** — D12 wants ~6 standing (has commodity_shock, Fed_rate_shock, sector_regulatory; **missing NBER recession as a discrete tail and a broad risk-off/credit-spread tail**). |
| B10 | Position sizing | 9.0 | 5 mandates + Kelly + long-ET/short-EPD pair w/ beta ratio + K-1/UBTI caveat |
| **B11** | **Non-GAAP/GAAP reconcile** | **7.5** | Flag present (G11 ✓), "bridges to GAAP" + 260%-delta prose, **but no explicit line-item GAAP NI → Adj EBITDA → DCF table.** For an MLP where Adj EBITDA and DCF *are* the underwriting basis, the single most useful reconciliation is narrative-only. |
| B12 | SBC in FCF | 9.0 | OCF−capex; SBC ~0.15% rev, not added back, flagged |
| B13 | Factor exposure | 9.0 | 7 Barra tags + rationale; Value/Size lead is correct for the name |
| B14 | Capacity / ADV | 9.0 | Days-to-exit at 10/20/30%; ADV $320M (note: MLP ADV is modest — correctly flagged) |
| **B15** | **Consensus variance quality** | **8.7** | **The strength of the memo.** One load-bearing variance, *downward on the multiple while estimates rise* (a genuinely non-obvious split), S1-evidenced (4.4x leverage at top of target), sized (2.11pp), two-tailed and honest about it. Not consensus reproduction. |
| **B16** | **View defensibility (G20)** | **8.7** | The variance **survived an R-v2 base_rate_sanity attack** (midstream re-rate precedent) → *modified* (lifted base multiple 7.2x→7.5x, trimmed sizing) rather than rubber-stamped. Documented in `adjudication_trail`. Differentiation 10.75pp. |
| B17 | Revision velocity | 9.0 | n=22; guidance-raise quantified; estimate-up-but-multiple-is-the-edge correctly separated |

**Weighted overall: 8.6/10.** Band: **8.5–9.0 (IC-grade hardness).** The B15/B16 strength (a real, attacked-and-survived non-consensus view) offsets the B2/B3/B11 soft cluster; B9 is the next ceiling.

**What's genuinely good (the things PMs kill memos for, handled):** (1) the memo **separates the multiple call from the estimate call** — it is *bearish vs Street on the re-rate while acknowledging estimates are rising on a guidance raise*, which is the kind of split-view that demonstrates the analyst actually read the print rather than the tape; (2) it takes a **falsifiable below-Street PT** ($21.45 vs $23.5) and defends it three ways (comps 7.25x, DCF $20.50, SOTP $21.00) rather than hugging consensus; (3) it is **honest about the MLP machinery** — GAAP EPS declared non-informative, the per-unit metric explicitly relabeled DCF/unit not EPS, the net-leverage ratio flagged as calculated-not-reported, and the DAPL award correctly framed as an *asset* (ET is plaintiff), a detail a lazy memo gets backwards.

---

## Step 3 — Push from 8.6 → 9.0 (ordered by score-gain-per-effort)

> Per red-team protocol, the original memo is **not** modified — these are edits for you to approve. Each cites file + section. NB: applying Fixes 1–3 changes `ET_structured.json` / `ET_IC_memo.md`, so the provenance manifest must be **regenerated** (`write_manifest.py`) afterward or G19's SHA-256 check will fail.

### Fix 1 (highest gain) — B2/B3: replace modeled segment inputs with disclosed segment Adjusted EBITDA
**Why:** A sharp PM will catch that G2/G3 pass on constructed-to-reconcile inputs. ET *discloses* segment Adjusted EBITDA (FY25 ≈ NGL & Refined ~$4.2B, Midstream/Crude/Inter/Intra per Q4 splits, plus SUN/USAC). Reframe the GM taxonomy + G2 reconciliation on **Adjusted-EBITDA margin** (the midstream analog, as banks use NIM per D24) with an explicit reconciling "All Other / intersegment" row so Σsegment ties to *reported* consolidated Adj EBITDA, and drive SOTP off **disclosed segment Adj EBITDA × multiple**.
- **File:** `ET_structured.json` → `financials.ltm.segments`, `valuation.methods[SOTP].key_assumptions`, `gm_taxonomy.entries`. **Re-verify:** `verify_segment_gm.py`, `verify_sotp_monotonicity.py`. **Score: B2 7.0→9.0, B3 7.5→9.0.**
- **Data gap to close first:** the Phase-0 research flagged FY25 full-year segment Adj EBITDA for Midstream/Crude/Inter/Intra/SUN/USAC as *partially unverified* (only Q4 splits + NGL full-year confirmed; the rest sit in the Archives-hosted 10-K Item 7 segment table). Pull that table before swapping S5→S1.

### Fix 2 (low effort, high gain) — B11: add the explicit GAAP → Adj EBITDA → DCF bridge table
**Why:** For an MLP the Adj-EBITDA/DCF wedge IS the earnings-quality story; it deserves a table.
- **File:** `ET_IC_memo.md` §4, after the financials table:
  > GAAP NI to partners $4,433M **+** D&A **+** interest **+** non-cash items **±** unrealized derivatives **+** NCI add-back = **Adjusted EBITDA ~$16,000M**; less cash interest, maintenance capex, preferred = **DCF to partners $8,200M** (S2: ET FY25 8-K Reg-G reconciliation). **Re-verify:** `verify_non_gaap.py`. **Score: B11 7.5→9.0.**

### Fix 3 (low-medium) — B9: complete the A0 standing-tail catalog
**Why:** 4 tails; D12 wants the full standing set for a 4.4x-levered, 7.1%-yield name.
- **File:** `ET_structured.json` → `tail_risks`: add **NBER recession** (discrete, energy-volume + credit-spread) and a **broad risk-off / HY-credit-spread blowout** tail (this name is rate- and spread-sensitive), shifts conserving to zero. **Score: B9 7.5→8.8.**

### Fix 4 (trivial polish) — B8: one debt-basis footnote
- **File:** `ET_IC_memo.md` §3/§4: *"Debt bases: LT debt $69,317M (S1: Q1'26 10-Q); net debt ~$70.2B incl. current maturities less cash; the DCF/comps EV bridge uses ~$69.0B net."* **Score: B8 8.5→9.0.**

**Projected post-fix score: ~9.0.** Fixes 1+2 (the two that matter) lift the bottleneck cluster to ~8.9. **No fix changes the Buy call or the +15.4% expected price return** — the below-Street differentiation and the surviving variance are robust to all four edits.

---

## Honest bottom line
The memo is **IC-defensible today at 8.6** and would survive an IC discussion. Its real strength is the thing the 20-gate framework was built to reward but rarely sees: a *defensible non-consensus view that was attacked and survived* (G20 affirmative), with the edge correctly located on the **multiple** while estimates rise — not a repackaged Strong-Buy consensus. Its real weakness is shared with every non-industrial in this framework: a midstream MLP forces segment-level *constructs* to satisfy G2/G3 (gates built for disclosed-GM industrials), and the one table that would most reward the reader — the GAAP→Adj-EBITDA→DCF bridge — is prose. Close the disclosed-segment gap and add the bridge table and it is a 9.0. **Target ≥8.5 achieved: 8.6.**

*Gate logs: `outputs/ET_verification_gates.json` · Manifest (SHA-verified): `outputs/ET_manifest.json`. Round 1 of N; original memo unmodified per red-team protocol.*
