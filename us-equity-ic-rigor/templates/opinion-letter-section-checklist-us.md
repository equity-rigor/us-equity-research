# Investment Opinion Letter — 12-Section Rigor Checklist (US)

This is the canonical structure for the **institutional** IC memo (audience variant `institutional_full` per memo.json). Every section is mandatory; if a section is empty, justify why (typically you don't get to skip).

This file is the **WHAT** — the gate-style spec of which sections must appear. The deliverable **SHAPE** (filled-in template with placeholders) lives in `ic-memo-template-us.md` under the research skill's references.

Sections preserve the China §0–§12 numbering. Ported wholesale; US-localized for D1 rating bands, D4 audience set, ASC 606/842/718 forensic items, EDGAR-default sources (D5), and the mandatory quant overlay (D13).

---

## §0 — Cover / metadata

- Ticker + company name + exchange (NYSE / Nasdaq / AMEX)
- Author + mandate type (one of D3 five buckets) + audience variant (per memo.json `audience_variant` enum)
- Date stamp of memo
- Current price (USD) with intraday/EoD date stamp
- Market cap (USD B), 5-day ADV (USD M), beta (basis stated — `5y_monthly_vs_SP500` or `2y_daily_vs_SP500` or `industry_unlevered` or `adjusted_bloomberg`)
- Source data cutoff date (model knowledge cutoff + run-time verification cutoff)
- Fiscal-year-end (MM-DD) since FY ≠ CY for most US issuers

## §1 — Headline (executive summary)

Single page max. Required content:

- 12-month median expected return (single point estimate, %)
- Scenario-weighted return range (low / high, derived from P10 strong_bear and P90 strong_bull)
- Conviction tag (one of `high_conviction` / `moderate_conviction` / `low_conviction` / `source_conditional` / `reactive` per memo.json)
- **Source-conditional flag if any top-3 anchor is S3 or weaker** — explicit English conditional language per source-stratification-us.md
- Default position action by current mandate (e.g. "Initiate long 1.5% of NAV" / "Trim long −50 bps" / "Hold" / "Pair: long NVDA short AVGO at $X spread")
- Re-evaluation triggers (≤ 3 specific dated or numerical events)
- One-sentence core thesis (no jargon; must be repeatable from memory)

## §2 — Source stratification box (gate-style, mandatory)

Top-5 anchors with:
- Anchor name / claim
- S-level (S1 / S2 / S3 / S4 / S5 / Pending per source_tags.json)
- Source citation matching D16 regex `\((S[1-5]|Pending):.+?\)`
- Promotion path (how it graduates to S2 if S3-S5; or "primary anchor, no promotion needed" if S1-S2)
- Falsification path (what specific observable would falsify this anchor)

If top-3 contains any S3 or weaker, §1 headline must carry the conditional flag.

## §3 — Company / industry context

- Business model in one paragraph (≤ 4 sentences; what they sell, to whom, how they make money)
- Segment revenue mix (latest filed period, S1 source preferred; cite the 10-K Item 7 or Note)
- Industry position (market share %, GICS-Level-4 peer set, where the company sits)
- Why this stock is in the universe right now — what catalyst, mispricing, or change-in-view triggered coverage

## §4 — Anchor evidence (per top-anchor deep dive)

For each top-3 anchor:
- What the anchor is (specific quantitative claim, with units and period)
- Source level + full D16 citation
- Why it matters for the thesis (which scenario it loads probability into)
- What would falsify it (specific observable, with denominator)
- How it links to scenario probabilities (e.g. "if confirmed, base case probability shifts from 40% to 50%")

## §5 — Five-scenario valuation core

§5.1 — **5-scenario table** per scenarios.json. Columns: scenario_id (strong_bear / bear / base / bull / strong_bull) × probability × EPS × multiple × multiple_type × target_price × expected_return × anchors_ref × strongest_anchor_s_level

§5.2 — **Anchor weighting impact table** (G10 weighting sensitivity). For each top-3 anchor, show what happens to headline if that anchor's source level shifts up one tier or is falsified. Forces the memo to confront over-anchoring on a single S3.

§5.3 — **EPS path verification** — each scenario's EPS reconciles back to the bear-bridge layered construction per `bear-bridge-us.md`. Cross-reference the bridge step list; sum of `delta_eps` from `base_eps` to scenario `eps` must equal `(base_eps − scenario_eps)` within rounding.

§5.4 — **Headline calculation**: Σ(P × R) = median return; P10 / P90 of the return distribution = scenario-weighted range. Show the arithmetic explicitly.

## §6 — Three-method valuation reconcile

§6.0 — **GM taxonomy box** per `gm-taxonomy-us.md` declaring which of the 5 GM types (T1_consolidated / T2_segment / T3_sub_segment / T4_analyst_modeled / T5_marginal) is used at each layer of the model. Including **non-GAAP vs GAAP** parallel disclosure per B11 (US-specific addition).

§6.1 — **EPS × multiple** (primary; already in §5.1 by scenario). Cross-reference here, do not re-derive.

§6.2 — **SOTP** — segment-by-segment with revenue → GP → OP → NI columns. G3 monotonicity must hold (sum of segment values ≤ consolidated by ≤50bp; cannot exceed by accounting identity). Per-segment multiple_type allowed to differ (e.g. P/E for legacy, EV/Sales for growth segment).

§6.3 — **Multi-multiple bear floor** per `three-method-valuation-us.md`. Sector-branched per D8: P/B for banks; EV/EBITDA for mature industrial; EV/Sales for high-growth pre-profit; FCF yield for capex-heavy mature; AFFO/NAV for REITs; NPV pipeline for biotech. Used as the **strong_bear scenario floor**, not as a weighted average input.

§6.4 — **Reconcile table** — which method primary for which scenario, why. Methods are NOT averaged; they cross-check.

§6.5 — **Bear bridge** per `bear-bridge-us.md`. Three-layer construction (soft / clean / strong). Each named adjustment carries a source tag and delta_eps. Sum verification mandatory.

§6.6 — **Bull bridge** (symmetric to §6.5; same layering discipline).

## §7 — What-would-reverse triggers

Per `what-would-reverse-us.md`. Tiered triggers with:
- Direction (one of `reverse_bear_to_neutral` / `reverse_bear_to_bull` / `reverse_bull_to_neutral` / `reverse_bull_to_bear`)
- Numerical threshold WITH denominator (G9 gate — no handwave; "if X happens" without "vs Y baseline" fails)
- Unit
- Observable via (which specific S-source channel)
- Expected observation date

Both bull→bear and bear→bull triggers required (symmetric).

## §8 — A0 tail risk mapping

Per `tail-risk-mapping-us.md`. 3-5 bear tails + 2-3 bull tails. For each tail:
- Event class (one of the 6 standing per D12 + idiosyncratic: `NBER_recession` / `Fed_rate_shock` / `sector_regulatory_action` / `sanctions_export_control` / `tariff_trade_war` / `election_political_transition` / `FX_shock` / `commodity_shock` / `idiosyncratic`)
- Trigger description (specific observable)
- Probability shift across 5 scenarios — must sum to zero across the five `_delta_pp` fields (G10-related)
- Δ headline post-shift
- Worst- / best-case scenario value (EPS haircut %, multiple compression %, worst-case price %)

## §9 — Position sizing

Per `position-sizing-us.md`. Required content:

- σ (annual stock volatility) + horizon-scaled vol (annual / quarterly / monthly / weekly 1σ)
- E[R] (12-month, from §5.4)
- Sharpe ratio (with R_f = 10Y UST yield, FRED `DGS10`, dated)
- Kelly fraction + conviction multiplier rationale (per D6 — base × 0.10 to 0.50)
- **Specific position by mandate type — all 5 buckets per D3**:
  1. Long-only large-cap (vs S&P 500)
  2. Long-only SMID / all-cap (vs Russell 1000/2000/3000)
  3. L/S hedge fund (gross / net, single-name caps)
  4. Concentrated specialty / sector fund (vs sector ETF)
  5. Pair-trade structure (long / short / structure type / spread return)
- Re-sizing triggers (specific event → position adjustment mapping)

## §10 — Catalyst calendar

Sortable table by date. Columns: date / window / event type (one of `earnings_print` / `investor_day` / `product_launch` / `regulatory_decision` / `M&A` / `capital_return` / `guidance_update` / `macro_event` / `litigation_milestone`) / what you're watching for / expected impact direction + magnitude (% stock move on confirmation, signed) / anchor_ref (which anchor this catalyst would graduate to S2).

Per D10 — pre-announcement risk handling: if a coverage-name pre-announcement is expected, mark with `pre_announce_window` flag.

## §11 — Quant overlay (mandatory per D13)

Per `quant-overlay-us.md`. Mandatory in every institutional memo (NOT opt-in). Required content:

- **Factor tags** — Barra-style z-scores on Value / Quality / Momentum / Growth / Size / Low_Vol / Liquidity (B13 verification hook)
- **Capacity** — 30-day ADV (USD M), days-to-exit at 10% / 20% / 30% participation, max position constrained by ADV (% NAV) (B14 verification hook)
- **Edge decay** — thesis half-life (months), time-to-priced-in (months), refresh cadence (weekly / monthly / quarterly_print / event_driven), primary decay driver
- **Correlation overlay** — placeholder per D14 (book_file_path; `live_wired: false` acceptable for now)
- **Stress overlay** — stock % move under +200bp Fed funds, −20% oil, +5% USD, recession dummy

## §12 — Caveats / appendix

- Anchor verification status (Pending items listed; what would graduate them)
- Cross-section consistency known issues (e.g. FY+1 vs FY+2 EPS treatment if any ambiguity)
- Data gaps + what you'd want to look at if more time
- Verification report summary (link to `outputs/<ticker>_verification_gates.json`; 14-gate pass/fail tally)
- Source URLs (every S1-S2 citation must include EDGAR URL per source_tags.json `url` requirement)
- Comp set analysis (5-10 peers per memo.json `peers` array; GICS-Level-4 by default; cross-listed alternatives noted for ADRs)
- Disclosures (institutional buy-side audience; out of scope for FINRA Rule 2210 retail-comms; standard internal-research disclaimer)

---

## Cross-checks before sign-off

Before claiming the institutional memo is locked, every check below must pass:

1. **All 14 verification gates pass** (G1-G14 per `verification_gates.json`)
2. **PM rubric score ≥ 9.0** per `pm-redteam-rubric-us.md` score bands
3. **EPS year consistent across all tables** — every scenario's `eps_period` matches (FY+1 or FY+2 — pick one and stick with it)
4. **All specific numbers source-tagged at first appearance** per D16 regex `\((S[1-5]|Pending):.+?\)`
5. **Headline conditionality matches strongest-anchor S-level** — if top-3 contains S3 or weaker, §1 carries the conditional flag
6. **GM taxonomy declared + consistent** — §6.0 box matches every GM reference in the memo body; non-GAAP and GAAP both declared per B11
7. **SOTP reconciles + monotonic + sums to consolidated within ±50bp** per G3
8. **Bear bridge layered + sum verified** per G5 — each step has a source tag; sum of deltas equals scenario EPS − base EPS within rounding
9. **What-would-reverse has denominators** per G9 — every directional trigger has `numerical_threshold` AND `unit` AND `observable_via`
10. **A0 prob shifts sum to zero** per G10 — Σ of `_delta_pp` across 5 scenarios = 0 ± 0.01
11. **Position sizing translates to specific action by mandate** — all 5 mandate buckets per D3 have an explicit recommendation, not "consult PM"
12. **Quant overlay block present** per D13 — factor_tags + capacity required; edge_decay + correlation + stress recommended
13. **Non-GAAP / GAAP reconciliation present** per B11 (US-specific addition to G8 family)
14. **FCF definition declared** per B12 — one of `OCF_minus_capex` / `OCF_minus_capex_minus_sbc` / `EBITDA_minus_capex` / `non_standard`; SBC treatment explicit

If any fail, fix at source (the structured JSON conforming to `memo.json`) and rebuild. Do not patch the rendered Markdown without re-running verification.

---

## Audience derivation note

This 12-section structure is the `institutional_full` variant. Other audience variants (per D4 / memo.json `audience_variant` enum) are derived:

- **`ic_preread`** — sections §0 + §1 + §2 + §5.1 + §9 + §10 + §11 (3-4 pages max)
- **`ic_debate_script`** — verbal-form; see `ic-debate-script-template-us.md`
- **`lp_letter`** — quarterly LP-facing; see `lp-letter-template.md`
- **`earnings_prep`** — operational, pre-print; see `earnings-prep-template.md`
- **`earnings_flash`** — operational, T+30min; see `earnings-flash-template.md`
- **`kill_memo`** — exit rationale; falsification-triggered; not in scope of this checklist

Retail and Chinese-language variants are NOT in the US audience set per D4.
