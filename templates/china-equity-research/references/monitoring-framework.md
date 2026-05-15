# Monitoring Framework

After the IC memo is delivered, the position requires ongoing monitoring. This framework captures the standard approach.

## Three-Tier Trigger System

Every position has triggers at three tiers. Define them explicitly in the IC memo.

### Tier 1 — Auto-Exit Triggers (any → exit immediately)

Binary, observable, severe events. Examples:
- Regulatory designation (Entity List, NS-CMIC, OFAC SDN, DoD 1260H)
- Major customer formal removal
- Settlement/legal binary outcomes (specific dollar threshold)
- Geopolitical event (export control on critical input)
- Stock gap-down with confirmed bad news

These don't require quarterly re-underwrite. They trigger immediately when observed.

### Tier 2 — Position-Cut Triggers (any → reduce by half)

Significant but not catastrophic. Examples:
- Quarterly EPS miss > 20% with quality concerns
- Operating cash flow YoY decline > 10% for 2 consecutive quarters
- Industry pricing breaks lower > 10%
- Customer pipeline disappointment (specific deadline missed)
- Sell-side consensus revision crossing specific threshold
- Foreign capital structural net selling > 3 consecutive months
- Active congressional/regulatory pressure intensifying (named action)

These triggers are observable in scheduled reporting cycles (quarterly results, Wind data, news flow).

### Tier 3 — Watch / Re-Evaluate (re-think but don't act)

Subtler signals. Examples:
- Industry data trending against thesis without breaking thresholds
- Comparable peer's results disappointing
- Competing technology/product showing momentum
- Management commentary tone change
- Insider activity (small selling)

These trigger re-evaluation at next quarterly review, not immediate action.

## Weekly Monitoring Routine

### Monday Morning (15 minutes)

1. **Stock price** vs. CSI 300 (or relevant benchmark) weekly performance
2. **Northbound holding** 7-day change (data.eastmoney.com/hsgt/StockHdDetail/[code])
3. **Major news scan** — 5 sources, ~3 min each:
   - Sina announcements: vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/[code]
   - Industry trade press (sector-specific)
   - English supply chain (TheElec, DigiTimes, OLED-Info, AppleInsider for tech)
   - 中文 industry coverage (PjTime, Caixin, Yicai)
4. **Industry pricing print** if relevant (e.g., monthly Sigmaintell for displays)

### Wednesday (10 minutes)

1. **Sell-side ratings changes** (Investing.com / MarketScreener / Eastmoney research aggregator)
2. **Customer-side news** (Apple supplier rotations, OEM disclosures)
3. **Government press releases** (BIS, Treasury, House CCP Committee, MIIT/NDRC)

### Friday (10 minutes)

1. **Margin balance** weekly delta (10jqka 融资融券)
2. **Volume / turnover** vs. 20-day average — abnormal spikes
3. **Pending catalyst calendar** review for next 14 days

### Monthly (30 minutes, first Monday)

1. **Re-verify ownership structure** — top-10 shareholders via cninfo quarterly disclosures
2. **Mutual fund holding refresh** — Wind / Eastmoney 持股基金
3. **Industry monthly tracker** publication (Counterpoint, Omdia, DSCC)
4. **Reconcile market data vs. base case operating margin trajectory** — build delta column

### Quarterly (4 hours, after company results)

1. **Full re-underwrite** on quarterly results
2. **Update normalized P&L model** with reported segment splits
3. **Refresh peer comparison** — verify peer's quarterly results too
4. **Refresh sell-side consensus** vs. base case gap
5. **Walk through each Tier 1/2/3 trigger** — fired? closer to firing? receded?
6. **Walk through 5-10 open questions** — any resolved? Any new ones?

## Catalyst Calendar

Specific dated events for next 12-18 months. Maintain in a structured table:

| Date | Event | Bull/Bear/Neutral | Action if Triggered |
|---|---|---|---|
| [Date] | Industry conference / earnings | [Direction] | [Specific action] |
| [Date] | Customer product launch | | |
| [Date] | Regulatory deadline | | |
| [Date] | Quarterly results | | |
| [Date] | Annual report | | |
| [Date] | Discrete event-risk date | | |

For each catalyst:
- **Pre-position**: Days before, what to monitor
- **Day-of**: What signals confirm bull or bear scenario
- **Post**: How to update position based on outcome

## Key Third-Party Voices

Specific named analysts whose calls move the stock. For each:
- **Who** (name, affiliation)
- **What domain** (Apple supply chain, display industry, sell-side analyst)
- **Where to track** (Substack, X/Twitter, paid newsletter, conference talks)
- **Why they matter** (specific historical calls that moved the stock)

For Chinese listed equities, common high-impact voices:
- **Display industry**: Ross Young (DSCC), Hayden Hou (UBI Research), David Hsieh / Jerry Kang (Omdia)
- **Apple supply chain**: Mark Gurman (Bloomberg), Ming-Chi Kuo (TF International), Ross Young
- **Korean trade press**: TheElec, ETNews
- **China sell-side**: Top covering analysts (varies by sector — CITIC, CICC, Tianfeng, Zhongtai, Huatai are large houses)
- **Financial press**: Caixin (premium Chinese coverage), Reuters/Bloomberg China desks

## Preset Alert Triggers (page PM immediately)

Events that should immediately page the PM, not wait for the weekly cycle:

1. Any US administrative action affecting the company or sector
2. Apple supplier rotation announcement (or equivalent for other major customer)
3. Major company corporate action (M&A announcement, capital raise, equity issuance, controlling shareholder change)
4. Northbound flow > [X] in single day
5. Stock price move > [Y]% in single day without obvious benchmark explanation
6. Industry pricing reversal (first negative print after positive trend)
7. Major competitor's yield/production setback
8. Affiliates Rule news in T-60 day window before expiry

## Re-Underwrite Schedule

Schedule explicit re-underwrite at these milestones:

1. **Quarterly results** (mandatory)
2. **Specific catalysts identified in IC memo** (e.g., iPhone 18 supplier confirmation, B16 customer announcement, regulatory disposition)
3. **Annual report** (mandatory — full forensic review)
4. **Significant market moves** (>15% drawdown or rally requires re-underwrite)
5. **Identified pre-set alert triggering**

## What to Do When Triggers Fire

For each trigger that fires:

1. **Document the trigger event** with source URL and date
2. **Re-read the IC memo** — does the underlying thesis still hold?
3. **Check verification matrix** — were any base assumptions invalidated?
4. **Take action per the trigger framework** (auto-exit, half-cut, re-evaluate)
5. **Communicate to stakeholders** with specific reference to the IC memo's pre-defined triggers
6. **Update the IC memo** if the thesis evolves materially

The discipline is to ACT on triggers as defined, not to rationalize them away. This is where most position-management mistakes happen — investors define triggers in the IC memo, then talk themselves out of acting when triggers fire.
