# Chinese Equity Data Sources (Public)

This is the data source playbook for Chinese listed equities using only public/free sources. Useful when terminal access (Wind, Bloomberg, Choice) isn't available or for cross-checking terminal data.

## Tier 1: Primary Disclosures

### CNINFO (巨潮资讯网) — Official Securities Disclosure
- **Main URL**: http://www.cninfo.com.cn/new/disclosure/stock?stockCode=[CODE]
- **What you'll find**: All formal company disclosures (annual reports, quarterly reports, related-party transaction announcements, capital changes, etc.)
- **Document ID format**: PDFs named like `12XXXXXXXX.PDF` (10-digit IDs)
- **Pro tip**: Use Bash with `curl` + `pdftotext -layout` to extract content from PDFs, then `grep` for specific notes

Common search patterns:
- 京东方 重大投资公告 (BOE major investment announcements)
- 京东方 关联交易公告 (BOE related-party transactions)
- 京东方 增资公告 (BOE capital increase announcements)
- 京东方 减持公告 (BOE stake reduction announcements)

### Sina Finance — Aggregated Filings
- **Announcement listing**: https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/[CODE].phtml
- **Annual reports listing**: https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/[CODE]/page_type/ndbg.phtml
- **Financial highlights (multi-year)**: https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/[CODE]/displaytype/4.phtml
- **Income statement**: https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/[CODE].phtml
- **Balance sheet**: https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/[CODE].phtml
- **Cash flow**: https://vip.stock.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/[CODE].phtml

### Eastmoney F10
- **Main F10 page**: https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=SZ[CODE]  (use SZ for Shenzhen, SH for Shanghai)
- **Financial JSON APIs**: 
  - Income: `https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_F10_FINANCE_GINCOME&filter=(SECUCODE=%22[CODE].SZ%22)`
  - Balance: `RPT_F10_FINANCE_GBALANCE`
  - Cash flow: `RPT_F10_FINANCE_GCASHFLOW`
  - Segments: `RPT_F10_FN_MAINOP`
  - Latest period summary: `RPT_LICO_FN_CPD`
- **Data center for shareholders, fund holdings, northbound**: https://data.eastmoney.com/stockdata/[CODE].html

### SSE / SZSE Exchange Bond Disclosure (for forensic deep-dives)

**Use case**: When listco's controlling-shareholder LP entities have issued bonds, their bond prospectuses and annual rating reports often disclose contractual obligations of the listco (put/call clauses, share-swap commitments) that are NOT disclosed in the listco's own filings.

- **SSE bond market**: http://bond.sse.com.cn/disclosure/list/announce/
- **SZSE bond market**: http://bond.szse.cn/disclosure/notice/general/
- **Search pattern**: Search for "[Provincial/municipal investment company name]" credit rating reports

**Real example**: BOE Mianyang B11 share-swap obligation (due Dec 31, 2022, never executed) was discovered via Mianyang Tech City Development Investment Company's 2024 first-tranche professional investor public bond credit rating report at:
http://static.sse.com.cn/disclosure/bond/announcement/company/c/new/2024-08-06/241401_20240806_A24H.pdf

The original BOE listco filings did not disclose this clause. The LP-side filing was the only source.

## Tier 2: Industry Data & Trade Press

### Display / Semiconductor / Electronics

- **Sigmaintell (群智咨询)**: https://www.sigmaintell.com/en/ — China's leading display industry consultancy. Weekly TV/IT panel pricing. Some content paywalled but summaries free.
- **DSCC (Display Supply Chain Consultants)**: Display industry. Ross Young is the lead analyst.
- **OLED-Info**: https://www.oled-info.com — Free OLED industry news, supplier rotations, capacity announcements
- **Display Daily**: https://displaydaily.com — Industry analysis
- **Counterpoint Research**: https://counterpointresearch.com — Smartphone, OLED, IT panel forecasts. Some paywall, some free
- **Omdia**: https://omdia.tech.informa.com — Major industry tracker. Significant paywall but press releases free
- **TrendForce**: https://www.trendforce.com — Memory, display, panel pricing. Press releases free
- **UBI Research**: Korean OLED/display research. Often most timely on Asian supply chain
- **TheElec**: https://www.thelec.net — Korean trade press, deep on Korean tech and Asian supply chain
- **DigiTimes**: https://www.digitimes.com — Taiwan-based, deep on Asia supply chain. Free tier limited; paid tier comprehensive
- **SEMI**: https://www.semi.org — Equipment shipment data (leading indicator)

### Autos
- **CnEVPost**: https://cnevpost.com — China EV industry coverage
- **Gasgoo (盖世汽车)**: https://autonews.gasgoo.com — Chinese auto industry
- **Caixin auto**: https://auto.caixin.com — Premium financial coverage of autos
- **Wikipedia auto/EV pages**: Often surprisingly complete for product launches

### China-specific aggregators
- **Caixin (财新)**: https://www.caixin.com — Premium financial journalism. Some paywall.
- **Yicai (第一财经)**: https://www.yicai.com — Financial news
- **Jiemian (界面新闻)**: https://www.jiemian.com — Business news
- **PjTime**: http://www.pjtime.com — Display industry Chinese-language coverage
- **STCN (上海证券报)**: https://www.stcn.com — Securities news, often picks up listco announcements early
- **NBD (每经)**: https://www.nbd.com.cn — Beijing-based business news

## Tier 3: Sell-Side Aggregators

- **Eastmoney research aggregator**: http://data.eastmoney.com/notices/stock/[CODE].html — Sell-side reports on individual stocks
- **DongFangCaiFu PDFs (东方财富)**: PDFs at `https://pdf.dfcfw.com/pdf/H3_AP[YYYYMMDD]XXXX_1.pdf` — sell-side notes
- **Tonghuashun (同花顺) F10**: http://basic.10jqka.com.cn/[CODE]/ — Comprehensive financial summary, sell-side consensus
- **MarketScreener**: https://www.marketscreener.com/quote/stock/[code]/consensus/ — International sell-side consensus
- **Investing.com**: https://www.investing.com/equities/[name] — Consensus targets
- **TradingView News**: https://www.tradingview.com/symbols/[exchange]-[code]/ — News flow with auto-summaries

## Tier 4: US Government Sources (for restriction-list verification)

- **BIS Entity List**: https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list
- **OFAC SDN Search**: https://sanctionssearch.ofac.treasury.gov/
- **DoD 1260H List**: Search "DoD 1260H Chinese military companies list" — annual update typically in January, PDF posted at media.defense.gov
- **Federal Register**: https://www.federalregister.gov — Search for relevant agency rule changes
- **House Select Committee on the CCP**: https://chinaselectcommittee.house.gov/media — Letters and press releases from Moolenaar et al.
- **Hogan Lovells / Crowell / Squire Patton Boggs / Skadden / Arnold & Porter**: Legal firm client alerts on each list update — search firm name + "1260H" / "Entity List" / "Affiliates Rule"

**Critical**: Always verify regulatory designation against the actual government source PDF, not just legal alerts. Alerts may use ambiguous language about whether a name is "added", "considered", "requested", or "designated."

## Tier 5: Stock Quote / Market Data

- **Morningstar**: https://www.morningstar.com/stocks/xshe/[CODE]/quote — Reliable stock quote, basic financials
- **Yahoo Finance**: https://finance.yahoo.com/quote/[CODE].SZ/ — Stock quote, news, key statistics
- **Bloomberg**: https://www.bloomberg.com/quote/[CODE]:CH — Quote (free)
- **TradingView**: https://www.tradingview.com/symbols/SZSE-[CODE]/ — Charts and analysis
- **Investing.com**: https://www.investing.com/equities/[name] — Quote and consensus

## Tier 6: Social / Sentiment

- **Xueqiu (雪球)**: https://xueqiu.com/S/SZ[CODE] — Chinese investor community, qualitative sentiment
- **Eastmoney 股吧**: http://guba.eastmoney.com/list,[CODE].html — Retail investor discussion
- **Sina Stock Pages**: http://finance.sina.com.cn/realstock/company/sz[CODE]/nc.shtml — Quote + news + discussion

## Use Patterns

### "Pull the latest annual report"
1. Try CNINFO direct: `http://static.cninfo.com.cn/finalpage/[YYYY-MM-DD]/[ID].PDF`
2. If unknown ID, search Sina announcement listing for the latest 年度报告
3. Use Bash: `curl -o report.pdf "URL" && pdftotext -layout report.pdf report.txt && grep -A 5 "[search term]" report.txt`

### "Verify a regulatory designation"
1. Identify the specific list (BIS Entity, MEU, NS-CMIC, OFAC SDN, DoD 1260H)
2. Search the actual government source PDF, not legal alerts
3. Cross-check via multiple legal alerts to confirm interpretation
4. Document specific addition date and Federal Register volume/notice number

### "Identify a customer that's anonymized in financials"
1. Pull annual report 主要客户 (major customers) section — usually shows top 5 anonymized
2. Note revenue magnitude and geographic split
3. Search trade press for industry-wide supplier disclosures
4. Triangulate against customer-side disclosures (e.g., Apple supplier list, Samsung purchase data)

### "Verify Q1 / H1 / Q3 quarterly results"
1. Quarterly reports filed within 30 days of quarter-end
2. Check Sina/IT之家/中华网 for Chinese-language coverage of headline numbers
3. Pull actual PDF from CNINFO if footnote-level detail needed
4. Cross-check via Eastmoney CPD JSON API for headline P&L

### "Search the LP-side disclosures for hidden contractual obligations"
1. Identify the LP counterparty for each major operating subsidiary (often stated in the listco's 主要子公司 footnote)
2. Search SSE/SZSE bond market for the LP entity's bond filings
3. Pull credit rating reports — often disclose listco contractual obligations
4. Cross-check via Lianhe Ratings (联合资信) and other rating agency reports

## Common Failure Patterns

- **Wrong document ID**: Sub-agents may invent CNINFO PDF document IDs that don't exist. Always verify URL works before citing.
- **Wrong Note number**: Sub-agents may invent "Note V.57, p.186" references. Verify by searching the PDF.
- **亿 vs 亿元 vs billion confusion**: 1 亿 = 100 million = 0.1 billion. Don't translate "20.74亿" as "20.74 billion" — that's RMB 2.074 billion.
- **Date confusion**: Quarterly reports for Q[N] are filed in month [3*N+1]. Annual reports filed by April 30.
- **Stock code formats**: A-shares are 6 digits; sometimes ".SZ" (Shenzhen) or ".SH" (Shanghai) suffix. H-shares are 4-5 digit codes ending in ".HK"
