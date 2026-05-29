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

## CONSENSUS VARIANCE & REVISION VELOCITY (new in v0.2.0 — required for any non-Hold rating)

This section gates the rating per Plugin 2 gate **G15**. Discipline per `consensus-variance-us.md`. If no defensible non-consensus view exists, the memo must self-label "consensus-anchored" in the §RECOMMENDATION headline and rating ≤ Hold; otherwise this section enumerates each declared variance with magnitude, evidence, and sized impact.

### Consensus snapshot

| Line item | Consensus median | Source | n_analysts | Range (low–high) | Our number | Δ (%/bp) | Material? (Y/N) |
|---|---|---|---|---|---|---|---|
| FY[N+1] Revenue $M | | S4: [src + date] | | | | | |
| FY[N+1] EPS non-GAAP $ | | S4: [src + date] | | | | | |
| FY[N+1] GM % | | S4: [src + date] | | | | | |
| FY[N+1] OPM % | | S4: [src + date] | | | | | |
| Forward P/E (or sector multiple) | | S4 / 5y trailing | | | | | |
| 12-month PT median $ | | S4: [src + date] | | | | | |
| Rating mix (Buy / Hold / Sell %) | | S4: [src + date] | | | n/a | n/a | n/a |

### Declared variances (per G15 — at least one required for non-Hold rating; sizing impact ≥2.0pp for at least one)

For each variance below: type ∈ {Revenue, Margin, Multiple, Scenario-weight, Timing}.

**Variance 1 — [type]**
- Line item: [specific FY1/FY2/FY3 revenue / margin / multiple / scenario-weight / catalyst-timing line]
- Our number vs consensus: [your number] vs [consensus number] = [+/- X%/bp]
- Evidence (per `consensus-variance-us.md` evidence matrix — required S-levels for each type):
  - [S1 / S2 / S3 citation 1 with full ref + URL + date]
  - [S1 / S2 / S3 citation 2 — for margin variance, the explicit bridge step is shown here]
  - [Triangulation point consensus has not yet weighted — what specifically Street is missing]
- Sizing impact (per formula in `consensus-variance-us.md`): magnitude [X%] × probability_of_being_right [Y%] × scenario_sensitivity [Z%] = **[N] pp** shift in [scenario] probability vs consensus-implied
- Why consensus has not yet incorporated: [one-sentence operational mechanism — e.g. "Street's Q1 FY27 EPS revision occurred pre-call; the call transcript revealed the deposit beta inflection that mechanically shifts NIM trajectory; Street typically takes 2-6 weeks to re-incorporate post-call into median EPS"]
- Red Team challenge: [what falsification would look like + the trigger event/date that would resolve]

**Variance 2 — [type]** (if applicable)
[Same structure]

**Variance 3 — [type]** (if applicable)
[Same structure]

### If no defensible variance: "Consensus-anchored" disclosure

If zero load-bearing variances can be declared (or all declared variances have sizing_impact_pp < 2.0), the memo:
- Self-labels in §RECOMMENDATION headline as "**consensus-anchored**"
- Rating ceiling: Hold
- Headline_conditionality = `range_only` per `source-stratification-us.md`
- G15 status: n_a (Hold rating exempts the gate); rating cap enforced by G15 logic instead

### Revision velocity snapshot (per G17 — required disclosure if n_analysts ≥ 5)

| Window | FY1 EPS revision (%) | Direction | Breadth ((up−down)/N) | Comparison vs peer median |
|---|---|---|---|---|
| 1-month | | | | |
| 3-month | | | | |
| 6-month | | | | |

| Window | FY2 EPS revision (%) | PT revision (%) | Pre-print drift (last earnings -30d to -1d) |
|---|---|---|---|
| 3-month | | | |

**Revision velocity interpretation**: [Two sentences. Direction + magnitude + breadth. Cross with crowding score from §positioning_sentiment to identify highest-signal conjunction (revision-down + crowded-long = short setup; revision-up + crowded-short = squeeze setup). If n_analysts < 5: state "G17 = n_a, coverage too thin for revision velocity signal" and proceed.]

**Sources for this section**: all consensus data is S4-tagged per `source-stratification-us.md`. Variance-supporting evidence is S1-S3 per the evidence matrix. Revision velocity data is S4-derived.

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

### Bank-specific metrics (CONDITIONAL — required if sector ∈ {Financials/Banks, Diversified Banks, Regional Banks, Investment Banking & Brokerage, Insurance, BDC}; gated by Plugin 2 G16)

Full discipline in `phase-1-deep-dive-us.md` §FS-Banks Augmentation. This subsection is required for any depository / broker-dealer / insurer / BDC memo and surfaces the load-bearing metrics that generic income-statement analysis misses for banks. G16 verifies presence of (a) AOCI bridge, (b) CET1 walk, (c) NIM trajectory, (d) stress capital context.

**(a) AOCI bridge and tangible book reconciliation**

| Item | $B | Source | % of TCE |
|---|---|---|---|
| AFS securities book value | | S1: [10-K Schedule, Y-9C HC-B] | |
| AFS securities fair value | | S1: [same] | |
| AOCI mark (AFS) | | S1: [10-K Equity, Y-9C HC-R] | |
| HTM securities book value | | S1: [10-K Note] | |
| HTM securities fair value | | S1: [10-K Note "Fair Value Measurements"] | |
| HTM unrealized loss (not in AOCI) | | S1-computed | |
| Reported TBVPS $ | | S1 | n/a |
| Mark-to-market TBVPS $ (TBVPS − HTM unrealized loss × (1−tax)/diluted shares) | | S1-computed | n/a |
| Depositor uninsured concentration (% of total deposits) | | S2: [10-Q deposit composition note] | n/a |

**SVB-pattern flag**: HTM unrealized loss > 25% TCE AND uninsured concentration > 60% → flag as pre-failure signature. [Yes/No + reasoning]

**(b) CET1 walk with operational RWA decomposition**

| Item | $B / % | Source |
|---|---|---|
| Starting CET1 (prior period) | | S2: prior 10-Q / Y-9C |
| + Net income to common | | S1/S2 |
| − Common dividends | | S2 |
| − Net share repurchases | | S2 |
| − AOCI flow (only for Category I-III above $700B AOCI-flow-through) | | S2 |
| − Goodwill/intangibles delta | | S2 |
| − DTA disallowance delta | | S2 |
| = Ending CET1 ratio (%) | | S1-computed |
| Credit RWA $ | | S2: Y-9C HC-R Part II |
| Market RWA $ (Category I-II only) | | S2: Y-9C HC-R Part II |
| Operational RWA $ (Category I-II; expanding to III/IV under Basel III Endgame) | | S2 |
| Total RWA $ | | S2 |
| **AOCI opt-out election status** (Category III ≤$700B, Category IV) | Yes / No | S1: 10-K |
| **Reported CET1 ratio (%)** | | S1 |
| **Pro-forma CET1 ratio without AOCI opt-out (%)** (if opt-out applies) | | S1-computed |

**(c) Stress capital buffer (SCB) and capital return capacity**

| Item | Value | Source |
|---|---|---|
| SCB (current, from Fed determination letter) | %  | S2: Fed letter, [date] |
| GSIB surcharge (Category I only, Method 1 + Method 2 — use higher) | % | S2: Fed Methodology disclosure |
| Required CET1 (4.5% + 2.5% CCB + SCB + GSIB) | % | computed |
| Actual CET1 | % | S1 |
| **Capital return capacity (Actual − Required) × RWA × (1 + 4Q NI accretion)** | $B | computed |
| Most recent CCAR/DFAST severely adverse CET1 trough | % | S2: Fed CCAR/DFAST release |

**(d) NIM and deposit beta trajectory**

| Period | NIM (%) | Reported deposit beta (cumulative cycle) | Asset side delta (bp QoQ) | Liability side delta (bp QoQ) | Mix delta (bp QoQ) |
|---|---|---|---|---|---|
| Q[N-4] | | | | | |
| Q[N-3] | | | | | |
| Q[N-2] | | | | | |
| Q[N-1] | | | | | |
| Q[N] (latest) | | | | | |
| Forward 4Q (mgmt commentary / curve-implied) | | | | | |

**Asset repricing**: % of earning assets repricing within 12 months = [X%]. Source: S1: 10-K Item 7A market-risk disclosure.

**Deposit composition**: non-interest-bearing % = [X%]; money-market + HY savings % = [Y%]. (Rate-sensitive deposit beta is the binding constraint on NIM down-cycle.)

**(e) CECL and reserve trajectory** (additional disclosure)

| Period | ACL / loans HFI (%) | Office CRE ACL (%) | Reserve build/release ($B) | Provision / PPNR (%) |
|---|---|---|---|---|
| Q[N-4] | | | | |
| Q[N] | | | | |

CRE concentration: Total CRE / total loans = [%]; Office CRE / total loans = [%]; Office CRE / TCE = [%]. (Office CRE / TCE > 50% is the regulatory watch threshold post-2023.)

**(f) Bank category and regulatory currency**

- Bank Category: [I / II / III / IV / Below $100B]
- Assets at period end: $[X]B; threshold to next category: $[Y]B (gap [Z%])
- Basel III Endgame status (as of memo date): [In final rule review / Implementation effective YYYY-MM-DD / Phase-in to YYYY] (cite Federal Register)
- Live SCB date: [next determination letter expected YYYY-Q[N]]

**G16 declaration**: ☐ All four required disclosures (AOCI bridge / CET1 walk / NIM trajectory / Stress capital) present. ☐ G16 status: pass / fail / n_a (n_a only if sector ∉ Financials).

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
