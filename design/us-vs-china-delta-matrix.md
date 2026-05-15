# US-vs-China Delta Matrix

The architectural pattern of the China skills is being inherited wholesale: multi-agent specialization, parallel dispatch, PM synthesis, mandatory verification, S1-S5 source stratification, 5-scenario probabilistic framework, three-method valuation reconcile, GM taxonomy, bear bridge, what-would-reverse triggers, A0 tail mapping, position sizing, PM red-team rubric, multi-audience derivation, verification scripts. **This document is not about whether to inherit those — they're inherited.** It catalogues, layer by layer, what the China-specific implementation said and what the US replacement must say.

Every row below should be re-readable as: "the China skill assumed X. The US skill must instead assume Y. Implication for Phase B subagent prompts: Z."

Tags in the right column reference the Phase B file each delta lands in (per `BUILD_PROMPT.md` §"Phase B: Skill scaffolding + shared contracts").

---

## 1. Data sources (primary disclosure)

| Layer | China implementation | US implementation | Phase B target |
|---|---|---|---|
| Primary regulator | CSRC (China Securities Regulatory Commission) | SEC (Securities and Exchange Commission) | `us-data-sources.md` |
| Disclosure portal | CNINFO (cninfo.com.cn) — searchable PDF announcements; Sina Finance / Eastmoney F10 for aggregated financials | **SEC EDGAR** (sec.gov/edgar) — full-text search (efts.sec.gov), company filings page, EDGAR API (data.sec.gov), XBRL financial data (data.sec.gov/api/xbrl/companyfacts/CIK*.json) | `us-data-sources.md` |
| Annual filing | 年度报告 (filed by 4/30, prior year) | **10-K** (filed within 60 days of fiscal year end for LAFs; 75 days for AFs; 90 days for non-AFs) | `us-data-sources.md`, `forensic-accounting-checklist-us.md` |
| Quarterly filing | 季度报告 (Q1 by 4/30, Q2 (semi-annual 半年报) by 8/31, Q3 by 10/31) | **10-Q** (filed within 40/45 days of quarter end depending on filer status; Q4 results come in 10-K, no Q4 10-Q) | `us-data-sources.md` |
| Material event filing | 临时公告 (no rigid schedule) | **8-K** (filed within 4 business days; ~40 reportable Item types: Item 1.01 entry into material agreement, 2.02 results of ops, 4.02 restatement, 5.02 D&O changes, 8.01 other) | `us-data-sources.md`, `forensic-accounting-checklist-us.md` |
| Proxy / annual meeting | 股东大会公告 | **DEF 14A** (definitive proxy) — D&O comp, related-party tx, board independence, auditor approval, shareholder proposals | `us-data-sources.md` |
| IPO / shelf | 招股说明书 | **S-1** (IPO), **S-3** (shelf), **S-4** (M&A securities) | `us-data-sources.md` |
| Foreign issuer | (N/A — Chinese issuers list domestically or HK) | **20-F** (annual, foreign private issuer), **6-K** (interim disclosure FPIs) — for ADRs (Toyota, Spotify, BABA, etc.) | `us-data-sources.md` |
| Insider transactions | 减持公告 / 增持公告 (timing flexible) | **Form 4** (insider transaction, filed within 2 business days), **Form 3** (initial), **Form 5** (annual catchup) — sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=*&type=4 | `us-data-sources.md`, `positioning-sentiment-us.md`, `forensic-accounting-checklist-us.md` |
| Institutional holder | 北上资金 (HK Stock Connect northbound) + 公募基金 quarterly disclosures | **13F** (managers >$100M AUM, filed 45 days after quarter end; sec.gov/cgi-bin/browse-edgar?action=getcompany&type=13F-HR) — covers long equity + options-as-equity but not shorts | `us-data-sources.md`, `positioning-sentiment-us.md` |
| Activist filing | (rare under domestic regime) | **13D** (>5% with intent to influence, 10 days), **13G** (>5% passive, 45 days) | `us-data-sources.md`, `regulatory-desk-us.md` |
| Aggregated financials (free) | Sina Finance, Eastmoney F10 JSON APIs (RPT_F10_FINANCE_GINCOME etc.) | **EDGAR XBRL company facts API** (data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json), **stockanalysis.com**, **macrotrends.net**, **Yahoo Finance** (free tier, finance.yahoo.com/quote/{ticker}/financials) | `us-data-sources.md` |
| Aggregated financials (premium) | Wind, Bloomberg, Choice | **Bloomberg**, **FactSet**, **Capital IQ**, **Refinitiv Eikon**, **S&P CapIQ Pro** — all premium; treat as optional hooks | `us-data-sources.md` |
| Consensus / sell-side | Wind 一致预期 (free at Eastmoney), 卖方报告 (Eastmoney research aggregator) | **Visible Alpha** (premium, granular line items), **FactSet StreetAccount**, **Bloomberg EE**, **Refinitiv IBES**; free fallback: **Yahoo Finance Analysis tab**, **StockAnalysis.com forecasts**, **WSJ Markets** | `us-data-sources.md`, `valuation-discipline-us.md` |
| Earnings transcripts | 业绩说明会 transcripts on CNINFO + 公司微信公众号 | **Earnings call transcripts** — **AlphaSense** (premium), **Capital IQ Pro** (premium), **SeekingAlpha** (Pro tier, $239/yr), **Motley Fool transcripts** (free, fool.com/earnings-call-transcripts), **The Motley Fool** + **Sentieo**; also raw audio webcast replay on company IR pages | `us-data-sources.md` |
| Macro data | NBS, PBoC, MIIT releases via 国家统计局 | **FRED** (fred.stlouisfed.org) — primary; **BEA**, **BLS**, **Census**, **Fed** (federalreserve.gov), **Treasury** (treasury.gov), **CBO**, **EIA** (eia.gov for energy) | `us-data-sources.md` |
| Trade press by sector | Sigmaintell, DSCC, OLED-Info (display); Caixin auto, CnEVPost (autos); 第一财经 etc. | Sector-specific: **The Information**, **Stratechery** (tech); **STAT**, **BioPharma Dive** (biotech); **Bank Reg Blog**, **American Banker** (financials); **EnergyIntel**, **OilPrice** (energy); **Counterpoint**, **Omdia**, **IDC**, **Gartner**, **IHS Markit / S&P Global Commodity Insights** (cross-sector); **Wards Auto**, **Automotive News** (autos); **Modern Healthcare** (HC services) | `us-data-sources.md` |
| Alt-data / channel checks | 供应链调研, 行业协会, 渠道反馈 | **Yipit Data**, **Second Measure (Bloomberg)**, **Earnest Analytics**, **M Science**, **Placer.ai** (foot traffic), **SimilarWeb** (web traffic), **AppFigures** (app analytics), **AdvanResearch**; **expert networks**: GLG, Tegus, AlphaSights, Third Bridge | `us-data-sources.md`, `positioning-sentiment-us.md` |
| Litigation / docket | 中国裁判文书网 (limited) | **PACER** (federal court, paid per page), **CourtListener** (free wrapper), **RPX**, **Lex Machina** (premium IP litigation analytics) | `us-data-sources.md`, `regulatory-desk-us.md` |
| Federal agency rulings | CSRC, MIIT, NDRC websites | **Federal Register** (federalregister.gov), **agency-specific dockets** (FDA dashboards.fda.gov; FCC docs.fcc.gov; FERC ferc.gov; SEC press litigation releases) | `us-data-sources.md`, `regulatory-desk-us.md` |
| Portability constraint | Plugin works without paid sources (CNINFO is free) | **Plugin MUST work in EDGAR-only mode** for portability; premium hooks (Visible Alpha, Capital IQ, AlphaSense, Bloomberg) are optional and gated behind explicit user signaling | `SKILL.md` (mode flag), `us-data-sources.md` (sources tiered by access) |

---

## 2. Source stratification (S1-S5 + Pending)

| Tier | China definition | US definition | Notes |
|---|---|---|---|
| **S1** | 经审计年报 (audited annual) | **Audited 10-K** (or 20-F for FPIs); ICFR audit opinion under SOX §404(b); ASC-compliant | The bar is higher in the US than China: SOX §302/404, PCAOB-registered auditor, public auditor inspection reports |
| **S2** | 季报 / 公告 / 投资者关系活动记录表 (unaudited but public filing) | **10-Q** (reviewed by auditor not audited), **8-K** (incl. Item 2.02 results, Item 5.02 D&O changes), **DEF 14A**, **S-1/S-3/S-4**, **13D/13G/13F**, **Form 4**, **6-K** | Note: 8-K is highly heterogeneous — some Items more reliable than others (4.02 restatement is high-info; 8.01 other is junk-prone) |
| **S3** | IR commentary, 业绩说明会, 投资者交流 | **Earnings call transcript**, **management guidance** (often given as range in 8-K Item 7.01 or on call), **Investor Day presentations**, **non-deal roadshow** notes (if accessible), **press releases** (company-issued, not 8-K-attached) | Guidance is a contractual disclosure in the US (Reg FD §17 CFR 243) — same-day broad distribution required. Higher reliability than China IR commentary, but still S3 because not audited |
| **S4** | Wind/Bloomberg consensus, 卖方报告 | **Visible Alpha / FactSet / Bloomberg / Refinitiv IBES consensus**, **sell-side notes** (BoA, JPM, Morgan Stanley, Goldman, etc.); also **Yahoo Finance consensus** (free) | US sell-side coverage is denser (median NYSE/Nasdaq stock has 12-20 analysts) — use **median + dispersion**, not mean. Free consensus on Yahoo/StockAnalysis is often Refinitiv-derived |
| **S5** | Omdia, Counterpoint, CINNO, TrendForce + channel checks | **Gartner**, **IDC**, **IHS Markit (S&P Global)**, **NielsenIQ**, **Circana** (formerly IRI), **Forrester**, **Counterpoint**, **Omdia**, **Yipit**, **Second Measure**, **Placer.ai**, **SimilarWeb**; **expert networks** (GLG, Tegus, AlphaSights) | Alt-data is much more mature in US than China — but the same discipline applies: cite specific provider, methodology, sample size, freshness |
| **Pending** | 未核实 / 未溯源 | **Unverified**: rumor in trade press not confirmed by company/SEC, model-cutoff-suspect numbers, anonymous-source-only reporting | Same discipline — never a headline anchor |

**Hard rule preserved**: if any top-3 anchor is S3 or weaker, headline must be source-conditional. Conditional language patterns translate to English (see Layer 7 below).

---

## 3. Regulatory desk

| Domain | China-relevant | US-relevant | Phase B target |
|---|---|---|---|
| Antitrust / competition | SAMR (State Administration for Market Regulation) | **FTC** (federal, civil), **DOJ Antitrust Division** (federal, civil + criminal), **state AGs** (NY, CA, TX, etc.), **EU CMA** (Phase I/II), **UK CMA**, **CCI India**, **Canada Bureau**; Hart-Scott-Rodino premerger notification (HSR); **Second Request** signals deep review | `regulatory-desk-us.md` |
| Export control | BIS Entity List, MEU List, NS-CMIC List, OFAC SDN, DoD 1260H | **BIS** (Bureau of Industry and Security) — Entity List, Unverified List, MEU, Validated End User; **OFAC** (Treasury) — SDN, NS-CMIC, Sectoral Sanctions; **CFIUS** for inbound FDI; **State Department** ITAR (defense); **End-User Affiliates Rule** | `regulatory-desk-us.md` |
| Trade / tariffs | (importer side) | **USTR** Section 301 (China tariffs), **Section 232** (national security tariffs on steel/aluminum/etc.), **AD/CVD** (antidumping/countervailing duty) cases at ITC + Commerce | `regulatory-desk-us.md` |
| Securities enforcement | CSRC investigations | **SEC Division of Enforcement** — Wells notice, AAER (Accounting and Auditing Enforcement Release), parallel DOJ criminal; **PCAOB inspections** revealing audit deficiencies; **10b-5 class actions** + **derivative suits** + **Section 16(b) short-swing profits** | `regulatory-desk-us.md`, `forensic-accounting-checklist-us.md` |
| Sector regulators | MIIT (industrial), NDRC (planning), NMPA (drugs), CBIRC (banking/insurance), SARFT (media) | **FDA** (drugs, devices, biologics, food), **FCC** (telecom, broadcast, spectrum), **FERC** (energy infrastructure), **NHTSA** (autos), **EPA** (environment), **FAA** (aviation), **CFPB** (consumer finance), **Fed/OCC/FDIC** (banks), **NCUA** (credit unions), **SEC/CFTC** (markets), **NRC** (nuclear), **USDA** (ag/meat), **HHS/CMS** (healthcare reimbursement), **HUD** (housing), **PUC** state-level (utilities), **FTC** (consumer protection + competition), **DOL** (labor), **OSHA** (workplace) | `regulatory-desk-us.md` |
| State-level regulation | (limited federal-state structure) | **California** (CCPA/CPRA privacy, CARB emissions, Prop 65, AB5 labor), **New York** (DFS, NYAG), **Texas** (state regulators), **Massachusetts** (data breach), **Delaware** (corp law venue) | `regulatory-desk-us.md` |
| Tax policy | 增值税 super-deduction, R&D super-deduction, HNTE 15%, 两免三减半 holidays | **BEAT** (base erosion anti-abuse tax), **GILTI** (global intangible low-taxed income), **FDII** (foreign-derived intangible income), **Section 174** R&D capitalization (TCJA 2017), **Pillar 2 / GMT** (15% global minimum), **CAMT** (15% corporate alt min tax), **Wayfair** state sales tax nexus, **IRA Section 45X/48** clean energy credits, **CHIPS Act** Section 48D | `regulatory-desk-us.md`, `forensic-accounting-checklist-us.md` |
| Litigation | Class actions exist but rare; commercial arbitration more common | **Federal class actions** (Rule 23) — securities fraud, antitrust, product liability, consumer; **derivative suits**; **shareholder litigation** at Delaware Chancery; **ITC §337** import bans (esp. for tech IP); **PACER** docket search | `regulatory-desk-us.md` |

---

## 4. Rating taxonomy

| Element | China standard | US standard recommended | Notes |
|---|---|---|---|
| Bands | 买入 / 增持 / 中性 / 减持 / 卖出 | **Strong Buy / Buy / Hold / Sell / Strong Sell** (5-band, mirroring China). Alternative: **Overweight / Equal-weight / Underweight** (3-band, common at MS/Citi); **Buy / Hold / Sell** (3-band, basic) | Recommend 5-band — matches China precedent and gives finer conviction signal needed for institutional buy-side use |
| Return thresholds (12mo) | Buy ≥+15%, Outperform +5 to +15%, Neutral ±5%, Underweight -5 to -15%, Sell ≤-15% (absolute return) | **Strong Buy ≥+20%, Buy +10 to +20%, Hold ±10%, Sell -10 to -20%, Strong Sell ≤-20%** (absolute return vs current price) | Wider bands than China — reflects higher base-rate volatility and longer-duration US holding periods. **Open decision: confirm.** |
| Rating vs sizing distinction | Explicitly decoupled — "买入 ≠ 重仓" | **Same discipline preserved** — rating reflects 12mo expected return; sizing reflects conviction × volatility × capacity | `SKILL.md`, `ic-memo-template-us.md` |
| Pair-trade rating | (rare) | **Spread Buy / Spread Sell** for pair trades (long A / short B together) — explicit benchmark = pair spread, not index | `ic-memo-template-us.md`, `position-sizing-us.md` |
| Conviction tag | 中度偏空 / 中性轻偏空 / 中性 / 中性轻偏多 / 中度偏多 | **High conviction / Moderate conviction / Low conviction / Source-conditional / Reactive** — pair conviction tag with rating | `SKILL.md`, `pm-redteam-rubric-us.md` |

---

## 5. Valuation conventions

| Layer | China implementation | US implementation | Phase B target |
|---|---|---|---|
| Headline metric | EPS × PE primary | **EPS × P/E primary for mature equities; EV/EBITDA for high-leverage; EV/Sales for high-growth pre-profit; EV/FCF for capex-heavy mature; P/B for banks/insurers; AFFO/NAV for REITs; ARR multiple + Rule of 40 for SaaS; NPV pipeline for biotech; PEG for growth; SOTP for diversified** — sector-specific norm | `valuation-discipline-us.md` |
| Discount rate (R_f) | 10Y CGB yield | **10Y UST yield** (FRED `DGS10`, verify daily) | `valuation-discipline-us.md` |
| Equity risk premium | Damodaran China implied ERP (~7-9%) | **Damodaran implied US ERP** (~4.5-6%, monthly update at pages.stern.nyu.edu/~adamodar) | `valuation-discipline-us.md` |
| Beta | 5y monthly vs CSI 300 | **5y weekly or 2y daily vs S&P 500** (more common) or **levered/unlevered industry beta** (Damodaran); for thin-trade names use **adjusted beta** (Bloomberg formula = 0.67×raw + 0.33×1.0) | `valuation-discipline-us.md` |
| Cost of debt | Blended bank loans + bonds | **Investment-grade vs HY corp yield** by rating (Bloomberg or FRED `BAMLC0A0CM`); use **after-tax** = pre-tax × (1 − effective tax rate) | `valuation-discipline-us.md` |
| Terminal growth | 2-3% (mature Chinese industrial) | **2.0-2.5%** (long-run US nominal GDP growth, roughly real GDP + Fed inflation target) | `valuation-discipline-us.md` |
| Terminal multiple | Gordon growth standard | Both **Gordon growth** AND **exit multiple** (sanity cross-check) — US shops typically show both | `valuation-discipline-us.md` |
| Time horizon for forecast | 5-year explicit + terminal | **5-year explicit DCF + terminal** standard; for cyclicals use **10-year normalized**; for growth use **3-year explicit + 7-year fade** | `valuation-discipline-us.md` |
| Multiple bands | Historical 5-year P/E range cited | **Historical multiple percentiles** (5/25/50/75/95) over 5-10 years, sourced from **YCharts**, **Macrotrends**, or **Bloomberg HMI** | `valuation-discipline-us.md` |
| Trading comps | A-share peers in same sector | **US peer set** (S&P sub-industry GICS-Level-4 or custom curated peer group); cross-listed alternatives if multinational (e.g., Vale ADR for BHP comparison) | `valuation-discipline-us.md` |
| Precedent M&A | (limited domestic data) | **Capital IQ / SDC Platinum** for transaction multiples by sector; **Mergermarket**, **PitchBook** for PE/VC; rule of thumb: control premium 25-35% over LTM trading levels | `valuation-discipline-us.md` |
| LTM vs NTM vs forward | NTM = consensus 12mo forward | Same; **NTM** is common; for cyclicals **mid-cycle/normalized** is more important than NTM | `valuation-discipline-us.md` |
| Currency | CNY | **USD** for US-listed; for ADRs decide: native vs USD (default USD, native disclosed in appendix) | `valuation-discipline-us.md` |

---

## 6. Forensic accounting

China-specific forensic items (subsidies, MI dilution, LP put/call, 亿 unit confusion, RPT with state) are largely **not relevant** in US. The US-specific replacements:

| Item | China analog | US-specific forensic check | Phase B target |
|---|---|---|---|
| Revenue recognition | (less prominent, China P/L is accrual but simpler) | **ASC 606** — five-step model: contract → performance obligations → transaction price → allocation → recognition. Red flags: bill-and-hold, channel stuffing (DSO spike), bundled SaaS+services with aggressive POB allocation, license-revenue front-loading, contract modifications, deferred revenue declines (SaaS canary) | `forensic-accounting-checklist-us.md` |
| Lease accounting | China CAS now ASC 842-aligned but less scrutiny | **ASC 842** — operating leases on BS as right-of-use asset + lease liability. Check **PV of lease commitments** in 10-K notes; **off-balance pre-2019 lease tails** still affect FCF comparability | `forensic-accounting-checklist-us.md` |
| Stock-based compensation | (limited use historically) | **ASC 718 SBC** — almost universally added back in non-GAAP. Standard rigor check: **SBC % of revenue**, **SBC % of operating cash flow**, **dilution from RSU/option vest schedule**, **buyback offset adequacy** (buyback $ ÷ SBC $ ≥ 1.0 means real return; <1.0 means dilution masked by ASR) | `forensic-accounting-checklist-us.md` |
| Goodwill | (less common) | **ASC 350** — annual impairment test; segment-level reporting unit; **triggering events** (stock price drop, segment underperformance). Red flag: large goodwill bal vs net assets + recent deal underperforming | `forensic-accounting-checklist-us.md` |
| Non-GAAP discipline | (relatively standardized in China — 扣非净利润) | **Non-GAAP vs GAAP gap** is the #1 US forensic check. Reconciliation table is mandatory under Reg G + Item 10(e). Common abuses: persistent "one-time" restructuring charges, "adjusted EBITDA" excluding SBC + recurring charges, "FCF" defined idiosyncratically (excluding capex but including capitalized R&D). Standard: track **non-GAAP-to-GAAP delta as % of net income** over 5 years; if >25% sustained, scrutinize | `forensic-accounting-checklist-us.md` |
| Working capital | DSO/DIO/DPO trends | Same — **DSO trend break** (receivables stretching = revenue quality concern), **DIO trend break** (inventory build = demand miss), **deferred revenue decline** (subscription churn signal) | `forensic-accounting-checklist-us.md` |
| Auditor changes | (rare, regulated) | **8-K Item 4.01** (auditor change) — **Big-4 → mid-tier** is a meaningful red flag; **going-concern qualification** on 10-K | `forensic-accounting-checklist-us.md` |
| Restatements | (rare) | **8-K Item 4.02** (non-reliance on prior financials) — material restatement is severe. Check **PCAOB inspection reports** for the company's auditor | `forensic-accounting-checklist-us.md` |
| Pension / OPEB | (state pension is govt-funded) | **PBO vs FV of plan assets** disclosed in 10-K Note "Employee Benefits"; **mandatory contribution** if underfunded ratio crosses thresholds (ERISA); some industries materially exposed (legacy autos, airlines, industrials) | `forensic-accounting-checklist-us.md` |
| Form 4 insider patterns | 减持公告 | **Form 4 net activity** (last 12mo): material C-suite selling = mild bear signal; cluster buying = mild bull. **10b5-1 plan** structure matters (formulaic plans are less informative than discretionary trades) | `forensic-accounting-checklist-us.md`, `positioning-sentiment-us.md` |
| Related-party tx | 关联交易 | **DEF 14A Item 404** — director/officer/5% holder transactions disclosed | `forensic-accounting-checklist-us.md` |
| Off-balance-sheet | (limited) | **VIEs** (variable interest entities; ASC 810), **JVs**, **securitizations**, **synthetic leases** | `forensic-accounting-checklist-us.md` |
| Contingent liabilities | (limited disclosure) | **10-K "Commitments and Contingencies"** note — litigation reserves, environmental remediation (CERCLA), tax positions (FIN 48 / ASC 740 reserves) | `forensic-accounting-checklist-us.md` |
| Subsidies → Tax credits | 政府补助 is dominant in China P/L | **IRA Section 45X/48 advanced manufacturing credit**, **CHIPS Act Section 48D**, **R&D credit Section 41**, **NOL carryforward** (80% post-TCJA), **PPP forgiveness** (legacy) — far smaller as % of NI than China subsidies typically | `forensic-accounting-checklist-us.md` |
| LP put/call | Unique to China's local-government-LP fab model | (N/A — US doesn't have this structure; check **redeemable preferred stock**, **earn-out liabilities**, **PIPE warrants** as analogs) | `forensic-accounting-checklist-us.md` |
| RMB 亿 unit confusion | Common error | **USD million vs billion** confusion — far less frequent but still check. Some companies report in thousands; some in millions | `forensic-accounting-checklist-us.md` |

---

## 7. Positioning / sentiment desk

| Layer | China implementation | US implementation | Phase B target |
|---|---|---|---|
| Long holder map | Top-10 shareholders + 北上资金 + 公募基金 quarterly | **13F holdings clusters** (Whale Wisdom, hedgefollow.com, fintel.io, insidermonkey.com, sec.gov direct); **mutual fund holdings** (SEC N-PORT filings); track **top hedge funds in name** + concentration | `positioning-sentiment-us.md` |
| Short side | (no meaningful short market) | **Short interest** (FINRA semi-monthly via finra.org; aggregated at shortinterest.com); **Days-to-cover** = short interest / 20-day ADV; **S3 Partners** / **Ortex** for real-time short data (premium); **stock loan rate** as crowding proxy | `positioning-sentiment-us.md` |
| Options market | 不发达 | **Open interest + IV term structure** at CBOE / ORATS; **skew** (25-delta put IV − 25-delta call IV); **put/call ratio**; **gamma exposure** dashboards (SpotGamma, Vol Suite); useful for crowding + pinned events | `positioning-sentiment-us.md` |
| Index inclusion | CSI 300 inclusion | **S&P 500 inclusion** (committee discretionary, profitability test, $14.6B market cap floor as of 2024), **Russell 1000/2000/3000 reconstitution** (annual late June, rules-based), **Nasdaq 100** (yearly Dec rebalance), **MSCI USA / EAFE / EM**, **FTSE Russell**; index inclusion/exit is significant flow event | `positioning-sentiment-us.md` |
| Passive flows | (limited domestic ETFs) | **ETF flow** by issuer: **SPY/IVV/VOO** (S&P 500), **QQQ** (Nasdaq 100), **IWM** (Russell 2000), sector SPDRs (XLK/XLF/XLV/XLE/etc.), iShares; **passive ownership %** (10-K shareholder list) | `positioning-sentiment-us.md` |
| Sell-side rating distribution | Buy/Hold/Sell distribution + dispersion | Same — **% Buy / % Hold / % Sell**, **PT range**, **PT dispersion** (1σ), **revision trend** (3mo/6mo) | `positioning-sentiment-us.md` |
| Insider activity | 减持/增持 | **Form 4** net activity (last 90d / 6mo / 12mo); **10b5-1 plan** disclosure; **insiderinsights.com**, **secform4.com**, **openinsider.com** | `positioning-sentiment-us.md` |
| Activist filings | (limited) | **13D activists** + **13G passive** (Schedule 13D Item 4 plans); **proxy contests** in upcoming annual meeting | `positioning-sentiment-us.md`, `regulatory-desk-us.md` |
| Sentiment | Xueqiu, 股吧 | **SeekingAlpha** (contributor ratings), **StockTwits**, **WSB / r/stocks**, **Substack** independent analysts; institutional sentiment via **TIM Group Marketviews**, **EstimizeBuzz**; **CFA society notes** | `positioning-sentiment-us.md` |
| Northbound analog | 北上 net buying | (N/A — foreign capital is the entire market; instead track **foreign ownership %** from 10-K, **Bloomberg international holdings**) | `positioning-sentiment-us.md` |
| Margin balance | 融资融券 | **FINRA margin debt** (aggregate market only, not per-name) | `positioning-sentiment-us.md` |
| 龙虎榜 | Large-trade disclosures | (N/A directly; **block trade detection** via TRF prints, **dark pool activity** via FINRA ATS reports) | `positioning-sentiment-us.md` |

---

## 8. Multi-audience derivatives

| Audience | China deliverable | US deliverable | Phase B target |
|---|---|---|---|
| Institutional (full) | `<ticker>_投资意见书_<author>.docx` | **`<ticker>_IC_memo_<author>.md`** — full 12-section IC memo per BUILD_PROMPT §B1.ic-memo-template | `ic-memo-template-us.md` |
| IC pre-read | `<ticker>_精简版_<author>.docx` | **`<ticker>_IC_preread_<author>.md`** — 3-4 page condensed | `ic-memo-template-us.md` (variant section) |
| IC debate | `<ticker>_IC_Debate_Script_<author>.docx` | **`<ticker>_IC_debate_<author>.md`** — verbal script + Q&A bank | `ic-memo-template-us.md` (variant section) |
| Client-facing | `<ticker>_零售版_<author>.docx` + `<ticker>_零售_对话_<author>.docx` (retail-investor flavored) | **`<ticker>_LP_letter_<author>.md`** — quarterly LP letter style (1-2 page, focused on attribution narrative + change-in-view, conforming to common buy-side LP comms norms). **Retail variant dropped** — US buy-side rarely delivers retail-flavored research; FINRA/SEC retail-comms rules add compliance burden | `lp-letter-template.md` |
| Earnings prep | (not in China skill) | **`<ticker>_earnings_prep.md`** — night-before checklist: consensus snapshot, KPI guide, mgmt-commentary watch list, beat/miss scenario tree | `earnings-prep-template.md` |
| Earnings flash | (not in China skill) | **`<ticker>_earnings_flash.md`** — T+30min same-day structured response | `earnings-flash-template.md` |
| Kill memo | (not in China skill) | **`<ticker>_kill_memo.md`** — falsification-triggered exit rationale, post-mortem of view | (deferred — Phase B or later as time allows) |

**Language**: English only by default. No bilingual requirement. Chinese-language variant is dropped entirely from US skill.

---

## 9. Headline conditional language (source-conditional patterns)

China conditional headline patterns (Pattern A-D in `source-stratification.md`) translate naturally to English:

| China pattern | English equivalent |
|---|---|
| "**Source-conditional 中性轻偏多 / 默认持有**. 中位 +0.5% 假设 [anchors] 在未来核验中向 S2 升级." | "**Source-conditional Hold (mild positive bias)**. 12-month median expected return +0.5% conditional on [anchor1: S3], [anchor2: S3], [anchor3: S5] graduating to S2 within [timeframe]. If any anchor is falsified in verification, downgrade to [revised view]." |
| "**基础情景中性偏空（中位 -3%）；若 4Q26 OLED IT 出货占比 ≥10%，则升级至中性轻偏多。**" | "**Base case neutral-bearish (median -3%). If [specific S2 trigger] confirmed, upgrade to neutral-mild-bullish.**" |
| "本意见以 1Q26 季报口径为基础" | "This view is anchored to [last filed period]. We will re-rate after [next anchor-S2-graduating filing]." |
| "12M 中位预期收益 +0.5%, 情景加权区间 [-2%, +3%], 该区间下沿由 S4 卖方一致 EPS 决定" | "12-month median expected return +0.5%; scenario-weighted range [-2%, +3%]; lower bound anchored to S4 consensus EPS $X (median, range $Y-$Z); if actual EPS lands at 25th percentile, lower bound shifts to -8%." |

The pattern catalogue itself is identical; only the linguistic surface differs.

---

## 10. PM red-team rubric (bug catalog adaptation)

The 10 bug classes B1-B10 are inherited largely unchanged. US-specific bug additions:

| US-specific bug | Why it appears | Verification hook |
|---|---|---|
| **B11 — Non-GAAP/GAAP gap not reconciled** | US filers report both; analysts often anchor to non-GAAP without reconciliation | `verify_non_gaap.py` (Phase D candidate) |
| **B12 — SBC not deducted from FCF** | "FCF" definitions vary; many companies exclude SBC from FCF construction; this is a free pass on real dilution | `verify_fcf_definition.py` (Phase D candidate) |
| **B13 — Factor exposure unstated** | Without Barra-style factor decomposition, the memo can't tell PM what the position adds at the book level | `verify_quant_overlay.py` (Phase D required) |
| **B14 — Capacity / ADV / days-to-exit unstated** | Position sizing without capacity check is theory; can't liquidate $50M of a $10M ADV name in 5 days at 10% participation | `verify_quant_overlay.py` (Phase D required) |

---

## 11. Verification protocol (web-search calls)

| Element | China | US | Notes |
|---|---|---|---|
| Minimum searches per memo | 12 | **12** (preserved) | `verification-protocol-us.md` |
| Primary search engine | WebSearch (Google), then site-specific (CNINFO, Sina, Eastmoney) | WebSearch + **EDGAR full-text search** (efts.sec.gov/LATEST/search-index?q=...) as the analog of CNINFO targeted search | `verification-protocol-us.md` |
| Cross-cutoff verification | Model cutoff May 2025; verify everything post-cutoff | **Model cutoff Jan 2026** (per Claude knowledge cutoff). Verify all post-cutoff specifics. **Note current date is 2026-05-15** per session context | `verification-protocol-us.md` |
| Highest-risk hallucination class | Regulatory designation status (Entity List, 1260H) | **Same** — Entity List, OFAC SDN, plus: M&A status (announced vs closed vs blocked), antitrust outcome (consent decree vs litigation vs cleared), litigation outcome (settled vs trial vs pending) | `verification-protocol-us.md` |
| Mgmt guidance verification | Against IR records | **Verify guidance against the EARNINGS CALL TRANSCRIPT** not the press release — companies sometimes give different guidance on the call vs in the 8-K. The call is the authoritative S3 source | `verification-protocol-us.md` |
| Unit confusion class | 亿 = 100M (10× error common) | **$M vs $B** (also 10×, less common but still seen); **basis points vs %** (100× error) | `verification-protocol-us.md` |

---

## 12. Tail-risk catalog (A0 events specific to US)

| A0 event | China analog | US-specific definition | Phase B target |
|---|---|---|---|
| Recession | (less probability-weighted in China skill) | **NBER recession** trigger; yield curve inversion (10Y-2Y, 10Y-3M); leading indicators (LEI); ISM PMI <48 sustained; nonfarm payrolls negative | `tail-risk-mapping-us.md` |
| Rate shock | (CGB driven) | **Fed funds +200bp** sustained; FOMC SEP shift; **10Y UST +150bp** in 6mo | `tail-risk-mapping-us.md` |
| Sector regulatory shock | MIIT/NDRC action | FDA approval/CRL outcome (biotech), FCC rulemaking (telecom), FERC order (energy), FAA grounding (aero), DOJ/FTC antitrust block (esp. M&A) | `tail-risk-mapping-us.md` |
| Sanctions / export control | BIS Entity List | **OFAC SDN addition**, **BIS Entity List addition**, **CFIUS forced divestiture** for foreign-owned US entities | `tail-risk-mapping-us.md` |
| Tariff / trade war | (consumer side) | **Section 301 tariff escalation**, **Section 232 expansion**, **EU CMA action** on US firm with EU exposure | `tail-risk-mapping-us.md` |
| Election / political | (less variable) | **Presidential transition** (Jan 20 of post-election year), **midterm Congress flip**, **state AG action**, **executive order** affecting sector | `tail-risk-mapping-us.md` |
| FX | (CNY moderate vol) | **USD index ±5% in 6mo** affects multinationals (S&P 500 ~40% foreign revenue) | `tail-risk-mapping-us.md` |
| Commodity | Mostly input side | **Oil +/-30%, gas +/-50%, copper +/-20%** sustained — affects E&P, miners, airlines, utilities, materials | `tail-risk-mapping-us.md` |
| Idiosyncratic | Customer concentration, IP litigation | **Customer concentration**, **ITC §337 import ban**, **major patent loss**, **class action settlement**, **product liability ruling** | `tail-risk-mapping-us.md` |

---

## 13. Quant-overlay layer (Phase D additions, US-specific)

Net-new in US skill (not in China skill):

| Component | Definition | Source |
|---|---|---|
| **Barra-style factor tags** | Value / Quality / Momentum / Growth / Size / Low-Vol / Liquidity exposure | Stated in memo + computed against Russell or S&P factor model (estimated from EOD prices if no premium access) |
| **Capacity analysis** | Max position size given ADV constraint; days-to-exit at 10% / 20% / 30% participation | Yahoo Finance / EDGAR for ADV; basic math |
| **Edge decay** | Time-to-priced-in estimate; thesis half-life; refresh cadence | Derived from anchor verification milestones |
| **Correlation overlay** | Pairwise corr of name with top-10 book holdings | Placeholder for now; live wiring deferred |
| **Stress overlay** | +200bp rates, -20% oil, +5% USD, recession dummy | Scenario-shock against forecast model |

---

## 14. Things in China skill that get DROPPED in US skill

- Chinese-language deliverable + Chinese rating taxonomy + 中文 retail Q&A (Layer 8)
- 北上资金 / Stock Connect (Layer 7)
- 政府补助 / subsidy carve-out as dominant forensic class (Layer 6) — replaced by ASC 606 etc.
- LP put/call on local-government-LP fab subsidiaries (Layer 6)
- RMB 亿 unit confusion (Layer 11) — replaced by $M/$B
- 龙虎榜 / 融资融券 per-name (Layer 7) — replaced by 13F / short interest
- CNINFO PDF document-ID search pattern (Layer 1) — replaced by EDGAR full-text search

## 15. Things in US skill that are NET-NEW (not in China skill)

- Earnings prep template (`earnings-prep-template.md`)
- Earnings flash template (`earnings-flash-template.md`)
- LP letter template (`lp-letter-template.md`)
- Quant-overlay layer (Barra factors, capacity, edge decay, correlation, stress) — Phase D
- 13F / Form 4 / 13D parsing as positioning primary
- Options market + short interest as positioning components
- Sector-specific valuation discipline (SaaS Rule of 40, biotech NPV pipeline, REIT AFFO, bank P/B+ROE)
- Non-GAAP/GAAP reconciliation as primary forensic gate
- Pre-announcement risk handling

---

## Implications for Phase B file-ownership table

These deltas drive the per-file scope:

- **`us-data-sources.md`** is the biggest delta (entire data substrate changes). Most content is net-new.
- **`forensic-accounting-checklist-us.md`** is large (ASC 606/842/718, non-GAAP, SBC, goodwill, pension, restatements, insider patterns, RPT, off-balance, contingent) — ~10 items, each with red/bull/bear flags
- **`regulatory-desk-us.md`** is denser than China (US has more parallel agencies + state-level)
- **`positioning-sentiment-us.md`** is denser than China (13F + Form 4 + short interest + options + ETF flows + index inclusion + activist filings + passive ownership)
- **`valuation-discipline-us.md`** requires sector branching (SaaS, banks, REITs, biotech) — keep ≤500 lines via reference structure
- **`ic-memo-template-us.md`** is structurally similar to China but English-only; preserve 12-section template
- **`source-stratification-us.md`** is a near-1:1 port; primary change is US document mapping
- **`five-scenario-framework-us.md`** is a 1:1 port; only English terminology
- **`three-method-valuation-us.md`** preserves DCF/SOTP/multi-multiple discipline; the **multi-multiple** part branches by sector (P/B for banks, EV/EBITDA for mature industrial, EV/Sales for high-growth, FCF yield for capex-heavy)
- **`gm-taxonomy-us.md`** is a 1:1 port; the only addition is **non-GAAP vs GAAP** parallel discipline
- **`bear-bridge-us.md`** is a 1:1 port; named drivers will be US-specific examples
- **`what-would-reverse-us.md`** is a 1:1 port; example denominators will be US-specific
- **`tail-risk-mapping-us.md`** uses the new US-specific A0 catalog (Layer 12)
- **`position-sizing-us.md`** adds **factor-aware sizing** (beta-adjusted vs S&P 500, sector-neutral vs sector ETF, pair-trade structure)
- **`pm-redteam-rubric-us.md`** preserves 6-9 score bands; adds B11-B14 US bugs
- **`multi-audience-delivery-us.md`** is institutional / IC pre-read / IC debate / LP letter only (no retail/Chinese)
- **`monitoring-framework-us.md`** preserves Tier 1/2/3 trigger structure; integrates earnings dates calendar, Form 4 alerts, 13F filing windows, sell-side estimate revision dashboards
- **`verification-protocol-us.md`** preserves the protocol; SEC EDGAR full-text search replaces CNINFO targeted-search; **mgmt guidance verified against transcript, not press release**

---

## Cross-references

- For shared-contract schemas to write in Phase B0, see `BUILD_PROMPT.md` §"Memory and isolation discipline" point 5 (`schemas/memo.json`, `schemas/source_tags.json`, `design/file-ownership.md`)
- For open decisions that require user confirmation before Phase B starts, see `./open-decisions.md`
