# Phase 1: Five-Agent Initial Deep-Dive (US)

Dispatch all five Phase 1 specialists in **a single message with parallel Agent tool calls**. Sequential dispatch wastes hours and breaks the parallel-specialization premise.

Each agent receives: company legal name, ticker + exchange, CIK, mandate type (one of 5 per `position-sizing-us.md`), horizon (12mo primary / 24mo secondary per D2), data access tier (EDGAR-only default per D5), sector (GICS Level-4), and the Phase 0 hypothesis tree (three competing theses).

Phase 1 outputs feed Phase 2 (see `phase-2-continuation-us.md`) and ultimately Phase 3 valuation (see `phase-3-valuation-us.md`). FS is the foundation for A7 normalized model construction.

---

## A1 — Industry & Cycle Desk

**Mandate**: Map the industry's cycle position, supply-demand balance, and top catalysts.

**Prompt template**:

```
You are the Industry & Cycle Desk specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. Public sources only. You MUST use WebSearch and WebFetch —
minimum 15 calls.

Your job is industry context, not company financial detail (that's FS).

Deliverables:

1) Industry structure
   - Market size by segment (last 3y actual + forward 3y consensus)
   - Top 5-8 producers with approximate market share
   - Recent M&A closed / pending / divestitures
   - HHI concentration vs 5 years ago

2) Cycle position
   - Explicit classification: trough / early-recovery / mid / peak / late-peak /
     downturn — anchored to:
     * Semis: SEMI book-to-bill, wafer-fab equipment shipments
     * Autos: SAAR, days-supply at dealers
     * Energy: Baker Hughes rig count, DUCs, OPEC+ posture
     * SaaS: net new ARR growth across listed peer set
     * Biotech: trial-readout density, FDA AdCom calendar
     * Banks: deposit beta, CET1, NCOs, card delinquency

3) Supply / demand
   - Global capacity adds next 24mo with announced operator + start date
   - End-market demand drivers
   - Channel inventory days vs normalized
   - Substitution / displacement risk

4) Top 5-8 catalysts for next 6-18 months — each with date, direction, magnitude,
   source

5) Bull case + bear case for the industry, each with 3-5 specific drivers and a
   falsifying observation

6) Confidence and gaps section — what couldn't be verified; which sub-segment
   data is freshest vs stalest; which trade-press sources disagree

Source priority (sector-specific):
- Tech / semis: The Information, Stratechery, SEMI, Counterpoint, Omdia, IDC,
  Gartner; customer earnings calls (MSFT/GOOG/META/AMZN/AAPL/ORCL)
- Biotech / pharma: STAT News, BioPharma Dive, Endpoints, FierceBiotech, FDA
  dashboards, IQVIA
- Financials: American Banker, Fed H.4.1, FDIC quarterly profile
- Energy: Energy Intelligence, OilPrice, Rystad, EIA, Baker Hughes
- Autos: Wards Auto, Automotive News, S&P Global Mobility, NHTSA
- Consumer: Placer.ai, NielsenIQ, Circana
- Cross-sector references in `us-data-sources.md`

Citation discipline per `source-stratification-us.md` — every numeric S-tagged.
Trade-press forecasts typically S5; show provider + methodology + sample size +
freshness.

Length: 2,500-3,500 words. Tables for pricing / share / capacity.

Be a red team — don't accept industry bullishness uncritically. If three of five
sources are bullish but the fourth (respected outlier) sees structural decline,
surface that outlier's case in full.
```

---

## A4 — Capacity, Asset Map & Segment Build

**Mandate**: Build the production-asset inventory and revenue/cost breakdown by segment.

**Required width**: per the B0 conformance backfill assigned in `b0-conformance-diff.md`, A4 produces a **revenue_by_product breakdown of 20-30 rows** and a **revenue_by_geography breakdown of 15-20 rows**. These conform to `equity-research:initiating-coverage` Task 2 expectations and feed `financials.revenue_by_product` and `financials.revenue_by_geography` in `schemas/memo.json`. Mandatory deliverables.

**Prompt template**:

```
You are the Capacity & Capex / Segment Build specialist analyzing [COMPANY]
([TICKER]). Today is [DATE]. You MUST use WebFetch on actual EDGAR filings —
minimum 20 tool calls.

For each major production asset or line of business:

1) Asset / line inventory
   - Name, location, capacity, technology
   - Total project capex ($M), construction start, in-service date
   - Useful life, depreciation method
   - Ownership: US subs typically wholly-owned per 10-K Exhibit 21 (Subsidiaries
     of the Registrant); flag any JVs (10-K Note "Investments in Affiliates")
     or VIEs (10-K Note "Variable Interest Entities" under ASC 810)
   - End markets / customers (named or triangulated)

2) Master asset table — every material asset on one page

3) Capex schedule next 2-3 years
   - Sustaining vs growth capex split
   - Announced capacity expansions ($M, date)
   - Cross-check 10-K Item 7 MD&A + 8-K Item 7.01 project announcements +
     Investor Day decks (8-K Item 7.01 Ex 99.1)

4) Depreciation waterfall — 5y forward, which assets roll off when; capitalized
   R&D under Section 174 (TCJA 2017) separate (5y US / 15y foreign amortization)

5) Segment build — REQUIRED WIDTHS (B0 conformance backfill)
   A) Revenue by product: 20-30 rows
      - Each product line / SKU family / segment sub-cut
      - Last 3y actuals + LTM + forward 2y modeled
      - Cite 10-K Item 1 Business + 10-K Item 8 Note "Segment Information"
        (ASC 280) + 10-Q segment update
      - SaaS: ARR by product line, NRR per product
      - Pharma: per-drug revenue (top 10-15 SKUs)
      - Autos: by vehicle platform / nameplate
      - Diversified consumer: by brand / category
   B) Revenue by geography: 15-20 rows
      - Major countries broken out separately when >5% of revenue
      - Remaining grouped as ROW / EMEA / APAC / LATAM
      - Last 3y + LTM + forward 1y modeled
      - Cite 10-K Item 8 Note "Geographic Information"
      - For multinationals (S&P 500 ~40% foreign rev), note FX translation
        effect from 10-K Item 7A
   These two tables feed `schemas/memo.json` financials.revenue_by_product and
   financials.revenue_by_geography. Required by `equity-research:initiating-
   coverage` Task 2 if user requests DOCX delegation per `tool-composition-us.md`.

6) Ownership / consolidation analysis
   - Wholly-owned vs JV / equity-method investments
   - Material JVs: equity-method income line, share of JV revenue / GM
   - VIEs per ASC 810 — primary beneficiary determination

7) Capex announcements last 24 months
   - 8-K Item 7.01 project announcements
   - 8-K Item 1.01 material agreements (long-term supply, factory builds)

8) Tax-credit overlay where material
   - IRA Section 45X / 48 advanced manufacturing
   - CHIPS Act Section 48D (semis fabs)
   - These materially shift after-tax cash; A7 valuation uses these inputs

Sources: 10-K Items 1, 7, 8 (Segment + Geographic Information Notes), Exhibit 21;
8-K Item 7.01; Investor Day decks; trade press for technical detail.

Citation discipline: every revenue_by_product / revenue_by_geography line
S-tagged. Most S1 (10-K Note) or S2 (10-Q); forward values S3 (mgmt commentary)
or S4 (consensus).

Length: 3,000+ words plus the two mandatory breakdown tables.
```

---

## A5 — Policy & Geopolitics / Regulatory Desk

**Mandate**: Map every active regulatory exposure. Coverage per `regulatory-desk-us.md`.

**Prompt template**:

```
You are the Regulatory & Policy specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. You MUST use WebSearch and WebFetch — minimum 20 calls,
including direct fetches of government sources.

Cover:

1) Antitrust / competition
   - FTC + DOJ Antitrust Division — open matters, Second Request signals,
     consent decree status
   - State AGs (NY, CA, TX, MA in particular)
   - EU CMA (Phase I / Phase II), UK CMA
   - HSR pending notifications if M&A active
   - Sources: ftc.gov/news-events/press-releases, justice.gov/atr, Federal Register

2) Export control / sanctions / inbound FDI
   - BIS Entity List — VERIFY DIRECTLY against
     https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list
     plus Federal Register notice. Distinguish "designated" from "lawmakers
     requested addition" — highest hallucination risk per `verification-
     protocol-us.md`.
   - BIS Unverified List, MEU, Validated End User
   - OFAC SDN — verify at https://sanctionssearch.ofac.treasury.gov
   - CFIUS — inbound FDI review; mitigation agreements
   - ITAR / State Dept DDTC

3) Trade / tariffs
   - USTR Section 301 (China-import tariffs) input exposure
   - Section 232 (national security)
   - AD/CVD cases at ITC + Commerce
   - ITC §337 IP-import investigations

4) Sector-specific regulators
   - Pharma: FDA dashboards.fda.gov; AdCom calendar; CRL / PDUFA dates
   - Telecom: FCC docket search docs.fcc.gov; spectrum auctions
   - Energy: FERC elibrary.ferc.gov
   - Autos: NHTSA recalls; investigations
   - Aerospace: FAA airworthiness directives
   - Environment: EPA ECHO enforcement; CERCLA
   - Consumer finance: CFPB enforcement
   - Banking: OCC / FDIC / Fed supervision; CCAR / DFAST stress tests
   - Healthcare reimbursement: CMS NCD / LCD

5) State-level
   - CA: CCPA / CPRA, CARB, Prop 65, AB5
   - NY: DFS; MA: data-breach; DE: Chancery venue

6) Tax policy
   - BEAT (international affiliate payments)
   - GILTI / FDII
   - Section 174 R&D capitalization (TCJA 2017) — material cash-tax drag for
     R&D-heavy names
   - Pillar 2 Global Minimum Tax 15%, CAMT 15%
   - IRA Section 45X / 48, CHIPS Act Section 48D
   - Wayfair state sales tax nexus
   - Cite specific 10-K Income Tax Note rate reconciliation

7) Securities enforcement
   - SEC Enforcement — Wells notice, AAERs
   - PCAOB inspection findings for company's auditor
   - 10b-5 class actions, derivative suits

8) Scenario tree
   - Status quo / modest tightening / severe / favorable
   - Probabilities sum to 1.00
   - Each scenario: specific trigger event + impact magnitude

9) Kill criteria — specific regulatory events that force exit (per `monitoring-
   framework-us.md` Tier 1). Examples: BIS Entity List addition; FDA Refuse-to-
   File; DOJ antitrust block of pending M&A; ITC §337 exclusion order.

Source verification rules:
- Always verify regulatory designation against actual government source PDF,
  not just legal alerts. "Added", "considered", "proposed", "designated" carry
  different operational meaning.
- Cross-check legal alerts: Hogan Lovells, Crowell & Moring, Skadden, Arnold
  & Porter, Squire Patton Boggs — at least two independent firm alerts.

Length: 2,500+ words. Cite every regulatory claim with URL and date.
```

---

## A8 — Positioning & Sentiment

**Mandate**: Who owns it, how crowded, what consensus is pricing in, what options signal. Coverage per `positioning-sentiment-us.md`.

**Prompt template**:

```
You are the Positioning & Sentiment specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. WebSearch + WebFetch on 13F aggregators, FINRA short data,
options chains, EDGAR Form 4 — minimum 15 calls.

Cover:

1) 13F holdings clusters
   - Top 10-20 institutional holders with quarterly change
   - Concentration: top-5 / top-10 / top-20 share of float
   - New buyers vs sellers last 1-2 quarters
   - Hedge fund vs mutual fund concentration
   - Free aggregators: whalewisdom.com, hedgefollow.com, fintel.io
   - 45-day lag — combine with options + short interest for current crowding

2) Form 4 insider activity
   - Net activity last 90d / 6mo / 12mo (shares + $)
   - Distinguish 10b5-1 plan dispositions (formulaic, less informative) from
     discretionary trades (higher signal)
   - Cluster patterns: 3+ insiders in 5 trading days
   - CEO / CFO outright purchases (rare, high-signal) vs option-exercise-and-sell
   - openinsider.com/screener?s={ticker}, secform4.com

3) 13D / 13G filings
   - 13D (>5% with intent to influence) — Item 4 Purpose of Transaction
   - Proxy contest activity, board-seat demands
   - 13G (passive) — mutual fund / ETF cluster

4) Short interest + days-to-cover
   - FINRA semi-monthly short interest data
   - Days-to-cover = SI / 20-day ADV
   - Stock loan rate as crowding proxy
   - shortinterest.com (free), Ortex / S3 Partners (premium)

5) Options market
   - OI by strike, IV term structure
   - Skew: 25-delta put IV − 25-delta call IV
   - Put/call ratio, gamma exposure (SpotGamma / Vol Suite paid; CBOE for raw)
   - Pinned-event signal: large OI clustering near catalyst expirations

6) ETF passive ownership %
   - Compute from 13F + N-PORT cross-tab on largest ETF holders
   - Index status: S&P 500 (committee), Russell (rules-based annual late June),
     Nasdaq 100 (annual December), MSCI USA / EAFE

7) Sell-side rating distribution
   - % Buy / % Hold / % Sell, PT median + range (1σ dispersion)
   - Revision trend last 3mo / 6mo
   - Sources: Yahoo Finance Analysis, StockAnalysis.com, MarketWatch, TipRanks;
     Visible Alpha if premium

8) Price action — 12mo / 6mo / 3mo / 1mo TR vs S&P 500 + sector ETF + peers;
   52-week range position

9) Sentiment — SeekingAlpha ratings, StockTwits buzz (retail contrarian),
   Substack independent analysts, CFA-society notes

10) Buybacks
    - Active authorization, execution pace
    - 10-Q Note "Share Repurchases" — share count change vs SBC dilution
    - SBC offset adequacy: buyback $ ÷ SBC $; <1.0 means real dilution

11) Crowdedness — under-owned / well-owned / contested; what consensus is
    pricing in (use S4 dispersion as analyst-conviction proxy)

Citation discipline: holding clusters tagged with 13F filing date; options
numbers tagged with date and source.

Length: 2,000+ words.
```

---

## FS — Financial Statements Forensics

**THE MOST IMPORTANT PHASE 1 AGENT.** If FS does not pull actual 10-K / 10-Q / DEF 14A via EDGAR + XBRL company facts API, the entire Phase 1 must be re-run via Phase 1.5 refresh. Coverage per `forensic-accounting-checklist-us.md`.

**Prompt template**:

```
You are the Forensic Accounting / Financial Statements specialist for [COMPANY]
([TICKER]). Today is [DATE]. Public sources only. You MUST use WebFetch on
actual EDGAR filings — minimum 60 tool calls expected.

Pull these documents BEFORE any analysis:

a) Most recent 10-K via EDGAR
   sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K
   Read Items in order: 1, 1A, 7, 7A, 8 (financials + ALL footnotes), 9A
b) Most recent 10-Q
   sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-Q
c) Most recent DEF 14A — read Items 401, 402, 403, 404, 407
d) Last 4 quarters of 8-K Item 2.02 earnings press releases
e) XBRL company facts API for 5y structured financials:
   data.sec.gov/api/xbrl/companyfacts/CIK{cik_10digit}.json
   GOTCHA: CIK must be zero-padded to 10 digits (CIK0001045810 not CIK1045810)
f) Any 8-K Item 4.02 (restatement) in last 5y
g) Last 24 months of Form 4 filings
h) For ADRs use 20-F instead of 10-K (per D11)

Deliver (long memo, 4,000+ words):

1) 5-year + LTM income statement
   - Revenue (consolidated + by segment per ASC 280)
   - COGS, GP, GM trajectory
   - R&D — gross AND capitalized-vs-expensed split (ASC 985-20 / 350-40 +
     Section 174 capitalized)
   - SG&A, operating margin
   - Other income / expense, ETR trajectory + 10-K rate reconciliation
   - GAAP NI + diluted EPS
   - Non-GAAP EPS + full Reg G / Item 10(e) reconciliation; compute non-GAAP /
     GAAP delta as % of NI over 5y
   - UNIT DISCIPLINE: check cover-page unit ($M / $B / thousands). $M vs $B
     confusion is the US analog of China 亿/billion (delta matrix §11).

2) 5-year balance sheet
   - PP&E gross / accumulated dep / net
   - ROU asset under ASC 842
   - Goodwill (flag if material vs net assets; ASC 350 segment-level)
   - Intangibles
   - Inventories (raw / WIP / finished if disclosed)
   - Receivables — DSO trend break is channel-stuffing canary
   - Deferred revenue — declines are SaaS-churn canary
   - Cash + ST investments
   - Total debt (ST / LT / revolver / bond)
   - Pension PBO vs FV plan assets (10-K Note "Employee Benefits") — flag if
     underfunded ratio crosses ERISA threshold
   - Equity: common, APIC, retained earnings, treasury, AOCI

3) 5-year cash flow
   - OCF, capex (in CFI), FCF (compute as OCF − capex; flag if company publishes
     different definition)
   - SBC — added back fully at OCF; check if company's "FCF" deducts SBC
     (G12 hook — real dilution masked if not)
   - Buybacks $ — compare to SBC $ for offset adequacy
   - Dividends, M&A, capital structure changes

4) ASC 606 revenue recognition deep-read
   - Red flags: bill-and-hold, channel stuffing (DSO spike), aggressive POB
     allocation, license front-loading, contract modifications
   - Deferred revenue trend
   - Performance obligation backlog (10-K Note "Revenue Recognition")

5) ASC 842 lease accounting
   - PV of operating lease commitments (ROU asset)
   - Pre-2019 off-BS lease tails still affect FCF comparability

6) ASC 718 stock-based compensation
   - SBC % of revenue (5y trend) and % of OCF
   - Dilution from RSU / option vest schedule
   - Buyback offset adequacy = buyback $ ÷ SBC $; ≥1.0 real return, <1.0
     dilution masked

7) Non-GAAP / GAAP reconciliation (G11 hook)
   - List every non-GAAP adjustment for last 5y
   - Compute delta as % of GAAP NI
   - If >25% sustained, scrutinize: persistent "one-time" restructuring,
     "adjusted EBITDA" excluding SBC + recurring acquisition costs

8) FCF definition disclosure (G12 hook)
   - Document company's stated "FCF" definition (IR pages, press releases,
     10-K MD&A)
   - Flag if SBC excluded
   - Buy-side standard: OCF − capex, no SBC add-back

9) Form 4 net activity (12mo)
   - Net buy / sell volume in $
   - 10b5-1 plan vs discretionary

10) Related-party transactions — DEF 14A Item 404

11) Restatement & going-concern checks
    - 8-K Item 4.02 in last 5y — severe
    - 8-K Item 4.01 (auditor change) — Big-4 → mid-tier flag
    - 10-K Item 9A material weakness disclosure
    - Going-concern qualification on 10-K audit report

12) Auditor + PCAOB inspection
    - Name + tenure (10-K Item 9A)
    - Audit fees + non-audit fees (DEF 14A Item 9)
    - Most recent PCAOB inspection
      (pcaobus.org/oversight/inspections/firm-inspection-reports)

13) Contingencies — 10-K Note "Commitments and Contingencies"; litigation
    reserves; CERCLA; uncertain tax positions (FIN 48 / ASC 740); VIEs (ASC 810)

14) Pension / OPEB (where material) — PBO vs FV plan assets; underfunded ratio
    vs ERISA threshold

15) Red flags & analytical tensions — call out anything that doesn't reconcile;
    cross-check segment GM to consolidated GM; cross-check OCF + capex to FCF

16) Phase 2 questions for forensic deep-dive — items A2 should resolve

Citation discipline: every numeric S-tagged. Most S1 (10-K Item / Note) or S2
(10-Q / 8-K). Non-GAAP figures S2 with explicit Reg G reconciliation reference;
never S1.

Length: 4,000+ words plus tables. Per delta matrix §11, verify guidance against
earnings call transcript, NOT press release.
```

---

## PM Synthesis After Phase 1 — Integrated Brief

After all five Phase 1 specialists return, the PM (you) writes the Phase 1 Integrated Brief. This is NOT a recommendation yet — it is a synthesis and a setup for Phase 2 (`phase-2-continuation-us.md`).

**Required sections**:

1. **Source quality and confidence map** — which agents returned primary-source-verified (≥15 tool calls, EDGAR documents fetched directly) vs framework-only (<10 tool calls). Flag any agent requiring Phase 1.5 refresh.

2. **The setup in one paragraph** — synthesize current state: ticker / sector / cycle position / cap-structure / regulatory posture / positioning posture. No opinions.

3. **The thesis tree** — three competing hypotheses with preliminary weights (typically 30/40/30 at Phase 1; never 60/30/10 yet). Each with one-line falsification criterion.

4. **The 5 things from Phase 1 that change the analytical work** — biggest findings. Specifically: any restatement / going-concern / auditor-change flag from FS; any active regulatory matter from A5; any 13D / activist filing from A8; any segment GM unexplained shift; any major capex announcement from A4.

5. **Conflicts adjudicated** — explicit table of agent disagreements (e.g., A1 says cycle is mid; FS revenue trajectory looks late-peak; reconcile). Don't paper over.

6. **The financial picture in numbers** — verified summary table: revenue / OP margin / FCF / non-GAAP-vs-GAAP delta / SBC % / capex / net debt — 5y + LTM + forward 1y, every number S-tagged.

7. **Preliminary Red Team view** — preliminary bear case (formal Red Team in Phase 2 R agent per `phase-2-continuation-us.md`). What's the strongest S1-S2 fact the bull case ignores?

8. **Phase 2 priorities** — anomalies for A2 to resolve, customers for A3 to triangulate, peers for A3-Peers to compare, monitoring items for A6 to dashboard.

9. **Preliminary direction** — NOT a recommendation. Just direction (mild bullish bias / mild bearish bias / genuinely neutral). Conviction tag (high / moderate / low / source-conditional / reactive per D1).

Save as `outputs/{ticker}_Phase1_Integrated_Brief.md`. Save workpapers as `outputs/{ticker}_Phase1_Workpapers.md`.

If Phase 1.5 refresh is needed, re-dispatch failed agents with explicit instructions to use WebSearch / WebFetch / EDGAR full-text search at efts.sec.gov, and write `outputs/{ticker}_Phase1_Integrated_Brief_v2.md`. Keep v1 marked superseded.

Phase 1 ends with hand-off to Phase 2 (`phase-2-continuation-us.md`).
