# US Equity Data Sources (Public)

This is the data-source playbook for US-listed equities. Per D5, the plugin operates in **EDGAR-only mode by default** (free, portable). Premium hooks (Visible Alpha, Capital IQ, AlphaSense, Bloomberg) are optional and gated behind explicit user signaling.

Every URL pattern below uses placeholders: `{ticker}` for the exchange ticker (e.g., NVDA), `{cik}` for the EDGAR CIK without padding, `{cik_10digit}` for the 10-digit zero-padded CIK (e.g., `0001045810` for NVDA), `{accession}` for the EDGAR accession number with dashes (e.g., `0001045810-25-000023`), `{accession_nodash}` for the same without dashes.

Sources are organized by **S-tier** (S1 audited → S5 alt-data) plus a cross-cutting **Tier 6** (government / macro / regulatory). Each source is explicitly tagged **free**, **premium**, or **paid per use**.

Per D9, every IC memo MUST execute a minimum of 12 WebSearch + WebFetch calls; this playbook is the lookup table.

---

## Tier S1 — Primary Disclosures (Audited)

### SEC EDGAR (free)

EDGAR is the single source of truth for all US-listed primary disclosures. Everything in S1 and most of S2 lives here. PCAOB-registered auditor opinion + SOX §302/404(b) ICFR opinion make 10-K / 20-F the strongest single S1 in any jurisdiction.

**Filer-status driven 10-K deadlines** (from cover page):
- Large Accelerated Filer (≥$700M public float): 60 days after fiscal year end
- Accelerated Filer ($75M–$700M float): 75 days
- Non-Accelerated Filer / Smaller Reporting Company: 90 days
- Foreign Private Issuer on 20-F: 4 months after fiscal year end (no quarterly 10-Q; 6-K for interim)

### Core EDGAR access patterns

- **Company filings page**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=40` — lists all filings for a CIK.
- **Filings filtered by form type**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K&dateb=&owner=include&count=40` (replace `10-K` with `10-Q`, `8-K`, `DEF 14A`, `S-1`, `S-3`, `13F-HR`, `13D`, `13G`, `4`, `20-F`, `6-K`, etc.).
- **Direct filing index** (per accession): `https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nodash}/` — landing page lists every exhibit + the primary document.
- **XBRL company facts API** (free, structured financials): `https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_10digit}.json` — returns the entire reported XBRL fact set for the issuer across all filings, keyed by GAAP concept. Example NVDA: `https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json`. **Gotcha**: CIK MUST be zero-padded to 10 digits or the endpoint returns 404. Request must include `User-Agent: Firstname Lastname email@example.com` header per SEC fair-access rules.
- **XBRL single-concept API**: `https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_10digit}/us-gaap/{concept}.json` — e.g., concept `Revenues`, `NetIncomeLoss`, `OperatingIncomeLoss`, `Assets`, `LiabilitiesAndStockholdersEquity`. Useful for pulling a single time series quickly.
- **XBRL frames API** (cross-issuer at a point in time): `https://data.sec.gov/api/xbrl/frames/us-gaap/{concept}/USD/CY{year}Q{q}I.json` — every company's reported value of the concept for the period.
- **CIK lookup**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={name}&type=10-K&dateb=&owner=include&count=10` or the JSON CIK ticker file at `https://www.sec.gov/files/company_tickers.json`.

### EDGAR full-text search (efts.sec.gov, free)

The analog of CNINFO targeted search; the primary way to find specific text inside any filing across the entire EDGAR corpus.

- **Web UI**: `https://efts.sec.gov/LATEST/search-index?q=%22{quoted_phrase}%22&dateRange=custom&startdt={YYYY-MM-DD}&enddt={YYYY-MM-DD}&forms={form_type}&ciks={cik}`
- **Human-readable**: `https://efts.sec.gov/LATEST/search-index?q=%22customer+concentration%22&forms=10-K&ciks=0001045810`
- **Example query — find every NVDA 10-K mentioning "Hopper"**: `https://efts.sec.gov/LATEST/search-index?q=%22Hopper%22&forms=10-K&ciks=0001045810`
- **Example query — find all 8-K Item 4.02 restatements industry-wide in 2025**: `https://efts.sec.gov/LATEST/search-index?q=%22Item+4.02%22&forms=8-K&dateRange=custom&startdt=2025-01-01&enddt=2025-12-31`

### 10-K reading map (Item-by-Item)

When asked to "pull the latest 10-K", read these Items in this order:
- **Item 1 Business** — segment structure, named customers (>10% concentration disclosure), geographic split, supplier dependencies.
- **Item 1A Risk Factors** — narrative bear case, written by company counsel; differences vs prior year (track via diff).
- **Item 7 MD&A** — management's discussion; segment results, year-over-year drivers, non-GAAP reconciliation discussion.
- **Item 7A Quantitative & Qualitative Disclosures About Market Risk** — FX, rate, commodity sensitivity tables.
- **Item 8 Financial Statements + Footnotes** — IS, BS, CF, equity, plus Notes (Revenue recognition / ASC 606 disaggregation, Leases / ASC 842, SBC / ASC 718, Income Taxes, Segments, Commitments & Contingencies, Subsequent Events).
- **Item 9A Controls & Procedures** — ICFR opinion, any material weakness disclosed.
- **Item 10–14** — DEF 14A territory cross-references for D&O, comp, board, RPT, auditor fees.

### 20-F (Foreign Private Issuer annual)

`https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=20-F`. Annual report for FPIs; broadly equivalent content to 10-K but follows Form 20-F instructions. Examples: Toyota (TM), Spotify (SPOT), Alibaba (BABA, formerly), AstraZeneca (AZN), Nestlé (NSRGY). Per D11, ADRs are in scope; valuation defaults to USD with native FX disclosed in appendix.

---

## Tier S2 — Other Public Filings

All S2 documents are unaudited public filings on EDGAR. Heterogeneity matters: an 8-K Item 4.02 restatement is higher information value than an 8-K Item 8.01 "other" press release.

### 10-Q (free, quarterly)

- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-Q`
- **Filing deadline**: 40 days post-quarter-end (LAF), 45 days (AF / non-AF). **Q4 results land in the 10-K, NOT a separate 10-Q** — common rookie error.
- **Content**: unaudited interim financials (auditor "review" only under SAS 100, no audit opinion), MD&A update, controls update, subsequent events.

### 8-K (free, material events)

- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=8-K`
- **Filing deadline**: 4 business days after the triggering event (some Items have shorter deadlines).
- **High-signal Items to scan**:
  - **Item 1.01** — Entry into material definitive agreement (M&A, supply, customer)
  - **Item 1.02** — Termination of material agreement
  - **Item 2.02** — Results of operations (quarterly earnings press release)
  - **Item 4.01** — Auditor change (Big 4 → mid-tier is a meaningful red flag)
  - **Item 4.02** — Non-reliance on prior financials (restatement — severe)
  - **Item 5.02** — Departure / appointment of directors / officers (CEO/CFO turnover)
  - **Item 5.07** — Submission of matters to a vote of security holders (annual meeting results)
  - **Item 7.01** — Reg FD disclosure (often investor day decks, conference presentations)
  - **Item 8.01** — Other events (kitchen-sink Item; lowest signal-to-noise)
  - **Item 9.01** — Financial statements & exhibits (where the press release and decks attach as Ex 99.1, 99.2)

### DEF 14A (definitive proxy, free)

- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=DEF+14A`
- **Filed**: ahead of annual shareholder meeting; once a year.
- **High-signal sections**:
  - **Item 401** — Directors and executive officers (background)
  - **Item 402** — D&O compensation (Summary Comp Table; equity grants; pay-vs-performance)
  - **Item 403** — Beneficial ownership (>5% holders, all D&Os)
  - **Item 404** — Related-party transactions (RPT — analog of China 关联交易)
  - **Item 407** — Board independence, committee composition, auditor approval, auditor fees

### S-1 / S-3 / S-4 (registration, free)

- **S-1** — IPO registration; new issuer disclosure; deepest prospectus content
- **S-3** — Shelf registration; for seasoned issuers; faster mechanic for follow-on, ATM, debt issuance
- **S-4** — Securities-component of M&A registration; merger proxy material
- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=S-1` (or S-3, S-4)

### 6-K (FPI interim, free)

- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=6-K`
- FPIs are NOT required to file quarterly 10-Qs; instead they furnish 6-K with whatever home-country interim disclosure they prepare. Typically semi-annual reporting (not quarterly). Be wary of the 6-month information gap when modeling FPIs.

### 13F (institutional holdings, free)

- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=13F-HR`
- **Filed**: within 45 days after each calendar quarter end by managers with ≥$100M AUM in §13(f) securities.
- **What's reported**: long equity positions + options-as-equity (treated as the underlying). **Not reported**: short positions, futures/swaps, cash, foreign securities (mostly), debt.
- **Free aggregators**: WhaleWisdom (whalewisdom.com), HedgeFollow (hedgefollow.com), Fintel (fintel.io), Insider Monkey (insidermonkey.com).
- **Gotcha**: 45-day lag means positioning data is always stale; combine with options + short interest for current crowding signal.

### 13D / 13G (5% blockholders, free)

- **13D**: filed within 10 days when a holder crosses 5% with intent to influence (activist territory). Schedule 13D Item 4 ("Purpose of Transaction") is the highest-signal disclosure.
- **13G**: filed within 45 days when a holder crosses 5% passively (no influence intent). Mutual funds and ETFs typically file 13G.
- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=SC+13D` (or `SC+13G`)

### Form 4 (insider transactions, free)

- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=4`
- **Filed**: within 2 business days of the transaction by §16 reporting persons (directors, officers, 10% holders).
- **Form 3**: initial statement of ownership (filed on becoming an insider).
- **Form 5**: annual catch-up for transactions exempt from Form 4.
- **Free aggregators**: OpenInsider (openinsider.com — by ticker `http://openinsider.com/screener?s={ticker}`), SECForm4 (secform4.com), InsiderInsights.
- **Discipline**: distinguish **10b5-1 plan dispositions** (formulaic, less informative) from **discretionary** trades (higher signal). Cluster C-suite buying is mild bull; cluster selling is mild bear; CEO/CFO outright purchases (rare) are higher-signal than option-exercise-and-sell.

### N-PORT (mutual fund holdings, free)

- **Listing URL**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={fund_cik}&type=NPORT-P`
- Monthly portfolio holdings of registered investment companies (mutual funds, ETFs); first two months of each quarter remain non-public, third month is public 60 days later. Useful for tracking which mutual funds hold a name and at what weight.

### PCAOB Inspection Reports (free)

- **URL pattern**: `https://pcaobus.org/oversight/inspections/firm-inspection-reports` — searchable by audit firm.
- Use case: if a company changes auditors or its current auditor has high inspection-deficiency rates, that's a forensic flag. Cross-check the auditor named on the 10-K cover with the most-recent PCAOB inspection report for that firm.

---

## Tier S3 — Management Commentary

S3 is unaudited, post-filing, often forward-looking — Reg FD §17 CFR 243 requires same-day broad distribution of material non-public information, which makes guidance a contractual disclosure (higher reliability than informal China IR commentary) but still S3 because not audited.

### Earnings call transcripts

The authoritative S3 record. Per D9 and verification protocol §11: **management guidance MUST be verified against the EARNINGS CALL TRANSCRIPT, not the press release.** The 8-K Item 2.02 press release and the call frequently diverge — guidance ranges are sometimes given on the call but headline figures (point estimates) appear in the press release. Always anchor to the call.

- **AlphaSense** (premium) — fastest indexed transcripts, sub-day; entity tagging, theme search.
- **Capital IQ Pro** (premium) — S&P Global; SDC consensus-line search; sell-side notes alongside.
- **SeekingAlpha Pro** (premium, $239/yr) — `https://seekingalpha.com/symbol/{ticker}/earnings/transcripts` — paywalled after free tier.
- **Motley Fool** (free) — `https://www.fool.com/earnings/call-transcripts/{YYYY}/{MM}/{DD}/{slug}/` — slower (T+1 to T+3) but free.
- **Sentieo** (premium, Sphera-owned) — transcript + filings search.
- **Company IR pages** — raw audio/video webcast replays, often live + archive. Pattern: `https://investor.{company}.com/events-and-presentations` or `https://ir.{company}.com/quarterly-results`.

### Investor day decks

Filed as 8-K Item 7.01 (Reg FD) with the deck attached as Exhibit 99.1. Search EDGAR 8-K listing for the IR event date. Often contain medium-term financial framework (3-5yr targets) more detailed than the quarterly call.

### Press releases

Two channels:
- **Company IR pages** — `https://investor.{company}.com/press-releases` or `https://ir.{company}.com/news`.
- **8-K attachment** — Item 2.02 (results) or Item 8.01 (other) with Ex 99.1.

Reg FD §17 CFR 243 — same-day broad distribution required for any material non-public info shared selectively. This is the legal floor; not all "important" disclosures rise to materiality.

### Pre-announcements

Positive or negative warnings issued ahead of the scheduled earnings date, usually via 8-K Item 2.02 with abbreviated tabular data. Per D10, pre-announcement triggers an immediate flash response (within 4 hours). Negative pre-announcement exceeding −5% beat/miss invokes the kill memo template.

### Non-deal roadshow notes

Not publicly filed; accessed via sell-side broker channels, expert networks (GLG, Tegus, AlphaSights — premium), or summary leakage on independent research. Treat as Pending unless multiple independent attendees corroborate.

---

## Tier S4 — Sell-Side and Consensus

US sell-side coverage is denser than China: median NYSE/Nasdaq large-cap has 12–20 covering analysts; SMID has 5–10. Always use **median + dispersion**, not mean. **Free consensus on Yahoo / StockAnalysis is often Refinitiv-derived** — same underlying data, free aggregation.

### Premium consensus

- **Visible Alpha** (premium) — most granular; line-item-by-segment consensus tables; analyst-by-analyst drill-down. Best for modeling segment GM, segment OpEx, and capex assumptions individually.
- **FactSet StreetAccount** (premium) — news + consensus + corporate-actions feed.
- **Bloomberg EE** (Estimates) — `EE <Equity> GO` — terminal-required.
- **Refinitiv IBES** (premium) — long-running consensus history (now LSEG-owned).
- **Capital IQ Pro** (premium, S&P Global) — consensus + sell-side notes + models.

### Free consensus fallback

- **Yahoo Finance Analysis tab**: `https://finance.yahoo.com/quote/{ticker}/analysis` — EPS / revenue consensus by quarter and FY; high/low/avg, # of analysts, surprise history. Default S4 source in EDGAR-only mode.
- **StockAnalysis.com forecasts**: `https://stockanalysis.com/stocks/{ticker_lower}/forecast/` — clean consensus tables, often deeper than Yahoo.
- **Macrotrends**: `https://www.macrotrends.net/stocks/charts/{ticker}/{slug}/eps-earnings-per-share-diluted` — historical EPS time series.
- **WSJ Markets**: `https://www.wsj.com/market-data/quotes/{ticker}` — quote, summary, recent recommendations.
- **MarketWatch**: `https://www.marketwatch.com/investing/stock/{ticker_lower}/analystestimates` — analyst estimates summary.
- **TipRanks**: `https://www.tipranks.com/stocks/{ticker_lower}/forecast` — analyst targets and ratings.
- **Zacks**: `https://www.zacks.com/stock/research/{ticker}/key-statistics` — proprietary rank + free consensus.

Per D5, EDGAR-only mode uses Yahoo Finance + StockAnalysis as the S4 substrate. Per D16, citations look like `(S4: Yahoo Finance consensus EPS $X, n=22, range $Y–$Z)`.

---

## Tier S5 — Alt-Data, Industry Research, Expert Networks

S5 is the broadest tier and the most heterogeneous. Discipline (per source-stratification-us.md): cite specific provider, methodology, sample size, freshness. Never anchor a headline solely on S5.

### Industry research firms (premium)

- **Gartner**: `https://www.gartner.com/en/research` — tech forecasting (cloud, AI, semis, software).
- **IDC**: `https://www.idc.com` — devices, infrastructure, services market sizing.
- **IHS Markit / S&P Global Commodity Insights**: `https://www.spglobal.com/commodity-insights` — energy, autos, chemicals.
- **NielsenIQ**: `https://nielseniq.com` — CPG point-of-sale.
- **Circana** (formerly IRI): `https://www.circana.com` — CPG / consumer.
- **Forrester**: `https://www.forrester.com` — tech / marketing / CX.
- **Counterpoint Research**: `https://www.counterpointresearch.com` — smartphones, semis, IoT.
- **Omdia**: `https://omdia.tech.informa.com` — telecom, display, security, AI.

Most have press-release tier (free) and full-data tier (premium).

### Alt-data providers (premium)

- **Yipit Data**: `https://www.yipitdata.com` — credit-card + receipt + web-scrape KPI tracking by company.
- **Second Measure** (Bloomberg): `https://secondmeasure.com` — credit-card panel.
- **Earnest Analytics**: `https://www.earnestanalytics.com` — card panel, sector-specific.
- **M Science**: `https://www.mscience.com` — alt-data across sectors.
- **Placer.ai**: `https://www.placer.ai` — physical foot traffic (retail, restaurants, travel).
- **SimilarWeb**: `https://www.similarweb.com` — web traffic, app intelligence.
- **AppFigures**: `https://appfigures.com` — mobile app downloads, revenue.
- **Apptopia**: `https://apptopia.com` — app analytics.

### Expert networks (premium, paid per use)

- **GLG** (Gerson Lehrman Group) — largest expert network; consultations $500–$2000/hr.
- **Tegus** — primary-research transcript library; subscription model.
- **AlphaSights** — expert calls.
- **Third Bridge** — expert calls + Forum interview library.

### Sector-specific trade press

- **Tech**: The Information (`theinformation.com`, paywalled), Stratechery (`stratechery.com`, paywalled), Platformer (`platformer.news`).
- **Biotech / pharma**: STAT News (`statnews.com`), BioPharma Dive (`biopharmadive.com`), Endpoints News (`endpts.com`), FierceBiotech.
- **Financials**: American Banker (`americanbanker.com`), Bank Reg Blog (`bankregblog.com`), S&P Global Market Intelligence Bank data.
- **Energy**: Energy Intelligence (`energyintel.com`), OilPrice (`oilprice.com`), Wood Mackenzie (`woodmac.com`, premium), Rystad.
- **Autos**: Wards Auto (`wardsauto.com`), Automotive News (`autonews.com`), InsideEVs.
- **Healthcare services**: Modern Healthcare (`modernhealthcare.com`), Fierce Healthcare.
- **Cross-sector**: Bloomberg Intelligence (premium, terminal), Counterpoint / Omdia / IDC / Gartner (above).

---

## Tier 6 — Government / Macro / Regulatory (cross-cuts S1–S5)

Government primary sources. Free unless noted. These also appear in `regulatory-desk-us.md` for compliance-side use; this section is the source catalog.

### Macro data

- **FRED** (Federal Reserve Bank of St. Louis) — `https://fred.stlouisfed.org/series/{series_id}` — the single most useful free macro source. High-leverage series:
  - `DGS10` — 10Y UST yield (R_f for DCF)
  - `DGS2` — 2Y UST yield
  - `T10Y2Y` — 10Y minus 2Y term spread (recession indicator)
  - `BAMLC0A0CM` — ICE BofA US Corporate Index OAS (IG credit)
  - `BAMLH0A0HYM2` — ICE BofA US High Yield Index OAS
  - `UNRATE` — unemployment rate
  - `CPIAUCSL` — CPI all urban consumers
  - `CPILFESL` — core CPI
  - `GDPC1` — real GDP
  - `INDPRO` — industrial production
  - `DCOILWTICO` — WTI crude
  - `DEXUSEU` — USD/EUR
  - `DTWEXBGS` — broad trade-weighted USD
- **BEA**: `https://www.bea.gov` — GDP, PCE, trade.
- **BLS**: `https://www.bls.gov` — employment, CPI, PPI, productivity, JOLTS.
- **Census Bureau**: `https://www.census.gov` — retail sales, manufacturing, construction, ACS demographics.
- **Federal Reserve**: `https://www.federalreserve.gov` — FOMC statements, SEP, beige book, H.4.1 balance sheet.
- **Treasury**: `https://home.treasury.gov` — issuance schedule, TIC capital flows, OFAC sanctions (below).
- **CBO**: `https://www.cbo.gov` — budget and economic outlook; long-run deficit projections.
- **EIA**: `https://www.eia.gov` — oil, gas, power, renewable; weekly petroleum status (Wednesdays).

### Trade / tariff

- **USTR**: `https://ustr.gov` — Section 301 tariffs (China), trade agreements.
- **USITC**: `https://www.usitc.gov` — Section 337 IP investigations; AD/CVD cases; HTS tariff schedule.
- **CBP**: `https://www.cbp.gov` — Customs and Border Protection; tariff classifications, withhold release orders (UFLPA).

### Antitrust / competition

- **FTC**: `https://www.ftc.gov` — federal civil antitrust + consumer protection; merger reviews; HSR notification database `https://www.ftc.gov/enforcement/competition-matters`.
- **DOJ Antitrust**: `https://www.justice.gov/atr` — federal civil + criminal antitrust.
- **State AGs**: NY (`ag.ny.gov`), CA (`oag.ca.gov`), TX (`texasattorneygeneral.gov`), MA (`mass.gov/orgs/office-of-attorney-general-maura-healey`).
- **EU CMA / European Commission DG COMP**: `https://ec.europa.eu/competition/index_en.html` — Phase I / Phase II decisions.
- **UK CMA**: `https://www.gov.uk/government/organisations/competition-and-markets-authority`.

### Export control / sanctions

- **BIS Entity List**: `https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list`. Updates via Federal Register.
- **BIS Unverified List**: same parent page, separate list.
- **OFAC SDN search**: `https://sanctionssearch.ofac.treasury.gov` — interactive lookup by name. Also bulk list at `https://www.treasury.gov/ofac/downloads/sdn.xml`.
- **CFIUS**: `https://home.treasury.gov/policy-issues/international/the-committee-on-foreign-investment-in-the-united-states-cfius` — inbound FDI review; annual report.
- **ITAR / State Dept DDTC**: `https://www.pmddtc.state.gov` — defense articles export control.

**Critical** (preserves China-skill discipline): always verify a regulatory designation against the actual government source PDF / search tool, not just legal alerts. Alerts use ambiguous wording — "added", "considered", "proposed", "designated" each carry different operational meaning. Same hallucination risk as China Entity List.

### SEC enforcement

- **Litigation releases**: `https://www.sec.gov/litigation/litreleases.htm`
- **AAERs** (Accounting and Auditing Enforcement Releases): `https://www.sec.gov/divisions/enforce/friactions.htm`
- **PCAOB inspections** (above, S2).

### Sector regulators

- **FDA**: dashboards `https://dashboards.fda.gov`; press announcements `https://www.fda.gov/news-events/press-announcements`; drug approvals tracker `https://www.accessdata.fda.gov/scripts/cder/daf/`; device 510(k) `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm`; CDER reports.
- **FCC**: docket search `https://docs.fcc.gov`; spectrum auctions `https://www.fcc.gov/auctions`.
- **FERC**: `https://www.ferc.gov`; eLibrary docket search `https://elibrary.ferc.gov`.
- **NHTSA**: recall portal `https://www.nhtsa.gov/recalls`; investigations.
- **EPA**: `https://www.epa.gov/laws-regulations`; ECHO enforcement `https://echo.epa.gov`.
- **FAA**: `https://www.faa.gov`; airworthiness directives.
- **CFPB**: `https://www.consumerfinance.gov`; enforcement actions; consumer complaint database.
- **OCC**: `https://www.occ.treas.gov`; bank enforcement actions.
- **FDIC**: `https://www.fdic.gov`; quarterly bank profile, problem-bank list.
- **Fed banking supervision**: `https://www.federalreserve.gov/supervisionreg.htm`; CCAR / DFAST stress test results annually.
- **NRC**: `https://www.nrc.gov` — nuclear reactor oversight; ADAMS docket.
- **USDA**: `https://www.usda.gov` — ag, food safety, FSIS recalls.
- **HHS/CMS**: `https://www.cms.gov` — Medicare/Medicaid reimbursement; coverage decisions.
- **NCUA**: `https://www.ncua.gov` — credit unions.

### Litigation

- **PACER**: `https://pacer.uscourts.gov` — federal court docket; **paid per page** ($0.10/page capped $3.00/document; free quarterly threshold $30).
- **CourtListener / RECAP**: `https://www.courtlistener.com` — **free** community RECAP wrapper over PACER documents that someone has already paid for.
- **Lex Machina**: `https://lexmachina.com` — premium IP litigation analytics.
- **RPX**: `https://www.rpxcorp.com` — patent litigation tracking.
- **ITC §337**: `https://www.usitc.gov/secretary/edis.htm` — EDIS docket for import-IP cases.
- **Delaware Chancery**: `https://courts.delaware.gov/chancery/` — corporate / shareholder litigation.

### Federal Register (free)

- **URL**: `https://www.federalregister.gov` — full text of proposed and final rules from every agency.
- **Daily index**: `https://www.federalregister.gov/documents/current`
- **API**: `https://www.federalregister.gov/developers/documentation/api/v1` — search by agency, topic, date.

### Damodaran reference data (free)

- **URL**: `https://pages.stern.nyu.edu/~adamodar/` — implied US ERP (monthly update), industry beta tables, country risk premium, levered/unlevered beta by sector. Default reference for DCF cost-of-equity inputs per `valuation-discipline-us.md`.

### IRS (free)

- `https://www.irs.gov` — corporate tax policy, regulatory guidance, revenue rulings. Relevant for BEAT/GILTI/FDII/Section 174/CAMT analysis (per delta §3 D8).

---

## Use Patterns

### "Pull the latest 10-K"

1. Locate CIK via `https://www.sec.gov/files/company_tickers.json` or company filings page.
2. List 10-K filings: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K`.
3. Open the most recent accession; pull primary `*.htm` document. WebFetch directly.
4. For structured financials, hit XBRL company facts API: `https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_10digit}.json`. Remember zero-pad CIK to 10 digits.
5. Read Items in order: 1, 1A, 7, 7A, 8 (financials + footnotes), 9A. Capture segment table, customer concentration, RPT cross-references, contingencies.

### "Verify a regulatory designation"

1. Identify the specific list (BIS Entity, MEU, Unverified, OFAC SDN, CFIUS forced-divestiture, NS-CMIC).
2. Go to the actual government source (BIS Entity List page, OFAC SDN search). NOT legal alerts.
3. If legal alert is the only easy entry, cross-check at least two independent firm alerts (Hogan Lovells, Crowell & Moring, Skadden, Arnold & Porter, Squire Patton Boggs) — and disambiguate language ("added", "considered", "proposed").
4. Document the Federal Register volume / notice number and the addition date.

### "Identify customer concentration"

1. 10-K Item 1 Business — companies must disclose any customer accounting for ≥10% of consolidated revenue (Regulation S-K Item 101). Customer may be named or anonymized.
2. DEF 14A Item 404 RPT — relevant if customer is also a 5% holder, director, or officer affiliate.
3. Downstream supplier disclosures — e.g., Apple Supplier List, Samsung supplier filings, hyperscaler datacenter capex statements — for triangulation.
4. Expert networks (Tegus / GLG) — when accessible, primary research with channel partners.

### "Verify quarterly results"

1. 10-Q filed within 40/45 days of quarter end; pull from EDGAR.
2. Same-day 8-K Item 2.02 attaches the press release as Ex 99.1 — verify headline numbers consistent with 10-Q (occasional restatement-style revisions exist).
3. Earnings call transcript is the authoritative S3 — per D9, mgmt guidance MUST be verified against the call, NOT the press release. The press release headline and the call commentary frequently diverge (guidance ranges, segment color, capex framing).
4. Watch for pre-announcement risk: if company pre-announced (8-K Item 2.02 with abbreviated tabular data) ahead of the scheduled date, that's the actual S3 anchor and the formal print confirms it.

### "Track insider activity"

1. Form 4 filings within 2 business days; listing at `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=4`.
2. Free aggregators: OpenInsider `http://openinsider.com/screener?s={ticker}`, SECForm4 `https://secform4.com/insider-trading/{cik}.htm`.
3. Discipline: flag 10b5-1 plan dispositions vs discretionary trades. Cluster CEO/CFO purchases > cluster sales > option-exercise-and-sell.
4. Per `forensic-accounting-checklist-us.md`, net Form 4 activity over last 12mo is a mild signal; combine with 13F clusters and short-interest momentum.

### "Pull consensus estimates"

1. Premium first (if available): Visible Alpha for segment-line granularity, FactSet / Bloomberg / Capital IQ for terminal-grade consensus.
2. Free fallback (EDGAR-only mode default): Yahoo Finance `https://finance.yahoo.com/quote/{ticker}/analysis`, StockAnalysis `https://stockanalysis.com/stocks/{ticker_lower}/forecast/`, WSJ `https://www.wsj.com/market-data/quotes/{ticker}`.
3. Use **median, not mean**. Report dispersion (range high to low, or 1σ if available). Note number of analysts and recent revision trend (3mo, 6mo).
4. Citation per D16: `(S4: Yahoo Finance consensus EPS $X, n=22, range $Y–$Z, freshness 3d)`.

### "Source verification protocol per D9"

Minimum 12 WebSearch + WebFetch calls per memo. The protocol enforces:
- Mgmt guidance MUST be verified against earnings call transcript, NOT against press release (Reg FD same-day-distribution doesn't mean the press release matches the call).
- Every post-knowledge-cutoff specific number (anything dated after Jan 2026) MUST be cross-cutoff-verified via WebSearch + WebFetch.
- Regulatory designation MUST be verified against the actual government source list, not the legal alert summary.
- Consensus snapshots MUST include sample size, range, and freshness date.

---

## Common Failure Patterns (US-Specific)

- **Wrong CIK or zero-padding error**. The XBRL API requires 10-digit zero-padded CIK: `data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json` for NVDA (not `CIK1045810`). The browse-edgar UI accepts un-padded CIK; the XBRL JSON API does not.
- **$M vs $B vs thousands confusion**. Some companies report in thousands (smaller filers), most in millions, some in billions. ALWAYS check the unit header on the cover page (e.g., "(in millions, except per-share data)"). Per delta §11, this is the US analog of the China 亿 confusion (10× / 1000× error).
- **Stale earnings transcript**. Model knowledge cutoff is Jan 2026; today's session date is 2026-05-15. ANY earnings disclosed after Jan 2026 MUST be verified via WebSearch + WebFetch. Do not anchor headline math to memorized transcripts.
- **Press release vs call transcript divergence**. Guidance ranges are sometimes given only on the call; headline number in the press release is the point estimate or top-of-range. The call is authoritative S3 — verify against the call, NOT the press release.
- **10-Q vs 10-K period mismatch**. Q4 results land in the 10-K, NOT a separate 10-Q. Looking for a "Q4 10-Q" is a rookie error and will return zero EDGAR hits.
- **Foreign-private-issuer (ADR) confusion**. FPIs file 20-F annually + 6-K for interim; semi-annual reporting (not quarterly). Modeling an FPI as if it filed 10-Qs leads to 6-month information gaps.
- **Class share confusion**. GOOG (Class C, no vote) vs GOOGL (Class A, vote); BRK.A vs BRK.B (different economic + voting rights, 1/1500 economic ratio post-split); FOX vs FOXA; META has only one share class currently but historically had A/B/C distinctions. Verify which class the consensus / 13F / Form 4 is referencing.
- **Form 4 reporting delays**. Some companies file late; check filing date vs transaction date. A Form 4 with a transaction date 30+ days before filing is a late filing — flag for §16 compliance (and rarely useful as a timely signal).
- **EDGAR User-Agent requirement**. SEC fair-access policy requires every programmatic request to set a `User-Agent: Firstname Lastname email@example.com` header. Anonymous bulk requests get rate-limited or 403'd. When using WebFetch, this is usually handled, but custom scripts must set it.
- **Index reconstitution date confusion**. S&P 500 inclusion is committee-discretionary with explicit profitability test + $14.6B float (2024); Russell rebalances rules-based annually late June; Nasdaq 100 annually December. Don't conflate.
- **Consensus aggregator drift**. Yahoo Finance, StockAnalysis, Zacks, MarketWatch all show "consensus" but may pull from different underlying feeds (Refinitiv / Zacks-proprietary / S&P) with different snapshot times. When in doubt, cite the aggregator explicitly.

---

## Cross-References

- Per D5, the plugin runs EDGAR-only by default; premium hooks are optional.
- Per D9, every memo executes ≥12 WebSearch + WebFetch calls using the sources above.
- Per D11, ADRs use 20-F as S1; valuation defaults to USD with native FX in appendix.
- For S-tier discipline and citation format, see `source-stratification-us.md` and schema `schemas/source_tags.json`.
- For forensic-specific source patterns (auditor change 8-K Item 4.01, restatement 8-K Item 4.02, RPT DEF 14A Item 404, ASC 606/842/718 footnote locations), see `forensic-accounting-checklist-us.md`.
- For positioning-specific source patterns (13F clusters, short interest, options OI, Form 4 patterns, ETF flows, index inclusion events), see `positioning-sentiment-us.md`.
- For regulatory-desk-specific source patterns (FTC/DOJ, BIS/OFAC/CFIUS, sector regulators, ITC §337), see `regulatory-desk-us.md`.
- For valuation-input-specific sources (FRED DGS10, Damodaran ERP, sector beta tables, multiple history), see `valuation-discipline-us.md`.
