# Phase 1: Five-Agent Initial Deep-Dive

Dispatch all five agents in **a single message with parallel Agent tool calls**. Sequential dispatch wastes hours.

Each agent receives: company name, ticker, mandate (long-only / hedge fund), horizon, and the Phase 0 hypothesis tree.

---

## A1 — Industry & Cycle Desk

**Mandate**: Map the industry's cycle position. Where in the cycle are we? Who's winning supply/demand? What catalysts move prices?

**Prompt template**:

```
You are the Industry & Cycle Desk specialist on a buy-side fundamental research team
analyzing [COMPANY] ([TICKER]). Today is [DATE]. Use only public sources.
You MUST use WebSearch and WebFetch — minimum 15 calls.

Your job is industry context, not company-specific analysis.

Deliverables:
1. Industry structure: market size by segment (last 3 years + forward 3),
   key producers with approximate share, recent consolidation events
2. Cycle position: where are we (trough/early-recovery/mid/peak/late-peak/downturn)?
   Pull current product pricing data, capacity utilization, channel inventory
3. Supply/demand: capacity additions globally, demand drivers, end-market health
4. Top 5-8 catalysts for the next 6-18 months with directional impact
5. Bull case + bear case with specific falsifying observations
6. Confidence and gaps section flagging what couldn't be verified

Source priority:
- Industry trade press (sector-specific — for displays: Sigmaintell/DSCC/Omdia/TrendForce;
  for semis: SEMI/IC Insights; for autos: IHS/S&P)
- Customer-side disclosures (downstream company earnings calls)
- Equipment supplier order books (leading indicator)

Cite every numeric. Length: 2,500-3,500 words. Tables for pricing/share data.
Be a red team — don't accept industry bullishness uncritically.
```

---

## A4 — Capacity / Capex / Production Map

**Mandate**: Build the production-asset inventory. Line-by-line. Capex schedule. Depreciation timing. Critically: **minority interest ownership at the asset level**, which sell-side often skips.

**Prompt template**:

```
You are the Capex / Production Modeling specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. Public sources only.
You MUST use WebFetch on actual company filings.

For each major production asset (factory line, fab, mine, fleet), produce:
- Asset name/code, location, capacity, technology
- Total project capex (RMB bn), with split: listco share vs. local government LP share
- Construction start / mass production date
- Ownership structure: parent stake, local LP funds (provincial/municipal investment vehicles)
- Depreciation status: when did MP start, useful life assumed, when rolls off
- End markets / customers

Then produce:
A) Master asset table
B) Capacity-by-tech-node summary
C) Depreciation waterfall by year (which assets roll off when, P&L impact)
D) Sustaining vs growth capex split for current and next 2 years
E) Ownership / minority interest analysis: for each fab subsidiary, what % does
   listco own economically vs. local government LPs? This is critical for understanding
   how much of consolidated EBITDA accrues to listco shareholders.
F) Recent capex announcements last 24 months
G) Put/call clauses on local government LP equity (these are often disclosed in
   the LP counterparty's bond rating reports, not in the listco's filings)

Sources:
- Company annual report 主要子公司 footnote
- Company annual report 在建工程 (CIP) footnote
- CNINFO 关联交易公告 / 重大投资公告 for each fab subsidiary
- Trade press for technical details
- LP counterparty bond rating reports (for put/call clauses) — search SSE/SZSE bond
  market for [provincial/municipal investment company] credit rating reports

Length: 3,000+ words plus extensive tables. Cite source for every number.
```

---

## A5 — Policy, Subsidy & Geopolitics

**Mandate**: Map the policy environment. Industrial policy. Subsidy regime. US/allied restriction risk. Controller structure.

**Prompt template**:

```
You are the Policy & Geopolitics specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. You MUST use WebSearch extensively.

Cover:

1) China industrial policy framework: Five-Year Plan provisions for the sector,
   MIIT/NDRC/big fund involvement, provincial industrial policies, "whole-industry-chain"
   localization status

2) Government subsidy detail:
   - Asset-related vs operating-related subsidies (CAS 16 classification)
   - Run-rate as % of net income — historical 5-year
   - Deferred income balance ("tank" of asset-related subsidies waiting recognition)
   - Subsidy sustainability under current Five-Year Plan direction

3) US export controls / restriction lists:
   - VERIFY DIRECTLY against source: BIS Entity List, MEU List, NS-CMIC List,
     OFAC SDN, Pentagon 1260H List
   - Do not accept "designated" claims without checking the actual list
   - Distinguish "designated" from "lawmakers have requested addition"
   - This is the highest-risk hallucination zone in agent research

4) Customer geopolitics: major customer relationships and political exposure

5) Domestic regulatory: A-share market regulation (CSRC dividend mandates, refinancing
   rules, ESG disclosure)

6) Controller structure: pull the actual controlling shareholder chain. For Chinese
   listcos, this often runs through state-owned holding companies. Identify Beijing
   SASAC / provincial SASAC / central SASAC level.

7) Scenario tree: probability-weighted policy scenarios (status quo / modest tightening
   / severe tightening / subsidy normalization)

8) Kill criteria: specific policy events that force exit

Sources:
- Direct search of government source lists (DoD 1260H official PDF, BIS website,
  Federal Register, OFAC SDN Search)
- Legal alerts (Hogan Lovells, Crowell, Squire Patton Boggs, Skadden — these
  publish detailed analysis of each list update)
- MIIT/NDRC/CSRC official announcements
- Caixin/Reuters/Bloomberg/FT for policy coverage

Length: 2,500+ words.
```

---

## A8 — Positioning & Sentiment

**Mandate**: Who owns it, how crowded, what's the consensus, what's the market saying.

**Prompt template**:

```
You are the Positioning & Sentiment specialist analyzing [COMPANY] ([TICKER]).
Today is [DATE]. Use Eastmoney / Sina Finance / CNINFO / Xueqiu / HKEX.

Cover:

1) Shareholder structure: top 10 shareholders, controlling shareholder, free float,
   recent significant changes (last 4 quarters)

2) Northbound (HK Stock Connect): current foreign holding, 12-month trajectory,
   index inclusion (MSCI/FTSE), passive ETF ownership
   IMPORTANT: HKSCC nominee total includes Stock Connect AND non-Stock-Connect
   custody. They can move in opposite directions. Distinguish.

3) Mutual fund positioning: 公募基金 quarterly top-10 disclosures, # of funds,
   total value, marquee star manager presence

4) Margin / short interest: 融资融券 balance, % of free float, trend

5) Sell-side consensus: # analysts, Buy/Hold/Sell distribution, target price range,
   dispersion (narrow = low conviction signal), recent rating changes

6) Price action: 12mo / 6mo / 3mo / 1mo, vs. CSI 300, vs. peers, 52-week range

7) Sentiment: 龙虎榜 large-trade activity, Eastmoney 股吧 / Xueqiu retail tone,
   news flow last 30 days

8) Insider activity: management buying/selling, major shareholder pledges,
   buybacks (with specific structure: cancellation vs. equity incentive)

9) Financing: equity issuances (SPO, convertible, GDR) last 24 months,
   convertible bond outstanding, dilution potential

10) Crowdedness assessment: is this an under-owned / well-owned / contested name?
    What is consensus pricing in?

Sources:
- Sina Finance: vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/[code]
- Eastmoney: data.eastmoney.com/stockdata/[code], data.eastmoney.com/hsgt/StockHdDetail/[code]
- CNINFO for shareholder filings
- 10jqka for margin balance
- Investing.com / MarketScreener for sell-side consensus

Length: 2,000+ words. Cite specific numbers with dates.
```

---

## FS — Financial Statements Forensics

**Mandate**: Pull and forensic-read the actual financial statements. This is the foundation everything else builds on. **The most important Phase 1 agent.**

**Prompt template**:

```
You are the Forensic Accounting / Financial Statements specialist for [COMPANY] ([TICKER]).
Today is [DATE]. Public sources only.
You MUST use WebFetch on actual annual reports — minimum 60 tool calls expected.

Pull:
- Most recent annual report PDF from CNINFO (search by ticker)
- Most recent quarterly report
- Prior-year annual report for comparison
- 5 years of financial highlights via Eastmoney F10 JSON API:
  https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_F10_FINANCE_GINCOME&filter=(SECUCODE=%22[code].SZ%22)
  (also GBALANCE, GCASHFLOW, FN_MAINOP for segments)

For PDFs, use Bash with curl + pdftotext to extract content, then grep for specific notes.

Deliver (long memo, 4,000+ words):

1) Income statement 5-year + latest quarter (RMB 亿 units carefully):
   - Revenue by segment if disclosed
   - Gross profit, gross margin trajectory
   - SG&A, R&D (with capitalized vs. expensed split)
   - 其他收益 (other income — operating subsidies)
   - 营业外收入/支出 (non-operating income/expense — asset-related subsidies)
   - 公允价值变动损益 (fair value changes)
   - 投资收益 (JV/associate equity-method)
   - 资产减值 / 信用减值 (impairments)
   - Net income to parent vs. minority interest split
   CAREFUL WITH UNITS: Chinese reports use 亿 (100 million). 1亿 = RMB 100m =
   RMB 0.1bn. Don't confuse 亿 with bn — that's a 10x error.

2) Balance sheet 5-year:
   - PP&E, CIP (with breakdown of major projects under construction)
   - Inventories (with composition: raw materials / WIP / finished goods —
     the composition matters for cycle interpretation)
   - Cash, debt, bonds payable
   - Deferred income (asset-related subsidy "tank")
   - Equity to parent vs. minority equity

3) Cash flow 5-year:
   - CFO, capex, FCF
   - Cash subsidies received specifically (separate disclosure usually exists)
   - Cash from new equity / minority equity raises (subsidiary-level LP injections)
   - Dividends paid

4) Government subsidy DEEP DIVE (mandatory):
   - Asset-related vs income-related split
   - Recognition through 其他收益 vs 营业外收入
   - Subsidy as % of NI to parent — calculate by year
   - Deferred income tank balance and movement
   - Subsidy as % of operating profit
   - This often determines whether reported earnings reflect operating economics
     or are a transfer payment

5) Minority interest DEEP DIVE:
   - For each material subsidiary: name, listco economic %, revenue, net profit
   - Most disclosed in the consolidated subsidiaries footnote
   - Important MI subs (typically 5+ for capex-heavy industrials) often
     get aggregate disclosure of MI equity, revenue, net loss/profit, OCF
   - Critical for understanding gap between consolidated and listco-attributable EPS

6) Normalized earnings bridge (5-year):
   Reported NI to parent
   - Less: total subsidies (after-tax)
   - Less: asset disposal gains
   - Less: fair-value gains (after-tax)
   - Less/Plus: investment income from JVs (case by case)
   = Cash earnings ex-subsidy
   
   Compare cash earnings trajectory to reported. If cash earnings have been
   negative or near-zero through cycle, that's a critical finding.

7) Capex vs depreciation 5-10 year:
   - Annual capex vs annual D&A
   - Cumulative capex vs cumulative D&A
   - Tells you: harvest mode (capex < D&A) or reinvestment treadmill (capex > D&A)

8) Working capital metrics:
   - Inventory days, receivable days, payable days
   - Cash conversion cycle trend

9) Debt structure:
   - Composition (bank loans, bonds, short-term, long-term)
   - Coupon range
   - Maturity ladder if disclosed
   - Interest cover

10) Related-party transactions:
    - Identify controlling shareholder umbrella entities
    - Material RPT volume

11) Segment performance if disclosed

12) Red flags & analytical tensions: explicitly call out anything unusual

13) Phase 2 questions for forensic deep-dive

Length: 4,000+ words. Cite specific note numbers. Tables liberally.
Be a red team — flag everything that doesn't reconcile.
```

---

## PM Synthesis After Phase 1

After all five agents return, the PM (you) writes the Phase 1 Integrated Brief.

**Required sections**:

1. **Source quality and confidence map** — which agents returned primary-source verified vs. framework only?
2. **The setup in one paragraph** — synthesize current state
3. **The thesis tree** — three competing hypotheses with preliminary weights
4. **The five things from Phase 1 that change the analytical work** — biggest findings
5. **What the data says about cycle position** — reconcile A1 framework with FS data
6. **Conflicts surfaced and adjudicated** — explicit table of agent disagreements
7. **The financial picture in numbers** — verified financial summary
8. **Red Team summary** — preliminary bear case (formal Red Team comes in Phase 2)
9. **Phase 2 priorities** — what gates the next phase
10. **Preliminary view** — explicitly NOT a recommendation, just direction

Save as `[Company]_Phase1_Integrated_Brief.md`. Save the five workpapers as `[Company]_Phase1_Workpapers.md`.

If Phase 1.5 refresh is needed, write `[Company]_Phase1_Integrated_Brief_v2.md` after refresh and tag corrections explicitly. Keep v1 for record but note it's superseded.
