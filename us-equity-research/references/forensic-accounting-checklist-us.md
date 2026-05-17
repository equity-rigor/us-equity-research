# Forensic Accounting Checklist — US Listed Companies

This checklist is the US-localized analog of the China forensic discipline. Where the China skill anchored on government subsidies, MI dilution, LP put/call clauses, and RMB 亿 unit confusion, the US version anchors on **ASC 606 revenue recognition**, **ASC 842 lease accounting**, **ASC 718 SBC and the non-GAAP/GAAP reconciliation gap**, **goodwill impairment triggers**, **insider Form 4 patterns**, **8-K restatement / auditor-change signals**, and **§174 R&D capitalization**. The single most-common red-team kill in US IC memos is an unscrutinized non-GAAP → GAAP gap; the second is treating "FCF" as defined by management when SBC is excluded.

This file feeds the structured `forensic_flags` block in `schemas/memo.json`. It hooks into verification gates G11 (non-GAAP/GAAP reconciliation), G12 (SBC-in-FCF treatment), and indirectly G6 (source-tag discipline on first appearance of any forensic finding). Bug classes B11 and B12 in `pm-redteam-rubric-us.md` are the failure modes this checklist exists to prevent.

Apply Items 1–6 in Phase 1 FS-agent prompt; Items 7–10 in Phase 2 forensic continuation; Items 11–15 cross-cuttingly. Every finding tagged with `(S1: …)` or `(S2: …)` at first appearance per `source-stratification-us.md` and D16.

---

## Item 1 — ASC 606 Revenue Recognition

**What to pull**: 10-K Item 7 MD&A revenue commentary; 10-K Note "Revenue" (typically Note 2 or 3, references ASC 606); 10-Q quarterly revenue disclosures; 8-K Item 2.02 quarterly earnings exhibits. Five-step model: contract → performance obligations (POBs) → transaction price → allocation → recognition.

**Checklist sub-items**:
- [ ] Pull POB structure from Revenue note. Identify distinct POBs (license, hosting, support, professional services, hardware bundles).
- [ ] Compare deferred revenue / contract liabilities balance YoY (BS) and as % of forward 12mo revenue. Declining deferred revenue in a subscription business = churn canary.
- [ ] Calculate DSO trend (accounts receivable / quarterly revenue × 90). A DSO spike of >5–10 days vs prior 4-quarter average signals bill-and-hold or channel stuffing.
- [ ] Identify any "bill-and-hold" or "right-of-return" language in revenue note.
- [ ] For SaaS / software: check POB allocation method (relative-SSP) and whether the company front-loads license vs ratable subscription components.
- [ ] Check 10-K Item 7 for contract modifications language and any cumulative catch-up adjustments.

**Red flag pattern**: DSO +7 days YoY with revenue acceleration → revenue quality concern. Material "contract modification" adjustments inflating recognized revenue. Deferred revenue declining >5% YoY in a stated growth business.

**Bull supporting evidence**: Deferred revenue / RPO growing > revenue growth (forward demand visibility expanding). Sequential DSO compression. POBs clearly enumerated with stable allocation methodology multi-year.

**Bear warning**: License-revenue front-loading creating non-recurring boosts; aggressive bundled-SaaS POB allocation pulling subscription forward. **G11 hook**: any ASC 606 adjustment that lands in non-GAAP-only reconciliation must be reconciled to GAAP.

---

## Item 2 — ASC 842 Lease Accounting

**What to pull**: 10-K Note "Leases" (typically Note 8–12); operating lease right-of-use (ROU) asset on BS; lease liability current + non-current; future minimum lease payments schedule by year.

**Checklist sub-items**:
- [ ] Pull operating lease ROU asset and lease liability balances; reconcile to PV of future minimum lease payments at the disclosed discount rate.
- [ ] Compare PV of operating lease commitments to net debt — adjusted leverage = (net debt + lease liability) / EBITDAR.
- [ ] For pre-2019 multi-year comparisons, adjust legacy off-BS operating leases back onto BS; ASC 842 became effective for public companies in FY2019.
- [ ] Identify any synthetic leases or build-to-suit arrangements in the lease note.
- [ ] Lease-vs-buy distortion: companies that lease heavily (retailers, restaurants) report lower capex but higher rent; comparable-store FCF requires lease-adjusted view.

**Red flag pattern**: ROU asset materially smaller than 5-year sum of future minimum lease payments (suggests aggressive discount rate). Lease liability growing while same-store revenue declines (over-expansion + later writedowns).

**Bull supporting evidence**: Lease liability flat or declining while revenue grows (operating leverage on existing footprint).

**Bear warning**: Retail / restaurant operators with rising lease liability + declining same-store sales — classic over-expansion pattern that ends in store-closure charges and ROU impairment.

---

## Item 3 — ASC 718 Stock-Based Compensation

**What to pull**: 10-K Note "Stock-Based Compensation"; CF Statement "Stock-based compensation expense" add-back to OCF; share count walk (basic and diluted) in 10-K Item 6 or Note "Earnings per Share"; buyback disclosures in 10-K Item 5 / 10-Q Part II Item 2 (ASR programs).

**Checklist sub-items**:
- [ ] Compute SBC as % of revenue (5-year trend). Software / semis often run 10–25%; mature industrials <2%. NVDA runs ~15-20% — a real number that drives the B12 conversation.
- [ ] Compute SBC as % of operating cash flow. If SBC > 50% of OCF, the company's OCF is heavily a non-cash add-back, not real cash generation.
- [ ] Compute **buyback-to-SBC ratio** = buyback $ / SBC $. ≥1.0× = real return to shareholders, SBC dilution offset. <1.0× = dilution masked by ASR optics. AAPL historically ~3-5× (true return); some SaaS names <0.5× (pure dilution).
- [ ] Pull RSU / option vest schedule from 10-K Note. Project dilution from un-vested awards.
- [ ] Identify whether non-GAAP EPS adds back SBC (it usually does). Quantify the non-GAAP/GAAP EPS gap attributable solely to SBC.

**Red flag pattern**: SBC > 15% of revenue with buyback-to-SBC ratio < 0.8× for 3+ consecutive years — real dilution being masked.

**Bull supporting evidence**: Buyback-to-SBC ratio sustainably > 1.5× with declining share count (AAPL pattern).

**Bear warning**: SBC > 20% of revenue + buyback < SBC + diluted share count growing — classic Silicon Valley dilution treadmill. **G12 hook**: if the memo's "FCF" definition adds back SBC, the memo MUST disclose this and present an alternative FCF metric net of SBC; not doing so is B12.

---

## Item 4 — ASC 350 Goodwill Impairment

**What to pull**: 10-K Note "Goodwill and Other Intangible Assets"; 10-K Item 7 critical accounting estimates; segment goodwill allocation table.

**Checklist sub-items**:
- [ ] Compute goodwill as % of total assets and as % of equity. >50% of equity = high concentration.
- [ ] Identify reporting units (ASC 350 requires impairment test at reporting-unit level, typically = segment or one level below).
- [ ] Check for recent triggering events: stock price drop >20%, segment underperformance, loss of major customer, regulatory ruling.
- [ ] Pull historical impairment charges and their reporting-unit attribution.
- [ ] Cross-reference recent M&A deals against current segment performance — under-performing acquisitions are impairment candidates.

**Red flag pattern**: Goodwill > 60% of equity + segment containing recent large deal shows declining revenue / margins → likely impairment in next reporting period.

**Bull supporting evidence**: Goodwill stable or declining (clean BS); no recent triggering events.

**Bear warning**: Stock down >25% intra-quarter + goodwill > 40% of equity = forced ASC 350 step-1 test that may produce material non-cash impairment (JPM-style large bank acquired franchises, financial-services rollups, ad-tech rollups historically vulnerable).

---

## Item 5 — Non-GAAP-to-GAAP Reconciliation Discipline (Reg G + Item 10(e))

**The single most important US forensic check.** SEC Reg G (17 CFR 244) and Item 10(e) of Regulation S-K require: (a) GAAP measure given equal or greater prominence, (b) quantitative reconciliation to nearest GAAP measure, (c) explanation of why non-GAAP is useful to investors. The reconciliation table is mandatory in any 8-K Item 2.02 earnings press release and any S-1 / 10-K filing that uses non-GAAP measures.

**What to pull**: 8-K Item 2.02 earnings press release exhibit (most accessible); 10-K Item 7 MD&A; investor presentations on company IR site; 10-Q non-GAAP reconciliation tables.

**Checklist sub-items**:
- [ ] Pull 5-year history of non-GAAP NI vs GAAP NI. Compute the delta as a % of GAAP NI for each year.
- [ ] Identify the largest line items in the reconciliation. Common: SBC, restructuring, M&A integration, amortization of acquired intangibles, litigation reserves, "other".
- [ ] Flag any "one-time" charge recurring 3+ consecutive years — by definition not one-time.
- [ ] Test the "adjusted EBITDA" definition. Companies sometimes adjust away SBC + recurring restructuring + "transaction costs" → adj. EBITDA can be 2× GAAP EBITDA.
- [ ] Test the "FCF" definition. Common abuses: (a) excluding capex but capitalizing R&D, (b) adding back SBC, (c) excluding lease payments, (d) excluding working capital. **Tie to G12**.

**Red flag pattern**: Non-GAAP-to-GAAP NI delta > 25% sustained for 5 years; "restructuring" charges recurring annually; "adjusted EBITDA" excluding SBC + lease + recurring litigation. **G11 hook**: this is the gate trigger. If non-GAAP NI > GAAP NI by >25% 5y average AND reconciliation table not present in citations, G11 fails.

**Bull supporting evidence**: Non-GAAP-to-GAAP delta stable and <15% (modest adjustments); reconciliation table consistently present and discussed in MD&A; AAPL-style discipline (minimal non-GAAP usage, primarily for FX-neutral revenue).

**Bear warning**: Persistent "one-time" charges that re-appear; "Adjusted EBITDA" that is 50%+ above GAAP EBIT after rolling D&A back in; FCF defined to exclude SBC + lease + capitalized R&D simultaneously.

---

## Item 6 — Working Capital Trends

**What to pull**: 10-K Item 8 Balance Sheet; CF Statement working-capital section; quarterly 10-Q same.

**Checklist sub-items**:
- [ ] DSO trend (AR / quarterly revenue × 90). 5-quarter rolling.
- [ ] DIO trend (inventory / quarterly COGS × 90). 5-quarter rolling.
- [ ] DPO trend (AP / quarterly COGS × 90).
- [ ] Deferred revenue / contract liabilities trend.
- [ ] Cash conversion cycle = DSO + DIO − DPO. Trend break is the signal.

**Red flag pattern**: DSO +10 days YoY (revenue acceleration funded by receivables stretching); DIO +20% YoY without commensurate revenue growth (channel stuffing or demand miss — WBA/WMT historical patterns).

**Bull supporting evidence**: DSO compressing while revenue accelerating; deferred revenue / RPO growing > revenue growth.

**Bear warning**: Finished-goods inventory build > 25% YoY while revenue growth flat — classic demand miss pattern; expect inventory writedown in next 1-2 quarters.

---

## Item 7 — Auditor Changes and Going Concern

**What to pull**: 8-K Item 4.01 (changes in registrant's certifying accountant); 10-K Report of Independent Registered Public Accounting Firm; PCAOB inspection reports for the firm (pcaobus.org).

**Checklist sub-items**:
- [ ] Identify current auditor and tenure. Big 4 = PwC, EY, Deloitte, KPMG.
- [ ] Search EDGAR for 8-K Item 4.01 filings in past 3 years.
- [ ] If auditor changed: was it Big 4 → Big 4 (often benign) or Big 4 → mid-tier (BDO, Grant Thornton, RSM) — the latter is mild red flag.
- [ ] Check for any "going concern" language in the auditor's report on the 10-K — severe red flag.
- [ ] Pull PCAOB inspection report for the company's auditor (annual for ≥100 issuers, triennial otherwise). High deficiency rate at the firm level adds caution.

**Red flag pattern**: Big 4 → mid-tier auditor change + concurrent CFO departure (8-K Item 5.02) = compounding signal. Going-concern qualification = severe.

**Bear warning**: Auditor resignation (vs dismissal — distinguish in 8-K Item 4.01 text) is materially worse than dismissal.

---

## Item 8 — Restatements (8-K Item 4.02)

**What to pull**: 8-K Item 4.02 (non-reliance on previously issued financial statements); subsequent 10-K/A or 10-Q/A amendments.

**Checklist sub-items**:
- [ ] Search EDGAR for any 8-K Item 4.02 in past 5 years.
- [ ] If present: identify which periods are non-reliable, what items are affected, magnitude.
- [ ] Distinguish "Big R" (full restatement, formal 10-K/A) from "little r" (out-of-period adjustment, no formal restatement).
- [ ] Check PCAOB inspection reports for the auditor in the affected period.
- [ ] Cross-reference any concurrent SEC AAER (Accounting and Auditing Enforcement Release) on the company.

**Red flag pattern**: Material "Big R" restatement = severe; downgrades all S1 data from restated periods to "non-reliable" pending the 10-K/A. **S-tag discipline**: any 10-K filing from a restated period must be tagged Pending until amended filing posts.

**Bear warning**: Restatement + recent auditor change + insider selling cluster (Form 4) = composite signal that typically precedes major drawdowns.

---

## Item 9 — Pension / OPEB Underfunding

**What to pull**: 10-K Note "Employee Benefits" or "Pensions and Other Postretirement Benefits"; PBO (projected benefit obligation), ABO (accumulated benefit obligation), and fair value of plan assets; service / interest / expected return / actuarial gain-loss components of expense.

**Checklist sub-items**:
- [ ] Compute funded status = FV of plan assets − PBO. Negative = underfunded.
- [ ] Funded-status ratio = FV plan assets / PBO.
- [ ] Check ERISA mandatory contribution triggers (typically <80% funded triggers benefit restrictions; <60% triggers additional restrictions).
- [ ] Identify discount rate used (sensitive to long-bond rates) and expected return on plan assets (sensitive to mix).
- [ ] For OPEB: retiree medical obligations are typically unfunded by design; check growth in OPEB liability.

**Red flag pattern**: Funded-status ratio < 80% + discount rate at decade low (rate-rise relief temporary) + workforce aging.

**Bear warning**: Legacy autos (GM, Ford, Stellantis), airlines (legacy LCCs less exposed than legacy carriers AAL/UAL/DAL on certain plans), and industrials (BA — Boeing — material PBO + OPEB) materially exposed. BA's OPEB liability is large enough to be a non-trivial part of EV; an analyst who treats pension obligations as net debt vs ignoring them gets a 5-10% different equity value.

**Bull supporting evidence**: Plans frozen for new hires (closed groups); funded-status ratio > 100% (over-funded) — rare but exists (Lockheed at times).

---

## Item 10 — Form 4 Insider Patterns

**What to pull**: SEC EDGAR Form 4 filings (`sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=*&type=4`); free aggregators: openinsider.com, secform4.com, insiderinsights.com.

**Checklist sub-items**:
- [ ] Aggregate net insider activity over trailing 90 days, 6 months, 12 months in $ terms.
- [ ] Distinguish transaction codes: **P** (open-market purchase, highest signal), **S** (open-market sale), **A** (grant), **F** (tax withholding), **M** (option exercise), **G** (gift).
- [ ] Distinguish 10b5-1 plan dispositions (formulaic — Box 10b5-1 checked) from discretionary trades (higher informational value).
- [ ] Look for **cluster patterns**: ≥3 insiders transacting in same direction within 30 days.
- [ ] Track each insider's position-after-transaction. A cluster of executives selling 50% of their holdings = stronger signal than each selling 5%.

**Red flag pattern (mild bear)**: 3+ executive cluster selling in discretionary transactions (not 10b5-1) ahead of earnings; CEO+CFO+COO all selling within 60 days.

**Bull supporting evidence (mild bull)**: Cluster buying — multiple insiders open-market purchasing (transaction code P), especially at recent stock lows. Very rare and high-signal when it occurs.

**Bear warning**: Form 4 selling + 8-K Item 4.02 restatement + auditor change forms a composite high-conviction bearish cluster historically associated with major drawdowns.

**Note on 10b5-1 plans**: Plans adopted are disclosed in 8-K (often Item 8.01); SEC's 2022 Rule 10b5-1 amendments require a 90-day cooling-off period after plan adoption. A plan adopted shortly before a sequence of large dispositions is worth scrutiny.

---

## Item 11 — Related-Party Transactions (DEF 14A Item 404)

**What to pull**: DEF 14A (definitive proxy) Item 404 "Certain Relationships and Related Transactions"; 10-K Note "Related Party Transactions" (if material).

**Checklist sub-items**:
- [ ] Pull D&O / 5%-holder transactions disclosed under Item 404.
- [ ] Identify any transactions at non-market pricing (e.g., D&O consulting agreements, family-member employment, real-estate transactions with insiders).
- [ ] Verify the company's RPT policy and approval mechanism (audit committee or independent directors).
- [ ] For controlled companies (>50% voting held by a single holder, e.g., META Class B): the Item 404 disclosure regime is the primary investor protection.

**Red flag pattern**: Material consulting / service fees paid to D&O family entities without commercial rationale; founder-controlled entity with extensive related-party leasing or supply arrangements.

**Bear warning**: Multi-class share structures (founder super-vote) combined with material related-party transactions often signal weak governance; price in the governance discount.

---

## Item 12 — Off-Balance-Sheet Items

**What to pull**: 10-K Note "Variable Interest Entities" (ASC 810); 10-K Item 7A market risk / contractual obligations; 10-K Note "Commitments"; any synthetic-lease structures.

**Checklist sub-items**:
- [ ] Identify any VIEs and whether the company is the primary beneficiary (consolidated) or holds a variable interest (not consolidated).
- [ ] Pull material JV equity-method investments — segment-level economic interest may differ from accounting consolidation.
- [ ] Identify securitizations (receivables financing, asset-backed structures) — pre-2008 abuse class, still relevant for financials and consumer finance names.
- [ ] Check for synthetic leases or build-to-suit arrangements not on BS.
- [ ] Pull contractual purchase commitments (10-K Item 7A or Commitments note) — long-dated supply agreements that create operating leverage exposure.

**Red flag pattern**: Material unconsolidated VIE with company exposure (guarantees, performance commitments) where economic interest > accounting interest.

**Bear warning**: For consumer finance / specialty finance names — large receivables sold into off-BS securitization vehicles with retained risk; for industrials — long-dated take-or-pay supply contracts that bind capex.

---

## Item 13 — Contingent Liabilities (Commitments and Contingencies)

**What to pull**: 10-K Note "Commitments and Contingencies"; quarterly updates in 10-Q.

**Checklist sub-items**:
- [ ] Pull litigation reserves disclosed under ASC 450 ("probable" + reasonably estimable).
- [ ] Identify environmental remediation accruals (CERCLA / Superfund) — common for materials, energy, legacy industrials.
- [ ] Pull uncertain tax positions under FIN 48 / ASC 740 — gross unrecognized tax benefits and reasonably possible 12-month change.
- [ ] Identify guarantees (parent guarantees of subsidiary debt, performance bonds, letters of credit).
- [ ] Cross-reference open litigation against PACER docket (federal) and state-court searches for material cases.

**Red flag pattern**: ASC 740 uncertain tax positions > 10% of cash + investments AND IRS examination open in multiple jurisdictions; environmental remediation accrual growing while disclosed sites unchanged (cost overruns); litigation reserves disclosed as "not estimable" for matters where peers have disclosed estimates.

**Bear warning**: Multi-billion-$ CERCLA exposure (legacy chemicals — DD/DOW historical), opioid litigation reserves (CVS / WBA / TEVA), product-liability class actions (autos, healthcare).

---

## Item 14 — IRA / CHIPS / §174 Tax Effects

**What to pull**: 10-K Note "Income Taxes"; ETR reconciliation table; 10-K Item 7 MD&A tax commentary.

**Checklist sub-items**:
- [ ] Identify any IRA Section 45X advanced-manufacturing production credit (solar, batteries, wind components, semis); 45X is refundable / transferable — meaningful cash add for FSLR, ON, MP, etc.
- [ ] Identify Section 48 / 48D investment tax credits — CHIPS Act 48D (25% for advanced semi fabs) is material for INTC, TSM US fabs, GFS, MU.
- [ ] R&D credit Section 41 — typically <2% of pre-tax income reduction for tech / pharma.
- [ ] **§174 R&D capitalization** — under TCJA 2017, effective FY2022, all R&D must be capitalized and amortized (5-year domestic, 15-year foreign). This created a cash tax headwind for R&D-heavy names. Material for MRK, PFE, large pharma; meaningful for software / semis. Reconcile book R&D expense to tax R&D capitalized.
- [ ] NOL carryforward — post-TCJA limited to 80% of taxable income annually; pre-TCJA NOLs grandfathered with different rules.
- [ ] Pillar 2 GMT (15% global minimum) and CAMT (15% corporate alternative min tax) — material for highly profitable multinationals (MSFT, AAPL, GOOG, META).

**Red flag pattern**: Effective tax rate volatility >5pp YoY without disclosed driver; §174 amortization creating cash tax > book tax with no quantitative disclosure of the gap.

**Bull supporting evidence**: 45X / 48D credits monetized via tax-credit transfer market (refundable / transferable) adding 5-10% to cash flow for clean-energy manufacturers.

**Bear warning**: §174 cash tax headwind is real but transient (5-year amortization), and there is bipartisan interest in repeal. Memos that assume repeal embedded in base case carry a policy assumption that must be flagged S3-S5.

**Note**: This is a much smaller analog to China's government-subsidy carve-out. In most US names tax credits and §174 effects move EPS 1-5%; they rarely dominate the thesis. Exceptions: clean-energy manufacturers where 45X is 20%+ of operating cash flow.

---

## Item 15 — Unit Confusion (USD millions vs billions vs thousands)

**What to pull**: 10-K filing cover page or first page of financial statements; small-cap filings under $300M revenue.

**Checklist sub-items**:
- [ ] Identify reporting unit on the financial statements header — "(in millions, except per share data)" is most common; some smaller filers use "(in thousands)"; some larger filers use "(in millions of US dollars)" or "(in US$ billions)".
- [ ] Cross-check that the memo's specific numbers carry explicit `$M` / `$B` / `$K` units consistently.
- [ ] Reconcile market cap (in billions) vs revenue (sometimes in millions) — easy 1000× error.
- [ ] Basis points vs % — 50 bps ≠ 50%. The percentage-vs-bps confusion is 100×.

**Red flag pattern**: Same memo using "$ million" and "$ billion" interchangeably for the same metric; price target stated without unit (e.g., "200" not "$200"); margin compression stated as "50 bps" but modeled as 0.50% (correct) vs 50% (wrong).

**Bear warning**: Less frequent than China's 亿 = 100M confusion, but still a documented hallucination class. The verification protocol (G6 source-tag gate at first appearance, plus the cross-cutoff verification rule per `source-stratification-us.md`) catches most cases but human review of unit consistency is the final defense.

---

## How to Use This Checklist

1. **Phase 1 FS-agent prompt** — Items 1, 2, 3, 4, 5, 6 systematically. The non-GAAP/GAAP discipline (Item 5) is the highest-priority US gate and feeds the `non_gaap_to_gaap_delta_pct_ni_5y_avg` field in `forensic_flags`.
2. **Phase 2 forensic continuation** — Items 7, 8, 9, 10. The 8-K Item 4.01 / Item 4.02 / Form 4 cluster check is the standard US auditor + insider sweep.
3. **Cross-cutting** — Items 11, 12, 13, 14, 15.

Every forensic finding tagged with:
- **Source S-level + citation** per `source-stratification-us.md` (e.g., `(S1: NVDA 2024 10-K Note 11 Stock-Based Compensation)`).
- **Magnitude** ($M, $B, %, bps — explicit units always; Item 15).
- **Direction** (bull / bear / neutral).
- **Verification status** (verified via primary source / inferred / estimate).

Forensic findings populate `forensic_flags` in the structured memo and the "what would change my mind" section. Items 3 (SBC) and 5 (non-GAAP) drive the G11 / G12 verification gates; the rest are informational inputs that strengthen the rigor score per `pm-redteam-rubric-us.md`.

---

## Cross-references

- **Schema**: `schemas/memo.json` `forensic_flags` definition — the structured target for this checklist.
- **Verification gates**: `schemas/verification_gates.json` G11 (non-GAAP/GAAP reconciliation), G12 (SBC-in-FCF), G6 (source-tag discipline).
- **Source discipline**: `source-stratification-us.md` — citation regex and S-level tagging for every forensic finding.
- **Data sources**: `us-data-sources.md` — EDGAR full-text search patterns for 8-K Item 4.01 / 4.02 lookups, Form 4 aggregators, PCAOB inspection reports.
- **Red-team rubric**: `pm-redteam-rubric-us.md` — B11 (non-GAAP gap unscrutinized) and B12 (SBC not deducted from FCF) are the failure modes this checklist exists to prevent.
- **Phase prompts**: `phase-1-deep-dive-us.md` and `phase-2-continuation-us.md` — operational entry points where this checklist applies.
- **Open decisions referenced**: D5 (EDGAR-only default — all sources above are free at the SEC), D9 (12 WebSearch minimum — restatement / auditor / Form 4 checks count), D16 (citation regex), D22 (forensic_flags structured field decomposition).
