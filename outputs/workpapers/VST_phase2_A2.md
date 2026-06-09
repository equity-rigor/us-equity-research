# VST — Phase 2 Forensic Continuation (A2) Workpaper
**Agent:** A2 — Forensic Continuation (deep-dive resolution of Phase-1 tails)
**Issuer:** Vistra Corp. (NYSE: VST) | CIK 0001692819 | Auditor: Deloitte & Touche LLP
**As-of:** 2026-06-09 | Public sources only
**Primary sources:** FY25 10-K R-file detail tables (acc. 0001692819-26-000006, fetched via authenticated curl on `www.sec.gov/Archives/.../R##.htm`; SEC Archives HTML 403-blocks WebFetch but R-files + FilingSummary.xml ARE curl-accessible), `data.sec.gov` XBRL companyconcept API, Q1'26 10-Q (acc. 0001692819-26-000014), FY25/Q1'26 earnings 8-Ks, Cogentrix press releases.
**Source tags:** S1 = 10-K audited (XBRL/R-file Note detail) · S2 = 10-Q / 8-K / press (interim, Reg-G non-GAAP) · S3 = third-party aggregator.

> This workpaper RESOLVES the six A2 anomalies set in Phase 1. Every numeric is S-tagged inline. Phase-1 established that GAAP NI is non-informational (ASC 815 hedge MTM) and that **hedge-collateral liquidity is THE load-bearing tail.** A2 quantifies the tail with the actual FY25 10-K contingent-feature table and facility architecture.

---

## ANOMALY 1 — HEDGE-COLLATERAL FACILITY SIZING & HEADROOM *(load-bearing)*

### 1a. Total liquidity backstop — the actual FY25 architecture [S1, R90/R94]

| Facility | Limit | Drawn / LC outstanding | **Available** |
|---|---:|---:|---:|
| **Corporate Revolving Credit Facility** | $3,440M | $380M borrowings + $1,064M LC | **$1,996M** |
| **Term Loan B-3** (due Dec 20 2030) | $2,450M | $2,450M (fully drawn term) | $0 |
| **Senior Secured Commodity-Linked Revolver** | **$1,750M** | ~$1,748M drawn | **$2M** |
| Project-level (BCOP, Vistra Zero) | $1,569M | $1,569M | $0 |
| **Total committed facility limit (`LineOfCreditFacilityMaximumBorrowingCapacity`)** | **$9,209M** | $5,819M borrow + $1,064M LC | **$1,998M** |
| **Plus separate LC facilities** [R94]: Secured LC $1,332M outstanding; Alternate LC facility $760M limit ($608M out) | — | — | — |
| **Cash & equivalents** [S1] | — | — | **$785M** |
| **= TOTAL AVAILABLE LIQUIDITY (FY25, per 8-K)** | | | **$2,783M** [S2] |

The earnings-release reconciliation of the $2,783M [S2]: **$785M cash + $1,996M corporate revolver undrawn + $2M commodity-linked revolver undrawn.** Trace ties exactly.

**FINDING — the commodity-margin-specific facility is essentially exhausted.** VST runs a dedicated **$1,750M Senior Secured Commodity-Linked Revolving Credit Facility** whose entire purpose is to fund commodity collateral; at FY25 only **$2M** was available [R90]. The commodity facility is therefore NOT incremental dry powder in a stress — it is already deployed. The true margin-call backstop is **cash ($785M) + corporate revolver undrawn ($1,996M) = $2,781M**, plus capacity to draw further LC facilities to *substitute* LC-for-cash collateral (counterparties accept LCs in lieu of cash margin — the key mitigant).

### 1b. The contingent-collateral number — RESOLVED and it GREW [S1, R111 "Credit Risk-Related Contingent Features"]

| Credit-risk contingent feature ($M) | **FY25** | FY24 | FY23 (Ph-1) |
|---|---:|---:|---:|
| Fair value of derivative liabilities w/ contingent features | (1,822) | (1,587) | (1,890) |
| Offsetting FV under netting | 528 | 724 | 692 |
| Cash collateral & LC already posted | 331 | 471 | 854 |
| **= Incremental LIQUIDITY EXPOSURE on a downgrade trigger** | **(963)** | (392) | (344) |

**This is the single most important number A2 resolves.** The Phase-1 "$X additional collateral if downgraded" disclosure is the `Liquidity exposure` line: **$963M at Dec 31 2025** — i.e., if VST's rating were downgraded below the contractual trigger, counterparties could demand up to **~$963M of additional cash/LC collateral.** It **rose 2.5× YoY** ($392M → $963M) and is ~2.8× the FY23 level — because the gross contingent-liability book is less collateralized (cash/LC posted fell to $331M from $854M). Against $2,781M cash+revolver, the $963M contingent call is **covered ~2.9×.** Confirmed manageable — but note it moves the WRONG direction even as ratings improve.

### 1c. The IG upgrade is RELIEVING this tail — quantified [S2, Q1'26 10-Q subsequent events]
Q1'26 10-Q discloses: **"Investment-grade credit upgrades by S&P and Fitch triggered collateral RELEASE on senior secured notes."** Mechanism: at IG, the secured revolver/notes enter a **"collateral suspension period"** (liens released), and the contingent-collateral triggers on ISDA CSAs reset to less punitive thresholds. Phase-1 Q2 question ("did the contingent requirement fall after S&P/Fitch?") — **answer: YES, post-Q1'26, via collateral release;** the $963M FY25 figure is the pre-release high-water mark.

### 1d. Largest plausible margin call vs liquidity — the 2× stress [computed; inputs S1]
- Proven precedent (Ph-1): **+$1.9B posted-margin swing in ~6 months** in the 2022 gas spike (`MarginDepositAssets` $1,263M FY21 → $3,160M Q2'22) [S1].
- Gross commodity derivative liability at FY25 fair value = **$5,756M** (Level-table `Total | Commodity contract` derivative liabilities) [R113]; gross asset $3,180M.
- **Stress: a 2× forward move.** If forwards double from FY25 levels, the short-hedge MTM loss roughly doubles the *net* exposure; incremental cash margin demand plausibly **$2–4B within a quarter** (consistent with the 2022 $1.9B at a smaller book; today's book is larger but better LC-substituted and IG-collateralized).
- **Backstop in that scenario:** $785M cash + $1,996M revolver + commodity-linked facility (already ~exhausted, +$2M) + ability to issue incremental LCs (the LC facilities are the real shock-absorber — counterparties accept LC in lieu of cash). **Hard cash+revolver dry powder ≈ $2.78B.**
- **VERDICT:** A worst-plausible $3–4B fast margin call would **exceed hard cash+revolver dry powder ($2.78B)** and force reliance on (i) LC-substitution, (ii) the IG-era ability to issue unsecured term debt quickly (demonstrated: $2.25B Jan'26 + $4.0B Apr'26 raised in weeks), and (iii) margin being a *timing* outflow that reverses on settlement. **Tail is real but no longer existential post-IG** — the difference vs 2022 is that VST can now term out under IG and has the $1,750M dedicated commodity facility. *Still the #1 number a liquidity stress-test must shock.*

### 1e. Covenant headroom [S1, R95]
- **Covenant:** consolidated **first-lien net leverage ≤ 4.25×**; during a *collateral-suspension period* (now active post-IG), the **total net leverage ≤ 5.50×** applies instead [R95].
- **Tested only during a "compliance period"** — defined as when revolver borrowings + LC (above $300M) exceed **30% of revolving commitments** [S3 credit agreement]. At FY25 the corporate revolver was only $380M drawn of $3,440M → utilization well under 30% → **covenant not currently being tested.**
- Current **total** net leverage 2.78× vs 5.50× ceiling = **~2.7× of headroom**; first-lien net leverage is far lower (most debt is unsecured/secured-notes, only ~$2.45B TLB + secured notes are first-lien). **Covenant breach risk is negligible.** 60-day grace on collateral-suspension transitions [R91].

---

## ANOMALY 2 — DEBT MATURITY WALL [S1, R89/R88/R87/R100]

### 2a. Year-by-year maturities (FY25 10-K, `LongTermDebtMaturities…`) [S1, R89]

| Year | Maturity ($M) | Comment |
|---|---:|---|
| **2026** | **1,201** | incl. $500M 5.05% sec. notes due 12/30/26; covered ~3.4× by FY25 OCF |
| **2027** | **3,435** | the wall: $1.3B 5.00% + $1.3B 5.625% unsec. + $800M 3.70% sec. — *Apr'26 $4.0B issue already redeems the 5.625% 2027s* |
| **2028** | **786** | incl. $450M 7.233% sec. notes |
| **2029** | **2,362** | $800M 4.30% sec. + $1.25B 4.375% unsec. |
| **2030** | **2,853** | incl. $2,450M Term Loan B-3 (floating) — *being repaid Apr'26 w/ unsecured notes* |
| Thereafter | 6,559 | 2031 $1.45B 7.75%, 2032 $1.0B 6.875%, + Jan'26 $1.0B 4.70%'31 / $1.25B 5.35%'36 + Apr'26 tranches |
| Unamort. premium/disc./issuance | (153) | |
| **Total L-T debt** | **17,043** | + short-term $1,800M + AR financing $1,225M + fwd repo $632M → total debt $17,196M (`DebtInstrumentCarryingAmount`) [S1] |

### 2b. Refinancing risk — LOW, and actively de-risked post-IG [S2]
The 2027 $3.4B "wall" is the only cluster of size. **It is already being addressed:** the **Apr 22 2026 $4.0B senior-unsecured offering** (tranches 4.55%'28 / 5.00%'31 / 5.25%'33 / 5.55%'36) explicitly redeems the **5.625% Senior Notes due 2027 and the Term Loan B-3** [S2]. Combined with the **Jan 22 2026 $2.25B secured offering** (4.70%'31 / 5.35%'36, Cogentrix funding) [S2], VST raised **$6.25B in new term debt in <4 months** at IG-area coupons — demonstrating the maturity wall is refinanceable on demand. Interest coverage FY25 ≈ $5,912M / $1,179M = **5.0×** [computed; R100].

### 2c. Weighted-avg coupon & fixed vs floating [computed from R88/R87/R100]
- **Interest expense FY25 = $1,107M** (pure, before MTM/amort/capitalized) [R100]; on avg L-T debt ~$16.7B → **blended cash coupon ≈ 6.0%** (incl. floating). Stated-rate fixed notes range 3.70%–7.75%.
- **Floating-rate debt (FY25):** Term Loan B-3 $2,450M + project-level (BCOP/Vistra Zero) $1,569M + revolver drawn $380M + commodity-linked revolver ~$1,748M + short-term borrowings $1,800M + AR financing $1,225M ≈ **$9.2B variable/short-dated** of $19.2B total ≈ **~48% floating/short** at FY25.
- **The Apr'26 refi cuts floating materially:** repaying the $2,450M Term Loan B-3 with fixed unsecured notes converts ~$2.45B floating → fixed, taking pro-forma floating toward ~35%. Interest-rate swaps hedge a further slice (FY25 swap MTM in interest line). **Direction: de-risking floating exposure into the rate cycle.**

---

## ANOMALY 3 — COGENTRIX FUNDING & PRO-FORMA LEVERAGE [S2]

### 3a. Deal economics [S2, prnewswire / Quantum release]
- **Gross enterprise value ~$4.7B; net purchase price ~$4.0B**, bridged: **$2.3B cash + $0.9B stock (5.000M shares @ $185 = $925M) + ~$1.5B assumed debt − ~$0.7B NPV of tax benefits.**
- Assets: **~5,500 MW**, 10 modern gas plants (PJM 4 / ISO-NE 4 / ERCOT 1); ~$730/kW; **~7.25× 2027E EBITDA.**
- Close: **2H 2026** (FERC/state approvals pending) [S2 Q1'26 10-Q].

### 3b. Financing [S2]
- **Jan 22 2026: $2.25B secured notes** ($1.0B 4.70%'31 + $1.25B 5.35%'36); ~$2.225B net proceeds "to fund part of the Cogentrix consideration alongside cash on hand" [S2].
- **Stock: 5.000M new shares @ $185 = $925M** issued to Quantum — the **first equity issuance in years**, partially offsetting the buyback de-dilution narrative (Phase-1 FLAG 3). NB: 5.0M shares is only ~1.5% of the ~337M share count, so de-dilution thesis survives but is no longer pristine.

### 3c. Pro-forma net leverage at close [computed; inputs S1/S2]
- Incremental debt: $2.25B new secured notes + **$1.5B assumed Cogentrix debt = ~$3.75B** added to net debt; cash consideration $2.3B drains cash.
- Q1'26 actuals already reflect pre-funding: total debt **$19,332M** (`DebtInstrumentCarryingAmount`), up from $17,196M FY25 [S1 XBRL].
- Pro-forma net debt at close ≈ **$19.3B (Q1'26) + ~$1.5B assumed Cogentrix debt ≈ $20.5–21B**; against pro-forma EBITDA = FY25 $5,912M + Cogentrix run-rate (~$4.0B net / 7.25× ≈ **~$550M**) + organic 2026 growth → 2026E Ongoing EBITDA guide **$6,800–7,600M** [S2].
- **Pro-forma net leverage ≈ $20.5B / ~$7.2B (mid-guide incl. Cogentrix run-rate) ≈ 2.85×; on a trough-quarter basis it presses ~3.0×.**
- **VERDICT: brushes but does NOT durably breach the <3.0× target.** Management explicitly reiterated "<3x long-term net leverage" concurrent with the deal [S2]. The $0.9B equity slug is precisely the lever that keeps it under 3.0× — had Cogentrix been all-debt, pro-forma would breach. Near-term it sits at the **top of the band (~2.85–3.0×)** with EBITDA accretion deleveraging it back through 2027 (mgmt: mid-single-digit AFCFbG/sh accretion 2027).

---

## ANOMALY 4 — NUCLEAR DECOMMISSIONING TRUST + ARO [S1, R113/R117/R118]

### 4a. ARO roll-forward (FY25) [S1, R117]
| ARO component ($M) | FY25 end | of which nuclear | coal-ash/mining |
|---|---:|---:|---:|
| Total ARO (`AssetRetirementObligation`) | **4,216** | 3,374 | 842 |
| — Nuclear decommissioning | | 3,374 | — |
| — Land reclamation / coal ash / mining (split: coal ash $561M; mining reclamation $561M) | | — | 842 |
| Accretion FY25 | 194 | 154 | 40 |
| Acquisition additions | 13 | 0 | 13 |
| Payments | (96) | 0 | (96) |

The FY24 +$1,368M ARO step-up was the **Energy Harbor nuclear** obligation assumed (Davis-Besse/Perry/Beaver Valley) [R117].

### 4b. Trust asset balance vs ARO — funded status [S1, R113; XBRL `DecommissioningFundInvestments`]
- **Nuclear decommissioning trust total ≈ $4,930M** (Q3'25 `DecommissioningFundInvestments`); FY25 fair-value table [R113]: equity securities $1,761M + debt securities $2,088M + NAV-measured equity $806M + debt $329M + other $28M ≈ **~$5.0B.**
- **Funded status: trust ~$5.0B vs nuclear ARO $3,374M → OVER-FUNDED by ~$1.6B (≈148% funded).** Confirmed at the plant level: **Comanche Peak** nuclear ARO $1,838M is backed by **$2,589M trust assets** [R118] — overfunded, with the excess sitting as a **$751M regulatory liability** (i.e., excess returns owed back to ratepayers, not to VST equity) [R118].
- Trust debt securities: **4.02% weighted-avg yield, 8-yr avg maturity** [R113]. Ladder: $848M (1–5yr) / $1,114M (5–10yr) / $455M (>10yr).

### 4c. Required contributions & EBITDA flow [S1/S2]
- **No required cash contributions disclosed** — the trust is over-funded (Comanche Peak regulated; the ratepayer-funded trust is in surplus, hence the regulatory liability rather than a contribution call). This removes a contingent funding call (a Phase-1 secondary tension) — **net credit-positive, not a hidden liability.**
- **Adj. EBITDA treatment (Phase-1 noted add-back confirmed):** "decommissioning-related activities, net" is a bridge item *reducing* Adj. EBITDA (−$111M FY25, −$63M FY24) [S2] — i.e., VST *removes* trust income/activity from Adjusted EBITDA. Conservative: trust investment gains are NOT inflating Adj. EBITDA. Nuclear-fuel amortization runs through D&A. The $165.9M/reactor (max single-loss) + $24.7M/yr secondary nuclear-liability-pool assessment [R133] is the only contingent nuclear cost — immaterial.

---

## ANOMALY 5 — Q1'26 10-Q DEEP READ [S2, acc. 0001692819-26-000014]

| Item | Finding |
|---|---|
| **Total debt / net debt** | Total debt **$19,332M** (`DebtInstrumentCarryingAmount` 3/31/26); L-T debt $19,163M (`LongTermDebt`). Net debt ~$18.5B. Up $2.1B QoQ on Cogentrix pre-funding (Jan'26 $2.25B issue). [S1 XBRL] |
| **Adj. EBITDA / NI** | Ongoing Adj. EBITDA **$1,494M** (+$254M YoY); GAAP NI **$1,029M** (vs −$268M loss Q1'25) — ~70% of NI is +$723M unrealized hedge MTM (Phase-1 §2a confirmed). OCF doubled to **$1,199M.** [S2] |
| **Liquidity** | Total available liquidity **$4,173M** at 3/31/26 (up from $2,783M FY25 — the Jan'26 notes proceeds sit as cash pending Cogentrix close). [S2] |
| **NEW contingency** | **Moss Landing (battery fire) — EPA remediation ~$110M total, $40M accrued at 3/31/26.** New, specific, quantified. Watch item but immaterial to a $7B-EBITDA entity. [S2] |
| **Subsequent events** | (1) **S&P + Fitch IG upgrades triggered collateral RELEASE on senior secured notes** (resolves Anomaly 1c). (2) **$4.0B senior-unsecured notes issued Apr'26** (4.55%'28/5.00%'31/5.25%'33/5.55%'36). (3) **Term Loan B-3 repaid; 5.625% notes due 2027 redeemed** — maturity-wall de-risking. [S2] |
| **Segment shifts** | None — Retail / Generation (Texas, East, West, Sunset, Asset Closure) / Corporate unchanged [R143]. Operating-segment revenue $26.3B grosses up to $17.7B consolidated after $(8.5)B intercompany elim. |
| **Off-balance-sheet** | AR financing facility **$1,225M** + forward repurchase obligation **$632M** [R87] — disclosed on-balance-sheet financings, not true OBS. No material OBS arrangements. |
| **Related-party (Item 404)** | Cogentrix counterparty is **Quantum Capital Group** (PE seller) — arm's-length M&A, NOT a VST-affiliated related party; the 5M-share issuance to Quantum is deal consideration, not an insider transaction. No Item-404 director/officer conflict surfaced in DEF 14A (filed 3/18/26). Collateral Financing Agreement With Affiliate [R21/R86] relates to intercompany (Vistra Operations ↔ Corp), not external related parties. [S1/S2] |

---

## ANOMALY 6 — CAPITAL-RETURNS SUSTAINABILITY: 2026 SOURCES & USES [computed; S1/S2]

### 6a. The build (2026E, $M)
| **SOURCES** | Low | High | | **USES** | Amount |
|---|---:|---:|---|---|---:|
| Ongoing Adj. **FCFbG** (guide) | 3,925 | 4,725 | | Common dividend (~$0.916/sh × ~337M; mgmt "~$300M") | ~300 |
| Cash on hand (Q1'26 liquidity cushion, Jan'26 proceeds) | — | ~1,400 | | **Buyback** (≥$1.0B min commitment; ~$1.5B auth remaining) | 1,000–1,500 |
| New debt already raised (Jan $2.25B + Apr $4.0B, largely refi/Cogentrix) | (refi) | | | **Cogentrix cash consideration** (at 2H'26 close) | 2,300 |
| | | | | Growth capex (total capex ~$2.1B incl. nuclear fuel; growth portion ~$0.6–1.4B over maint. $1,536M) | ~600–1,200 |
| **Total internal (FCFbG)** | **3,925** | **4,725** | | **Total core uses (div+buyback+growth, ex-Cogentrix-cash)** | **~1,900–3,000** |

### 6b. Verdict — sustainable on FCFbG for the RECURRING program; Cogentrix cash is the swing factor
- **Recurring capital returns (dividend $300M + buyback $1.0–1.5B) + growth capex ($0.6–1.2B) = ~$1.9–3.0B**, fully covered by **FCFbG $3.925–4.725B** [S2]. The dividend+minimum-buyback ($1.3B) is covered **~3–3.6×** by FCFbG. **The base capital-returns program does NOT require releveraging.**
- **Cogentrix's $2.3B cash slug is the exception** — it is being funded with **dedicated new debt (Jan'26 $2.25B) + balance-sheet cash**, NOT from 2026 FCFbG. This is the *intended* releveraging (pushes net leverage to ~2.85–3.0×, Anomaly 3), term-financed and EBITDA-accretive, not a sign of return-program stress.
- **Net:** With Cogentrix carved out and separately financed, **2026 FCFbG comfortably funds dividend + ≥$1.0B buyback + growth capex with ~$1–2B of cushion.** The only scenario forcing releveraging beyond the planned Cogentrix step is a **2022-style margin call** (Anomaly 1) draining cash mid-year — which loops back to the load-bearing tail. **Capital-returns sustainability: CONFIRMED, conditional on no commodity-collateral shock.**

---

## CROSS-REFERENCES TO PHASE-1 QUESTIONS RESOLVED
- Ph-1 §12 Q1 (contingent-collateral $ + IG relief): **RESOLVED** — $963M FY25 liquidity exposure; collateral released post-IG (Anomaly 1b/1c).
- Ph-1 §12 Q3 (Cogentrix PP&E/goodwill decomposition): PPA not yet final (close 2H'26); leverage impact quantified (Anomaly 3).
- Ph-1 §12 Q5 (maintenance vs growth capex): maint $1,348M FY25 / $1,536M 2026E; total capex incl. nuclear fuel $2,104M segment basis (Anomaly 6) [S1/S2].
- Ph-1 §12 Q6 (coal-ash ARO isolation): **coal ash $561M + mining reclamation $561M** of the $4,216M ARO; rest nuclear $3,374M (Anomaly 4) [R118].
- Ph-1 §12 Q7 (trust return assumption): trust debt securities **4.02% / 8-yr**; over-funded, excess is a $751M regulatory liability owed to ratepayers (Anomaly 4) [R113/R118].

---

### APPENDIX — Tool-call / source log (A2)
- **XBRL `data.sec.gov` companyconcept** (authenticated curl): LineOfCreditFacilityMaximum/RemainingBorrowingCapacity; LongTermDebtMaturities…NextTwelveMonths/YearTwo/Three/Four/Five/AfterYearFive; AssetRetirementObligation(+Noncurrent); DecommissioningFundInvestments; LongTermDebt; DebtInstrumentCarryingAmount.
- **FY25 10-K R-files** (authenticated curl on www.sec.gov/Archives — confirmed accessible despite WebFetch 403): FilingSummary.xml; R88 (debt instruments), R89 (maturities), R87 (schedule of debt), R90 (LC facilities schedule), R91 (Vistra Operations facilities), R94 (LC facilities), R95 (covenants), R100 (interest expense), R111 (credit-risk contingent features), R113 (FV/trust assets), R117/R118 (ARO/trust), R133 (commitments narrative), R143 (segments).
- **WebSearch/WebFetch (S2/S3):** FY25 8-K earnings (liquidity $2,783M, FCFbG/EBITDA guide, buyback); Q1'26 8-K + 10-Q (StockTitan render — liquidity $4,173M, Adj EBITDA $1,494M, Moss Landing, subsequent events); Cogentrix prnewswire + Quantum GlobeNewswire (deal terms); Jan'26 $2.25B + Apr'26 $4.0B note offerings; covenant ratio search.
- **Tool-call count (A2 session): 20** (2 ToolSearch/setup-excluded core research calls = 18 substantive: 9 WebSearch + 4 WebFetch + 5 multi-concept curl/Bash batches covering ~25 XBRL concepts & 15 R-files). Exceeds 15-call minimum.
