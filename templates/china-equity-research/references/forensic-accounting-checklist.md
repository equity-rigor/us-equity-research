# Forensic Accounting Checklist for Chinese Listed Companies

This checklist captures the forensic-accounting attention that distinguishes institutional-grade research from sell-side commentary on Chinese listed companies. Apply systematically to every name.

## Why Chinese A-Share Companies Need Special Forensic Attention

Three structural features make Chinese listcos particularly susceptible to misreading:

1. **Government subsidies** are pervasive and structurally important. Many "high-quality" listcos are receiving 30-60% of reported earnings as transfer payments from local or central government. The headline EPS often masks negative operating economics.

2. **Local government LP equity in subsidiaries** dilutes listco shareholders' economic interest in fab/factory profits. Listco may consolidate 100% of revenue/EBITDA but only own 25-50% economically. Sell-side often misses this.

3. **Under-disclosed contingent obligations** to local government LPs (put options, share-swap obligations, repurchase commitments) are frequently disclosed in the LP counterparty's bond rating reports rather than the listco's annual report. Forensic search of LP-side disclosures often reveals what listco didn't.

## Checklist Item 1: Subsidy Carve-Out

For every Chinese listed company:

- [ ] Pull "其他收益" (other income) line from 5-year P&L
- [ ] Identify in annual report 政府补助 (government subsidy) footnote: split between asset-related and operating-related
- [ ] Compute subsidy as % of NI to parent for each of the past 5 years
- [ ] Identify deferred income balance ("tank" of asset-related subsidies) and movement
- [ ] Check VAT super-deduction (增值税加计抵减) and R&D super-deduction tax effects
- [ ] Identify tax holidays at subsidiary level (两免三减半 for new high-tech entities)
- [ ] Compute "cash earnings ex-subsidy" — reported NI minus aftertax subsidies
- [ ] Compare cash earnings trajectory to reported earnings — are they tracking, or diverging?

**Red flag**: Subsidy as % of NI > 40% sustained — earnings quality is heavily dependent on government transfer.

**Bull supporting evidence**: Deferred income tank growing — secures future recognition for years.

**Bear warning**: Operating subsidies declining or central guidance signaling rationalization — forward run-rate at risk.

## Checklist Item 2: Minority Interest Look-Through

For every Chinese listed company with material consolidated subsidiaries:

- [ ] Pull 主要子公司 (principal subsidiaries) footnote from annual report
- [ ] For each material subsidiary, identify: listco economic %, registered capital, net assets, revenue, net profit
- [ ] Calculate aggregate minority interest in NI for past 5 years
- [ ] Calculate cumulative MI absorbed losses (when net result is negative) — this measures the dollars of LP capital that absorbed listco losses
- [ ] Calculate cumulative minority equity raises in cash flow — measures the dollars of LP capital injected
- [ ] Identify the largest 5 "important MI subsidiaries" (often disclosed as aggregate)
- [ ] Map LP counterparties to provincial/municipal investment vehicles (Hefei BIG, Chengdu SDIC, Wuhan Optical Valley, etc.)

**Red flag**: Listco economic % in major operating subsidiary < 30% — most fab profit accrues to LPs, not listco shareholders.

**Bull supporting evidence**: Listco buying up minority stakes (LP exits at par) — eliminates future MI dilution.

**Bear warning**: LP counterparty with put option that may be exercised — contingent cash drain.

## Checklist Item 3: LP Put/Call Clauses (Hidden Obligations)

The most under-disclosed risk in Chinese listcos. Often surfaced via LP-side bond rating reports rather than listco filings.

For each major operating subsidiary co-owned with local government LPs:

- [ ] Pull original 关联交易公告 / 重大对外投资公告 from CNINFO for the subsidiary's establishment
- [ ] Identify the LP counterparty's investment terms: original contribution, voting rights, exit mechanism
- [ ] Search for the LP counterparty's bond rating reports on SSE / SZSE bond market
- [ ] Look for clauses like:
  - "[Listco] 承诺于 [date] 前完成定向增发或资产重组将LP股权置换为上市公司股份" (share swap commitment)
  - "[Listco] 有权于 [date] 后按照原始出资额回购LP股权" (call option)
  - "[LP] 有权要求[Listco] 按照原始出资额加X%年利率回购" (put option with IRR)
- [ ] Document trigger conditions, deadline, default remedies, cash settlement alternatives
- [ ] Estimate dilution impact (if share placement) or cash impact (if cash buyout)
- [ ] Check whether the obligation has been executed, deferred, or is still pending

**Red flag**: Pending obligation past deadline with no listco disclosure — under-disclosed material item.

**Reference precedent**: BOE Technology's Mianyang B11 obligation due Dec 2022, never executed, surfaced via Mianyang Tech City Development Investment 2024 bond rating report. RMB 4.3bn book value, ~2.1% IV haircut probability-weighted.

## Checklist Item 4: Capex / Depreciation / FCF

For capex-heavy industrials specifically:

- [ ] Pull 10-year history of capex (cash flow statement: "购建固定资产" line) and D&A
- [ ] Calculate cumulative capex vs. cumulative D&A
- [ ] Identify ratio: < 1.0x = harvest mode; > 1.0x = reinvestment treadmill
- [ ] For each major project under construction (在建工程), identify: budget, deployed to date, remaining capex
- [ ] Build depreciation waterfall: which production assets roll off when? Annual P&L impact.
- [ ] Project capex run-rate next 3 years based on remaining project capex + maintenance
- [ ] Project FCF (CFO - capex - dividend - LP buyouts)
- [ ] Identify FCF inflection year if capex tapers

**Red flag**: Capex > D&A for 5+ years — capital being consumed faster than depreciated; cumulative FCF likely negative.

**Bull supporting evidence**: Capex tapering and D&A peaking — FCF inflection in next 1-2 years.

**Critical**: Depreciation will RISE as CIP transfers to PP&E, even as new capex declines. Don't model "capex down → FCF up" without modeling D&A increase from project completion.

## Checklist Item 5: Inventory Composition

Especially for cyclical commodity producers (display, semis, autos, materials):

- [ ] Pull inventory composition footnote from annual report
- [ ] Categorize: 原材料 (raw materials), 在产品 (WIP), 库存商品 (finished goods), 周转材料 (consumables)
- [ ] Calculate YoY change in each category
- [ ] Compare to write-down provisions movement: new provisions, reversed/written off

**Bull pattern**: Raw materials + WIP build > 15% YoY (input-side build for ramp) + finished goods flat or declining + write-down provisions running off (clean-out of legacy stale inventory)

**Bear pattern**: Finished goods build > 20% YoY (channel-stuffing or demand miss) + new write-down provisions accelerating

**Reference**: BOE FY2025 had RMB 27.7bn net inventory (+19% YoY) BUT raw materials +12.9% and WIP +28.2% drove most of the build, while finished goods only +4.7% and existing reserves were drawn down — bull pattern, validated by Q1 2026 inventory drop -8% Q/Q.

## Checklist Item 6: Operating Cash Flow Quality

Beyond absolute CFO, examine quality:

- [ ] CFO / NI to parent ratio — should be > 1.0x sustainably (D&A is non-cash; CFO benefits from depreciation)
- [ ] Working capital changes — receivables, payables, inventory contributions to CFO
- [ ] Tax refunds received — common in China for VAT export refunds + R&D super-deduction
- [ ] Other operating cash inflows — often captures cash subsidies received separately
- [ ] CFO ex-WC changes — "true" cash earnings adjusted for working capital noise

**Red flag**: CFO declining YoY while NI growing — working capital deterioration, possibly receivables stretching

**Bull pattern**: CFO consistently > NI × 2x (depreciation-heavy business with positive working capital trajectory)

## Checklist Item 7: Debt Structure & Refinancing

For leveraged industrials:

- [ ] Pull long-term loan composition: bank loans (project finance), bonds, lease liabilities
- [ ] Coupon range: identify spread between high and low rates
- [ ] Recent issuance trend: are new bonds at lower rates than legacy debt? (Refinancing tailwind)
- [ ] Maturity ladder if disclosed (often only coarse buckets in Chinese filings)
- [ ] Foreign currency exposure of debt (USD-denominated portion)
- [ ] Net long/short USD position from foreign assets vs. liabilities
- [ ] Pledged assets — what % of net PP&E and CIP is collateralized

**Bull pattern**: New bond issuance at 1.7-2.5% replacing legacy 4-5% bank loans — material interest expense tailwind.

**Bear pattern**: Pledged assets > 60% of PP&E — limited remaining collateral capacity for additional borrowing.

## Checklist Item 8: Effective Tax Rate Volatility

For Chinese listcos with multiple subsidiary tax statuses:

- [ ] Pull 5-year ETR (income tax / pre-tax income)
- [ ] Identify drivers of variability: NOL utilization, R&D super-deduction, HNTE 15% rate, two-free-three-half holidays
- [ ] Project normalized ETR — most Chinese listcos normalize to 22-26%
- [ ] Identify subsidiaries entering/exiting tax holidays — discrete ETR jumps possible

**Bear warning**: NOL utilization exhausting → ETR jumps from low to normalized → reported NI compression.

## Checklist Item 9: Related-Party Transactions

For controlled subsidiaries with state ownership:

- [ ] Pull 关联交易 footnote from annual report
- [ ] Identify controlling shareholder umbrella entities and other listed companies under same parent
- [ ] Material RPT volume — purchases from related parties, sales to related parties
- [ ] Look for related-party financing (loans from / to)
- [ ] Look for asset transfers between RPs at potentially non-market prices

**Red flag**: Material RPT volume with explanation that doesn't make commercial sense — possible value transfer.

**Reference precedent**: BOE sits within Beijing Electronics Holding umbrella with NAURA (002371), Yandong Micro (688172), ChipONE (688593). Captive procurement channel from controller is RPT optionality but also potential captive pricing.

## Checklist Item 10: Segment Performance

For diversified listcos:

- [ ] Pull segment revenue and segment NI from annual report (often only annual, not quarterly)
- [ ] Calculate segment gross margins
- [ ] Identify segments hiding losses or generating most of profit
- [ ] Cross-check segment growth rates vs. industry data — is segment outperforming or underperforming?

**Bull pattern**: Subsidies-dependent segment shrinking as % of revenue while profitable core segment grows — reduced subsidy reliance.

**Bear pattern**: Core segment margin declining + non-core / one-time segment driving headline growth.

---

## How to Use This Checklist

Apply Items 1, 2, 3, 4, 5 systematically in Phase 1 FS agent prompt. Items 6, 7, 8 in Phase 2 A2 forensic continuation. Items 9, 10 throughout.

Each forensic finding should be tagged with:
- **Source** (specific footnote / page)
- **Magnitude** (RMB or % impact)
- **Direction** (bull / bear)
- **Verification status** (verified via primary source / inferred / estimate)

Forensic findings inform the normalized P&L bridge in the IC memo and the "what would change my mind" appendix.
