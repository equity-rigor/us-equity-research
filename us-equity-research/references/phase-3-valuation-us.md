# Phase 3: Valuation + Final Synthesis (US)

Phase 3 dispatches four agents in parallel. This is where the analytical framework from Phase 1 (`phase-1-deep-dive-us.md`) + Phase 2 (`phase-2-continuation-us.md`) converts into a sized recommendation. Phase 3 ends with the IC Memo, which then runs through mandatory verification (`verification-protocol-us.md`) before delivery.

Four specialists: A7 (valuation + quant overlay — most important), Mirror (full analysis on top peer if pair-trade), [Topic]-Forensic (specific risk deep-dive), R-v2 (refreshed Red Team).

Each agent receives the Phase 1 Integrated Brief, Phase 2 Integrated Brief (v3), all workpapers, Phase 0 mandate / horizon / sector / hypothesis tree.

---

## A7 — Valuation + Quant Overlay

**THE MOST IMPORTANT PHASE 3 AGENT.** A7 produces: DCF; peer-multiple valuation; SOTP (if multi-segment); the 5-scenario probabilistic framework with each scenario carrying its own EPS path + multiple + bridge; the mandatory quant overlay (Barra factors, capacity, edge decay, correlation placeholder, stress); position sizing across 5 mandate types. Reconcile per `three-method-valuation-us.md`. WACC build per `valuation-discipline-us.md`. Sector-default primary multiple per D8. Scenarios per `five-scenario-framework-us.md` + `schemas/scenarios.json`. Quant overlay mandatory per D13.

**Prompt template**:

```
You are the Valuation specialist analyzing [COMPANY] ([TICKER]). Today is
[DATE]. WebSearch + WebFetch (20+ calls) to verify peer multiples, R_f, ERP,
beta, sector multiple, current consensus.

KEY INPUTS FROM PHASES 1 + 2 (use these — do not re-derive):
[Insert summary stats from Phase 2 Integrated Brief]
- 5y P&L + LTM + Phase 2 fresh quarter
- Segment revenue + GM trajectory
- Capex schedule next 2-3y
- ETR trajectory
- SBC % trend
- Non-GAAP / GAAP delta history
- FCF definition (whether company excludes SBC)
- Phase 2 Red Team v1 bear PT
- Phase 2 A3-Peers peer set with multiples

## 1. WACC DERIVATION

Full build discipline in `valuation-discipline-us.md`. Required inputs for
this name with citations:
- R_f from FRED DGS10 (cite date + value).
- ERP from Damodaran implied US (cite date + value).
- Beta basis stated (5y_monthly_vs_SP500 / 2y_daily / industry_unlevered /
  adjusted_bloomberg).
- After-tax cost of debt = pre-tax × (1 − ETR); pre-tax from FRED BAMLC0A0CM
  (IG OAS) or BAMLH0A0HYM2 (HY OAS) for company's rating tier.
- Capital structure at MARKET value; equity_weight + debt_weight = 1.00.
- Compute WACC; sanity-check against typical bands per `valuation-discipline-
  us.md`.

## 2. NORMALIZED 5-YEAR FORWARD MODEL

For each FY+1 through FY+5:
- Revenue by segment (using A4's revenue_by_product + revenue_by_geography)
- Operating margin trajectory
- D&A schedule from A4 depreciation waterfall
- SG&A and R&D (with §174 capitalization cash-tax impact)
- Specific drag items (litigation reserves draw-down, restructuring tail
  charges, contingent payments)
- ETR
- GAAP NI
- Diluted share count (SBC dilution + buyback offset)
- GAAP EPS
- Non-GAAP EPS with explicit reconciliation
- FCF (OCF − capex deducting SBC — buy-side standard, NOT company's
  idiosyncratic definition; document difference)

Structure: high-growth → 3y explicit + 7y fade. Cyclicals → 10y normalized.
Mature → 5y explicit + terminal. State choice + rationale.

## 3. DCF VALUATION

Base case:
- FCF year-by-year for forecast horizon
- Terminal year normalized (mid-cycle multiple or Gordon-growth)
- Terminal growth 2.0-2.5% (US long-run nominal GDP)
- Discount at WACC
- Bridge: + cash + ST investments − total debt − pension underfunding −
  identified contingent obligations − terminal tail-risk haircut
- Per-share IV

Cross-check terminal value with exit-multiple approach (sector-default exit
multiple per D8).

## 4. PEER MULTIPLES

Using A3-Peers peer set, apply the sector-default primary multiple per D8 +
`valuation-discipline-us.md` (full sector table there). Derive implied IV.
Document premium / discount vs peer median. Normalize for capex intensity,
SBC %, leverage, regulatory exposure. Pull historical multiple percentiles
5/25/50/75/95 over 5-10y from YCharts / Macrotrends.

## 5. SOTP (if multi-segment)

Per-segment revenue + GM (from A4 build) × segment-appropriate multiple.
Sum segment EVs; + cash, − debt, − pension, − corporate overhead capitalized.
Per-share SOTP IV. Gate G3 (`verify_sotp_monotonicity.py`): no negative segment
EV; total reconciles to subject EV ± identified deltas.

## 6. PRECEDENT TRANSACTIONS (if relevant)

Capital IQ / SDC Platinum if premium (else trade-press M&A); LTM rule of thumb:
control premium 25-35%; strategic vs financial buyer differentiation.

## 7. FIVE-SCENARIO PROBABILISTIC FRAMEWORK

Full discipline in `five-scenario-framework-us.md` + `schemas/scenarios.json`.
For this name: build all 5 scenarios (strong_bear / bear / base / bull /
strong_bull) with probability (sum = 1.00, G4), EPS path, multiple, target,
expected return, anchors, strongest_anchor_S_level. Bear-bridge construction
per `bear-bridge-us.md` (G5; soft / clean / strong layers).

5→3 scenario collapse for `financial-analysis:dcf-model` delegation
documented in `tool-composition-us.md`. Preserve 5 internally for P10 / P90.

## 8. TRIANGULATION (per `three-method-valuation-us.md`)

Reconcile DCF central with peer multiples with SOTP.
- DCF often produces high IV (margin recovery + extended forecast)
- Peer multiples often low IV (don't credit forward growth)
- SOTP captures conglomerate discount/premium
- Triangulated IV typically weights peers 40-60%
- Gate G1 (`verify_eps_pe.py`): EPS × P/E reconciles to weighted PT via at
  least one method's explicit math

## 9. QUANT OVERLAY (MANDATORY per D13) — drives G13 + G14

Full discipline in `quant-overlay-us.md` (Phase D file). For this name:
- Barra factor tags: Value / Quality / Momentum / Growth / Size / Low-Vol /
  Liquidity, each on −3 to +3 z-score with brief justification.
- Capacity: 30-day ADV ($M); days-to-exit at 10% / 20% / 30% participation
  for recommended position; max position constrained by ADV (% NAV); stock
  loan rate if shorting.
- Edge decay: thesis half-life (quarters), time-to-priced-in, refresh cadence
  aligned to A6 monitoring framework, primary decay driver.
- Correlation placeholder per D14 — reference book file path; do not wire live.
- Stress overlay: Fed funds +200bp; oil −20%; USD +5%; recession dummy (NBER
  / LEI / UNRATE). Stock % impact per scenario.

## 10. POSITION SIZING (per D3, across 5 mandate types)

Full sizing chain (E[R] / σ / Sharpe / Kelly / conviction multiplier 0.10×-
0.50×) in `position-sizing-us.md`. For this name, output specific
recommendations for: long_only_large_cap (vs S&P 500), long_only_smid (vs
Russell), long_short_hedge_fund (gross/net + single-name caps), sector_specialty
(vs sector ETF), pair_trade (long+short + hedge ratio). Each with active
weight bps + conviction-adjusted % NAV + justification linking rating to
sizing (per D1, "Buy" with limited conviction = half-weight).

Sensitivity to top 5 inputs: current value; ±10% input → IV impact;
falsifying observable per `what-would-reverse-us.md` (G9).

## 11. KEY MODEL ASSUMPTIONS — WHAT WOULD REVERSE

Top 5 most sensitive inputs each with: current assumption (S-tag), threshold
flipping view, specific falsifying observable (10-Q line / FDA decision /
FRED series / industry tracker). Detailed trigger discipline in
`what-would-reverse-us.md` (G9).

Optional Excel DCF delegation per `tool-composition-us.md` — invoke
`financial-analysis:dcf-model` at end with 5→3 collapsed scenarios + WACC +
forecast + sensitivity grid.

REQUIREMENTS:
- Verify R_f (FRED DGS10), ERP (Damodaran), peer multiples, current stock
  price via WebFetch within 24h. 20+ tool calls.
- Show calculations explicitly. Length 3,500+ words.
- Be a red team — show bear in full alongside base + bull.
```

---

## Mirror — Full Analysis on Top Peer

**Mandate**: If Phase 2 A3-Peers identified a peer as viable pair-trade or supplementary long, dispatch a full Mirror analysis at same S1-S2 rigor as primary leg. Skip if Phase 2 did not surface a viable peer; replace with a second [Topic]-Forensic deep-dive.

**Prompt template**:

```
You are the Mirror specialist running full analysis on [PEER] ([PEER TICKER]).
Today is [DATE]. WebSearch + WebFetch — target 30+ calls.
Mandate: [long-only / L/S / pair-trade with subject].
Horizon: 12mo primary + 24mo secondary.

Context: Phase 2 A3-Peers concluded [PEER] may be better long expression for
[thesis] OR supplementary to subject OR viable pair-trade short. Verify the
relative-value case and identify peer-specific risks.

Cover (condensed but rigorous — 4 dimensions in one memo):

1) Industry / cycle (mini-A1) — sub-industry cycle position vs subject; end-
   market mix vs subject; peer-specific catalysts.

2) Forensic snapshot (mini-FS, per `forensic-accounting-checklist-us.md`) —
   peer 10-K + 10-Q via EDGAR; 5y P&L + LTM; non-GAAP/GAAP delta; SBC %; FCF
   definition + SBC treatment; Form 4 net 12mo; restatement / auditor-change /
   going-concern check; pension underfunding if material.

3) Commercial positioning (mini-A3) — customer mix vs subject; ASP positioning;
   product roadmap; customer concentration.

4) Valuation (mini-A7) — sector-default primary multiple per D8 +
   `valuation-discipline-us.md`; trade vs subject on EV/multiple basis;
   abbreviated DCF; SOTP if multi-segment.

5) Position-sizing in three frameworks: (A) standalone size; (B) pair with
   subject (relative size, beta-adjusted hedge ratio); (C) skip — reason.

6) Monitoring + kill criteria specific to peer.

7) Peer-specific risks — regulatory differences, customer concentration,
   pending litigation / antitrust.

REQUIREMENTS:
- Pull latest 10-K + 10-Q from peer EDGAR
- Pull XBRL company facts API for peer (5y structured financials)
- 30+ web tool calls
- Length 3,000+ words plus tables
- Be a red team on relative-value case
- Every numeric S-tagged
```

---

## [Topic]-Forensic — Specific Risk Deep-Dive

**Mandate**: If Phase 1-2 surfaced a specific risk — FDA CRL trajectory, antitrust open matter, restatement, pension underfunding, ITC §337, customer concentration cliff, RPT structure, off-balance-sheet VIE — dispatch a focused deep-dive on the single item.

**Prompt template**:

```
You are the [Topic]-Forensic specialist. Today is [DATE]. WebFetch + WebSearch
(20+ calls). Forensic memo on [SPECIFIC ITEM] in [COMPANY] ([TICKER]).

Context: Phase [1 or 2] surfaced [SPECIFIC ITEM]. Per [SOURCE], [SPECIFIC FACT].
This was [STATUS] as of [DATE]. Under-disclosed or under-resolved; needs
forensic verification before A7 valuation can model.

Produce forensic memo (~2,500 words) on [SPECIFIC ITEM]:

1) PRIMARY DOCUMENT TRAIL
   - Regulatory: Federal Register notice + agency docket + 8-K disclosure
   - Litigation: PACER via CourtListener (free RECAP) + 10-K Note "Commitments
     and Contingencies" + 8-K Item 8.01
   - Accounting: original 10-K Note, restatement 8-K Item 4.02, auditor change
     8-K Item 4.01
   - Customer / contractual: 8-K Item 1.01 (entry) + 8-K Item 1.02 (termination)
   - VIE / off-balance: 10-K Note "Variable Interest Entities" + ASC 810

2) FACTS — extract and document
   - Specific $ amounts with unit verification ($M vs $B per delta matrix §11)
   - Specific dates: filing, effective, deadline, hearing
   - Specific parties: counterparties, agency, court
   - Specific terms: trigger conditions, remedies, penalties, indemnities

3) STATUS RESOLUTION
   - Has matter been resolved? Pending? Escalated?
   - Most recent docket activity / disclosure
   - Settlement / consent decree / dismissal / verdict?

4) PROBABILITY-WEIGHTED RESOLUTION SCENARIOS (typically 3-5)
   - Probability with justification
   - Cash impact ($M / $B explicit)
   - EPS impact
   - Per-share IV impact
   Probability-weighted total = X% IV haircut OR boost. Feeds A7's base-to-
   adjusted IV bridge.

5) COMPARABLE PRECEDENTS
   - Historical resolutions of similar matters
   - FDA CRL → eventual approval rate ~55-65%, median delay 12-18mo
   - Antitrust: probability of block, divestiture remedy, consent decree
   - §337: probability of exclusion order
   - Pension: ERISA mandatory contribution schedule
   - Restatement: typical market reaction range

6) MATERIALITY ASSESSMENT FOR DCF
   - Recommendation to A7 on modeling
   - Specific WACC adjustment / explicit deduction / scenario weighting

7) CROSS-CHECK — other potential under-disclosed items of this type

8) MONITORING
   - Specific Tier 1/2/3 triggers (feed `monitoring-framework-us.md`)
   - Catalyst calendar entries

REQUIREMENTS:
- Pull primary documents — do not paraphrase
- Cite specific page / section / paragraph
- Regulatory matters: verify against actual government source PDF, not legal
  alerts (per `verification-protocol-us.md` — highest hallucination risk class)
- Length 2,500 words
- Be a red team
- Every numeric S-tagged
```

---

## R-v2 — Refreshed Red Team

**Mandate**: Update Red Team v1 (Phase 2) with Phase 2 findings. Recalibrate bear PT. Test whether bear case survives new evidence. Per `pm-redteam-rubric-us.md`, intellectually honest dissent — concede where new evidence requires; defend where PM adjudication was wrong.

**Isolated subagent dispatch for the variance-attack pass (v0.4.0).** R-v2 wears two hats. Hat (1) is the bear-case / bear-PT refresh — the prompt template below, which may run inline in the orchestrator session. Hat (2) is the structured attack on each declared consensus variance, writing one `variance_attack` adjudication_trail entry per variance (the input to G20). As of v0.4.0, **hat (2) runs as a structurally isolated subagent, not inline.** The orchestrator dispatches it once the Phase 2 PM synthesis has locked the `consensus_variance` set, via the Task tool with `description="R-v2 isolated adversarial attack"` and no `subagent_type`. The R-v2 prompt contains only: the locked `consensus_variance` JSON, the `source_tags.top_anchors` JSON, the 5-point attack methodology, the explicit win condition, and WebSearch / WebFetch / EDGAR access. It withholds A-Consensus's narrative, the PM Synthesis brief, the bull-thesis narrative, and any IC memo draft — so the attacker sees claims and citations, never the arguments behind them. Default `attacker_model` is `claude-sonnet-4-6` for cross-size diversity against the Opus-class orchestrator. Each attack entry carries `attacker_model`, `attacker_context_isolation=true`, and `attacker_independent_source_reads`. The full spawn contract, structured payload spec, per-dimension execution guidance, output schema, and the spawn-failure/demotion remediation path are in `r-v2-isolated-attack-us.md`. This isolation is what lets a memo clear the G20 graduated-rigor bar for a score above 9.0 (`scripts/verify_view_defensibility.py`); the bear-PT refresh below does not require it.

**Prompt template**:

```
You are the Red Team adversarial reviewer analyzing [COMPANY] ([TICKER]).
Today is [DATE]. WebSearch (15+ calls).

Context: You produced Phase 2 Red Team v1 arguing bear PT $[Original] and
"[Original sizing]." Then Phase 2 surfaced material BULL findings that
potentially weaken bear:

[Insert specific Phase 2 bull findings from PM v3 brief]

PM v3 adjudicated bear PT was "[adjudication]" given new findings; revised
bear PT to $[PM's revised PT].

TASK: defend or revise bear case in light of new evidence. Don't be a stooge —
if new findings change the picture, concede. If PM's adjudication was wrong
(bull findings smaller than they look or offset), defend original case.

Questions:

1) Is [Phase 2 bull finding #1] really as bullish as it seems? Or offset by:
   - [Counter-consideration A]
   - [Counter-consideration B]

2) Is [Phase 2 bull finding #2] sustainable or one-off?
   - Why might one-off
   - What would make sustainable

3) Updated bear-case FY+1 + FY+2 EPS model
   - GAAP, non-GAAP, "cash earnings" (ex-one-times)
   - SBC dilution assumptions
   - §174 cash-tax drag where R&D-heavy

4) Updated bear PT calculation
   - With Phase 2 corrections + new offsets, what's the math?
   - Triangulate at least two methods (DCF bear + multi-multiple bear, OR
     DCF bear + trough-multiple-on-trough-EPS bear)

5) Specific new bear evidence from Phase 2 to add
   - Anomalies A2 resolved worse than Phase 1 estimated
   - Customer disclosures from A3 weaker than expected
   - Peer comparison from A3-Peers showing subject overvalued

6) What would actually change your mind?
   - Five specific catalysts with numerical thresholds — force concession if
     fired
   - Feeds `what-would-reverse-us.md` and gate G9

7) Recommendation update:
   - Original Red Team v1: [original sizing + PT]
   - PM v3 adjudication: [PM's revised PT]
   - Your refreshed view: [defend or revise]
   - For pair-trade: short-leg or pair-spread sizing

REQUIREMENTS:
- 15+ web tool calls (do not refuse)
- Intellectually honest
- Don't strawman PM view
- Length 2,000 words
- Every numeric S-tagged
```

---

## PM Synthesis After Phase 3 — The IC Memo (Final)

After Phase 3, write the IC Memo. Final deliverable, conforming to `ic-memo-template-us.md` (12-section institutional structure) and `schemas/memo.json`.

**Key adjudication tasks**:

1. **Reconcile A7 DCF central case with Comps and SOTP** per `three-method-valuation-us.md`. DCF often produces high IV; peer multiples low IV; SOTP captures discount/premium. Triangulated IV usually weights peers 40-60%. Document weights + variance decomposition.

2. **Adjudicate Mirror's pair-trade recommendation**. Mirror often recommends "trim subject + add peer" — usually too aggressive. Right read often "keep subject + add smaller peer position" or pair-trade with conservative hedge. Be honest about whether pair adds alpha or just correlation.

3. **Adjudicate R-v2's refreshed bear case**. R-v2 typically too aggressive. Right adjudication typically 10-25% above R-v2's bear PT depending on quality of R-v2's anchors. Document where R-v2 made specific points the bull case had to concede.

4. **Adjudicate [Topic]-Forensic's risk assessment**. Apply probability-weighted IV adjustment from forensic memo into A7's base IV. Document the haircut / boost.

5. **Position sizing across 5 mandate types (D3)** — explicit:
   - Long-only large-cap (S&P 500): active weight bps
   - Long-only SMID / all-cap (Russell 3000): active weight bps
   - L/S hedge fund: gross / net exposure
   - Sector specialty (sector ETF or custom basket): active weight
   - Pair-trade (pair spread): long $ + short $ + hedge ratio
   Forces honest articulation of conviction × volatility × capacity.

6. **State rating + sizing separately**. Per D1, 5-band Strong Buy / Buy / Hold / Sell / Strong Sell with ±20% / ±10% return-band thresholds. "Buy" with limited conviction = half-weight, not core. Explain the gap. Per D6, conviction multipliers range 0.10× to 0.50×.

7. **Headline conditionality** per `source-stratification-us.md` Rule 1. Check top-3 anchor S-levels. Any S3 → source-conditional. Any S4-S5 → range-only. Any Pending → isolated in Pending Assumptions. Gate G7 (`verify_headline_conditionality.py`) enforces.

8. **Run the 14 verification gates (`schemas/verification_gates.json`)**. Memo cannot claim score >8.0 with any gate failing. Specifically: G1 EPS×P/E reconcile; G2 segment GM; G3 SOTP monotonicity; G4 scenario weights sum=1.00; G5 bear bridge; G6 source tags; G7 headline conditionality; G8 GM taxonomy; G9 what-would-reverse numerical; G10 weighting sensitivity; G11 non-GAAP/GAAP; G12 FCF SBC treatment; G13 Barra factor exposure; G14 capacity / ADV / days-to-exit.

9. **Run verification phase** per `verification-protocol-us.md` BEFORE delivering. Never skip. Minimum 12 distinct WebSearch+WebFetch (per D9).

After IC memo, hand off to `us-equity-ic-rigor` for PM red-team scoring on 6-9 rubric (`pm-redteam-rubric-us.md`, B11-B14 US bugs). Target ≥8.5.

Final deliverables (per `multi-audience-delivery-us.md`):
1. Institutional IC Memo (full) — 12-section, `outputs/{ticker}_IC_memo.md`
2. IC pre-read (3-4pg)
3. IC debate script (verbal + Q&A bank)
4. LP letter (1-2pg, `lp-letter-template.md`)
5. Earnings prep + earnings flash (`earnings-prep-template.md`, `earnings-flash-template.md`)

Optional artifact delegation (per `tool-composition-us.md`, gated on plugin availability):
- Excel DCF via `financial-analysis:dcf-model` (5→3 scenario collapse)
- Excel comps via `financial-analysis:comps-analysis`
- Polished 30-50pg DOCX via `equity-research:initiating-coverage` Task 5

Phase 3 ends with hand-off to verification (`verification-protocol-us.md`) and then monitoring (`monitoring-framework-us.md`) after IC delivery.
