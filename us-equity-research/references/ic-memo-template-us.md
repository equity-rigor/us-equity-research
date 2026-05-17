# IC Memo Template (US) — Deliverable Shape

This is the fill-in-the-blanks shape of the institutional IC memo (audience variant `institutional_full` per memo.json). It shows **HOW** the rendered memo looks; the **WHAT** (mandatory sections + cross-checks) lives in `opinion-letter-section-checklist-us.md` under the rigor skill.

Output as Markdown (.md) per D15. The structured JSON twin lives at `outputs/<ticker>_structured.json` conforming to `schemas/memo.json`. No DOCX from this skill — polished DOCX is delegated to `equity-research:initiating-coverage` Task 5 when the user requests it per `tool-composition-us.md`.

NVDA as the running example where useful.

---

## Required structure (rendered)

```markdown
# Investment Committee Memo: [Company Name] ([TICKER])

**Author**: [Author / PM]
**Date**: [YYYY-MM-DD]
**Mandate**: [Long-only large-cap / Long-only SMID / L/S hedge fund / Concentrated specialty / Pair-trade]
**Horizon**: 12 months primary; 24 months secondary (per D2)
**Stage**: [Initiation / Update / Final IC memo]
**Audience variant**: `institutional_full`
**Source data cutoff**: [YYYY-MM-DD]
**Current price**: $[X] (as of [YYYY-MM-DD])
**Market cap**: $[X]B | **5-day ADV**: $[X]M | **Beta**: [X] (basis: [5y_monthly_vs_SP500 / 2y_daily_vs_SP500 / industry_unlevered / adjusted_bloomberg])

---

## RECOMMENDATION

**[Strong Buy / Buy / Hold / Sell / Strong Sell]** (per D1 bands: SB ≥+20%, B +10/+20, H ±10, S −10/−20, SS ≤−20%)

- 12-month price target: $[PT] (range $[low]–$[high])
- 24-month price target: $[PT24]
- Stop discipline: $[stop level], triggered on [specific condition]
- Conviction tag: [high_conviction / moderate_conviction / low_conviction / source_conditional / reactive]
- Default action: [initiate_long / add_long / hold_long / trim_long / exit_long / initiate_short / add_short / cover_short / no_action / spread_long_short]

[One-paragraph rationale. ≥100 words. State the core thesis in 1-2 sentences, the strongest anchor and its S-level, the headline conditionality posture (unconditional or source-conditional), and the asymmetry math in one line.]

**Asymmetry**: Bear PT $[X] / Base PT $[Y] / Bull PT $[Z] vs current $[P]. Downside [−A%] / upside [+B%]. Probability-weighted IV $[W] = upside [+C%]. Asymmetric on a [B/A ratio]:1 basis.

**Strongest top-3 anchor S-level**: [S1 / S2 / S3 / S4 / S5] → headline is [unconditional / source-conditional]

## INVESTMENT THESIS

[One-paragraph framing tying all legs together. ≥150 words.]

**Leg 1 — [Title]**
- Key statistic: [specific quantification with units + period + source tag per D16]
- Narrative: [≥200 words per memo.json `narrative` minLength. What the leg claims, why it's true now, what the mechanism is, how it compounds over the horizon, how it interacts with the other legs.]
- Anchor refs: [A1, A3 from source_tags.json]
- Timeline: [when this leg matters most — e.g. "FY26 first half"]

**Leg 2 — [Title]**
[Same structure]

**Leg 3 — [Title]**
[Same structure]

[Continue for 3-5 legs per memo.json minItems/maxItems]

## VALUATION FRAMEWORK

### Scenario probabilities and per-share IV (5-scenario per scenarios.json)

| Scenario | Probability | EPS (FY[NN]E) | Multiple | Multiple type | Target $ | Return % | Strongest anchor S-level |
|---|---|---|---|---|---|---|---|
| strong_bull | [%] | $[X] | [x] | [P/E / EV/EBITDA / EV/ARR / etc.] | $[P] | [%] | [S-level] |
| bull | [%] | $[X] | [x] | [type] | $[P] | [%] | [S-level] |
| base | [%] | $[X] | [x] | [type] | $[P] | [%] | [S-level] |
| bear | [%] | $[X] | [x] | [type] | $[P] | [%] | [S-level] |
| strong_bear | [%] | $[X] | [x] | [type] | $[P] | [%] | [S-level] |

Probabilities sum to 1.00 ± 0.01 per G4. EPS period consistent across rows per cross-check #3.

**Probability-weighted IV**: $[W] | **Scenario range** [P10, P90]: $[low] – $[high] | **Headline return**: Σ(P × R) = [%]

### Methodology triangulation

| Method | Value $ | Weight in triangulation | Use |
|---|---|---|---|
| DCF (5y explicit + terminal per D2) | $[X] | [%] | Cash-flow rigor |
| Trading comps (peer median + percentile) | $[X] | [%] | Market-priced check |
| SOTP (segment-by-segment) | $[X] | [%] | Internal consistency |
| Multi-multiple bear floor (sector-branched per D8) | $[X] | strong_bear floor only | Downside discipline |
| Precedent transactions (if available) | $[X] | [%] | M&A reference |

**Triangulated range**: $[low] – $[high]. Methods cross-check; not averaged.

### Position sizing across mandate types (per D3)

| Mandate type | Benchmark | Recommended active weight (bps) | Conviction-adjusted % NAV | Rationale |
|---|---|---|---|---|
| Long-only large-cap | S&P 500 | [±X bps] | [%] | [Why this size — Kelly × conviction multiplier per D6] |
| Long-only SMID / all-cap | Russell 1000/2000/3000 | [±X bps] | [%] | [Why] |
| L/S hedge fund | n/a (gross/net) | gross [%], net [%], single-name long cap [%], short cap [%] | [%] | [Why] |
| Concentrated specialty / sector fund | [Sector ETF, e.g. SOXX/XLK] | [±X bps] | [%] | [Why] |
| Pair-trade structure | Pair spread | Long [TICKER] X% / Short [TICKER] Y%; structure: [dollar_neutral / beta_neutral / value_neutral / ratio] | spread expected return [%] | [Why pair, why this structure] |

## KEY FINANCIAL DATA

### LTM actuals (last 4 quarters rolled)

[Hard numbers with D16 source citation for revenue, GP, OP, EBITDA, EBIT, NI GAAP, NI non-GAAP, EPS diluted GAAP, EPS diluted non-GAAP, diluted shares, capex, FCF, SBC, buyback, net debt. Disclose `fcf_includes_sbc_addback` boolean per memo.json — required for G12.]

### Latest 10-Q actuals (Q[N] FY[NN])

[Hard numbers from most recent 10-Q with full citation — `(S2: <TICKER> FY[NN]Q[N] 10-Q Note [X], filed [date], URL: edgar...)`]

### Forward forecast (5 years explicit per D2)

| Period | Revenue $M | Rev growth % | GM % | EBIT margin % | EPS diluted non-GAAP $ | FCF $M |
|---|---|---|---|---|---|---|
| FY[NN+1]E | | | | | | |
| FY[NN+2]E | | | | | | |
| FY[NN+3]E | | | | | | |
| FY[NN+4]E | | | | | | |
| FY[NN+5]E | | | | | | |

### Specific contractual / regulatory items

- [Material customer contracts with concentration risk, with source]
- [Regulatory designations: Entity List status / OFAC SDN / CFIUS posture / ITAR / antitrust open matters — verified within run]
- [Tax exposures from regulatory_status: BEAT / GILTI / FDII / Section 174 / Pillar 2 / CAMT / IRA 45X/48 / CHIPS 48D / R&D Credit Section 41]
- [Pension funded status %, material lease PV, VIE exposure, going-concern qualification status]

## RISKS AND KILL CRITERIA

### Tier 1 — Auto-exit triggers (any single → exit position immediately)

1. [Specific binary regulatory event — e.g. "BIS Entity List addition, verified via OFAC SDN query / Federal Register"]
2. [Specific binary customer event — e.g. "Top-1 customer concentration loss confirmed in next 10-Q"]
3. [Specific binary geopolitical / litigation event — e.g. "ITC §337 import ban issued"]
4. [Restatement — 8-K Item 4.02 filed]

### Tier 2 — Position-cut triggers (any → reduce by half)

1. [Quarterly miss threshold — e.g. "FY[NN]Q[N] revenue more than 5% below consensus median per S4 anchor"]
2. [Cycle / pricing trigger — e.g. "GM compression >200bp from current consensus path"]
3. [Commercial pipeline trigger — e.g. "Backlog declines QoQ AND book-to-bill <0.9x"]
4. [Insider pattern — Form 4 cluster selling >$50M over 3-month window]

### Tier 3 — Watch / re-evaluate triggers

1. [Subtler change-of-mind catalyst — e.g. "Hyperscaler capex guidance YoY <0% in next reporting cycle"]
2. [Competitor positioning shift]
3. [Sell-side consensus revision >2σ from current path]

Per `monitoring-framework-us.md` tier system.

## MONITORING PLAN

### Weekly (Monday morning, ~15 min)

- [Price + relative-strength check vs sector ETF and S&P 500]
- [Form 4 alert check via openinsider.com / secform4.com]
- [Trade press scan: The Information / Stratechery / sector-specific outlets per `us-data-sources.md`]
- [Options market: short interest update (semi-monthly FINRA), put/call ratio, IV rank]

### Monthly (~30 min)

- [13F filing window check (45 days post quarter end) — top-10 holder QoQ deltas]
- [Sell-side estimate revision dashboard — median + dispersion + revision direction]
- [Federal Register sector docket scan per `regulatory-desk-us.md`]
- [Anchor freshness review — any S3 anchors approaching their promotion path date]

### Quarterly (after results, ~4 hours)

- [Full re-underwrite — 10-Q line-by-line against base case scenario]
- [Run all 14 verification gates against updated structured JSON]
- [Update bear bridge step list with new actuals]
- [Refresh `outputs/<ticker>_scenarios.json` with new EPS path]

### Key dated events (catalyst calendar — see §10)

| Date | Event | Significance |
|---|---|---|
| [YYYY-MM-DD] | [Next earnings print] | [Beat/miss vs S4 consensus + KPI guide threshold] |
| [YYYY-MM-DD] | [Investor day / product launch / FDA decision / FTC ruling] | [Which scenario it loads] |
| [YYYY-MM-DD] | [Regulatory deadline — e.g. EU CMA Phase II decision] | [Which tail it fires] |

### Re-underwrite triggers

Schedule explicit re-underwrite at:
- [Each S3 anchor's promotion-path date]
- [Any Tier 2 trigger fire]
- [Index inclusion / exclusion decision date]
- [Annual: 10-K filing review]

## RED TEAM POSTURE

**Bear PT range**: $[low] – $[high]
**Bear case probability**: strong_bear [%] + bear [%] = [%] combined

**Concessions from Red Team**: [Specific points where the bear case yields after the rigorous internal debate. E.g. "Red Team concedes Hopper-to-Blackwell ASP step is empirically supported by S2 anchor; concession reduces bear probability from 25% to 20%."]

**Defended bear points** (survived the debate):
1. [Bear point with anchor]
2. [Bear point with anchor]
3. [Bear point with anchor]

**Falsification criteria** (any 3 of 5 fires → bear concedes the trade):
1. [Specific measurable event with denominator]
2. [Specific measurable event]
3. [Specific measurable event]
4. [Specific measurable event]
5. [Specific measurable event]

**Recommended weight (Red Team's view)**: [Position size if Red Team owned the book — typically smaller than base recommendation; states the conservative bound]

## FINAL ADJUDICATION

[How the PM weighed bull vs bear vs valuation vs forensic vs positioning evidence to arrive at the final recommendation. This is where specialist disagreements (Phase 1 deep-dive vs Phase 2 continuation vs Phase 3 valuation) are explicitly resolved. ≥150 words.]

**Path to upsizing**:
- [Specific catalyst → add X bps active weight or +X% NAV]
- [Specific catalyst → add X]

**Path to position cut**: any Tier 1 or Tier 2 trigger from §Risks above.

## OPEN QUESTIONS / WHAT WOULD CHANGE THE VIEW

Typically 5-10 items ranked by importance. Each item:

1. **[Question]** — What we'd want to learn: [specific observable]. Source / how to verify: [where it would appear; S-level expected].
2. **[Question]** — [Same structure]
3. **[Question]** — [Same structure]

[Continue for 5-10 items]

These drive the next research cycle. If any item resolves in a verifiable way before the next IC review, re-rate without waiting for the calendar.

## APPENDICES

### Appendix A — Document map

| Artifact | Path | Phase produced |
|---|---|---|
| IC memo (this document) | `outputs/<TICKER>_IC_memo.md` | Phase 4 synthesis |
| Structured JSON | `outputs/<TICKER>_structured.json` | Phase 4 (conforms to memo.json) |
| 5-scenario JSON | `outputs/<TICKER>_scenarios.json` | Phase 3 |
| Source tags JSON | `outputs/<TICKER>_source_tags.json` | Phase 1.5 |
| Verification gates JSON | `outputs/<TICKER>_verification_gates.json` | Phase 4 verification |
| Research document (delegation input, optional) | `outputs/<TICKER>_Research_Document_<date>.md` | Phase 1 |
| Valuation analysis (delegation input, optional) | `outputs/<TICKER>_Valuation_Analysis_<date>.md` | Phase 3 |
| DCF workbook (if delegated) | `outputs/<TICKER>_DCF.xlsx` | financial-analysis:dcf-model |
| Comps workbook (if delegated) | `outputs/<TICKER>_Comps.xlsx` | financial-analysis:comps-analysis |
| Polished DOCX (if delegated) | `outputs/<TICKER>_Initiation_Report_<date>.docx` | equity-research:initiating-coverage Task 5 |

### Appendix B — Source links (verified primary)

[Every S1-S2 citation listed here with full EDGAR URL. Every S3 transcript with call date + minute mark. Every S4 consensus snapshot with provider + sample size + freshness. Every S5 alt-data with provider + methodology + sample.]

### Appendix C — Verification report reference

Link: `outputs/<TICKER>_verification_gates.json`
Pass tally: [N of 14 gates pass]. Any fail must be reflected in §Recommendation conviction tag.

### Appendix D — Quant overlay (mandatory per D13)

**Factor tags (Barra-style z-scores, −3 to +3)**:
- Value: [z]
- Quality: [z]
- Momentum: [z]
- Growth: [z]
- Size: [z]
- Low_Vol: [z]
- Liquidity: [z]

**Capacity**:
- 30-day ADV: $[X]M
- Days-to-exit at 10% participation: [N]
- Days-to-exit at 20% participation: [N]
- Days-to-exit at 30% participation: [N]
- Max position constrained by ADV: [%] NAV

**Edge decay**:
- Thesis half-life: [months]
- Time-to-priced-in: [months]
- Refresh cadence: [weekly / monthly / quarterly_print / event_driven]
- Primary decay driver: [specific catalyst]

**Correlation overlay** (placeholder per D14):
- Book file path: [`~/book/holdings.json` or n/a]
- Live wired: [false — placeholder per D14]

**Stress overlay**:
- Fed funds +200bp: [stock % move]
- Oil −20%: [%]
- USD +5%: [%]
- Recession dummy: [%]

### Appendix E — Disclosures

[Audience is institutional buy-side / qualified purchasers / accredited / institutional LPs. Out of scope for FINRA Rule 2210 retail-comms. Standard internal-research disclaimer; author conflicts statement if applicable; firm position disclosure if applicable.]

```

---

## Key Quality Standards

- **Rating + sizing explicit and explained.** A "Buy" with low conviction is half-weight; a "Hold" can be 0% (avoid) or 1% (show position). State both rating AND sizing for every mandate type per D3.
- **Sizing across mandate types is mandatory.** Five mandate buckets per D3. Different funds have different benchmarks; one number does not work.
- **Bear case present and not strawmanned.** Even on a Buy recommendation, the Red Team's strongest case is visible in §Red Team Posture. Falsification criteria are specific and measurable.
- **Open questions section forces intellectual honesty.** Every IC memo has gaps. Listing 5-10 explicit unknowns sharpens the next research cycle.
- **Cite specific source URLs in appendix.** Every material number traceable. S1-S2 citations require EDGAR URLs per `source_tags.json`.
- **Cross-reference rigor.** §1 headline conditionality must match §Recommendation `conviction_tag`. §5 scenario probabilities must sum to 1.00 ± 0.01. §6 SOTP must reconcile to consolidated within ±50bp. Bear bridge sum must verify.

---

## What NOT to Include

- **Process commentary**: "We ran 5 specialists in parallel, then synthesized..." — belongs in internal documentation, not the IC memo. The IC reader cares about the conclusion and the evidence path, not the choreography.
- **Self-promotion**: "Our framework is more rigorous than..." — just be rigorous.
- **Excessive hedging**: "Could be either bull or bear depending on..." without adjudication is useless. Pick the rating; show the math; state the conditions under which you'd flip.
- **Padding**: Length is not value. A 4,000-word IC memo done well beats an 8,000-word one with filler. Bias toward dense paragraphs over bullet lists where the argument needs prose.
- **Retail-style language**: No "this stock is set to soar" or "must-own at any price". Audience is institutional. Per D4, retail variant is dropped from US scope entirely.

---

## Audience variant note

The structure above is for `audience_variant: institutional_full`. Other variants render selected sections only:

- `ic_preread` — §Recommendation + §Investment Thesis (legs only, no narrative) + §Valuation (scenario table only) + §Risks (Tier 1 only) + §Catalyst calendar. 3-4 pages max.
- `ic_debate_script` — see `../../us-equity-ic-rigor/templates/ic-debate-script-template-us.md`.
- `lp_letter` — see `lp-letter-template.md` (prose-heavy, 1-2 page client-facing).
- `earnings_prep` — see `earnings-prep-template.md` (operational, pre-print).
- `earnings_flash` — see `earnings-flash-template.md` (operational, T+30min).
- `kill_memo` — exit rationale; falsification-triggered; out of scope here.
