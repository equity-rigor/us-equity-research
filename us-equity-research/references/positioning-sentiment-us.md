# US Positioning & Sentiment Desk

Desk reference for the `positioning_sentiment` block of `schemas/memo.json`. Covers every required field plus the supporting context needed to fill it from public sources. Per D9, this work is part of the 12-call minimum WebSearch+WebFetch budget; per D5, all primary sources below are accessible in EDGAR-only mode with optional premium hooks.

This file is the analog of China-side A8 (Positioning & Sentiment). Northbound / 公募基金 / 龙虎榜 are replaced by 13F + Form 4 + short interest + options + ETF flows + index inclusion + activist filings + foreign ownership.

Citation discipline (D16): every field below ends in the memo as `(<Stier>: <source>, <date>, <freshness>)`. Aggregator citations should name the aggregator AND the underlying filing (e.g. `(S2: WhaleWisdom 13F snapshot 2026-04-15 reflecting 13F-HR filings for Q1 2026, n=87 holders)`).

---

## 1. 13F Institutional Holdings

**Field**: `top_holders_13f[]` (holder, shares_m, pct_so, qoq_delta_pct).

**Where**:
- EDGAR direct: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=13F-HR` returns 13F filings BY managers whose CIK matches; to find managers holding a TICKER, use aggregators.
- WhaleWisdom (`whalewisdom.com/stock/{TICKER}`) — free 13F-by-stock view; identifies top holders, new-buyers/sellers QoQ, hedge-fund cluster moves.
- HedgeFollow (`hedgefollow.com/stock/{TICKER}`) — alternate view, lighter UI.
- Fintel (`fintel.io/so/us/{TICKER}`) — ownership summary, includes mutual fund + 13F.
- InsiderMonkey (`insidermonkey.com/insider-trading/company/{slug}/`) — hedge-fund-focused.
- N-PORT for mutual fund holdings (S2): `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={fund_cik}&type=NPORT-P`.

**Timing**:
- 13F filing deadline: 45 days after calendar quarter end (Q1 → mid-May; Q2 → mid-Aug; Q3 → mid-Nov; Q4 → mid-Feb).
- Positioning data is ALWAYS at minimum 45 days stale — never current. Combine with options + short interest for a real-time crowding read.
- N-PORT: first two months of each quarter are non-public; third month publishes 60 days after quarter end.

**What to capture**:
- Top-10 holders by share count, % of shares outstanding.
- Concentration: top-5 hedge funds' aggregate % holdings (the "crowding-in-marquee-funds" signal).
- QoQ delta per top holder: new positions, eliminated, increased >25%, decreased >25%.
- Cluster analysis: which marquee funds (Tiger Global, Coatue, D1, Lone Pine, Viking, Citadel, Millennium, Renaissance, Two Sigma, Bridgewater) own and how they moved. New-buyer cluster among 3+ marquee funds is a mild bull signal; cluster-selling is mild bear.
- Mutual fund weight: aggregate weight in S&P 500-tracking + actively-managed mutual funds via N-PORT.

**Signal interpretation**:
- Top-5 hedge fund concentration >15% of float ⇒ "crowded long" candidate; rotation risk on adverse catalyst.
- 3+ marquee funds adding QoQ ⇒ momentum signal but priced-in risk.
- Top-1 holder with single-name >5% AND no 13D filed ⇒ passive holder (13G probable).
- Marquee fund EXIT (top-10 → not-disclosed) is a meaningful bear data point.

**Gotchas**:
- **13F is long-side only**. It captures long equity + options-as-equity treated as the underlying. It does NOT show shorts. Quoting "13F shows shorts" is wrong — flag and reject.
- 13F covers §13(f) securities (US-listed equities, ADRs, certain options); excludes futures, swaps, foreign stocks, cash.
- Confidential treatment requests can hide positions for up to 1 year (rare; granted only on showing of competitive harm).
- Funds-of-funds and master-feeder structures can double-count if you aggregate naively across related CIKs.
- 13F shows position at quarter-end snapshot — intra-quarter trading is invisible.
- Multiple share classes (GOOG vs GOOGL, BRK.A vs BRK.B) — verify which class the 13F line references.

---

## 2. Form 4 Insider Transactions

**Field**: `form_4_pattern` (enum: cluster_buying / cluster_selling / 10b5_1_routine / discretionary_buying / discretionary_selling / mixed / no_activity).

**Where**:
- EDGAR direct: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=4`.
- OpenInsider (`http://openinsider.com/screener?s={TICKER}`) — free, by-ticker view; tags 10b5-1 plan dispositions vs discretionary; shows cluster patterns visually.
- SECForm4 (`secform4.com/insider-trading/{cik}.htm`) — by-CIK.
- InsiderInsights (`insiderinsights.com`) — proprietary scoring.

**Timing**:
- Form 4 filing deadline: 2 business days after the transaction by §16 reporting persons (directors, officers, 10% holders).
- Form 3: initial statement of ownership when person becomes an insider.
- Form 5: annual catch-up for transactions exempt from Form 4 (small gifts, etc.).
- Trailing windows to evaluate: 90-day / 6-month / 12-month.

**What to capture**:
- Net $ amount: aggregate buying minus aggregate selling over 12 months. Schema field: `forensic_flags.form_4_net_12mo_usd_m`.
- Transaction codes (Box 5 on Form 4): **P** = open-market purchase (highest signal), **S** = open-market sale, **A** = grant/award (zero signal), **M** = option exercise (low signal — usually paired with S), **F** = payment of tax via share withholding (low signal), **G** = gift (informational only).
- Position-after-transaction column: a "sell 10% of position" is different from "sell 90% of position".
- 10b5-1 plan indicator (checkbox on Form 4): formulaic plans set months earlier; less informative than discretionary trades. Recent 10b5-1 plan ADOPTION can be a sell signal in itself (insider locking in a forward sale schedule).

**Pattern enum interpretation**:
- `cluster_buying` — 2+ insiders making Code P purchases within ~30 days; rare event; meaningful bull. CEO/CFO direct purchases (not exercise-and-hold) are the strongest insider signal in US markets.
- `cluster_selling` — 3+ insiders Code S within ~30 days outside of 10b5-1; mild-to-moderate bear.
- `10b5_1_routine` — selling activity attributable to pre-set plans; treat as roughly neutral; flag if plan amount escalates materially vs prior year.
- `discretionary_buying` — single insider Code P outside any plan; modestly bullish if material $.
- `discretionary_selling` — single insider Code S outside any plan; mildly bearish.
- `mixed` — both buying and selling within window; treat as noise unless one direction dominates by 3x in $.
- `no_activity` — explicit data point worth recording, not a gap.

**Gotchas**:
- Option-exercise-and-immediate-sell (Code M + Code S same day) is the most common pattern and carries LOW signal — insider is monetizing a vested grant, not expressing a view. Distinguish from open-market sales of long-held shares.
- Late filings (transaction date > 2 days before filing date) are §16 violations but happen; flag for governance but discount as a timely signal.
- Insider OWNERSHIP level matters: a CFO with $200K position selling $50K is very different from a CFO with $50M position selling $50K.
- "Insiders selling" is the modal state in US large-caps — most large-cap C-suite has more equity comp than they can rationally hold; persistent moderate selling is structural, not signal.
- 10% holder selling can be a fund liquidation (Tiger, Sequoia, Andreessen exiting after IPO lockup), structurally different from operator-level selling.

---

## 3. 13D Activist Filings

**Field**: `activist_13d_filed` (boolean).

**Where**:
- EDGAR: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=SC+13D` (13D) and `type=SC+13G` (13G passive).
- 13D Tracker (`13dmonitor.com`, premium), Insightia (premium), WhaleWisdom 13D view (free).

**Timing**:
- **13D**: 5% threshold WITH INTENT TO INFLUENCE; filed within 10 days of crossing 5%.
- **13G**: 5% threshold passive (no influence intent); filed within 45 days (Qualified Institutional Investors get extended timelines). Mutual funds, ETFs, indexers file 13G.
- Schedule 13D amendments filed promptly on material changes (additional purchases, change in plans).

**What to capture**:
- Activist identity and recent track record: Elliott, Starboard, ValueAct, Trian, Engine No. 1, Sachem Head, Ancora, Land & Buildings, Politan, JANA, Pershing Square, Carl Icahn, Third Point. Each has a stylized playbook (capital-return-heavy / break-up / governance-overhaul / strategic-review).
- Schedule 13D **Item 4 Purpose of Transaction** — the highest-signal disclosure. Reads the activist's intentions in their own words (board representation, strategic alternatives, capital allocation, M&A).
- Cost basis (Item 5d): average purchase price across the activist's stake; signals where their pain point is.
- Pre-existing toehold via 13G that converts to 13D — meaningful escalation signal.
- Proxy contest flag: activist nominating directors at upcoming annual meeting (DEF 14A counter-proxy filing).

**Signal interpretation**:
- New 13D from a known activist ⇒ event-driven setup. Typical 6-month outcomes: settlement (board seat / strategic review announced; 20-30% of cases), proxy fight (escalation to vote; 10-15%), withdrawal (~5%), quiet accumulation continuing (~50%).
- 13G → 13D conversion ⇒ activist escalating from passive watch to active engagement.
- Multiple activists filing 13D on same name within 6 months (e.g., Salesforce 2023: Elliott + Starboard + ValueAct + JANA + Inclusive Capital) ⇒ "swarm" — sells extreme conviction in undervaluation OR governance dysfunction.

**Gotchas**:
- 13G ≠ 13D. A Vanguard 13G is passive index-fund mechanics, not an activist event. Don't conflate.
- Wolf-pack coordination concerns: activists sometimes act in concert without forming an explicit "group" (which would trigger joint 13D). SEC has scrutinized this; courts have varied views.
- 13D filing deadline is 10 calendar days — by the time a 13D files, the activist has had 10+ days to accumulate before disclosure. Price action immediately post-13D-filing often reflects the activist's last purchases already happening.

---

## 4. Short Interest

**Fields**: `short_interest_pct_float`, `days_to_cover`, `stock_loan_rate_bps`.

**Where**:
- **FINRA semi-monthly aggregated short interest** (S2): `https://www.finra.org/finra-data/browse-catalog/short-sale-volume-data/daily-short-sale-volume-files` and consolidated reports. Free; aggregated across exchanges; ~7-business-day lag after settlement date.
- **NYSE / Nasdaq exchange short interest pages**: redundant but commonly cited.
- Aggregators (free): shortinterest.com, marketbeat.com, stockanalysis.com short interest tab.
- **S3 Partners** (`shortsight.com`, premium) — real-time daily short interest estimates; stock loan economics.
- **Ortex** (`ortex.com`, premium) — alternative real-time short interest + cost-to-borrow + utilization.
- **IHS Markit Securities Finance** (premium, terminal) — institutional stock loan market data.

**Timing**:
- FINRA short interest: published twice per month (mid-month and end-of-month settlement dates). Lag ~7 business days post-settlement.
- Premium real-time sources update intraday; useful for catalyst-driven setups.

**What to capture**:
- **Short interest as % of float**: more useful than % of shares outstanding (insider-held / founder-held shares can't be borrowed).
- **Days to cover** = short interest ÷ 20-day ADV. Schema field: `days_to_cover`.
- **Stock loan rate** in bps (proxy for crowding from the borrow side): 0-50bps = easy to borrow; 200-500bps = tight; 500-2000bps = squeezable; >2000bps = hard-to-borrow / utility-grade short.
- Utilization %: % of lendable supply currently lent out. >80% utilization is the classic squeeze prerequisite.
- Trend: 3-month / 12-month direction in % of float.

**Signal interpretation**:
- Short interest >10% of float ⇒ worth discussing.
- Short interest >20% of float ⇒ high; explicit squeeze risk in catalyst-driven setups.
- Short interest >50% of float ⇒ extreme (think GME Jan 2021 at 140% via rehypothecation; AMC); requires careful framing of squeeze mechanics.
- Days to cover >5 ⇒ illiquid short; squeeze risk if catalyst forces covering.
- Rising short interest WITH falling stock loan rate ⇒ unusual; indicates ample supply to borrow despite demand (often passive lenders releasing more shares).
- Falling short interest WITH rising stock price ⇒ classic short-covering rally; mean-reverts when shorts re-establish.

**Gotchas**:
- Short interest **>100% of float is possible** due to rehypothecation (shares lent are re-lent). Flag explicitly when citing >100% as it confuses unfamiliar readers. GME, BBBY, RKT have all printed >100%.
- FINRA data is settlement-date based, not trade-date; effectively 2-day lag plus the publication lag.
- "Short interest spike" can be hedging activity (convertible arb shorts to delta-hedge a long convert position), not directional bear. Cross-check with convertibles outstanding before drawing directional conclusions.
- Days-to-cover uses ADV — recent volume spikes (post-earnings) inflate ADV and artificially compress DTC; use 3-month ADV not just 20-day for unstable names.

---

## 5. Options Market

**Fields**: `options_skew_25d_put_minus_call`, `options_implied_move_earnings_pct`, `iv_rank_pct`.

**Where**:
- **CBOE** (`cboe.com`) — primary US options exchange; quote data; some free, deeper data subscription-gated.
- **ORATS** (`orats.com`, premium) — historical IV surface, term structure, skew data; institutional.
- **SpotGamma** (`spotgamma.com`, premium) — gamma exposure dashboards; dealer positioning.
- **Vol Suite** (`volsuite.com`, premium) — vol surface + dealer GEX.
- **Tradier / TastyTrade / Interactive Brokers** — broker chains free for accountholders.
- Free: Yahoo Finance options chain (`finance.yahoo.com/quote/{TICKER}/options`), MarketChameleon (limited free), Barchart options.

**Timing**:
- Real-time during market hours; historical IV percentile uses trailing 1-year window standard.
- Earnings-week implied move: compute from front-week ATM straddle (call + put) ÷ stock price.

**What to capture**:
- **25-delta put-call skew** = 25-delta put IV − 25-delta call IV (in vol points). Schema field: `options_skew_25d_put_minus_call`. Positive skew = tail-protection bid (markets pricing put protection); typical S&P single-name skew is +2 to +5 vol pts. Negative skew (rare for equities) = call demand exceeds put demand (acquisition speculation, retail call-buying frenzies).
- **Earnings-implied move**: from front-week ATM straddle: $straddle / $stock = implied 1-σ move. Schema field: `options_implied_move_earnings_pct`. Typical S&P large-cap: 4-7%; high-beta growth/biotech: 8-15%. Compare to realized move history to gauge if market is over- or under-pricing.
- **IV rank** = (current 30-day IV − 52-wk IV low) / (52-wk IV high − 52-wk IV low) × 100. Schema field: `iv_rank_pct`. IV rank >70 = elevated; <30 = compressed.
- **IV percentile**: % of trading days over trailing year with IV below current; complementary to IV rank.
- **Put/Call open-interest ratio**: total put OI / total call OI. >1.0 = put-heavy (defensive positioning); <0.5 = call-heavy (speculative bullish).
- **Term structure**: front-month vs 6-month IV; backwardation (front > back) = event/stress; contango (back > front) = normal.
- **Gamma exposure** (GEX): aggregate dealer gamma at price levels; positive GEX dampens moves, negative GEX amplifies.

**Signal interpretation**:
- High put skew + high IV rank pre-earnings ⇒ market pricing meaningful downside tail; setup can asymmetric (squeeze higher on print-as-expected).
- High call skew (rare) ⇒ event speculation; check for M&A rumors, FDA decision, contract awards.
- Compressed IV rank into a known catalyst ⇒ market complacent; cheap to own straddles for tail.
- Negative dealer GEX (often when stock has rallied through call-strike clusters) ⇒ amplified intraday vol; daily moves >5% on no news.

**Gotchas**:
- Earnings-implied move from straddle assumes log-normal distribution; in practice fat-tailed. Realized move >> implied is common in misses; realized move < implied is common in inline prints.
- Pin risk on monthly expiry: if heavy OI is clustered around a strike near current price, stock can be magnetized to that strike on expiration Friday. Distorts intraday signal.
- IV rank can be artificially elevated by stale low (illiquid quotes 6 months ago) or compressed by recent vol spike. Cross-check with at least one other IV percentile source.
- Put-call ratio retail vs institutional: ISE-ratio is retail-heavy; CBOE total ratio includes both. They diverge on hot meme names.

---

## 6. Index Inclusion

**Field**: `index_inclusion` (array of strings).

**Where**:
- **S&P Dow Jones Indices** (`spglobal.com/spdji/en/`) — S&P 500 / 400 / 600 methodology, additions, rebalances.
- **Russell / FTSE Russell** (`research.ftserussell.com/Analytics/RussellIndexAnalytics/`) — Russell reconstitution schedules; preliminary lists published in May; effective late June.
- **Nasdaq** (`indexes.nasdaqomx.com`) — Nasdaq 100 annual rebalance December.
- **MSCI** (`msci.com/our-solutions/indexes/equity/global-equity-indexes`) — MSCI USA, ACWI, etc. quarterly index reviews.
- IR communication: companies announce S&P inclusion via 8-K Item 8.01 the day before effective date.

**What to capture**:
- Current membership: S&P 500 / 400 / 600 / Russell 1000 / 2000 / 3000 / Nasdaq 100 / MSCI USA / FTSE All-World.
- Pending inclusion / deletion if announced (`Pending` per source-tag enum until effective date).

**Methodology highlights**:
- **S&P 500**: committee-discretionary (not rules-based). Criteria as of 2024: US domicile, NYSE/Nasdaq listed, market cap floor **$14.6B** (raised June 2024 from $14.5B), 50% of shares public float, **GAAP positive** earnings in most recent quarter AND most recent four quarters combined, liquid trading. Committee meets quarterly + ad-hoc.
- **S&P 400 (MidCap)**: $7.4B–$18.0B band (2024); other criteria similar.
- **S&P 600 (SmallCap)**: $1.0B–$7.4B band.
- **Russell 1000 / 2000 / 3000**: rules-based annual reconstitution. Russell 3000 = top 3000 US-listed by market cap; Russell 1000 = top 1000 of that; Russell 2000 = ranks 1001-3000. **Preliminary lists** published in May; **rank day** is last business day of April (2024 shift to May); **effective** last Friday of June. Two-banded methodology since 2007: stocks within 2.5% on either side of cutoff stay in current index.
- **Nasdaq 100**: top 100 non-financial Nasdaq-listed by market cap. Annual reconstitution announced 2nd Friday of December, effective 3rd Friday of December. Special rebalances if any single stock exceeds 24% weight or sum of >4.5% stocks exceeds 48%.
- **MSCI USA**: rules-based quarterly review (Feb / May / Aug / Nov). Free float adjustment matters more than total market cap.

**Signal interpretation**:
- Inclusion event ⇒ passive ETF flow demand; mechanical buying = price impact. S&P 500 inclusion historically generates +5-10% pre-effective-date rally followed by partial give-back (the "index effect" has compressed over time as front-running has industrialized).
- Russell 2000 → Russell 1000 promotion ⇒ index buyers shift from small-cap ETFs (IWM) to large-cap ETFs (IWB) — net flow can be positive (large-cap ETF AUM > small-cap ETF AUM by ~3x) but pricing fluctuates.
- Deletion ⇒ mechanical selling; classic for fallen-from-grace names. Russell deletion is rules-based and largely predictable from rank.

**Gotchas**:
- **Inclusion rumors are not events**. Until S&P Dow Jones Indices issues a press release with the announcement date and effective date, "inclusion expected" is `Pending` per D16 citation discipline.
- **Russell rebalance date vs effective date confusion**: preliminary lists late May; rank day end of April / early May; effective last Friday of June. Don't conflate.
- S&P 500 GAAP profitability rule: a company with non-GAAP profitability but GAAP losses (common for SaaS, biotech) does NOT qualify. Tesla famously waited for inclusion until GAAP profitability was confirmed.
- Foreign-domiciled companies cannot be in S&P 500 even if NYSE/Nasdaq-listed (ADRs ineligible); but CAN be in S&P Global indices / MSCI USA depending on domicile/listing rules.

---

## 7. Passive Flows / ETF Ownership

**Field**: `etf_passive_ownership_pct`.

**Where**:
- 10-K shareholder list / DEF 14A Item 403 beneficial-owner table — name the largest passive holders (Vanguard, BlackRock, State Street typically each 7-10%).
- **etf.com flow data** (`etf.com/etf-watch/etf-fund-flows`) — daily ETF inflow / outflow.
- **ETFGlobal** / **FactSet ETF flows** (premium) — granular by-ETF flows.
- **VettaFi** — ETF analytics.
- 13F filings from major passive issuers (BlackRock CIK 1086364, Vanguard CIK 102909, State Street CIK 93751).

**What to capture**:
- **Aggregate passive ownership %** (Vanguard + BlackRock + State Street + Invesco + Schwab + Fidelity index funds + others). For S&P 500 names, often 30-40%; for smaller names, lower.
- **ETF-specific flows**: SPY / IVV / VOO (S&P 500), QQQ / QQQM (Nasdaq 100), IWM / IWN / IWO (Russell 2000), DIA (Dow 30), sector SPDRs (XLK tech / XLF financials / XLV healthcare / XLE energy / XLI industrials / XLY consumer disc / XLP consumer staples / XLU utilities / XLB materials / XLRE real estate / XLC communication services), industry-specific (XOP E&P / KRE regional banks / SMH semis / IBB biotech / ITA aerospace), thematic (ARKK innovation / KWEB China internet / TAN solar).
- iShares sector ETFs (IYW tech / IYF financials / etc.) as alternatives.

**Signal interpretation**:
- Passive ownership 25%+ ⇒ "index-anchored" stock; passive flow becomes the dominant marginal buyer / seller. Less responsive to fundamentals shorter-term.
- Sector-ETF flow surges ⇒ secondary signal of sector positioning; XLK net inflow with NVDA-heavy weight pulls NVDA passively.
- Hyperscaler-heavy names (NVDA ~7% of S&P 500 as of 2025) have outsized passive flow sensitivity to S&P 500 ETF flows.

**Gotchas**:
- Passive funds vote shares; they're not pure mechanical owners. BlackRock Investment Stewardship reports show how index funds vote on proxy items.
- Vanguard / BlackRock ownership in 13F is sum of MANY funds; the 13F shows aggregate, but the underlying funds have different mandates (active mutual fund vs index ETF).
- Securities lending: passive holders lend out shares heavily (revenue stream for index funds); inflates apparent short interest without reflecting active positioning.

---

## 8. Sell-Side Rating Distribution

**Field**: `sell_side_distribution` (buy_pct, hold_pct, sell_pct, pt_median_usd, pt_low_usd, pt_high_usd, pt_revision_3mo_pct).

**Where**:
- **Premium**: Visible Alpha, Bloomberg EE (terminal: `EE <Equity> GO`), Refinitiv IBES (LSEG), FactSet StreetAccount, Capital IQ Pro.
- **Free fallback** (EDGAR-only mode): Yahoo Finance Analysis tab (`finance.yahoo.com/quote/{TICKER}/analysis`), StockAnalysis (`stockanalysis.com/stocks/{ticker_lower}/forecast/`), TipRanks, WSJ Markets, MarketWatch, Zacks.

**What to capture**:
- **Buy / Hold / Sell %** distribution.
- **PT median** (not mean), high, low. Use median because mean is dragged by extreme PTs (a single $1,000 PT skews mean).
- **Dispersion**: range high-to-low, or 1σ standard deviation if available.
- **# of covering analysts** — useful as a coverage-density signal; large-cap median 12-20; SMID 5-10; micro-cap 0-3.
- **PT revision trend**: 3-month change in median PT, 6-month change. Direction (raising / cutting) more informative than level.

**Signal interpretation**:
- Wide dispersion (PT high/low > 3x) ⇒ analyst disagreement = look for the non-consensus angle; thesis has room.
- Narrow dispersion (PT high/low < 1.5x) ⇒ low conviction signal across street = priced-in; thesis must justify differentiated view.
- 80%+ Buy ratings ⇒ "consensus long"; downside surprise = pain.
- 60%+ Sell ratings ⇒ rare; usually distressed; potential contrarian setup if turn-around is plausible.
- PT cuts of 10%+ across 3+ analysts within 30 days ⇒ negative revision momentum; persists 2-4 weeks typically.

**Gotchas**:
- **Use median, NOT mean**. Mean is dragged by outliers.
- Free aggregators (Yahoo, StockAnalysis, Zacks, MarketWatch) may pull from DIFFERENT underlying feeds (Refinitiv vs Zacks-proprietary vs S&P) with different snapshot times. Cite the aggregator explicitly per D16: `(S4: Yahoo Finance consensus EPS $X, n=22, range $Y-$Z, freshness 3d)`.
- Rating-system mapping varies by broker: MS uses Overweight/Equal-weight/Underweight; JPM uses Overweight/Neutral/Underweight; Goldman uses Buy/Neutral/Sell; BoA uses Buy/Neutral/Underperform. Aggregators normalize to Buy/Hold/Sell but lose granularity (Strong Buy vs Buy).
- Sell-side analyst conflicts: investment banking relationship (managed M&A or follow-on) can bias upward. Watch for "research independence" disclosures.
- "Buy with PT below current price" ⇒ stale rating not refreshed post-rally.

---

## 9. Sentiment

**Field**: not directly schema'd; informs narrative around `recommendation` and `forensic_flags`.

**Where**:
- **SeekingAlpha** (`seekingalpha.com/symbol/{TICKER}`) — contributor ratings, Quant rating, Wall Street rating. Pro tier $239/yr for transcript access. Free tier shows aggregated contributor sentiment.
- **StockTwits** (`stocktwits.com/symbol/{TICKER}`) — retail real-time sentiment; bullish/bearish tags per post. Useful for meme-stock setups.
- **Reddit**: `r/stocks`, `r/investing`, `r/wallstreetbets` — qualitative tone, esp. for retail-favorite names (TSLA, GME, AMC, NVDA, AAPL, PLTR, etc.).
- **Substack independent analysts** — Doomberg, The Bear Cave (short reports), Hindenburg Research, Muddy Waters, Citron — explicitly bear-side reports can move stocks.
- **TIM Group Marketviews** (premium) — institutional sentiment surveys.
- **Estimize Buzz** — community estimates + sentiment.
- **CFA society notes** — local society-level commentary.
- **News sentiment**: Bloomberg / Reuters / WSJ / FT / NYT business — formal news flow; Ravenpack and similar premium services quantify.
- AlphaSense (premium) — semantic search across news + filings + transcripts for sentiment phrases.

**What to capture**:
- Retail tone: bullish-to-bearish ratio on StockTwits, top posts on r/stocks for the name.
- Institutional sentiment: TIM Marketviews if available; otherwise sell-side rating distribution serves as proxy.
- Short-report exposure: any active campaign (Hindenburg, Muddy Waters, Citron, Spruce Point, Iceberg)? Date of the report, claim summary, company response.
- News-flow density: how often is the name mentioned in tier-1 financial press? Volume + tone direction.

**Signal interpretation**:
- StockTwits bullish ratio >80% sustained ⇒ retail euphoria; contrarian bear flag.
- Active short report from credible activist short (Hindenburg, Muddy Waters) ⇒ requires explicit forensic response in memo — never ignore.
- Steady mainstream press coverage + neutral sentiment ⇒ uneventful; less retail-vol risk.

**Gotchas**:
- Reddit/StockTwits sentiment swings hours-to-days; not a slow-money signal. Useful for setup risk, not thesis input.
- Short reports often have factual errors mixed with legitimate concerns; do not accept claims; verify each claim against primary filings.

---

## 10. FINRA Margin Debt

**Field**: not in per-name schema; market-wide overlay.

**Where**:
- FINRA (`finra.org/investors/insights/finras-margin-statistics`) — monthly aggregate margin debt for FINRA-member firms. Aggregate only — not disclosed per-name.

**Use**:
- Macro-wide crowding indicator; rising aggregate margin debt = leverage building in market.
- Useful for `tail_risks` section as input to recession / de-grossing scenarios.
- NOT a per-name positioning input; do not cite per-ticker.

---

## 11. Dark Pool / Off-Exchange Activity

**Field**: not in schema; supplementary.

**Where**:
- **FINRA ATS reports** (`finra.org/finra-data/browse-catalog/short-sale-volume-data`) — weekly alternative trading system volumes by ticker. Free.
- **TRF (Trade Reporting Facility)** prints — off-exchange trades reported to FINRA; aggregated.
- Bloomberg dark-pool dashboards (premium).
- SqueezeMetrics DIX (Dark Index, free): `squeezemetrics.com/monitor/dix` — % of NYSE volume executed off-exchange.

**Use**:
- Block trade detection: large prints flagged on TRF can indicate institutional accumulation / distribution.
- Granular work; flag only when meaningful (>20% of volume in a single session off-exchange in a name not normally dark-pool-heavy).

**Gotchas**:
- ATS volume ≠ "smart money" — includes retail wholesaler internalization (Robinhood / Schwab flow routed to Citadel, Virtu) which is retail, not institutional.

---

## 12. Foreign Ownership

**Field**: not in schema enum, but captured in narrative; relevant for ADRs and dual-listed names.

**Where**:
- 10-K shareholder list (DEF 14A Item 403 Beneficial Ownership of Securities) — names 5%+ holders by domicile.
- Bloomberg international holdings (premium, terminal `INH <Equity>`).
- 20-F shareholder section for FPIs.
- For ADRs, sponsoring bank (BNY, Citi, JPM, Deutsche Bank) publishes depositary statistics.

**Use**:
- ADR positioning: how much of the float trades as ADR vs. home-country shares (BABA, NIO, JD, ASML, NVO, SAP).
- Dual-listed names (RIO, BHP, AZN, UL): US ADR vs LSE/ASX home-listing ownership split.
- Foreign holders' regulatory exposure: CFIUS-relevant foreign ownership in defense / tech names.

---

## Crowding Score Synthesis

Combine the components above into a simple 4-bucket crowding read. Each component scored 0-2; sum = 0-8.

| Component | 0 (under) | 1 (neutral) | 2 (crowded) |
|---|---|---|---|
| **13F top-5 HF concentration** | <5% of float | 5-15% | >15% of float |
| **Short interest % float** | >15% | 5-15% | <5% (consensus long) |
| **Options 25d put skew** | <0 (call-heavy speculation) | 0-5 vol pts | >5 vol pts (defensive bid) — note: high skew can mean either tail-protected long OR sentiment fragility |
| **Sell-side Buy %** | <40% | 40-70% | >70% |

Bucket map:
- **0-2: Under-owned** — non-consensus name; thesis has structural room; expect slower price discovery; potential value setup.
- **3-4: Well-owned** — balanced; price reflects current fundamentals; differentiated view required for alpha.
- **5-6: Contested** — consensus exists but contested; sentiment mixed; binary catalysts move it asymmetrically.
- **7-8: Crowded long** — uniformly long-positioned; downside surprise creates outsize moves (de-grossing pain trade); upside is priced in unless thesis materially shifts.

The score is a discipline tool, not a precise input. Document each component explicitly in the memo; do not just state "crowding score 5".

---

## Concrete Examples

**NVDA** — 13F: top hedge fund + mega-fund concentration (Tiger Global, Coatue, D1, Lone Pine, Viking, Citadel, Renaissance, Two Sigma, Berkshire indirectly via S&P 500 ETF holdings). S&P 500 weight ~7% as of 2025; passive ownership ~30%; sector ETF (XLK) weight ~20%. Options skew elevated pre-earnings; earnings-implied move historically 8-12%. Short interest low (<2% of float). Sell-side ~85% Buy. Crowding score: **7-8 (crowded long)**. Implication: upside priced in; downside surprises asymmetric.

**TSLA** — historically high short interest (15-25% of float in 2019-2022; compressed post-S&P 500 inclusion Dec 2020). Options-driven name; high gamma exposure; retail sentiment via StockTwits / WSB extreme. 13F: low marquee-fund concentration relative to size (Ron Baron persistent long). Crowding score depends on cycle. Implication: vol-driven price action; options flow more diagnostic than 13F.

**GME (Jan 2021 reference)** — short interest peaked at ~140% of float (rehypothecation; 13F + put-call ratio + retail StockTwits/WSB sentiment all extreme; squeeze playbook reference. Crowding score: **8 on the short side, 0 on long-13F** — classic crowded-short / asymmetric upside. Useful as a template for squeeze setup detection.

**AAPL** — large-cap; S&P 500 weight ~6%; passive ownership ~30%; well-covered (40+ analysts); narrow dispersion; sell-side ~60% Buy / 35% Hold. 13F top-holder concentration via Berkshire (~5-6% of SO). Short interest <1%. Crowding score: **5-6 (well-owned to contested)**. Implication: low-vol; differentiated alpha hard; positioning rarely a primary driver.

**DDOG (SMID growth example)** — concentrated growth-fund 13F (Lone Pine, ARKK exposure historically, Whale Rock, Tiger Cubs). Smaller float; passive ownership 15-20%; coverage ~25 analysts but dispersion wider than mega-caps. Earnings-implied move 10-15%. Short interest 4-8% (post-pandemic compression then expansion). Crowding score: **6 (contested-to-crowded)** at peaks; rotates with growth-vs-value cycle.

**JPM** — broad institutional ownership; low concentration in any single fund; Berkshire historical holder. Low short interest (<2% float). Sector ETF exposure (XLF). Sell-side ~70% Buy / 25% Hold / narrow dispersion. Passive ownership 25%. Crowding score: **5 (well-owned)**. Sector rotation flows (XLF inflows / outflows) dominant marginal driver.

---

## Hallucination Guards

These are the recurring errors when working positioning/sentiment data; explicit guard rules:

1. **"13F shows shorts"** — wrong. 13F is long-side only (equity + options-as-equity). Shorts disclosed via FINRA short interest, not 13F. Reject this assertion on sight.
2. **Quoting short interest >100%** — possible due to rehypothecation but must be flagged as such. State the mechanism in the same sentence (e.g., "short interest 130% of float (rehypothecation; lent shares re-lent)"). Otherwise unfamiliar readers will assume data error.
3. **Russell rebalance date vs effective date** — preliminary lists late May; rank day end of April / early May (2024 methodology shift); effective last Friday of June. Don't conflate.
4. **Index inclusion "rumors"** — until S&P Dow Jones Indices issues a press release with announcement and effective dates, all inclusion talk is `Pending` per source-stratification-us.md and D16 citation discipline. Do not anchor a thesis on rumored inclusion.
5. **Sell-side mean vs median** — use median. Mean is dragged by extreme PTs (single $1,000 PT skews the mean meaningfully). State explicitly: "median PT $X (n=22, range $Y-$Z)".
6. **10b5-1 plan dispositions interpreted as discretionary signal** — 10b5-1 plans are formulaic and set months earlier. Flag separately on Form 4 read. Do not lump with discretionary selling.
7. **"Insiders are selling" as the bear case without dollar-amount and position-after** — many large-cap C-suite have more equity comp than they can rationally hold; structural selling is the modal state. Always state $ AND % of position liquidated.
8. **Confusing GOOG vs GOOGL, BRK.A vs BRK.B** — multiple share class names. Verify which class the 13F line, Form 4, or short interest references.
9. **Treating 13G as activist** — 13G is passive; only 13D + Item 4 plans signals activist intent. Vanguard/BlackRock/State Street 13Gs are index-fund mechanics.
10. **Anchoring crowding read on stale 13F** — 13F data is minimum 45 days stale. For real-time crowding, supplement with options skew + IV rank + short interest + sell-side revision direction. Don't claim "currently crowded" on a Q1 13F when Q2 data won't print for 6 more weeks.

---

## Cross-References

- Source-catalog URLs for every endpoint above are documented in `us-data-sources.md`.
- S-tier discipline (S2 for 13F/Form 4/13D/short interest filings; S4 for sell-side; S5 for sentiment aggregators; Pending for inclusion rumors and unconfirmed short reports) is in `source-stratification-us.md`.
- Forensic-side use of Form 4 (insider patterns as leading indicator of accounting concern) is in `forensic-accounting-checklist-us.md`.
- Activist 13D as regulatory event is in `regulatory-desk-us.md`.
- Schema field definitions for `positioning_sentiment` are in `schemas/memo.json`.
- Citation format (D16) and S-tier graduation are in `source-stratification-us.md`.
