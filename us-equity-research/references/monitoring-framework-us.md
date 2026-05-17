# Monitoring Framework (US)

After the IC memo is delivered (per `phase-3-valuation-us.md`) and verified (per `verification-protocol-us.md`), the position requires ongoing monitoring. This framework captures the standard approach. The Phase 2 A6 specialist (per `phase-2-continuation-us.md`) populates the company-specific dashboard during the build; this document is the standing template.

The discipline: **act on triggers as defined, do not rationalize them away.** This is where most position-management mistakes happen — investors define triggers in the IC memo, then talk themselves out of acting when triggers fire.

---

## Three-Tier Trigger System

Every position has triggers at three tiers. Define them explicitly in the IC memo per `ic-memo-template-us.md`.

### Tier 1 — Auto-Exit Triggers (any → exit immediately)

Binary, observable, severe events. Examples (US-specific):
- **BIS Entity List addition** confirmed via Federal Register notice
- **OFAC SDN addition**
- **CFIUS forced divestiture** order
- **FDA Refuse-to-File** on key drug, or **CRL** for a thesis-load-bearing approval
- **Antitrust block** by FTC, DOJ, EU CMA on pending M&A — PI granted by court
- **ITC §337 exclusion order** on key product
- **Customer formal removal** (8-K Item 1.02 disclosure of contract termination by >10% customer)
- **8-K Item 4.02 (restatement)** — non-reliance on prior financials
- **Going-concern qualification** on 10-K
- **Major settlement** crossing pre-defined materiality threshold (specific $ in the IC memo)
- **Stock gap-down with confirmed bad news** (e.g., −15% intraday with material 8-K)

These do NOT require quarterly re-underwrite. They trigger immediately when observed. The IC memo must list specific Tier 1 events for the name.

### Tier 2 — Position-Cut Triggers (any → reduce by half)

Significant but not catastrophic. Observable in scheduled reporting cycles. Examples:
- **Quarterly EPS miss >20%** vs S4 consensus median with quality concern (non-GAAP/GAAP gap widening, DSO blow-out, deferred revenue decline)
- **Operating cash flow YoY decline >10%** for 2 consecutive quarters
- **Industry pricing break >10%** (sector-specific monthly tracker — Counterpoint / Omdia / IDC / Wood Mackenzie / IHS)
- **Customer pipeline disappointment** (specific 8-K Item 1.01 expected announcement window passes without disclosure)
- **Sell-side consensus revision crossing threshold** (median PT cut >10%, or % Buy ratings drops below 40%)
- **Foreign capital structural selling** — visible via 13F clusters shifting, or TIC capital flow data signaling structural foreign-net-selling for 3 consecutive months
- **Regulatory pressure intensifying** — FTC / DOJ Second Request issued, FDA AdCom negative vote, FCC docket trending against company, FERC order issued with adverse remedies
- **§174 cash-tax materializing** materially above book ETR — visible in 10-Q cash tax paid line
- **SBC dilution accelerating** — fully diluted share count growing >3% YoY without offsetting buyback
- **Buyback offset adequacy <0.7×** (buyback $ ÷ SBC $) — real dilution masked
- **Form 4 cluster** — 3+ insiders selling on same side in 5 trading days, not 10b5-1 plan dispositions

### Tier 3 — Watch / Re-Evaluate (re-think but don't act)

Subtler signals. Re-evaluate at next quarterly review, not immediate action.
- Industry data trending against thesis without breaking the Tier 2 threshold
- Peer (sector comp) results disappointing while subject still on track
- Competing technology / product showing momentum
- Management commentary tone change (earnings call transcript sentiment shift)
- Small insider selling (single insider, single transaction, <0.5% of holdings)
- Short interest creeping (rising 10-20% from prior period but not crossing crowding threshold)
- Options IV term structure flattening (less event-pricing in)
- Index inclusion / exit risk approaching (S&P 500 borderline market cap, Russell rebalance window)

---

## Weekly Monitoring Routine

### Monday Morning (15 minutes)

1. **Stock price** vs S&P 500 + sector ETF + peer set (5d / WTD / MTD / YTD)
2. **Form 4 alerts** from `http://openinsider.com/screener?s={ticker}` — any new filings over the weekend
3. **News scan** — major sources by sector (each ~3 min):
   - Tech: The Information, Stratechery, Platformer, Reuters / Bloomberg tech feeds
   - Biotech: STAT News, BioPharma Dive, Endpoints, FierceBiotech, FDA dashboards
   - Financials: American Banker, S&P Global Market Intelligence
   - Energy: Energy Intelligence, OilPrice, Reuters energy
   - Autos: Wards Auto, Automotive News
   - Cross-sector: WSJ Markets, FT US, Bloomberg
4. **EDGAR alert** — any new filings on the name (8-K especially) via
   `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=`

### Wednesday (10 minutes)

1. **Sell-side ratings & revisions** — Yahoo Finance Analysis tab, StockAnalysis forecasts, TipRanks, MarketWatch
2. **Customer-side news** — customer 8-K Item 1.01 / 1.02 supplier rotation; major customer earnings calls within the week
3. **Government press** — FTC, DOJ ATR, BIS, OFAC, Treasury, USTR, EPA, FDA, FCC, FERC, NHTSA (sector-specific)
4. **EIA weekly petroleum status** (Wednesdays) if energy-relevant

### Friday (10 minutes)

1. **Options flow** — CBOE OI changes, IV term structure shifts, large block trades
2. **Volume vs 20-day ADV** — abnormal spikes flag possible information asymmetry
3. **Short interest** if mid-month / month-end FINRA update available
4. **Pending catalyst calendar** review for next 14 days

---

## Monthly Routine (30 minutes, first Monday)

1. **Re-verify 13F clusters** — Whale Wisdom / fintel / HedgeFollow / Insider Monkey for top-10 holder shifts
2. **Mutual fund holdings refresh** — N-PORT filings via EDGAR (60-day lag)
3. **Industry monthly tracker** publication — Counterpoint / Omdia / IDC / Gartner / IQVIA scripts / Yipit / Placer.ai / Earnest
4. **Reconcile market data vs base case** — track delta column: actual vs base case operating margin, revenue trajectory, SBC %
5. **Refresh FRED macro series** that anchor scenarios — DGS10, T10Y2Y, BAMLC0A0CM, UNRATE, ISM, DCOILWTICO, DTWEXBGS

---

## Quarterly Routine (4 hours after company earnings results)

1. **Full re-underwrite** on quarterly results
2. **Update normalized P&L model** with reported segment splits (the revenue_by_product and revenue_by_geography breakdowns from Phase 1 A4 get a fresh data point)
3. **Refresh peer comparison** — verify each peer's quarterly results too (per `phase-2-continuation-us.md` A3-Peers)
4. **Refresh sell-side consensus** vs base case gap — pull post-print consensus + revision velocity
5. **Walk through each Tier 1 / 2 / 3 trigger** — fired? Closer to firing? Receded?
6. **Walk through 5-10 open questions** from the IC memo — any resolved? Any new ones?
7. **Update the IC memo** if the thesis evolved materially. Tag this as a refresh ("v2 after 2026Q1 results"), not a new memo. If the thesis materially flipped, write a kill memo.

---

## Catalyst Calendar (12-18 months)

Maintain in a structured table. Sortable by date / event / direction / action.

| Date | Event | Direction | Action if Triggered |
|---|---|---|---|
| YYYY-MM-DD | FY+0Q+1 earnings print | Bull / Bear / Mixed | [specific] |
| YYYY-MM-DD | Annual 10-K filing | Mixed (forensic refresh) | Re-run forensics |
| YYYY-MM-DD | DEF 14A / annual meeting | Bull / Bear / Neutral | RPT + comp check |
| YYYY-MM-DD | Industry conference (CES / OFC / HBA / JPM Healthcare) | Mixed | Trade-press scan |
| YYYY-MM-DD | FDA PDUFA on Drug X | Bull / Bear binary | Tier 1 trigger if CRL |
| YYYY-MM-DD | FCC docket close / FERC order window | Bull / Bear | Sector-specific |
| YYYY-MM-DD | M&A close target | Bull / Bear binary | 8-K Item 2.01 |
| YYYY-MM-DD | FOMC SEP release | Bull / Bear (rate-sensitive) | Stress overlay |
| YYYY-MM-DD | Russell rebalance | Mixed (passive flow) | Index inclusion check |
| YYYY-MM-DD | S&P committee meeting | Mixed | If borderline inclusion |

For each catalyst:
- **Pre-position**: days before, what to monitor
- **Day-of**: what signals confirm bull or bear scenario
- **Post**: how to update position based on outcome

---

## Key Third-Party Voices to Track

Specific named analysts whose calls move the stock. For each:
- **Who** (name, affiliation)
- **What domain**
- **Where to track** (Substack, X/Twitter, paid newsletter, conference talks)
- **Why they matter** (specific historical calls that moved the stock)

By sector (representative — refresh by sub-sector):

### Tech / semis
- **Pierre Ferragu** (New Street Research) — datacenter, AI semis
- **Stacy Rasgon** (Bernstein) — semis, broader chip stack
- **Mark Lipacis** (Evercore ISI) — semis architecture
- **Tim Arcuri** (UBS) — memory, foundry
- **Vivek Arya** (BoA) — semis
- **Dylan Patel** (SemiAnalysis Substack) — semis supply chain, AI infrastructure
- **Doug O'Laughlin** (Fabricated Knowledge Substack) — semis ecosystem
- **Mark Gurman** (Bloomberg) — Apple supply chain
- **Ming-Chi Kuo** (TF International) — Apple supply chain
- **Ben Thompson** (Stratechery) — tech strategy

### Software / SaaS
- **Mark Murphy** (JPM) — large-cap software
- **Brad Sills** (BoA) — SaaS
- **Karl Keirstead** (UBS) — enterprise software
- **Brent Thill** (Jefferies) — internet, software

### Biotech / pharma
- **Tim Anderson** (Wolfe Research) — large-cap pharma
- **Geoff Meacham** (BoA) — biotech, pharma
- **Olivia Brayer** (Cantor) — SMID biotech
- **Terence Flynn** (Morgan Stanley) — biotech
- **Adam Feuerstein** (STAT News) — biotech reporter
- **Damian Garde** (STAT News) — biotech reporter

### Energy
- **Doug Terreson** (Evercore ISI) — integrated oils, refiners
- **Devin McDermott** (Morgan Stanley) — E&P
- **Bob Brackett** (Bernstein) — E&P, services
- **Stephen Richardson** (Evercore ISI) — E&P
- **Doomberg** (Substack) — energy macro, contrarian

### Banks / financials
- **Mike Mayo** (Wells) — large-cap banks
- **Ebrahim Poonawala** (BoA) — banks
- **Glenn Schorr** (Evercore ISI) — broker-dealers, asset managers
- **Charles Peabody** (Portales) — banks, independent
- **Marty Mosby** (Vining Sparks) — regional banks

### Autos
- **Adam Jonas** (Morgan Stanley) — autos, EVs
- **Dan Levy** (Barclays) — autos
- **Itay Michaeli** (Evercore ISI) — autos

### Consumer / retail
- **Oliver Chen** (TD Cowen) — softlines retail
- **Robby Ohmes** (BoA) — restaurants
- **Sara Senatore** (BoA) — restaurants
- **Brian Nagel** (Oppenheimer) — retail

### Macro / cross-sector
- **David Kostin** (Goldman) — US equity strategy
- **Mike Wilson** (Morgan Stanley) — US equity strategy
- **Savita Subramanian** (BoA) — US equity strategy
- **Doug Cifu / Andrew Brenner** (NatAlliance) — rates macro

This list is illustrative. Each name's coverage list shifts; refresh quarterly.

---

## Preset Alert Triggers (page PM immediately, do not wait for weekly cycle)

Events that should immediately alert the PM:

1. **Form 4 cluster** — 3+ insiders selling in 5 trading days, not 10b5-1 plan dispositions
2. **13D filing** on the name (Item 4 Purpose of Transaction is the high-signal field)
3. **FDA decision letter** posted (approval / CRL / delay)
4. **AdCom outcome** announced
5. **Antitrust action** announcement — FTC / DOJ / EU CMA / UK CMA
6. **ITC §337 filing** or **determination** on the name
7. **8-K Item 4.02** (restatement) on the name, or anywhere in close peer set
8. **8-K Item 4.01** (auditor change) on the name
9. **Fed FOMC dot-plot shift** (rate-sensitive names)
10. **Stock move >5σ** in single day vs S&P 500 with no clear benchmark cause
11. **Unusual options activity** — large block, unusual strike, expiration clustering near catalyst date
12. **BIS Entity List update** — Federal Register notice
13. **OFAC SDN list update**
14. **Major customer 8-K Item 1.02** (termination of material agreement) where subject is a counterparty

---

## Re-Underwrite Schedule

Schedule explicit re-underwrite at these milestones:

1. **Quarterly results** (mandatory) — full update cycle
2. **Specific catalysts identified in IC memo** (PDUFA date, FCC docket close, M&A close, FOMC meeting, etc.)
3. **Annual 10-K filing** (mandatory — full forensic refresh per `forensic-accounting-checklist-us.md`)
4. **Significant market moves** — >15% drawdown or >15% rally requires re-underwrite
5. **Preset alert triggering** — any of the items above

---

## What to Do When Triggers Fire

For each trigger that fires:

1. **Document the trigger event** with source URL and date (per `verification-protocol-us.md` discipline)
2. **Re-read the IC memo** — does the underlying thesis still hold?
3. **Check the verification matrix** — were any base assumptions invalidated?
4. **Take action per the trigger framework**:
   - Tier 1 → auto-exit
   - Tier 2 → reduce by half
   - Tier 3 → watch list; re-evaluate at next quarterly
5. **Communicate to stakeholders** with specific reference to the IC memo's pre-defined triggers — show that the action was pre-committed, not reactive
6. **Update the IC memo** if the thesis evolves materially. Tag as a refresh (v2, v3) or — if materially flipped — write a kill memo

The discipline is to ACT on triggers as defined. This is where most position-management mistakes happen — investors define triggers in the IC memo, then talk themselves out of acting. Pre-commitment to the trigger framework is the protection.

---

## Earnings-Cycle Special Handling

Per D10, pre-announcement detection has special handling:

- **Pre-announcement detection**: if company files 8-K Item 2.02 with abbreviated tabular data ahead of scheduled earnings date, trigger immediate flash response (within 4 hours). Use `earnings-flash-template.md`.
- **Negative pre-announcement >5% beat/miss** vs S4 consensus median — invoke the kill memo flow.
- **Positive pre-announcement** — run earnings flash; update Tier 2/3 triggers; check whether to upgrade.

Standard quarterly earnings cycle:

- **T−7 days**: earnings prep night-before checklist activates (`earnings-prep-template.md`)
- **T−1 day**: final consensus snapshot, KPI guide, management-commentary watch list, beat/miss scenario tree, options-implied move
- **T (print day)**: earnings flash at +30 minutes (`earnings-flash-template.md`) — print vs consensus, guidance change, KPI delta, scenario weight update, what-would-reverse trigger check, position-sizing recommendation
- **T+1 day**: full update memo if material; otherwise just note in monitoring log
- **T+4 hours through T+1 day**: pull earnings call transcript when available (Motley Fool free, T+1 to T+3 lag; AlphaSense / SeekingAlpha Pro premium near-real-time). Verify guidance against transcript per delta matrix §11.

---

## Cross-References

- For the IC memo template that defines triggers, see `ic-memo-template-us.md`.
- For earnings prep + earnings flash templates, see `earnings-prep-template.md` and `earnings-flash-template.md`.
- For the verification discipline that catches false-positive triggers, see `verification-protocol-us.md`.
- For S1-S5 source discipline applied to trigger evidence, see `source-stratification-us.md`.
- For the Phase 2 A6 specialist who populates this dashboard during the build, see `phase-2-continuation-us.md`.
- For position-sizing decisions when triggers fire (Tier 1 exit, Tier 2 half-cut, Tier 3 watch), see `position-sizing-us.md`.
- For the kill memo flow on Tier 1 trigger firing, see `kill-memo-template.md` (when available).
- For the catalyst calendar interop format with `equity-research:catalyst-calendar`, see `tool-composition-us.md`.
