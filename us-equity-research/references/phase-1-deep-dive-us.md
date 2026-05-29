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

2) Cycle position — explicit classification trough / early-recovery / mid /
   peak / late-peak / downturn, anchored to sector-appropriate indicator
   (semis: SEMI book-to-bill; autos: SAAR + days-supply; energy: Baker Hughes
   rig count + OPEC+ posture; SaaS: net new ARR across peer set; biotech:
   trial-readout density + FDA AdCom calendar; banks: deposit beta + CET1 +
   NCOs).

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

Source priority — sector trade press per `us-data-sources.md` Tier 5 (The
Information / Stratechery for tech; STAT News / BioPharma Dive / Endpoints
for biotech; American Banker for financials; Energy Intelligence / Rystad
for energy; Wards Auto for autos; Placer.ai / NielsenIQ / Circana for
consumer). Customer-side earnings calls for downstream signal.

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

6) Ownership / consolidation — wholly-owned vs JV / equity-method (10-K Note
   "Investments in Affiliates"); material JV equity-method income line; VIE
   primary beneficiary per ASC 810.

7) Capex announcements last 24 months — 8-K Item 7.01 project announcements;
   8-K Item 1.01 material agreements (long-term supply, factory builds).

8) Tax-credit overlay where material — IRA §45X / §48, CHIPS §48D. Materially
   shifts after-tax cash; feeds A7 valuation.

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

Cover (full domain coverage and URLs in `regulatory-desk-us.md`; this prompt
lists what the agent must surface, not how the regulators work):

1) Antitrust / competition — FTC + DOJ Antitrust + state AGs (NY/CA/TX/MA) +
   EU Commission DG COMP + UK CMA. HSR Second Request signal; consent decree
   status; pending Phase II reviews. Materiality threshold per `regulatory-
   desk-us.md`.

2) Export control / sanctions / inbound FDI — VERIFY DIRECTLY against actual
   government sources: BIS Entity List + UVL + MEU + VEU + FDPR; OFAC SDN +
   NS-CMIC + SSI; CFIUS mitigation/divestiture; ITAR/DDTC. Highest-risk
   hallucination class per `verification-protocol-us.md`: lawmaker letter ≠
   ERC recommendation ≠ Federal Register designation. Cite Fed Reg volume/
   page/date for any addition.

3) Trade / tariffs — USTR §301 / §232 input exposure; AD/CVD at ITC + Commerce;
   ITC §337 IP-import investigations. Per `regulatory-desk-us.md`.

4) Sector regulators — FDA (dashboards.fda.gov, AdCom calendar, CRL/PDUFA);
   FCC (docs.fcc.gov, NPRM/R&O); FERC; NHTSA recalls + ODI; FAA AD; EPA ECHO/
   CERCLA; CFPB; OCC/FDIC/Fed banking (CCAR/DFAST); NRC; USDA/FSIS; CMS NCD/
   LCD. Per `regulatory-desk-us.md` for stages and URLs.

5) State-level — CA (CCPA/CPRA, CARB, Prop 65, AB5); NY DFS / Martin Act;
   MA 201 CMR 17; DE Chancery venue.

6) Tax policy — BEAT, GILTI, FDII, §174 R&D capitalization (TCJA 2017 — cash-
   tax drag, 5y US / 15y foreign amortization, material for R&D-heavy names),
   Pillar 2 GMT 15%, CAMT 15%, IRA §45X/§48, CHIPS §48D, §41 R&D credit,
   Wayfair. Cite 10-K Income Tax Note rate reconciliation.

7) Securities enforcement — SEC Wells/AAER, PCAOB inspections for auditor,
   10b-5 PSLRA class actions, Delaware derivative suits, §16(b) short-swing
   recoveries.

8) Scenario tree — status quo / modest tightening / severe / favorable.
   Probabilities sum to 1.00. Each scenario: specific trigger event + impact
   magnitude.

9) Kill criteria — specific regulatory events forcing exit (per `monitoring-
   framework-us.md` Tier 1). Examples: BIS Entity List addition; FDA Refuse-
   to-File; DOJ antitrust block of pending M&A; ITC §337 exclusion order.

Verification: every regulatory designation cited as an investment-thesis
anchor must resolve to an S1 source (Federal Register notice, agency list,
docket entry) with date + identifier. Cross-check against at least two
independent legal firm alerts (Hogan Lovells, Crowell & Moring, Skadden,
Arnold & Porter, Squire Patton Boggs) when interpreting agency action.

Length: 2,500+ words. Every claim S-tagged with URL + date per D16.
```

---

## A8 — Positioning & Sentiment

**Mandate**: Who owns it, how crowded, what consensus is pricing in, what options signal. Coverage per `positioning-sentiment-us.md`.

**Prompt template**:

```
You are the Positioning & Sentiment specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. WebSearch + WebFetch on 13F aggregators, FINRA short data,
options chains, EDGAR Form 4 — minimum 15 calls.

Cover (full source URLs, timing, and field definitions in `positioning-
sentiment-us.md`; this prompt lists what the agent must surface):

1) 13F clusters — top 10-20 institutional holders, QoQ deltas, concentration
   top-5 / top-10 / top-20 % of float, marquee fund cluster moves (Tiger
   Global, Coatue, D1, Lone Pine, Viking, Citadel, Millennium). 45-day lag.

2) Form 4 insider activity — net $ last 90d / 6mo / 12mo. Distinguish 10b5-1
   plan vs discretionary; flag cluster patterns (3+ insiders in 5 trading
   days); CEO/CFO Code-P open-market purchases are the highest-signal pattern.

3) 13D / 13G filings — 13D Item 4 Purpose of Transaction; proxy contest
   activity; 13G passive cluster. Flag any 13D filed in last 12 months.

4) Short interest + days-to-cover — FINRA semi-monthly; DTC = SI / 20-day ADV;
   stock loan rate as crowding proxy. Threshold: SI >10% float warrants
   discussion; >20% is high.

5) Options market — OI by strike, IV term structure, 25-delta put-call skew,
   put/call ratio, gamma exposure, earnings-implied move from straddle.

6) ETF passive ownership % — compute from 13F + N-PORT; index inclusion
   status (S&P 500 / S&P 400 / S&P 600 / Russell 1000/2000/3000 / Nasdaq 100
   / MSCI USA).

7) Sell-side rating distribution — % Buy/Hold/Sell, PT median + 1σ dispersion,
   3mo/6mo revision trend. Use MEDIAN not mean.

8) Price action — 12mo / 6mo / 3mo / 1mo total return vs S&P 500 + sector ETF
   + peers; 52-week range position.

9) Sentiment — SeekingAlpha contributor ratings, StockTwits buzz (retail
   contrarian), Substack independent analysts, CFA-society notes.

10) Buybacks — active authorization, execution pace, share-count change vs
    SBC dilution, buyback-to-SBC ratio (<1.0× means real dilution masked by
    ASR; per `forensic-accounting-checklist-us.md` Item 3 G12 hook).

11) Crowdedness synthesis — under-owned / well-owned / contested / crowded
    long, combining 13F concentration + short interest + options skew + sell-
    side dispersion per `positioning-sentiment-us.md` crowding score.

Citation: holding clusters tagged with 13F filing date; options numbers tagged
with date and source. Per D16 regex on every numeric.

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

4) ASC 606 + ASC 842 + ASC 718 deep-reads — full discipline per `forensic-
   accounting-checklist-us.md` Items 1, 2, 3. Pull and surface for this name:
   - 606: POB structure, deferred revenue trend (SaaS churn canary), DSO break,
     bill-and-hold language, contract modifications
   - 842: ROU asset, lease liability vs net debt for adjusted leverage
   - 718: SBC % of revenue + % of OCF (5y trend), buyback-to-SBC ratio (<1.0
     = dilution masked; ≥1.0 = real return)

7) Non-GAAP / GAAP reconciliation (G11) — per `forensic-accounting-checklist-
   us.md` Item 5. List 5y non-GAAP adjustments; compute delta as % GAAP NI;
   scrutinize if >25% sustained.

8) FCF definition disclosure (G12) — per `forensic-accounting-checklist-us.md`
   Item 3. Document company's stated FCF definition; flag if SBC excluded.
   Buy-side standard: OCF − capex; SBC deducted not added back.

9) Form 4 net activity (12mo)
   - Net buy / sell volume in $
   - 10b5-1 plan vs discretionary

10) Related-party transactions — DEF 14A Item 404

11) Restatement / governance — 8-K Item 4.02 last 5y (severe); 8-K Item 4.01
    (auditor change; Big-4 → mid-tier flag); 10-K Item 9A material weakness;
    going-concern qualification on audit report.

12) Auditor + PCAOB — name + tenure (10-K Item 9A); audit fees + non-audit
    fees (DEF 14A Item 9); most recent PCAOB inspection at
    pcaobus.org/oversight/inspections/firm-inspection-reports.

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

### FS-Banks Augmentation — Conditional on Phase 0 sector ∈ {Financials/Banks, Diversified Banks, Regional Banks, Investment Banking & Brokerage, Insurance, BDC}

**This section is load-bearing for any depository institution, BDC, life/P&C insurer, or broker-dealer. If sector = Financials/Banks and this augmentation is not executed, Phase 1 fails and Phase 1.5 refresh is mandatory.** Bank discipline is the largest single sector gap in v0.1.x and the single most common LLM failure on US equities — banks fail catastrophically under generic income-statement-and-cash-flow analysis because the balance sheet *is* the engine, capital adequacy *is* the constraint, and earnings quality reduces to the AOCI bridge + reserve build trajectory + NIM path. v0.2.0 closes this via the discipline below, verified by Plugin 2 gate **G16**.

The augmentation is additive to the standard FS prompt — execute the standard FS prompt AND the bank-specific extensions below. Output goes into the same FS deliverable, with bank-specific findings in a dedicated "Bank-Specific Forensics" section.

**Bank-specific filings to pull (in addition to 10-K / 10-Q / DEF 14A):**

- **FR Y-9C** (Consolidated Financial Statements for Holding Companies) via Federal Reserve at chicagofed.org/research/data/bhc-data — quarterly, ~3-4 week lag. The Y-9C is the regulator-grade BHC balance sheet and contains line items not in the 10-Q (e.g., line-item RWA breakdown, regulatory capital line items at the BHC level).
- **Call Report (FFIEC 031/041)** via FFIEC at cdr.ffiec.gov for the lead bank subsidiary — quarterly, ~30 day lag. Contains loan-level Schedule RC-N (past due / nonaccrual) and Schedule RC-O (deposit insurance assessment base) detail not in the 10-Q.
- **FR Y-14A** (annual capital stress disclosure) — published as part of Dodd-Frank stress test results, second half each year. Discloses CCAR / DFAST stress capital trajectory under severely adverse macro.
- **Stress Capital Buffer (SCB) determination letter** — published by Fed Q3 each year, sets Category I/II/III bank capital requirement for the next 4 quarters.
- **CCAR / DFAST results** — annual release in late Q1 / early Q2; pre-tax net income, PPNR, ACL, AOCI under severely adverse and adverse scenarios. The CCAR severely adverse stress capital trajectory is the binding constraint on capital return for Category I-IV banks.
- **For insurers**: NAIC Schedule D (investment portfolio detail) and statutory financial statements via individual state insurance department websites. Statutory accounting (SAP) differs materially from GAAP — statutory equity ≈ GAAP equity less DAC less AOCI for life insurers; P&C reserves on SAP basis are larger than GAAP. Solvency II disclosures for European primaries' US subs available via parent's Pillar 3 disclosure.

**Required bank-specific deliverables (extend the standard FS sections):**

**B-1. AOCI bridge and tangible-book reconciliation.** This is the SVB lesson and the single largest analytical gap in v0.1.x bank work. For any bank with material AFS securities portfolio (most regional banks; many G-SIBs to a lesser extent):

   - Report AFS portfolio book value, fair value, and accumulated OCI mark in $B and as % of tangible common equity (TCE). Pull from 10-Q Schedule of AFS Securities or Y-9C Schedule HC-B.
   - Report HTM portfolio book value vs fair value separately. HTM is held at amortized cost on the balance sheet but the fair-value disclosure is required in 10-Q footnotes; the gap is the *unrealized HTM loss*, which is NOT in AOCI but is real economic loss and limits balance-sheet flexibility (selling the HTM book to fund deposit outflows triggers OCI taint that flushes the gap into earnings).
   - Compute tangible book bridge: reported TBVPS → mark-to-market TBVPS = reported TBVPS − (HTM unrealized loss × (1 − tax rate)) / diluted shares. Track YoY change.
   - For Category III/IV banks specifically: AOCI opt-out election status. Most regional banks elected to opt out under the 2019 tailoring rules — AOCI does not flow through CET1 capital, which masks balance-sheet impairment. Disclose whether opt-out applies and what reported CET1 would be without the opt-out.
   - SVB pattern: HTM unrealized loss > 25% of TCE and depositor uninsured concentration > 60% of deposits is the canonical pre-failure signature. Flag if either threshold crossed.
   - S-tag discipline: AFS fair value = S1 (10-K Schedule), AOCI mark = S1, HTM fair value = S1 (10-K footnote), tangible book bridge = S1-computed.

**B-2. CET1 walk with operational risk RWA decomposition.** Regulatory capital is the binding constraint. Walk consists of:

   - Starting CET1 (period-prior 10-Q or Y-9C Schedule HC-R Part I)
   - + Net income attributable to common (period)
   - − Common dividends declared
   - − Net share repurchases
   - − AOCI flow (for AOCI-non-opt-out banks: Category I/II/III above $700B asset size)
   - − Goodwill/intangibles changes (acquisition tail, impairment)
   - − DTA disallowance changes (under Basel III, certain DTAs are CET1 deductible above thresholds)
   - = Ending CET1
   - ÷ Ending RWA
   - = CET1 ratio
   - For Category I-III banks: decompose RWA into credit RWA, market RWA, operational RWA. Operational RWA under Basel III standardized approach (Internal Loss Multiplier + Business Indicator Component) is now disclosed; Basel III Endgame proposes a flat ORWA based on revenue + losses without the ILM offset. The current proposal as of v0.2.0 issuance (May 2026): US final rule on Endgame implementation has been deferred to mid-2027 effective date with phase-in to 2030; track Federal Register for the final rule.
   - For Category IV banks: simplified standardized credit RWA only; no formal market or ORWA decomposition required pre-Endgame, but post-Endgame Category IV becomes subject to the standardized framework.

   **Stress capital buffer (SCB) overlay.** Required CET1 = 4.5% minimum + 2.5% capital conservation buffer + SCB (bank-specific, from Fed determination letter) + GSIB surcharge (Category I only, 1.0%-4.5% from Methodology 2). For most large regionals, total required CET1 lands at 8-10%; for G-SIBs, 11-13.5%. The buffer above required = capital return capacity. Track quarterly.

   S-tag discipline: CET1 ratio = S1 (10-K / 10-Q / Y-9C), SCB = S2 (Fed determination letter), CCAR severely adverse trough = S2 (Fed CCAR release), GSIB surcharge = S2 (Fed Methodology 2 disclosure).

**B-3. NIM and deposit-beta sensitivity grid.** Net interest margin is the dominant earnings driver for most US depositories. The discipline:

   - 5-year NIM trajectory with peer benchmark (peer = same-bucket comparator: large regional vs large regional, G-SIB vs G-SIB, super-community vs super-community).
   - **Asset-side repricing**: walk the loan and securities book by repricing speed. Floating-rate commercial loans reprice within 90 days; fixed-rate residential mortgage and longer-duration securities reprice on amortization schedule. Disclose the % of earning assets repricing within 12 months. Bank 10-K Item 7A market-risk disclosure typically shows a 100bp instantaneous shift sensitivity table — pull this.
   - **Liability-side repricing (deposit beta)**: this is the load-bearing sensitivity. Deposit beta = Δ(deposit rate paid) / Δ(Fed Funds rate over the cycle). Cumulative cycle deposit beta typically lands 30-55% for retail-heavy banks, 55-80% for commercial-heavy banks. Disclose: (a) reported through-cycle deposit beta from earnings call commentary (S3), (b) current quarter incremental deposit beta, (c) mix shift between interest-bearing and non-interest-bearing deposits.
   - **NIM bridge for the most recent quarter**: prior-quarter NIM → asset-side delta (bp) + liability-side delta (bp) + mix delta (bp) + day-count adjustment + accretion (PCD loan accretion if recent M&A; loss-share runoff) = current-quarter NIM. Each bridge item cited to S3 (call) or S2 (10-Q).
   - **Forward NIM scenario**: under current forward curve (S5: FRED `DFF` + OIS curve), what is the NIM 4 quarters forward? Most banks disclose NIM directional bias in earnings commentary (S3).
   - **Deposit-beta normalization timing**: this is the variance flashpoint vs Street. Street typically over-models deposit-beta sticky-down (deposit rates fall slower than Fed Funds when cycle turns). For names where the actual deposit composition is concentrated in money-market and HY savings (rate-sensitive), beta normalization is faster than Street model. This is a recurring Type 5 (timing) consensus variance — see `consensus-variance-us.md`.

   S-tag discipline: reported NIM = S1, deposit beta = S3 (call) or S1-computed, forward curve = S5 (FRED), peer comparison = S4 (FactSet bank coverage).

**B-4. CECL allowance methodology and reserve build trajectory.** Under ASC 326 (CECL), the allowance for credit losses (ACL) is a lifetime-loss forward-looking estimate, not the prior incurred-loss model. ACL trajectory is now an earnings driver in its own right.

   - ACL as % of loans HFI (held for investment) — 5-year trajectory; peer comparison
   - ACL by loan category (10-K Note "Allowance for Credit Losses"): C&I, CRE, residential mortgage, consumer, credit card, auto. CRE concentration is the post-2022 watch item — track CRE ACL specifically.
   - Reserve build/release as % of quarterly PPNR (pre-provision net revenue). A 50bp ACL build on $400B of loans = $2B provision expense — for a bank with $5B quarterly PPNR, that's 40% of PPNR. Reserve release is the symmetric earnings boost. Flag if 4-quarter rolling provision is materially above or below peer median — release-driven earnings beats are low-quality (Street typically models normalized provision).
   - Day-2 CECL adoption impact (one-time CET1 hit at 2020 transition, phased in over 5 years through 2024 — 100% phased in as of v0.2.0). Document.
   - Office CRE specifically (the late-2023/2024/2025 watch sub-category): exposure $ + LTV + GeoConcentration if disclosed in 10-K Item 7. Many regionals disclose office CRE in MD&A as separate sub-bucket; pull explicitly.

   S-tag discipline: ACL = S1, by-category breakdown = S1 (10-K Note) or S2 (10-Q Note), provision expense = S1, peer ACL ratio = S4.

**B-5. OCI roll-through and tangible book volatility.** AOCI changes flow through OCI on the comprehensive income statement, then accumulate on the balance sheet. For AOCI-flow-through banks (Category I-III above $700B): AOCI changes hit CET1 directly. For AOCI-opt-out banks (Category III below $700B + Category IV): AOCI sits on balance sheet but does not affect CET1.

   - Quarterly OCI volatility: track AOCI delta vs benchmark 10Y UST move. AFS-heavy banks: AOCI delta ≈ −(modified duration of AFS book) × (10Y UST move bp) × (AFS book size). A 100bp 10Y move on a $20B AFS book with 5-year modified duration = −$1B AOCI hit, ~5% of TCE for a $20B-TCE regional. Disclose the sensitivity grid.
   - For G-SIBs with large derivative books: AOCI also includes cash-flow hedge mark-to-market. Disclose hedge program structure (10-K Note "Derivatives") and whether it offsets balance-sheet duration risk.
   - Tangible book per share (TBVPS) trajectory: 5-year track vs peer. TBVPS growth = ROE × (1 − payout) − OCI drag. OCI drag has been 100-300bp on TBVPS growth for most regionals 2022-2024 and will reverse symmetrically when rates fall.

**B-6. Stress-test capital trajectory under CCAR / DFAST severely adverse.** For Category I-IV banks (any bank above $100B in assets), CCAR / DFAST severely adverse scenario disclosure is the binding capital return ceiling. The discipline:

   - Pull most recent DFAST / CCAR severely adverse scenario disclosure (Fed publishes in Q2 each year; bank publishes its own midcycle disclosure with 10-K Item 7A).
   - Report stress capital trough (lowest CET1 ratio across the 9-quarter projection) and 4Q PPNR + 4Q ACL + 4Q AOCI under stress.
   - Stress capital buffer (SCB) = max(2.5%, peak-to-trough decline + planned dividend over next 4 quarters). The Fed's SCB determination letter sets this number for the bank for the following year.
   - **Capital return capacity** = (Actual CET1 − Required CET1) × RWA × (next 4 quarters of net income accretion factor). This is the buyback + dividend ceiling. Track quarterly.
   - For non-CCAR banks (under $100B): disclose own internal stress testing methodology and capital adequacy framework. Smaller community banks rely on Tier 1 leverage ratio (>8% well-capitalized PCA threshold) more than CET1.

   S-tag discipline: CCAR / DFAST results = S2 (Fed release / bank 8-K), SCB = S2 (Fed determination letter), required CET1 = S2 (Fed regulation).

**B-7. Category tiering and regulatory currency.** US bank regulation post-2019 tailoring: banks are placed in Category I-IV based on asset size, cross-jurisdictional activity, weighted short-term wholesale funding, non-bank assets, and off-balance-sheet exposure. Each category triggers different regulatory requirements:

   - **Category I** (G-SIBs: JPM, BAC, C, WFC, GS, MS) — full Basel III standards, LCR, NSFR, TLAC, GSIB surcharge under both Method 1 and Method 2 (use higher), AOCI flows through CET1, biennial CCAR, semi-annual DFAST. SCB minimum 2.5%, no GSIB cap.
   - **Category II** ($700B+ assets or cross-jurisdictional): similar to Category I but no GSIB surcharge.
   - **Category III** ($250-700B): SCB applies, modified LCR (85% of full requirement), no NSFR public requirement, AOCI opt-out available, biennial CCAR.
   - **Category IV** ($100-250B): SCB applies, no LCR public requirement, AOCI opt-out, biennial DFAST (no CCAR public release pre-2024 but disclosure required post-Senior Officer Letter).
   - Below $100B: "tailored" — community bank leverage ratio (CBLR) elections common (use 9% Tier 1 leverage in lieu of full Basel III stack).

   Pull current category from the most recent 10-K Item 1 or DEF 14A Compensation Discussion (often referenced for stress testing context). Re-categorization triggers (asset growth crossing $100B, $250B, $700B thresholds) drive multi-year capital requirements increases — this is the central planning question for any large regional approaching a category boundary (e.g., FITB / KEY / MTB at ~$100B; USB / TFC / PNC at ~$500B).

**B-8. Basel III Endgame status and timing.** The Federal Reserve's Basel III Endgame proposal (originally proposed July 2023, re-proposed September 2024 after industry pushback) implements the final Basel III standards in the US. Key impacts: standardized credit RWA replaces the Advanced IRB model for Category I-II banks (increases RWA materially for large banks); operational RWA based on Internal Loss Multiplier × Business Indicator Component (with ILM floored at 1.0 in re-proposed rule — was variable in original); market risk RWA under FRTB. As of v0.2.0 issuance (May 2026): final rule is in interagency review with effective date most likely July 1, 2027, phase-in to 2030. Track Federal Register for final rule publication. **Currency caveat: this section dates fastest in the file — refresh quarterly.**

**B-9. Insurance-specific extensions** (if sector = Insurance, BDC, or PE-affiliated specialty finance):

   - Statutory accounting (SAP) vs GAAP delta — for life insurers, statutory equity ≈ GAAP equity less DAC less goodwill less AOCI. RBC (Risk-Based Capital) ratio is the regulatory capital ratio (>300% well-capitalized). Pull RBC from statutory statements.
   - Reserve methodology: for life insurers, principle-based reserving (PBR) under VM-20 vs formulaic reserves. PBR adoption increases reserves for term life; decreases reserves for universal life with secondary guarantees.
   - Asset duration mismatch: life insurer asset duration vs liability duration. Most life insurers run 30-90% asset-liability duration matched; the gap is the interest-rate exposure.
   - For P&C: combined ratio (loss ratio + expense ratio); reserve development (favorable / adverse); catastrophe loss exposure (Florida wind, California wildfire, Gulf hurricane); reinsurance program structure.
   - BDCs: NAV trajectory, NII coverage of dividend, non-accrual % of fair value (>5% = elevated stress), PIK income % of total income (>30% = quality concern).

**B-10. Anti-patterns specific to bank work (LLM and junior-analyst failure modes):**

   - Applying P/E to a bank without adjusting for AOCI normalization. P/E on stressed earnings during AOCI bleed-out periods over-rewards the discount; AOCI reversal as rates fall produces low-quality TBVPS growth that does not deserve full multiple.
   - Treating ROTCE as a primary multiplier without checking what's in ROTCE (release-driven? trading-driven? PPNR-driven?). Composition matters.
   - Anchoring on absolute CET1 ratio without contextualizing required CET1 (SCB + GSIB surcharge). A 12% CET1 ratio is excess capital for a Category IV bank (required ~8%) but inadequate buffer for a G-SIB (required ~13%).
   - Ignoring the HTM unrealized loss (because it's not in AOCI). HTM losses are real economic losses that constrain balance-sheet flexibility.
   - Treating deposit beta as constant. It is highly path-dependent — early in the cycle, beta is low; late in the cycle, beta accelerates; on the down-cycle, beta is sticky down then accelerates.
   - Confusing "office CRE" with "total CRE." Office is the watch sub-bucket; total CRE includes multifamily / industrial / retail with very different default trajectories.

**G16 gate enforcement.** Plugin 2 gate **G16** validates that any memo with `sector` ∈ {Financials/Banks, Diversified Banks, Regional Banks, Investment Banking & Brokerage, Insurance, BDC} contains:

   (a) AOCI bridge (B-1) — explicit fair value of AFS securities + AOCI mark + HTM unrealized loss disclosed; mark-to-market TBVPS computed,
   (b) CET1 walk (B-2) — explicit period-over-period CET1 ratio with bridge,
   (c) NIM trajectory (B-3) — explicit 5-year NIM trajectory + deposit-beta disclosure,
   (d) Stress capital context (B-6) — explicit SCB + capital-return capacity.

If any of (a)-(d) is absent for a Banks-sector memo, G16 fails and `blocks_score_above` = 7.0. See Plugin 2 `verify_bank_metrics.py` for the verifier.

**Validation tickers for the bank discipline (v0.2.0 self-test set):**
- **JPM** (Category I G-SIB): full-stack discipline including GSIB surcharge.
- **USB** (Category III): SCB + AOCI opt-out + CRE concentration + recent acquisition (Union Bank).
- **MTB** (Category IV, ~$200B): Category IV simplifications + heavy CRE exposure (35-40% of loans).
- **SCHW** (broker-dealer with bank sub): broker-dealer plus depository plus AOCI-heavy AFS book — the post-SVB bank-sub-of-broker case.

For Sprint 1 v0.2.0 acceptance, JPM is the required validation re-run (see CHANGELOG).

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
