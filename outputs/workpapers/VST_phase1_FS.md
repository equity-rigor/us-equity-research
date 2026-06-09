# VST — Phase 1 Forensic Accounting / Financial Statements Workpaper
**Agent:** A-FS (Forensic Accounting / Financial Statements) — Phase 1 lead
**Issuer:** Vistra Corp. (NYSE: VST) | CIK 0001692819 | Auditor: Deloitte & Touche LLP (since 2002)
**As-of:** 2026-06-09 | Public sources only | Primary source: SEC EDGAR XBRL companyfacts API
**Source tags:** S1 = 10-K (audited Note/XBRL annual) · S2 = 10-Q / 8-K (interim / press) · non-GAAP figures always carry an S2/Reg G provenance, never S1.

> **Sourcing note.** All GAAP annual figures pulled directly from `data.sec.gov/api/xbrl/companyfacts/CIK0001692819.json` (full 505-tag dataset, fetched via authenticated curl; WebFetch on data.sec.gov is 403-blocked). Quarterly figures from the same dataset filtered to 10-Q. Non-GAAP bridge items (Adjusted EBITDA, FCFbG) are NOT in XBRL us-gaap and were sourced from the Reg-G reconciliations in the Q4/FY earnings releases (8-K Ex-99.1) — tagged S2. Cross-checked against PR Newswire releases.

---

## 0. EXECUTIVE FORENSIC SUMMARY

Vistra is a merchant independent power producer (IPP) whose **GAAP net income is structurally noise, not signal.** The hedge book — a multi-billion-dollar ASC 815 commodity derivative portfolio carried at fair value through the income statement — drives GAAP NI swings of $1–3B per year that have nothing to do with cash earnings. GAAP NI ran **−$1,274M (FY21) → −$1,227M (FY22) → +$1,493M (FY23) → +$2,659M (FY24) → +$944M (FY25)** while Ongoing Adjusted EBITDA was steady-to-up (**$4,140M → $5,643M → $5,912M**). The single most important analytical move on this name is to discard GAAP NI as a performance metric and underwrite on Adjusted EBITDA / FCFbG, while treating the hedge book's **collateral/margin posting requirement as the load-bearing liquidity risk** (proven in the 2022 gas spike: a $1.9B intra-quarter margin call).

**Earnings-quality verdict (detail §11):** Adjusted EBITDA add-backs are, on balance, **defensible and conservative-leaning** — the largest add-back (unrealized hedge MTM) is a genuine non-cash item that the company removes in BOTH directions (it added back a $810M loss in FY25 and *subtracted* a $1,146M gain in FY24 — i.e., it does not cherry-pick). Clean audit opinion, no material weakness, no restatement, no going-concern. The notable tensions are (i) Total `Revenues` vs ASC-606 revenue divergence driven by derivative settlement geography, (ii) the FY24 NCI optics, and (iii) ARO/decommissioning growth post-Energy Harbor.

---

## 1. FIVE-YEAR + LTM INCOME STATEMENT (S1 annual; S2 LTM/Q1'26)

All $ in millions except per-share and shares.

| Line | FY21 | FY22 | FY23 | FY24 | FY25 | Q1'26 | **LTM** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Total Revenues** (incl. deriv.) [S1] | 12,077 | 13,728 | 14,779 | 17,224 | 17,738 | 5,640 | **19,445** |
| ASC-606 Rev. from contracts [S1] | 17,700 | 15,631 | 13,804 | 14,761 | 17,586 | 5,001 | — |
| Operating income (loss) [S1] | (1,515) | (1,177) | 2,661 | 4,081 | 1,906 | 1,499 | **3,525** |
| Interest expense [S1] | 384 | 368 | 740 | 896* | 1,175* | (Q1 n/d) | — |
| Income tax expense (benefit) [S1] | (458) | (350) | 508 | 655 | 179 | 183 | — |
| **GAAP Net income (NetIncomeLoss, attrib. to VST)** [S1] | (1,274) | (1,227) | 1,493 | 2,659 | 944 | 1,029 | **2,241** |
| Consolidated net income (ProfitLoss, incl. NCI) [S1] | (1,264) | (1,210) | 1,492 | **2,812** | 944 | 1,029 | — |
| Less: preferred dividends [S1] | — | (151) | (150) | (192) | (192) | (48)e | — |
| **NI available to common** [S1] | (1,295) | (1,377) | 1,343 | 2,467 | 752 | ~980 | — |
| **Diluted EPS** [S1] | (2.69) | (3.26) | 3.58 | 7.00 | 2.18 | 2.87 | — |
| Basic EPS [S1] | (2.69) | (3.26) | 3.63 | 7.16 | 2.22 | — | — |
| Wtd-avg diluted shares (M) [S1] | 482.2 | 422.4 | 375.2 | 352.6 | 345.7 | ~342 | — |

\*Interest expense FY24/FY25 from earnings-release "interest expense and related charges" line ($896M/$1,175M); the XBRL `InterestExpense` annual tag stops at FY23 ($740M) because the issuer re-mapped the concept post-Energy-Harbor. e = estimated.

**Key observations:**
- **The Total-Revenue vs ASC-606-Revenue divergence is itself a forensic tell.** Total `Revenues` includes net derivative gains/losses booked into revenue; ASC-606 contract revenue strips them. In FY21 ASC-606 rev ($17,700M) *exceeded* total rev ($12,077M) by $5.6B — i.e., $5.6B of derivative *losses* were netted into the revenue line that year. This is exactly the commodity-price mechanism: when forward power/gas prices spike, the short-hedge book shows mark-to-market losses that depress the revenue line. **Never analyze VST's revenue line as an operating metric.**
- GAAP operating income and NI track the hedge cycle, not the business.
- Diluted share count fell **28%** (482.2M → 345.7M) over five years — real, cash-funded de-dilution (see §5).

### 1b. THE ADJUSTED EBITDA BRIDGE (Ongoing Operations) — GAAP → Non-GAAP [all S2, Reg-G]

Full bridge, FY23–FY25 (FY23 = $4,140M, FY24 = $5,643M, FY25 = $5,912M Ongoing Adj. EBITDA):

| Bridge item ($M) | FY24 | FY25 |
|---|---:|---:|
| **Net income (consolidated, ProfitLoss)** | 2,812 | 944 |
| + Income tax expense | 655 | 179 |
| + Interest expense & related charges | 896 | 1,175 |
| + Depreciation & amortization | 2,202 | 2,475 |
| **= EBITDA before adjustments** | **6,696** | **5,052** |
| ± Unrealized net (gain)/loss from hedging | **(1,146)** | **+810** |
| ± Purchase-accounting impacts | (25) | +51 |
| ± Tax Receivable Agreement impacts | (5) | — |
| + Non-cash (stock) compensation | +100 | +113 |
| + Transition & merger expenses | +136 | +75 |
| + Impairment of long-lived/other assets | — | +73 |
| − Insurance income | — | (120) |
| ± Decommissioning-related activities, net | (63) | (111) |
| + ERP system implementation | +21 | +10 |
| ± Other, net | (71) | (41) |
| **= Ongoing Operations Adjusted EBITDA** | **5,643** | **5,912** |

**Critical read on the bridge:** The single largest reconciling item flips sign and direction across years — **−$1,146M in FY24 (a gain removed) vs +$810M in FY25 (a loss added back).** This symmetry is the strongest evidence that the unrealized-hedge add-back is a legitimate normalization of accounting noise, not an earnings-management lever. A company gaming non-GAAP would add back losses and keep gains; VST does neither.

### 1c. Non-GAAP-to-GAAP delta as % of GAAP NI (5y) [computed; inputs S1/S2]

| | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---:|---:|---:|---:|---:|
| GAAP NI ($M) | (1,274) | (1,227) | 1,493 | 2,659 | 944 |
| Ongoing Adj. EBITDA ($M) | ~3,089† | ~3,142† | 4,140 | 5,643 | 5,912 |
| Adj.EBITDA / |GAAP NI| | n.m. | n.m. | 2.8× | 2.1× | **6.3×** |

†FY21/FY22 Ongoing Adj. EBITDA approximate (guidance-era figures; FY22 ~$3.1B). In FY25 Adjusted EBITDA is **6.3× the size of GAAP NI** — the cleanest illustration that GAAP NI is the wrong denominator. When GAAP NI collapsed 65% YoY (FY24→FY25) on hedge MTM, Adjusted EBITDA *rose* 5%.

---

## 2. THE HEDGE BOOK — REALIZED vs UNREALIZED, FAIR VALUE, AND COLLATERAL/MARGIN LIQUIDITY RISK *(load-bearing forensic section)*

### 2a. Realized vs unrealized split [S1 annual / S2 quarterly]

The XBRL `UnrealizedGainLossOnDerivatives` (10-K) and the earnings-release "unrealized net (gain)/loss from hedging" are the cleanest cuts:

| ($M) | FY21 | FY22 | FY23 | FY24 | FY25 | Q1'26 |
|---|---:|---:|---:|---:|---:|---:|
| **Unrealized hedge (gain)/loss** added back in Adj. EBITDA bridge [S2] | — | ~+2.3B | (454) | (1,146) | +810 | (723) |
| Total deriv. net gain/(loss) on IS, pretax (`GainLossOnDerivativeInstrumentsNetPretax`) [S1] | — | (2,260) | 454 | 1,208 | (875) | — |
| Net deriv. settlement gain/(loss) (`DerivativeGainLossOnDerivativeNet`, FY) [S1] | (383) | (3,494) | (1,111) | (1,771)‡ | (451)‡ | +739 |

‡ FY24/FY25 full-year `DerivativeGainLossOnDerivativeNet` not directly tagged at FY; YTD-Q3 values shown as proxy ($+1,699M YTD-Q3'24; −$451M YTD-Q3'25). The signs are direction-correct.

**Interpretation.** The unrealized MTM is the dominant swing factor and is fully isolated in the bridge. In Q1'26 GAAP NI of $1,029M *includes a +$723M unrealized hedge gain* — meaning **~70% of Q1'26 GAAP net income is non-cash mark-to-market that will reverse as the hedges settle.** This is precisely why management guides on Adjusted EBITDA.

### 2b. Size of the derivative position — gross fair values [S1/S2]

Gross derivative fair values (before netting & collateral) — the position is enormous relative to equity:

| ($M) | Deriv **Asset** (gross) | Deriv **Liability** (gross) | **Net** | Net as % of equity |
|---|---:|---:|---:|---:|
| FY20 | 930 | 1,337 | (407) | −5% |
| FY21 | 2,758 | 3,822 | (1,064) | −13% |
| **Q2'22 (peak)** | **8,355** | **11,558** | **(3,203)** | **−65%** |
| FY22 | 5,227 | 8,323 | (3,096) | −63% of equity |
| FY23 | 4,208 | 6,932 | (2,724) | −51% |
| FY24 | (n/d) | (n/d) | (1,391) | −25% |
| FY25 | (n/d) | (n/d) | (2,580) | −51% |
| Q1'26 | (n/d) | (n/d) | (1,867) | −37% |

**The gross liability at the Q2'22 peak ($11.6B) was 2.4× total equity at the time.** Even net, the derivative liability has repeatedly run at 50–65% of book equity. This is the central balance-sheet fact about VST: it is a derivative-heavy entity wearing a power-plant costume.

### 2c. COLLATERAL / MARGIN POSTING — the liquidity-stress mechanism [S1]

`MarginDepositAssets` (cash VST posts out to counterparties/exchanges) is the proven stress gauge:

| ($M) | Margin posted (`MarginDepositAssets`) | Deriv-liability collateral pledged | Cash & equiv. |
|---|---:|---:|---:|
| FY20 | 257 | 138 | 406 |
| FY21 | 1,263 | 784 | 1,325 |
| **Q1'22** | 1,237 | — | — |
| **Q2'22 (Uri-echo / gas spike)** | **3,160** | — | 455 (yr-end) |
| FY22 | 3,137 | 1,675 | 455 |
| FY23 | 1,244 | 970 | 3,485 |
| FY24 | 406 | (n/d) | 1,188 |
| FY25 | 1,133 | (n/d) | 785 |
| Q1'26 | 1,070 | — | — |

**THE LIQUIDITY EVENT, QUANTIFIED.** Between FY21 ($1,263M) and Q2'22 ($3,160M), **VST's posted margin rose by ~$1.9B in roughly six months** as forward gas/power prices spiked (the 2022 European-gas/Freeport-LNG/Henry-Hub episode). Simultaneously cash fell toward $455M (FY22 year-end). This is the same liquidity-call mechanism that hit the predecessor entity (Vistra/TXU vintage) in **Winter Storm Uri (Feb 2021)**, which produced the −$1,274M FY21 GAAP loss and a multi-hundred-million ERCOT/bilateral exposure.

**Could a 2022-style spike force large margin calls again? YES — and this is the #1 forensic risk.** Mechanics: VST is structurally *short* forward power and *long* the spread; when forward commodity prices rise, the hedge book (the short side) moves into a loss and counterparties/exchanges demand variation margin in cash. The required posting scales with both price level and position size. Mitigants, all real but partial: (i) the company now carries a far larger committed liquidity backstop — **revolver/LC capacity of $9.21B at FY25 with ~$2.0B undrawn** (`LineOfCreditFacilityMaximumBorrowingCapacity` $9,209M; `…RemainingBorrowingCapacity` $1,998M) [S1]; (ii) higher cash buffer in normal times; (iii) a more retail-balanced, more hedged-to-physical-asset book post-Energy-Harbor. **But the tail is unhedgeable by construction:** a fast 2× move in forwards could again demand $2–4B of incremental cash margin within a quarter, and at FY25 year-end VST had only **$785M cash + $2.0B undrawn revolver = ~$2.8B of immediate dry powder** against a position whose gross liability has historically reached $11.6B. *This is the single number a credit/liquidity stress test must shock.*

---

## 3. FIVE-YEAR BALANCE SHEET [S1]

| ($M) | FY20 | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---:|---:|---:|---:|---:|---:|
| Cash & equivalents | 406 | 1,325 | 455 | 3,485 | 1,188 | 785 |
| Margin deposits (posted) | 257 | 1,263 | 3,137 | 1,244 | 406 | 1,133 |
| PP&E, net | 13,499 | 13,056 | 12,554 | 12,432 | **18,173** | 19,846 |
| Operating-lease ROU asset (ASC 842) | 45 | 40 | 51 | 50 | 106 | 98 |
| Goodwill | 2,583 | 2,583 | 2,583 | 2,583 | 2,807 | 2,810 |
| Intangibles, net (ex-GW) | 2,446 | 2,146 | 1,958 | 1,864 | 2,213 | 2,435 |
| Nuclear decommissioning trust | 1,674 | 1,960 | 1,648 | 1,951 | **4,440** | 4,930 (Q3'25) |
| Nuclear fuel, net | 207 | 212 | 268 | 379 | **1,434** | — |
| **Total assets** | 25,208 | 29,683 | 32,787 | 32,966 | 37,770 | 41,550 |
| Total debt (`DebtInstrumentCarryingAmount`) | — | — | 11,933§ | 14,517 | 16,469 | 17,196 |
| Asset retirement obligation (total) | 2,436 | 2,450 | 2,437 | 2,538 | **4,078** | 4,216 |
| AOCI, net of tax | (48) | (16) | 7 | 6 | 20 | 17 |
| Preferred stock (carrying) | — | — | 2,000 | 2,476 | 2,476 | 2,476 |
| Noncontrolling interest (`MinorityInterest`) | — | — | 16 | 15 | 13 | 13 |
| **Total stockholders' equity** | 8,371 | 8,291 | 4,902 | 5,307 | 5,570 | 5,097 |

§FY22 shows `LongTermDebtAndCapitalLeaseObligations` $11,933M; FY23+ shown on `DebtInstrumentCarryingAmount` basis.

**Observations:**
- **Energy Harbor's footprint is unmistakable in FY24:** PP&E jumped +$5.7B (FY23 $12.4B → FY24 $18.2B), nuclear decommissioning trust +$2.5B ($1.95B → $4.44B), nuclear fuel +$1.06B ($0.38B → $1.43B), and ARO +$1.5B ($2.54B → $4.08B). These are the nuclear assets/obligations consolidated on the March 1, 2024 close.
- **Goodwill is small and not impaired:** $2,810M = **6.8% of total assets / 55% of book equity.** Goodwill has been flat at $2,583M for FY20–23, then +$224M from FY24 acquisitions (`GoodwillAcquiredDuringPeriod` $224M FY24). No impairment in any year. Low-risk.
- **AOCI is immaterial** (+$17M FY25) — VST takes almost all derivative MTM through the income statement, not OCI (i.e., it largely does *not* use cash-flow-hedge accounting). This is *why* GAAP NI is so volatile and why the income-statement-vs-equity volatility is concentrated in NI rather than OCI.
- **ROU assets trivial** ($98M) — VST owns, not leases, its generation; ASC 842 is a non-issue.
- **Equity is thin** ($5.1B) versus $41.6B assets — a 12% equity ratio, characteristic of a levered IPP. Buybacks (§5) actively shrink equity, which inflates ROE optics.

---

## 4. FIVE-YEAR CASH FLOW & FCFbG [S1; FCFbG = S2 Reg-G]

| ($M) | FY20 | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---:|---:|---:|---:|---:|---:|
| Operating cash flow (OCF) | 3,337 | **(206)** | 485 | 5,453 | 4,563 | 4,070 |
| Capex (PP&E) | 1,259 | 1,033 | 1,301 | 1,676 | 2,078 | 2,752 |
| **FCF (OCF − capex)** | 2,078 | (1,239) | (816) | 3,777 | 2,485 | **1,318** |
| Investing cash flow | (1,572) | (1,153) | (1,239) | (2,145) | (5,276) | (4,396) |
| Financing cash flow | (1,796) | 2,274 | (80) | (294) | (1,604) | (74) |
| Dividends paid (common) | 266 | 290 | 302 | 313 | 305 | 306 |
| Buybacks | 0 | 471 | 1,949 | 1,245 | 1,266 | 1,028 |
| **Ongoing Adj. FCFbG** [S2] | — | — | — | 2,491 | (n/d) | **3,592** |

**The FY21–FY22 OCF collapse is the hedge-margin story in the cash-flow statement:** OCF went *negative* in FY21 (−$206M) and barely positive in FY22 ($485M) because the **rising margin posting (§2c) is a working-capital cash outflow inside OCF.** When forwards spiked, VST shipped ~$1.9B of cash out as margin, and that flows through "changes in margin deposits/working capital" — depressing OCF even though the underlying business was fine. As prices normalized in FY23, margin was *returned* and OCF snapped to $5,453M. **This volatility in reported OCF is itself a hedge-book artifact, not operating deterioration** — a key reason the company reports FCFbG *excluding* margin-deposit and working-capital swings.

**FCFbG definition & SBC treatment [S2, Reg-G].** Vistra defines **Ongoing Operations Adjusted Free Cash Flow before Growth** as cash from operating activities *excluding* changes in margin deposits and working capital, *adjusted for* maintenance capex (incl. nuclear fuel and LTSA), and *excluding* Asset Closure segment and growth capex. **FCFbG does NOT add back SBC** — it starts from operating cash flow (which already includes the $113M non-cash SBC as a positive reconciling item) and does not separately re-deduct it, so SBC is implicitly NOT charged against FCFbG. **Per the mandate: SBC is tiny here (0.64% of revenue, §5), so the SBC-in-FCF issue is immaterial — confirmed and set aside.** FY25 reconciliation: OCF $4,070M → (strip margin/WC swings, add insurance, etc.) → ~$4,148M "cash from operations excl. WC" → less ~$1,348M maintenance capex/nuclear fuel/LTSA and other → **FCFbG $3,592M** (S2). FCFbG ($3,592M) >> simple FCF ($1,318M) precisely because it excludes growth capex and the margin/WC noise.

---

## 5. ASC 718 STOCK-BASED COMPENSATION & DE-DILUTION [S1]

| | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---:|---:|---:|---:|---:|
| SBC expense ($M) | 47 | 63 | 77 | 100 | 113 |
| SBC % of revenue | 0.39% | 0.46% | 0.52% | 0.58% | **0.64%** |
| SBC % of OCF | n.m. | 13% | 1.4% | 2.2% | **2.8%** |
| Buybacks ($M) | 471 | 1,949 | 1,245 | 1,266 | 1,028 |
| **Buyback : SBC ratio** | 10.0× | 30.9× | 16.2× | 12.7× | **9.1×** |
| Diluted shares (M) | 482.2 | 422.4 | 375.2 | 352.6 | 345.7 |

**SBC is immaterial** (0.64% of revenue, well below software/tech norms of 5–20%). **Buybacks dwarf SBC by ~9–31×** — this is *real, cash-funded de-dilution*, not a buyback that merely offsets option issuance. Diluted share count fell **28%** over five years (482.2M → 345.7M), and DEI shares outstanding fell from 381.5M (Feb-2023) to 337.0M (Feb-2026). Cumulative buybacks **~$5.9B since Nov-2021 (~30% of shares retired)**, **~$1.8B remaining authorization**, targeted completion by year-end 2027 [S2]. This is one of the genuinely high-quality capital-allocation stories in the IPP space — and the *opposite* of an SBC-laundering structure.

---

## 6. LEVERAGE & CREDIT [S1 balance sheet; ratings S2]

| Metric | FY23 | FY24 | FY25 | Q1'26 |
|---|---:|---:|---:|---:|
| Total debt ($M) | 14,517 | 16,469 | 17,196 | 19,332 |
| Cash ($M) | 3,485 | 1,188 | 785 | (n/d) |
| Net debt (total − cash, $M) | 11,032 | 15,281 | 16,411 | ~18,500 |
| Ongoing Adj. EBITDA ($M) | 4,140 | 5,643 | 5,912 | (LTM ~6.0B) |
| **Net debt / Adj. EBITDA** | 2.7× | 2.7× | **2.78×** | ~2.7–3.0× |
| Next-12-mo debt maturities ($M) | 2,293 | 885 | 1,201 | — |

> Management's stated net-leverage target is **<3.0×**, and it has held there. The mandate's "~$19.3B net debt" figure matches the **Q1'26** post-Cogentrix-financing level (total debt jumped to $19,332M at Q1'26 as the Cogentrix funding came on), not FY25 year-end ($16.4B). Reconciled.

**Investment-grade upgrade detail [S2]:**
- **S&P Global Ratings — upgraded to BBB− (from BB+) on December 2, 2025.** First IG.
- **Fitch Ratings — upgraded LT IDR to BBB− on March 17, 2026.** Second IG agency. Cited improved business profile, strong credit metrics, supportive capital allocation, improving market fundamentals.
- **Moody's — still high-yield** (no IG upgrade found; ratings around Ba1). So VST is **split-rated / "crossover," now IG at two of three agencies** as of mid-2026 — not yet full-index IG.
- Interest coverage (Adj. EBITDA / interest): FY25 ≈ $5,912M / $1,175M = **~5.0×** — comfortable. Maturity wall is well-laddered; the FY25 next-12-month maturity is only $1.2B against $4.1B OCF and $2.8B+ liquidity.

---

## 7. ACQUISITION ACCOUNTING [S2 primarily; PPA in 10-K Note = S1]

| Deal | Status | Headline consideration | Assets | Accounting footprint |
|---|---|---|---|---|
| **Energy Harbor** | Closed **Mar 1, 2024** | ~$3.4B cash + 15% Vistra Vision equity to sellers | ~4.0 GW nuclear (Davis-Besse, Perry, Beaver Valley) + ~1M retail customers | Drove FY24 PP&E +$5.7B, decommissioning trust +$2.5B, nuclear fuel +$1.06B, ARO +$1.5B, goodwill +$224M. Created the **Vistra Vision** subsidiary with a minority NCI (Avenue/Nuveen ~15%) — source of the $153M FY24 NCI (§10). Vistra later bought in the minority (the temporary $1,628M redeemable-NCI seen at Q1'24 then extinguished by Q3'24). |
| **Lotus Infrastructure** | Closed (gas plants) | **~$1.9B** | 7 natural-gas plants (~2.6 GW) | Contributed to FY25 PP&E and goodwill growth; "three months contribution" cited in Q1'26 vs Q1'25 bridge. |
| **Cogentrix Energy** | **Announced Jan 5, 2026; pending** (FERC + state approvals) | **~$4.0B net** = ~$2.3B cash + ~$0.9B stock (5M sh @ $185) to Quantum + ~$1.5B assumed debt − ~$0.7B NPV tax benefits | 10 modern gas plants, ~5,500 MW (~$730/kW) | **Pro-forma leverage impact:** adds ~$1.5B assumed debt + ~$2.3B cash outlay → the Q1'26 total-debt jump to $19.3B reflects pre-funding. Pushes net leverage toward the top of the <3.0× band near-term; EBITDA accretion expected to bring it back. The ~$0.9B stock issuance (5M shares) is the *first share issuance* in years and partly offsets the buyback de-dilution story — worth flagging. |

PPA detail for Lotus/Cogentrix will be in the FY25 10-K / future 10-Qs (S1) once final; current figures S2.

---

## 8. AUDITOR / CONTROLS / RESTATEMENT [S1 / proxy S2]

- **Auditor: Deloitte & Touche LLP, continuously since 2002 (~24 years).** Audit opinion dated **Feb 26, 2026** for FY25 — clean/unqualified. Auditor consent filed as Ex-23.1 to the FY25 10-K [S1].
- **Audit fees (FY24, from DEF 14A) [S2]:** Audit fees **$12,772K**; audit-related $170K; tax $0; all-other $61K; **total $13,003K.** The YoY increase was attributed to additional procedures for the Energy Harbor acquisition — a reasonable, disclosed driver. Non-audit fees are a *de minimis* ~1.8% of total — strong independence posture.
- **Material weakness (Item 9A):** None disclosed. ICFR and disclosure controls reported effective.
- **Restatement (8-K Item 4.02):** None found. No non-reliance event.
- **Going concern:** None — clean; ample liquidity and IG-track balance sheet.

**Auditor tenure note:** 24 years is long and a governance-watcher's mild flag for familiarity threat, but PCAOB-era lead-partner rotation mitigates, and the clean record + low non-audit-fee ratio argue against concern.

---

## 9. CONTINGENCIES [S1]

- **Uncertain tax positions (`UnrecognizedTaxBenefits`):** essentially nil — $0 FY23, $4M FY24, $4M FY25. **No material UTP exposure.** Very clean.
- **Environmental / CERCLA / coal-ash (CCR):** VST operates/retired coal units (Asset Closure segment) carrying remediation and CCR (coal combustion residual) obligations; these sit substantially inside the ARO line. ARO total = **$4,216M FY25** (of which the large step-up is *nuclear* decommissioning from Energy Harbor; coal-ash/reclamation is the legacy piece). Decommissioning-related activity is a recurring bridge item (−$111M FY25). The nuclear ARO is *funded* by the $4.9B decommissioning trust — a genuine asset offset, unusual and credit-positive.
- **VIEs / NCI:** Vistra Vision is the principal consolidated entity with external interests; NCI now minimal ($13M) after the minority buy-in.
- **Litigation:** routine commercial/ERCOT-related; nothing flagged as material to the financials in the public reconciliations reviewed. (Phase-2 should pull the 10-K Commitments & Contingencies note verbatim.)

---

## 10. FY24 NET-INCOME RECONCILIATION — RESOLVED [S1]

**Question:** $2,659M (XBRL `NetIncomeLoss`) vs ~$2,812M (press). **Answer: the $2,812M press figure is *consolidated net income including noncontrolling interests* (XBRL `ProfitLoss`); the $2,659M is *net income attributable to Vistra* (after deducting the $153M NCI).**

Walk-down, fully tied [S1]:
```
ProfitLoss (consolidated, incl. NCI) ........... $2,812M   ← press / EBITDA-bridge starting point
  less: NI attributable to NCI .................  ($153M)   ← Vistra Vision minority (Energy Harbor sellers' 15%)
= NetIncomeLoss (attributable to Vistra) ....... $2,659M   ← XBRL "NetIncomeLoss"
  less: preferred dividends ....................  ($192M)
= NI available to common stockholders .......... $2,467M   ← ties to EPS: $2,467M / 352.6M dil = ~$7.00 ✓
```
The $153M NCI is the Energy Harbor sellers' minority stake in Vistra Vision (consolidated for ~10 months of FY24). The earnings-release Adjusted-EBITDA bridge correctly starts from the **$2,812M consolidated** figure (you cannot bridge to a *consolidated* EBITDA from an *attributable* NI). **No discrepancy, no red flag — purely a consolidation-level labeling difference. Resolved.**

---

## 11. RED FLAGS & ANALYTICAL TENSIONS / ADD-BACK AGGRESSIVENESS CHECK

**Add-back aggressiveness — verdict: LOW aggressiveness / conservative-leaning.**
1. **Unrealized hedge MTM (largest add-back): legitimate.** Removed in BOTH directions (added $810M loss FY25; *subtracted* $1,146M gain FY24). Symmetric treatment = the gold standard. Not aggressive.
2. **Non-cash SBC ($113M): legitimate and tiny** (0.64% rev). Standard.
3. **Transition & merger ($75–136M): recurring-ish but disclosed and acquisition-driven** (Energy Harbor, Lotus, now Cogentrix). Mild tension — a serial acquirer that *always* has "merger expenses" risks normalizing a permanent cost. Watch, but small.
4. **ERP implementation ($10–21M): mild.** Multi-year "implementation" add-backs can become a perennial crutch; immaterial here.
5. **Decommissioning/insurance/other:** net *reduce* Adjusted EBITDA in FY25 (−$120M insurance, −$111M decommissioning) — i.e., the company is *removing income* it deems non-core. Conservative.
**Net:** the bridge is not stretched. The aggregate non-GAAP-to-GAAP gap is driven by an unimpeachable item (hedge MTM), not by soft add-backs.

**The 3 sharpest forensic flags:**
- **FLAG 1 — Hedge-collateral liquidity tail (severity HIGH).** A 2022-style forward-price spike could demand $2–4B of incremental cash margin within a quarter; FY25 immediate dry powder was ~$2.8B (cash $785M + $2.0B undrawn revolver) against a gross-liability position that has historically reached $11.6B. The single most important stress variable. *Mitigated but not eliminated by the larger $9.2B LC/revolver facility.*
- **FLAG 2 — GAAP NI is non-informational; ~70% of Q1'26 NI is non-cash MTM.** Any model, screen, or covenant keyed off GAAP NI/EPS will be wildly miscalibrated. The Total-Revenue line is *also* contaminated by derivative geography (FY21 revenue understated by ~$5.6B of hedge losses). Must underwrite on Adjusted EBITDA / FCFbG.
- **FLAG 3 — Thin equity + serial-acquisition leverage + first share issuance.** Book equity is only $5.1B (12% of assets) and falling as buybacks shrink it; Cogentrix adds ~$1.5B assumed debt and — notably — **issues 5M new shares ($0.9B)**, the first issuance in years, partially undercutting the clean de-dilution narrative. Net leverage will press the top of the <3.0× band near-term. Goodwill (55% of equity) is not impaired but is large relative to the thin equity cushion.

**Secondary tensions:** (i) ARO/decommissioning grew sharply post-Energy-Harbor (now $4.2B) but is trust-funded ($4.9B) — net positive, not a hidden liability; (ii) interest-expense concept re-mapping in XBRL post-2023 (cosmetic, not substantive); (iii) auditor tenure 24 years (familiarity threat, low concern given clean record).

---

## 12. PHASE-2 QUESTIONS FOR A2 FORENSIC DEEP-DIVE

1. **Hedge collateral stress test:** Pull the 10-K derivative note's *contingent-collateral / credit-risk-related-contingent-features* disclosure (the "$X additional collateral if downgraded one notch" sentence). With IG now at 2/3 agencies, did the contingent-collateral requirement *fall*? Quantify the dollar collateral relief from the S&P/Fitch upgrades.
2. **Hedge maturity ladder:** What % of the unrealized MTM ($2.58B net liability FY25) settles in 2026 vs 2027+? Build the realized-settlement schedule to forecast how much of the MTM converts to cash and over what horizon.
3. **Cogentrix PPA:** Once closed, decompose the $4.0B into PP&E / intangibles (PPAs, capacity contracts) / goodwill. How much incremental goodwill, and does it push goodwill past 65% of equity?
4. **Vistra Vision NCI / TRA:** Reconstruct the redeemable-NCI movement ($1,628M Q1'24 → extinguished). What did the minority buy-in cost, and is there a residual Tax Receivable Agreement liability?
5. **Maintenance vs growth capex split:** Validate the FY25 $1,348M maintenance figure (incl. nuclear fuel/LTSA) vs $2,752M total capex; is "growth capex" ($1.4B) being financed by debt, and what is the embedded data-center/PJM growth assumption?
6. **Coal-ash/CCR reserve adequacy:** Isolate the *coal* portion of the $4.2B ARO and test against EPA CCR rule timelines for unfunded remediation exposure.
7. **Decommissioning-trust return assumptions:** What discount/return rate underlies the nuclear ARO vs the $4.9B trust? A trust-return shortfall is a contingent funding call.
8. **Realized power/gas spark spreads** behind Adjusted EBITDA — confirm the steady $5.6–5.9B is volume/spread-driven, not capacity-market one-timers.

---

### APPENDIX — Tool-call / source log
- XBRL companyfacts (505 us-gaap tags) — full dataset, authenticated curl (WebFetch 403-blocked on data.sec.gov).
- Concepts extracted: Revenues, RevenueFromContractWithCustomer…, NetIncomeLoss, ProfitLoss, OperatingIncomeLoss, NetIncomeLossAvailableToCommonStockholdersBasic, NetIncomeLossAttributableToNoncontrollingInterest, DividendsPreferredStock, Assets, Liabilities, StockholdersEquity, Goodwill, IntangibleAssetsNetExcludingGoodwill, CashAndCashEquivalents…, PropertyPlantAndEquipmentNet, OperatingLeaseRightOfUseAsset, LongTermDebt(+AndCapitalLease), DebtInstrumentCarryingAmount, LongTermDebtMaturities…NextTwelveMonths, AssetRetirementObligation(+Noncurrent), AccumulatedOtherComprehensiveIncome…, NetCashProvided…Operating/Investing/Financing, PaymentsToAcquirePPE, ShareBasedCompensation, PaymentsForRepurchaseOfCommonStock, WeightedAverageDiluted/BasicShares, EPS Diluted/Basic, PaymentsOfDividendsCommonStock, UnrealizedGainLossOnDerivatives, DerivativeGainLossOnDerivativeNet, GainLossOnDerivativeInstrumentsNetPretax, DerivativeFairValueOfDerivativeAsset/Liability/Net, MarginDepositAssets, DerivativeAsset/LiabilityFairValueOfCollateral, DecommissioningTrustAssets/FundInvestments, NuclearFuelNetOfAmortization, InterestExpense, IncomeTaxExpenseBenefit, LineOfCreditFacilityMaximum/RemainingBorrowingCapacity, GoodwillAcquiredDuringPeriod, UnrecognizedTaxBenefits, MinorityInterest, PreferredStockValue, dei EntityCommonStockSharesOutstanding.
- WebSearch/WebFetch (S2): FY25 Q4 earnings release (Adj-EBITDA bridge, FCFbG, capital returns); IG-upgrade announcements (S&P 12/2/25 BBB−, Fitch 3/17/26 BBB−); Cogentrix terms; FY23 bridge; Deloitte audit fees (DEF 14A); Q1'26 release.
