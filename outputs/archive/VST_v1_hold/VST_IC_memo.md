# Vistra Corp. (NYSE: VST) — IC Memo

**Rating: HOLD** (source-conditional) · **12-mo PT $153.44** (range $73.80–$236.80) · **Expected return +2.6%** (prob-weighted)
**As of:** 2026-06-09 · **Price:** $146.90 (S4: 2026-06-08 close) · **Sector:** Utilities › Independent Power Producers
**Mandate sizing:** benchmark-weight long-only; **small long-VST / short-CEG market-neutral pair** is the cleaner expression.

> **Headline (source-conditional Hold, modestly positive bias):** VST at $146.90 carries a probability-weighted 12-month expected return of **+2.6%** to a base-case PT of **$153.44** (FY27E EPS $10.96 [S4: consensus, n=17] × P/E 14.0x [S4: VST fwd P/E ~13.8x; 5y range]); scenario-weighted range **[−49.8%, +61.2%]**. This is a **de-rate, not deterioration** — FY26 EPS estimates were revised **up ~+4% over 3 months** with 2026 guidance ($6.8–7.6B Adj EBITDA) reaffirmed, while the multiple compressed ~34% off the 2024 high on macro/rate and power-curve resets. **CONDITIONAL on** (i) PJM capacity revenue holding near the FERC cap through 2029/30 (S1: PJM 2027/28 BRA cleared $333.44/MW-day UCAP) **and** (ii) the ~35% open 2028 generation book not repricing below EIA STEO base (S1: hedge ratios 98/89/65% for 2026/27/28). **If** PJM 2028/29 BRA clears <$250/MW-day **or** 2027 Adj EBITDA guide <$7.0B **or** net leverage >3.2× post-Cogentrix, the bear branch dominates; **if** Comanche Unit 2 or a gas co-location PPA signs >$100/MWh 15yr+ **or** the BRA clears >$300, upgrade toward Buy.

---

## 1. Thesis in brief
VST is the **value/integrated leg of the AI-power cohort** — the cheapest large merchant IPP on EV/EBITDA (~9.4x 2026E) and EV/kW (~$1,360), with the highest FCF yield (~7.2%), uniquely hedged by a ~5M-customer competitive retail book. It has converted ~9% of fleet MW into **20-year investment-grade hyperscaler annuities** (AWS 1,200 MW at Comanche Peak; Meta 2,609 MW across PJM nuclear) (S2: VST 8-Ks 2025-09-29 / 2026-01-09), reached **crossover investment grade** (S&P + Fitch BBB−), and sits in a capacity market clearing at the **FERC cap**. Yet at ~$147 the probability-weighted return is only **+2.6%**: the bear anchors to VST's own private-market gas multiple (~7.25x for Cogentrix vs ~9.4x public) and a **~35%-open 2028 book** that EIA modeling suggests has thin PJM upside; the bull anchors to un-signed PPA optionality and capacity durability. The risk is genuinely two-sided → **Hold**. The actionable edge is **relative value (long VST / short CEG)**, not direction — and even that spread has largely converged.

## 2. The five-scenario framework (FY27E EPS × P/E)
| Scenario | Prob | FY27E EPS | P/E | PT | Return |
|---|---:|---:|---:|---:|---:|
| strong_bear | 10% | $8.20 | 9.0x | $73.80 | −49.8% |
| bear | 22% | $9.60 | 11.0x | $105.60 | −28.1% |
| **base** | **38%** | **$10.96** | **14.0x** | **$153.44** | **+4.5%** |
| bull | 22% | $11.80 | 16.5x | $194.70 | +32.5% |
| strong_bull | 8% | $12.80 | 18.5x | $236.80 | +61.2% |

**Weighted expected return +2.6%; P10/P90 [−49.8%, +61.2%].** Near-symmetric, fat-tailed both sides. The bear multiples (9–11x) reflect the private-market / no-growth-merchant analog; the bull (16.5–18.5x) a re-rating toward CEG. (Full EPS bridges in `outputs/VST_scenarios.json`; G1/G4/G5 verified.)

## 3. Three-method valuation reconcile
- **EV/EBITDA comps (primary, D8 IPP): ~$153.** 8.75x 2027E EBITDA $8.1B (incl Cogentrix) → EV $70.9B − net debt $19.3B = $51.6B / 324M sh. Multiple between the private-market gas floor (~7.25x) and the CEG ceiling (~11.4x). (S4: peer comps)
- **DCF: ~$107** (range $95–121). 10y FCFbG, WACC 9.61% (β 1.41; CoE 11.24%; after-tax Kd 4.74%), g 2.25%. Below spot — disciplines the merchant-cyclical tail; the market price embeds PPA-conversion optionality a contracted DCF cannot underwrite. (S1: FRED DGS10 4.536%; S5: Damodaran ERP 4.23%)
- **SOTP: ~$132.** East (PJM nuclear+capacity+Meta) 9.5x, Texas (Comanche+AWS) 8.5x, Retail 7.0x, West 6.0x. Monotonicity NI≤OP≤GP≤Rev holds (G3).
- **Bear floor (not weighted): $53–74.** Normalized 2028 EBITDA ~$5.5B × 7.5x private-market multiple. Anchors strong_bear $73.80.

Methods cluster $107–153; the EV/EBITDA primary and the EPS×P/E base agree at **~$153**.

## 4. Financials & earnings quality (S1: XBRL companyfacts, CIK 0001692819)
| $M unless noted | FY23A | FY24A | FY25A | Q1'26A | 2026 guide |
|---|---:|---:|---:|---:|---:|
| Revenue | 14,779 | 17,224 | 17,738 | 5,640 | — |
| GAAP net income | 1,493 | 2,659¹ | 944 | 1,029² | — |
| Ongoing Adj EBITDA | ~5,004 | 5,643 | 5,912 | 1,494 | 6,800–7,600 |
| Adj FCFbG | — | — | ~3,590 | — | 3,925–4,725 |
| SBC | 77 | 100 | 113 | — | — |
| Diluted shares (M) | 375.2 | 352.6 | 345.7 | ~337 | — |

¹ Reconciled: $2,812M consolidated incl NCI vs $2,659M attributable to Vistra; $153M = Energy Harbor NCI; less $192M preferred = $2,467M to common ≈ $7.00 EPS. ² Incl +$723M non-cash unrealized hedge gain.

**Earnings quality is high on the dimensions that usually fail**: SBC ~0.6% of revenue (S1: XBRL companyfacts); Deloitte 24-year clean opinion (since 2002, ratified 4/29/26, S2); no restatement, no going-concern. **But GAAP net income is non-informational** — dominated by ASC 815 unrealized hedge mark-to-market (FY25 −$808M unrealized loss; Q1'26 +$723M gain). Adj EBITDA was **6.3× GAAP NI** in FY25. **Underwrite on Adj EBITDA / FCFbG (G11 non-GAAP reconciliation present; G12 FCF = OCF − capex, SBC immaterial).** Add-back discipline is **conservative** — the hedge MTM is removed in both directions (symmetric, the gold standard).

## 5. The load-bearing risks
1. **Hedge-collateral liquidity tail.** Gross derivative liability peaked $11.6B (2.4× equity, Q2'22); a ~$1.9B cash margin call hit in 6 months during the 2022 gas spike. FY25 contingent collateral exposure $963M (rose 2.5× YoY). A 2× forward move could demand **$3–4B vs ~$2.8B immediate dry powder**; the dedicated $1,750M commodity-margin revolver was ~exhausted at FY25. *Mitigant:* IG upgrades triggered collateral release; $9.2B LC/revolver; covenant tested only when revolver >30% utilized (2.78× vs 4.25× first-lien).
2. **2028 open-book power-price (the consensus variance).** ~35% of 2028 generation is open (S1: hedge ratios 98/89/65%). EIA shows PJM power upside ~+4% even in a high-demand scenario; ERCOT upside is high-demand-only. A 15–20% open-book reprice + capacity reverting toward the $179.55 floor cuts 2028 EBITDA ~$0.6–0.9B (modal) to $1.4–2.3B (tail).
3. **45U PTC anti-double-count.** ~$545M (~9% of EBITDA) self-erases above ~$43.75/MWh gross receipts (ERCOT base already $47.39) and sunsets end-2031/2032 (OBBBA). The bull cannot hold both peak power AND full PTC.
4. **Crowded-long unwind / Meta-AWS concentration.** Well-owned long mid-unwind (SI ~4% float rising, but DTC ~2.3, cheap borrow → no squeeze); PPA book ~69% Meta / ~31% AWS.

## 6. Consensus variance (the edge, honestly stated)
**One defensible, S1/gov-evidenced load-bearing variance: a DOWNWARD scenario-weight edge on the 2028 open book** (~60% conviction, ~−$0.6 to −$0.9B vs a peak-extrapolated 2028, sizing ~10pp into bear tails). Street's 2027–2028 EBITDA implicitly marks the open book at/above EIA STEO base and extrapolates cap-level capacity; EIA's own modeling caps PJM upside at ~+4% and ERCOT's spike is high-demand-only, with no published 2028 price. **This justifies sizing BELOW consensus and refusing the "annuity" framing — but it is two-tailed (ERCOT data-center load is genuine upside), so it supports Hold, not Sell.** Otherwise the memo is **consensus-anchored**: every Apr–May'26 PT cut was a multiple cut with Buy/OW maintained — estimates are intact-to-rising.

## 7. Regulatory desk (S1: FERC/PJM/EIA)
- **FERC co-location: LOW and declining threat for VST.** The Dec-18-2025 order (193 FERC ¶61,217, Docket EL25-49) **blesses front-of-meter contract-demand co-location** and restricts pure behind-the-meter. **VST's Meta deal is FTM; AWS sits in ERCOT** (outside FERC RTO jurisdiction) — VST avoided Talen's rejected BTM structure. *Tail:* a rehearing/D.C. Circuit reversal (−15% to −30% EBITDA severe branch, low prob).
- **EPA:** deregulatory pivot (Endangerment Finding rescinded Feb 2026) removes the coal-retirement stick; ~4.6 GW coal (S1: VST FY25 10-K Item 2) retires 2027–28 on economics.
- **PJM/ERCOT:** capacity cap/collar binds near cap through 2029/30 (27/28 cleared 6,623 MW (S1: PJM 2027/28 BRA report) short of reliability → uncapped equilibrium above cap); ERCOT SB6 large-load rules curb bypass.
- **Export-control/sanctions: N/A** (US-domiciled domestic utility — BIS/OFAC/CFIUS not applicable; verified 2026-06-09).

## 8. Positioning & sentiment
Well-owned → **crowded-long mid-unwind**, unwind risk > squeeze. ~1,388 institutions (~86% of SO); Lone Pine the notable active long. SI ~4.0% float (rose ~52% in shares since March) but DTC ~2.3, cheap borrow. Sell-side ~88% Buy, PT median ~$230 (>+50% above spot) — but **PTs being trimmed while estimates rise** (de-rate). ~25–26% passive; buyback retires ~3.5–4%/yr net of trivial SBC. No activist 13D. Next print 2026-08-06, implied move ~±6–8%.

## 9. Pair-trade & sizing
**Long VST / short CEG**, dollar-neutral beta-adjusted ~1.00:0.88, on ~2-turn EV/EBITDA convergence + VST's +340bps FCF-yield carry. **Caveat:** the spread has **already largely converged** (CEG −16/−25% YTD vs VST −3/−4%) and CEG's balance sheet is cleaner (~1.7× vs 2.78×) — so **size small**, stop if the gap exceeds ~2.7 turns on a CEG hyperscaler-nuclear headline. Directional sizing: benchmark-weight long-only; **no directional short at $147** (don't fight rising estimates) — a tactical VST short only opens into the July BRA if the stock rallies to ~$170+ with a loose 2028/29 stack.

## 10. What-would-reverse (numerical triggers)
| Direction | Trigger | Observable |
|---|---|---|
| → Bull | PJM 2028/29 BRA >$300/MW-day **and** 2027 EBITDA guide ≥$7.6B | PJM BRA + VST Q2/Q3 guide |
| → Bull | Comanche Unit 2 or gas co-location signs 15yr+ PPA >$100/MWh | VST 8-K Item 1.01 |
| → Bear | PJM 2028/29 BRA <$250/MW-day (vs $333.44 cap) | PJM 2028/29 BRA (~Jul 2026) |
| → Bear | 2027 Adj EBITDA guide <$7.0B **or** net leverage >3.2× post-Cogentrix | VST earnings + 10-Q |
| → Bear | Margin posting >$2.8B in any 6-mo window (2022 analog $1.89B) | VST 10-Q (MarginDepositAssets) |
| → Bear | Top-4 hyperscaler cuts 2026/27 capex >10% **or** AWS/Meta PPA renegotiated | hyperscaler disclosures + 8-K |

## 11. Catalyst calendar
PJM 2028/29 BRA (~2026-07-09) · Q2 FY26 earnings (2026-08-06) · Cogentrix close (mid–late 2026) · next hyperscaler PPA (2026–27) · FERC EL25-49 compliance · AWS Comanche deliveries (Q4 2027).

## 12. Verification & gates
**36 web/data verification calls** across phases (Phase 0: 22; independent Verify pass: 14), plus ~250 across the multi-agent phases. **10 of 11 load-bearing specific claims independently re-verified** (FERC order, PJM clearing, IG upgrades, AWS/Meta PPAs, Cogentrix, 45U/OBBBA, FY25/Q1'26 financials, price). The one soft spot — **net leverage 2.78×** — is a *calculated* metric (net debt / Ongoing Adj EBITDA), **not company-reported**; treat it as modeled. Programmatic gates **G1–G17 all pass** (G16 banks N/A); see `outputs/VST_verification_gates.json`.

---
*Source matrix: `outputs/VST_source_tags.json` · Scenarios: `outputs/VST_scenarios.json` · Structured: `outputs/VST_structured.json` · Workpapers: `outputs/workpapers/`. GAAP financials verified against SEC XBRL companyfacts (primary). Phases 0–3 + Verification complete via 16 specialist agents.*
