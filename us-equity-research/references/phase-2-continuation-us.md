# Phase 2: Deepening + Forensic + Red Team (US)

Phase 2 dispatches five agents in parallel. Unlike Phase 1 (see `phase-1-deep-dive-us.md`), Phase 2 agents are **set up specifically based on Phase 1 findings** — they target the gaps and tensions surfaced in the Phase 1 Integrated Brief.

The five Phase 2 specialists: A2 (forensic continuation), A3 (customer / commercial pipeline), A3-Peers (competitive comparison), R (Red Team v1), A6 (channel pulse / monitoring framework setup). Dispatch in one message; parallel Agent tool calls.

Each agent receives the Phase 1 Integrated Brief + Phase 1 workpapers + specific Phase 1 anomalies + the Phase 0 hypothesis tree.

Phase 2 outputs feed Phase 3 valuation (`phase-3-valuation-us.md`).

---

## A2 — Forensic Continuation

**Mandate**: Pull most recent 10-Q + any 8-Ks filed post-Phase-1; resolve Phase 1 anomalies; deep-read 10-K footnotes Phase 1 didn't have time for.

**Prompt template**:

```
You are the Forensic Accounting specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. You did Phase 1 FS; now do Phase 2 continuation. WebFetch
extensively — minimum 25 calls.

Key questions:

1) Pull most recent 10-Q (or 8-K Item 2.02 if 10-Q not yet filed)
   - Revenue + segment trend vs Phase 1 baseline
   - GAAP gross margin + non-GAAP/GAAP delta movement
   - SBC % of revenue trend
   - DSO / DIO / DPO trend (breaks = revenue-quality / demand concern)
   - Deferred revenue trend (SaaS churn canary)
   - Net debt change, new disclosures (Subsequent Events especially)
   URL: sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-Q

2) Resolve each Phase 1 anomaly — investigate, pull primary doc, document
   corrected read with specific 10-K / 10-Q Note + page

3) Deep-read 10-K footnotes Phase 1 didn't cover — Commitments & Contingencies
   (litigation, CERCLA, FIN 48 / ASC 740); Off-Balance-Sheet (securitizations,
   synthetic leases, VIE per ASC 810); Subsequent Events; Income Taxes (rate
   reconciliation, valuation allowance on DTAs); Debt (maturity, covenants,
   coupon); Employee Benefits (pension PBO vs FV plan assets).

4) Restatement & §16(b) check — 8-K Item 4.02 (severe), 4.01 (auditor change),
   PCAOB inspection for current auditor, §16(b) short-swing recoveries.

5) Pension / OPEB (per `forensic-accounting-checklist-us.md` Item 9 if
   material) — PBO vs FV plan assets 5y; ERISA mandatory contribution
   trigger; discount rate sensitivity.

6) Debt structure — composition, maturity ladder, refinancing schedule,
   coupon vs current IG/HY yield (FRED BAMLC0A0CM IG OAS, BAMLH0A0HYM2 HY OAS),
   covenants, interest cover.

7) ETR trajectory — 10-K rate reconciliation drivers; GILTI/FDII/BEAT/§174
   impact; Pillar 2 GMT exposure; DTA valuation allowance movements. Per
   `forensic-accounting-checklist-us.md` Item 14.

8) Buybacks + capital return — 10-Q "Share Repurchases" note; buyback-to-SBC
   ratio (<1.0 = dilution masked); dividend payout vs FCF; ASR vs open-market.
   Per `forensic-accounting-checklist-us.md` Item 3.

9) Working capital — CCC (DSO + DIO − DPO) 8Q trend; FCF conversion
   (FCF / GAAP NI).

10) Form 4 net activity update since Phase 1 — openinsider.com; new filings
    since Phase 1 cutoff; cluster patterns.

Deliverables:
A) Most-recent-quarter detailed financial extract
B) Resolution of each Phase 1 anomaly (corrected reads)
C) Updated forensic red flags
D) Updated FCF / dividend / buyback trajectory through year+2
E) Updated normalized P&L bridge for forecast years
F) Phase 3 valuation inputs ready for A7

Length: 2,500+ words. Every numeric S-tagged.
```

---

## A3 — Customer / Commercial Pipeline

**Mandate**: Identify customers, win/loss positions, ASP dynamics, product roadmap. Most US companies do not disclose customers below the >10% threshold (Regulation S-K Item 101), but trade press, customer-side filings, and supply-chain teardowns triangulate.

**Prompt template**:

```
You are the Commercial Positioning specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. WebSearch + WebFetch — target 25+ calls.

Context: Phase 1 established baseline. Answer specific commercial questions
from Phase 1 brief.

1) [Major customer #1] — current account status, share trajectory, recent
   wins/losses, contract structure (8-K Item 1.01 if disclosed). Sector
   triangulation: TechInsights / The Information for tech; customer-side
   formulary for pharma; Wards Auto platform disclosures for autos; IR
   customer logos for SaaS.

2) [Customers #2-#5]: same analysis.

3) Top customer revenue concentration
   - 10-K Item 1 — ≥10% of consolidated revenue disclosure (Regulation S-K
     Item 101). Named or anonymized ("Customer A").
   - DEF 14A Item 404 if customer also 5% holder, director, officer affiliate
   - Triangulate anonymized using: geographic split, revenue magnitude vs
     industry estimates, product mix vs customer's lineup, downstream supplier
     disclosures (Apple Supplier List, hyperscaler capex statements)

4) Product roadmap
   - Forward launches with dates
   - Investor Day deck guidance (8-K Item 7.01 Ex 99.1)
   - Tech: chip / product cadence
   - Pharma: pipeline by phase, PDUFA dates, AdCom calendar from FDA dashboards
   - SaaS: product expansion within accounts

5) ASP analysis
   - Company average ASP vs competitor average
   - Premium / discount + trend
   - Tech: per-unit chip / system ASP
   - Pharma: gross-to-net adjustments, rebate exposure
   - SaaS: per-seat ACV

6) Major contracts and announcements
   - 8-K Item 1.01 material agreements last 12mo
   - 8-K Item 1.02 terminations last 12mo

7) Pipeline / backlog
   - 10-K Note "Revenue Recognition" performance obligation backlog (ASC 606)
   - Book-to-bill if disclosed
   - SaaS: RPO (remaining performance obligations)

8) Verdict — at realistic 2-year-forward customer mix, what's rev / GM
   trajectory? Is the implicit capex / opex value-creating?

Sources: The Information, Stratechery, STAT News, BioPharma Dive, Wards Auto,
Automotive News, Counterpoint / Omdia / IDC / Gartner, customer-side earnings
calls (Motley Fool free; AlphaSense / Capital IQ Pro / SeekingAlpha premium),
TechInsights teardowns, 10-K Item 1 + DEF 14A Item 404.

Citation discipline: every customer claim S-tagged. Anonymized customer
triangulation flagged with confidence level.

Length: 2,000-2,500 words.
```

---

## A3-Peers — Competitive Comparison

**Mandate**: Side-by-side vs 2-3 closest peers in same GICS sub-industry. Is subject still best expression of the thesis, or has a peer become a better play? Relative valuation per `valuation-discipline-us.md`.

**Prompt template**:

```
You are the Competitive Positioning specialist analyzing [COMPANY] ([TICKER])
vs closest peers. Today is [DATE]. WebSearch + WebFetch on peer EDGAR filings
+ sector trade press — target 30+ calls.

Identified peers from Phase 1 A1 + A3 + sector context:
[PEER 1] ([T1]), [PEER 2] ([T2]), [PEER 3] ([T3])

GICS Level-4 sub-industry: [code + name]

For each peer (from EDGAR + XBRL company facts API):

a) FY[latest]: revenue, growth, segments, GAAP NI, non-GAAP NI, EBITDA, EBIT,
   EPS, FCF (compute OCF − capex deducting SBC), SBC %
b) Latest 10-Q: revenue YoY, segment trend, GM trend
c) Stock data: spot, market cap, EV, 52-week range, YTD vs subject
d) Valuation multiples per sector default (D8 + `valuation-discipline-us.md`):
   - Mature industrial / consumer: P/E (NTM), EV/EBITDA, EV/Sales
   - Banks: P/B, P/E, ROTCE-implied P/B
   - Insurance: P/B, P/E, ROE-implied
   - REITs: P/AFFO, NAV, implied cap rate
   - SaaS: EV/ARR, Rule of 40, EV/Sales, FCF yield
   - Biotech (pre-revenue): NPV pipeline
   - E&P: EV/EBITDAX, FCF yield, NAV
   - Autos: EV/EBITDA, EV/Sales, P/E
   - Airlines: EV/EBITDAR
   - Asset managers: P/AUM, P/E, EV/EBITDA
e) Customer mix / end-market exposure (peer 10-K Item 1)
f) Capex intensity (peer 10-K Item 7)
g) Specific competitive thesis exposure (cycle, mix shift, end-market)
h) Recent strategic moves last 24mo: M&A (8-K Item 1.01), capacity, partnerships
i) Regulatory exposure differences
j) Positioning differences: 13F clusters, short interest, options skew

Deliverables:
A) Side-by-side comparison table covering all dimensions
B) Cycle exposure heatmap
C) Relative valuation (normalize for capex intensity, SBC %, non-GAAP gap,
   leverage)
D) Pair-trade framework if applicable:
   - Long subject / short [peer X]: thesis
   - Beta-adjusted hedge ratio (5y weekly betas vs S&P 500)
   - Capacity / liquidity check (ADV both legs, days-to-exit at 20% participation)
   - Cost of carry (short borrow rate, dividend mismatch)
E) Conclusion: is subject still best expression of thesis? Or has peer become
   better play?

Optional artifact delegation (per `tool-composition-us.md`): if user requested
Excel comps OR Phase 3 requires Excel comps for IC review, dispatch
`financial-analysis:comps-analysis` AT THE END with peer set + standardized
fields. Output: outputs/{ticker}_Comps.xlsx. Default: produce Markdown table
here; delegation on demand only.

Sources: EDGAR XBRL company facts API per peer (CIK lookup at
sec.gov/files/company_tickers.json); 10-K / 10-Q / 8-K browse per peer; sector
trade press; Yahoo Finance / StockAnalysis for free consensus.

Citation discipline: every peer numeric S-tagged with filing or aggregator URL.

Length: 3,000+ words plus tables. Be a red team on relative-value case — surface
strongest argument AGAINST subject and FOR a peer.
```

---

## R — Red Team v1

**Mandate**: Build the strongest possible bear case in good faith. Not balanced, not nuanced — bear at full strength. PM will adjudicate later. Per `pm-redteam-rubric-us.md`, judged on whether it identifies what bull side missed.

**Prompt template**:

```
You are the Red Team adversarial reviewer analyzing [COMPANY] ([TICKER]).
Today is [DATE]. WebSearch + WebFetch (20+ calls).

Your job is NOT to be balanced. Build the strongest possible bear case.

Attack vectors:

1) Base-rate analysis on peer set at this cycle position
   - Historical returns for comparable peers at similar multiple / cycle over
     last 10-15y
   - High-growth SaaS at 80x EV/ARR — what % retained that multiple 24mo later?
     (Historical base rate 15-25%)
   - Mature industrial at peak EV/EBITDA — what % held at next trough?
     (Usually 0-20%)
   - Biotech post-Phase 3 positive — what % delivered launch vs consensus?
     (~50-60% beat)
   - Bear default: median outcome is mediocre. Get actual return data.

2) Non-GAAP / GAAP gap exploitation (G11 hook)
   - Widening delta = earnings quality eroding
   - Persistent "one-time" restructuring across years = structural cost
     misclassification
   - "Adjusted EBITDA" excluding SBC + recurring acquisition costs masks real
     economics

3) SBC headwind + dilution case (G12 hook)
   - If SBC % rising AND buyback offset adequacy <1.0, real dilution accelerating
   - Bear-case fully-diluted share count growth over 5y

4) §174 R&D capitalization cash-tax bear case
   - R&D-heavy names: TCJA 2017 §174 creates material cash-tax drag (5y US /
     15y foreign amortization)
   - Bear: cash tax much higher than book ETR suggests

5) Customer concentration cliff
   - Specific named or triangulated customer (>10% revenue) structurally
     impaired or de-sourcing → revenue cliff
   - At incremental margin, NI hit

6) ASC 606 channel-stuffing / revenue-quality bear case
   - DSO trend break
   - Deferred revenue decline (SaaS churn)
   - Bill-and-hold disclosures
   - Contract modification frequency

7) Regulatory / antitrust tail (probability + impact bands)
   - Per `regulatory-desk-us.md` scenarios
   - Pending M&A: DOJ / FTC block probability; antitrust break fee
   - Drug stocks: FDA CRL / AdCom negative probability
   - Tech: §337 ITC exclusion order on key product

8) Structural margin compression vs consensus
   - If FY+1 NI is FLAT or DOWN due to identified pressures, consensus miss
     magnitude in stdevs of dispersion
   - Use S4 consensus median + dispersion as bar to beat

9) Hidden leverage / off-balance-sheet
   - Pension underfunding (ERISA mandatory contribution exposure)
   - Operating lease ROU
   - Securitization, VIEs
   - Bond refinancing schedule at higher current corporate yields
     (FRED BAMLC0A0CM IG OAS, BAMLH0A0HYM2 HY OAS)

10) Stock-specific bear setups
    - Form 4 insider net selling sustained 90d / 6mo
    - 13D activist
    - Short interest rising + DTC extending
    - Sell-side downgrades + negative revisions
    - TIC capital flow signal foreign selling
    - Index reconstitution risk if borderline S&P 500 / Russell

11) Cycle reality check
    - Late-cycle: yield-curve inversion (FRED T10Y2Y), ISM PMI <48 sustained,
      LEI rolling, UNRATE rising
    - Sector cycle indicators (Baker Hughes rig count, SAAR, SEMI book-to-bill)

12) Trough multiple stress test
    - Trough P/E or trough EV/EBITDA on cyclical-low earnings → floor
    - Compute bear PT with two-methodology triangulation

Deliverables:
A) Base-rate analysis with peer return data
B) Bear-case FY+1 + FY+2 EPS model (GAAP, non-GAAP, "cash earnings")
C) Bear-case PT with two methodology triangulation (DCF bear + peer-multiple
   bear, OR trough-multiple-on-trough-EPS bear, OR SOTP bear)
D) Specific events / data points that would falsify bear case (5-7 items with
   numerical thresholds — feeds `what-would-reverse-us.md`)
E) Stock-specific catalysts to short / position-cut on
F) Bear EPS bridge — named adjustments from base to bear (per `bear-bridge-us.md`,
   gate G5)

Length: 3,000+ words. Intellectually honest — don't strawman bull case.
Institutional-grade dissent, not takedown for sport. Per `pm-redteam-rubric-us.md`,
score 9+ requires identifying specific anchors bull case ignored.
```

---

## A6 — Channel Pulse / Monitoring Framework Setup

**Mandate**: Build ongoing monitoring infrastructure for after IC delivery. Coverage discipline per `monitoring-framework-us.md`.

**Prompt template**:

```
You are the Channel Pulse / Monitoring specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. WebSearch (15+ calls).

Build the monitoring framework following the full dashboard discipline in
`monitoring-framework-us.md` (Tier 1/2/3 triggers, weekly/monthly/quarterly
cadence, preset alerts, key third-party voices catalog).

Deliverables (each populated for THIS name and sector):

1) **Weekly data tracking dashboard** — table for each series with source URL,
   update frequency, current reading + 90-day prior, threshold for investment-
   relevant change, bull/bear interpretation. Categories: industry pricing
   (sector-specific); demand indicators (FRED series per sector — DCOILWTICO
   / INDPRO / UNRATE / CPIAUCSL / T10Y2Y / BAMLC0A0CM; EIA / Baker Hughes /
   SAAR / Placer.ai as relevant); company-specific (price vs S&P 500 + sector
   ETF; 13F clusters; Form 4 via openinsider; short interest; options OI +
   IV; sell-side ratings); customer signals; regulatory dockets (Federal
   Register, BIS Entity List, OFAC SDN, agency-specific FDA/FCC/FERC/NHTSA/
   EPA/FAA).

2) **Catalyst calendar** — sortable table: Date | Event | Bull/Bear/Neutral
   | Action if Triggered. Cover quarterly earnings (next 4Q + pre-announcement
   windows), 10-K, DEF 14A, industry conferences (CES/OFC/JPM Healthcare/
   etc.), product launches, regulatory deadlines (PDUFA, AdCom, FCC, FERC),
   FOMC for rate-sensitive names, index reconstitution windows.

3) **Three-tier trigger thresholds** per `monitoring-framework-us.md` —
   numerical thresholds per Tier 1 / Tier 2 / Tier 3 for THIS name. Every
   threshold a NUMBER, not "meaningful change."

4) **Weekly + Monthly + Quarterly routines** customized to this name —
   sector-specific data sources, customer-list watch, peer-print calendar.
   Full routine templates in `monitoring-framework-us.md`.

5) **Named third-party voices for this sector** — analysts whose calls move
   the stock (full catalog in `monitoring-framework-us.md`).

6) **Preset alert triggers** for this name — Form 4 cluster, 13D, FDA/agency
   decision dates, antitrust action, ITC §337, 8-K Item 4.02 restatement,
   FOMC if rate-sensitive, stock move >5σ unexplained. Specific numerical
   thresholds per trigger.

Format as tactical playbook. Length 2,500 words.
```

---

## PM Synthesis After Phase 2 — Integrated Brief v3

Phase 2 typically surfaces material new findings — bullish and bearish. Write the Phase 2 Integrated Brief ("v3" because it supersedes v1 and v2 of Phase 1).

**Required sections**:

1. **What changed since Phase 1 brief** — new findings with bull/bear coding. Tag each with S-level per `source-stratification-us.md`.

2. **Updated thesis tree** — re-weight Phase 1 hypotheses. Typically shifts by 10-20 percentage points; if no shift, Phase 2 didn't earn its keep.

3. **The 5 biggest Phase 2 findings** — typically: Phase 1 anomaly resolved with corrected read; customer triangulation result; peer that emerged as viable pair-trade; strongest bear evidence; monitoring trigger near firing.

4. **Updated cycle position** — incorporate A6 channel pulse + A2 fresh quarterly data.

5. **Conflicts re-adjudicated** — between Phase 1 and Phase 2 reads. Document where A2 corrected Phase 1 FS read explicitly.

6. **Updated financial picture** — corrections from A2. Updated 5y + LTM + forward 1y table; every numeric S-tagged.

7. **Red Team adjudication** — R agent ran in Phase 2. Take bear case seriously without capitulating. If R's bear PT is $X, PM-adjudicated bear PT typically $X + 5-20% of bear range, depending on quality of R's anchors. Document explicitly.

8. **Updated kill criteria** — refined Tier 1 triggers from A6's framework.

9. **Phase 3 priorities** — gates Phase 3 valuation (`phase-3-valuation-us.md`):
   - Specific normalized P&L to model
   - Whether Mirror analysis on top peer warranted
   - Whether [Topic]-Forensic deep-dive warranted (FDA CRL trajectory, pending §337, RPT structure)
   - Specific A7 valuation inputs (sector multiple, WACC components, terminal growth)
   - R-v2 brief: bull findings to test, what to defend

10. **Preliminary direction** — more nuanced than Phase 1. Conviction tag (high / moderate / low / source-conditional / reactive per D1). Still NOT a recommendation; that's Phase 3.

Save as `outputs/{ticker}_Phase2_Integrated_Brief.md`. Workpapers as `outputs/{ticker}_Phase2_Workpapers.md`.

**Common Phase 2 patterns**:
- A2 resolves Phase 1 anomalies; surfaces new ones (ETR trajectory, debt refinancing, fresh-quarter OCF deceleration)
- A3 reveals customer concentration more or less than Phase 1 estimated, or triangulates anonymized
- A3-Peers suggests at least one peer viable as pair-trade or supplementary
- R produces bear case 15-25% more aggressive than PM's preliminary view
- A6 produces dashboard for tracking after IC

Phase 2 ends with hand-off to Phase 3 (`phase-3-valuation-us.md`).
