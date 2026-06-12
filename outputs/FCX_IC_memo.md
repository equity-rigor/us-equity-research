# Freeport-McMoRan Inc. (NYSE: FCX) — IC Memo (v2, DE-BIASED rebuild)

**Rating: SELL / UNDERWEIGHT** (source-conditional) · **12-mo PT $57.09** (range $36.80–$100.00) · **Expected return −11.0%** (prob-weighted)
**As of:** 2026-06-11 · **Price:** $66.20 (S4: 2026-06-11 close) · **Sector:** Materials › Copper / Diversified Metals & Mining
**Mandate sizing:** −60bps underweight; **long-SCCO / short-FCX** is the primary (copper-neutral) expression.
*Methodology note: this is the de-biased rebuild of the prior Hold — the base case is anchored to an independent mid-cycle-copper fair value, NOT to "consensus EPS × the current multiple." The v1 Hold is archived at `outputs/archive/FCX_v1_hold/`.*

> **Headline (source-conditional Sell/Underweight, anchored to fair value):** FCX at $66.20 carries a probability-weighted 12-month expected return of **−11.0%** to a base-case PT of **$57.09** — an **independent mid-cycle fair value** (DCF $58 / NAV $60 / normalized-comps $54 → ~$57.5, **−13% vs spot**), **not** the spot-anchored "current multiple × consensus EPS" that produced the prior near-zero Hold. We sit **~19pp below the consensus PT-implied return** (median $70, +5.5%, S4). FCX is a high-quality copper leader, but it is at its **52-week high** (~$66, +55% over 1yr) on **near-record copper** (~$6.19/lb [S4: ~40–55% above a $4.00–4.50/lb mid-cycle]); capitalizing peak copper at an above-average ~10x EV/EBITDA (vs ~7.8x 5-yr avg) **double-counts the cycle**. **CONDITIONAL on** copper mean-reverting toward mid-cycle over 12 months — more likely than not on Goldman's 2026-decline call, China-property weakness, and record supply additions. The structural-deficit tail + Grasberg recovery cap this at **Sell/Underweight, not Strong Sell**; **cover toward Hold if** copper holds >$6.25/lb sustained.

---

## §1 Thesis in brief
This is a **de-biased rebuild** and a **rating flip** (Hold → Sell/Underweight) driven by one methodological change: we anchor the base case on an **independent fair value**, not on the current price/multiple. FCX is a quality copper franchise — large-cap leverage to a real structural deficit (declining grades, thin pipeline, grid/EV/AI demand), ~$400M EBITDA per $0.10/lb, Grasberg recovering in 2027, leaching scaling to ~800 Mlb. But at $66.20 it sits at its 52-week high on near-record copper (~$6.19/lb, ~40–55% above a $4.00–4.50 mid-cycle), and on **normalized mid-cycle earnings** the franchise is worth **~$57.5 — about 13% below spot**: DCF $58, NAV $60, comps at the 5-yr-average 7.5x on normalized ~$11.5B EBITDA $54. The prior Hold reached ~$66 only by applying ~7.7x to **peak-copper** $13.5B EBITDA — i.e., it let the base anchor to spot. Strip that anchor and the asymmetry is adverse: consensus rates it 83% Buy yet its **own PTs are only +5.5% above spot**, the FY2026 copper guide was already **cut** (3.4→3.1 Blb) and unit cash cost **raised** ($1.75→$1.95/lb), and Goldman models a 2026 copper decline. The view is **source-conditional** on copper mean-reverting toward mid-cycle — the disciplined base. The structural deficit and Grasberg recovery are genuine and copper deficits are sticky on *timing*, so this is sized as a **Sell/Underweight + a long-SCCO/short-FCX pair**, not a Strong Sell. Cover trigger: copper >$6.25/lb sustained.

## §2 The five-scenario framework (FY27E EPS × P/E, copper-path-driven; base anchored to fair value)
| Scenario | Prob | Copper | FY27E EPS | P/E | PT | Return |
|---|---:|---|---:|---:|---:|---:|
| strong_bear | 15% | ~$4.00 | $2.30 | 16.0x | $36.80 | −44.4% |
| bear | 27% | ~$4.60 | $2.95 | 17.0x | $50.15 | −24.2% |
| **base** | **33%** | **~$5.25** | **$3.30** | **17.3x** | **$57.09** | **−13.8%** |
| bull | 18% | ~$6.25 | $4.20 | 18.5x | $77.70 | +17.4% |
| strong_bull | 7% | ~$7.50 | $5.00 | 20.0x | $100.00 | +51.1% |

**Weighted expected return −11.0%; P10/P90 [−44.4%, +51.1%].** **HEADLINE CONDITIONALITY:** source_conditional (top-3 anchors led by the copper price (S4) + FY2026 guide (S3) → conditional per G7). The change vs v1: the **base no longer assumes the current ~18.5x multiple holds on peak-copper EBITDA** — it uses a ~17.3x through-cycle multiple on a mid-cycle-reverting EPS, so the base lands at fair value (−13.8%), not at spot (0%). The probability weights are left-skewed because mid-cycle reversion is more likely than continued ascent at +40–55% above mid-cycle. (Full bridges in `outputs/FCX_scenarios.json`; G1/G4/G5 verified.)

## §3 Three-method valuation reconcile (independent, mid-cycle-anchored)
- **EV/EBITDA comps (primary, normalized): ~$54.** 7.5x (FCX's 5-yr through-cycle average) on **NORMALIZED** mid-cycle Adjusted EBITDA ~$11.5B (at ~$4.75–5.00/lb copper, *not* the ~$13.5B that spot copper implies) → EV ~$86B − ~$9B net + project debt + minority = ~$77B / 1,443M (S4: SCCO ~20x / RIO ~7–8x). The v1 Hold used 7.7x on **$13.5B peak-copper** EBITDA to reach ~$66 = spot — that was the spot-anchoring.
- **DCF: ~$58** (range $48–70). 10y mine-life DCF on a mid-cycle deck ($4.75–5.00/lb), WACC 9.85% (beta 1.36 (S4: 5y weekly vs S&P 500); CoE 10.27%), g 2.0% (S1: FRED DGS10 4.52%; S5: Damodaran ERP 4.23%).
- **NAV/SOTP: ~$60** (mid-cycle). Indonesia/Grasberg (net of MIND ID 51% minority), North America (incl leaching optionality), South America (net minorities), less net + project debt. Monotonicity NI≤OP≤GP≤Rev holds (G3). Below the v1 ~$70, which had credited near-spot copper.
- **Independent weighted fair value: ~$57.5 (−13% vs spot).** Bear floor $36–42 (mid-cycle copper at a de-rated 6x) approaches the 52-week low $35.15.

Methods cluster $54–60 — **all below spot** once the copper deck is normalized. That is the entire difference between this Sell and the prior Hold.

## §4 Financials & earnings quality (S1: XBRL companyfacts, CIK 0000831259)
| $M unless noted | FY23A | FY24A | FY25A | FY26E | FY27E |
|---|---:|---:|---:|---:|---:|
| Revenue | 22,855 | 25,455 | 25,915 | ~26,500 | ~28,500 |
| GAAP EPS (diluted) | 1.28 | 1.31 | 1.52 | ~2.69 | ~3.30 (normalized) |
| Adjusted EBITDA (spot copper) | ~7,500 | ~8,800 | ~9,900 | ~11,500 | ~13,500 |
| Normalized EBITDA (mid-cycle) | — | — | — | ~10,500 | ~11,500 |
| Operating cash flow | 5,279 | 7,160 | 5,610 | — | — |
| Capex | 2,422 | 2,565 | 2,949 | ~4,300 | ~4,500 |

**GAAP/non-GAAP parallel (reconciliation: present).** GAAP earnings are commodity-volatile and provisional-pricing-driven (Q1'26 EPS $0.61 on a $5.78/lb realized copper price); the right frame is **copper-deck-explicit Adjusted EBITDA** with the sensitivity stated (~$400M EBITDA per $0.10/lb, S1) — and critically, the **base case uses normalized (mid-cycle) EBITDA, not spot-copper EBITDA**. Q1'26 carried a $406M idle-facility/restoration charge (Grasberg) + a $699M insurance settlement (G11 reconciliation present; G12 FCF = OCF − capex, SBC ~0.5% of revenue (S1: XBRL) and immaterial). A large minority interest (MIND ID 51% of PT-FI) sits between consolidated EBITDA and FCX-attributable cash flow. EY clean opinion; no restatement/going-concern.

## §5 The load-bearing risks (now to the SHORT/underweight)
1. **Copper stays elevated / supercycle (the cover risk).** Low inventories + a structural deficit can keep copper >$6/lb through the 12-month horizon; momentum (+55% to the 52-wk high) and index flows can sustain the premium. **Overvaluation is not a catalyst** — this is the timing tail that caps us at Sell/Underweight, not Strong Sell. *Cover trigger: copper >$6.25/lb sustained or a Grasberg de-risk.*
2. **Grasberg full recovery + new low-cost pounds.** An on-/ahead-of-plan 2027 ramp + leaching to ~800 Mlb adds volume the bear under-credits.
3. **US refined-copper Section 232 tariff** would lift US realized prices (a bull catalyst on the June-30-2026 review).
4. **(Confirming the short) copper correction + Grasberg/Indonesia.** A reversion toward $4.50 mid-cycle removes ~$5B+ EBITDA and, with the historical miner de-rate, maps to the −30% to −45% strong-bear/bear region.

## §6 Consensus variance (the edge — now load-bearing for a non-consensus Sell)
**V1 — a DOWNWARD load-bearing variance on peak-copper/multiple durability** (~60% conviction, sizing **2.40pp** = magnitude 20% × probability 60% × sensitivity 20% / 10000). The Street rates FCX **83% Buy yet its own PTs sit only +5.5% above spot** — a "Buy" belied by targets at fair value. We mark copper at ~$6.19/lb as ~40–55% above a $4.00–4.50 mid-cycle (S4; Goldman models a 2026 decline), FCX's ~10x EV/EBITDA as above its ~7.8x 5-yr average on **peak** earnings (S4), and note the FY2026 copper guide was **cut** (3.4→3.1 Blb, S2) and unit cash cost **raised** ($1.75→$1.95/lb, S1). On a mid-cycle-reversion base, independent fair value is ~$57.5 (−13%), putting our PT-implied return **~19pp below consensus**. **Stress-test (adjudication trail):** an isolated red-team attacked V1 on **timing-arbitrage** ("overvaluation ≠ 12-month downside; deficits are sticky"); it survived **modified** — we hold conviction at 60% and size as **Sell/Underweight + a long-SCCO/short-FCX pair**, not a Strong Sell, precisely to respect that timing risk. The structural copper-deficit + Grasberg recovery are the genuine two-tailed upside.

## §7 Regulatory & policy desk (S1/S2)
- **US Section 232 copper:** refined copper exempted 2025; June-30-2026 review may add a phased refined-copper duty (15% 2027 → 30% 2028) — two-sided (helps US cathode; but the record COMEX-LME premium in realized price could deflate if it disappoints).
- **Indonesia (MEMR / MIND ID):** IUPK to 2041 (Feb-2026 MoU for post-2041 extension via ~12% additional divestment, stake to ~37% from 2042); export permits + downstreaming + a contested duty.
- **Export-control/sanctions: N/A** (US-domiciled miner; verified 2026-06-11).

## §8 Positioning & sentiment
**Index-heavy, low short interest — a *constructive*-positioning headwind to the short.** Vanguard ~7.49%, BlackRock ~6.6% (S2: 13F); ~85% institutional. Short interest only ~1.98% float, DTC ~2.6 (declining) — so the short is *not* crowded (good entry) but also has no squeeze fuel either way. ~22% ETF/passive; S&P 500. Sell-side **83% Buy / 13% Hold / 4% Sell**, PT median $70 (only ~+5.5%); the conservative cluster (UBS/RBC/BofA ~$46) is ~30% below spot — closer to our fair value. Beta 1.36 (S4: 5y weekly). 30-day **ADV $790M** (S4: ~12.5M sh × ~$63) — ample liquidity for the short. Stock +55% over 1yr to its 52-week high $72.09. Next print ~2026-08-05, implied move ~±6%.

## §9 Pair-trade & sizing (the primary expression)
**Long SCCO / short FCX**, dollar-neutral beta-adjusted ~1.00:0.90 — the cleanest expression of the de-biased view: **short FCX** (above independent fair value at the cycle high + Grasberg/Indonesia single-asset risk + peak-multiple-on-peak-copper) vs **long SCCO** (better jurisdiction Peru/Mexico, superior organic growth, lower single-asset risk). The cost is SCCO's higher multiple (~20x vs ~10x EV/EBITDA), so it is a **quality/jurisdiction + valuation-discipline** trade; size moderate, **stop if copper accelerates** (FCX has the higher upside beta) **or FCX de-risks Grasberg**. Directional sizing: **−60bps underweight** vs S&P 500 (don't own at $66); for an outright book, a **modest FCX short** (net −1.5% NAV at the L/S level), **not aggressive** given the structural-copper timing tail. Re-enter long only on a copper dip <$5.50/lb or a Grasberg de-risk toward <$55.

## §10 What-would-reverse (numerical triggers)
| Direction | Trigger | Observable |
|---|---|---|
| → Cover/Bull | Copper sustained >$6.25/lb 2+ quarters **and** Grasberg on-track for full 2027 recovery (2027 Cu guide ≥3.4 Blb) | COMEX/LME + FCX guidance |
| → Cover/Bull | Leaching reaches ~300 Mlb FY26 run-rate **and** a US refined-copper Section 232 tariff is enacted | FCX disclosure + Commerce 232 |
| → Bear (confirm short) | Copper falls <$4.75/lb COMEX sustained 2+ months (~−20% from spot) | COMEX/LME monthly average |
| → Bear | FY2026 copper sales guide cut again <3.0 Blb **or** Grasberg restart slips past Q2'26 | FCX Q2/Q3 FY26 8-K |
| → Bear | FY2026 unit net cash cost guide raised >$2.10/lb (from ~$1.95) | FCX quarterly cost guide |
| → Bear | Indonesia export permit lapses **or** new export duty imposed **and** Manyar restart slips past 2026 | MEMR + FCX 8-K |
| → Re-enter long | Stock de-rates <$50 (toward fair value / bear floor) while the structural deficit stays intact | price + copper inventories/curve |

## §11 Quant overlay & A0 tail map
**Barra factor tags** (z-scores, analyst-asserted, match `quant_overlay.factor_tags`): **Momentum +1.4**, **Size +1.0**, **Liquidity +0.7**, **Growth +0.5**, **Quality 0.0**, **Value −0.3**, **Low-Vol −1.2**. A high-beta, large-cap, **strong-momentum** (+55% to the 52-wk high) cyclical that screens neither cheap nor defensive — *shorting it leans against Momentum*, the main risk to the trade. **Capacity:** 30-day ADV $790M (S4: ~12.5M sh × ~$63); days-to-exit at 10%/20%/30% participation = 2.5 / 1.3 / 0.8 days; max position ~4.0% NAV. **Stress overlay:** Fed +200bp −16%; copper −20% −38%; Grasberg further setback −22%; recession −40%. **A0 tail map** (6 tails; probability-shifts sum to zero per row): copper correction (bear), Grasberg/Indonesia action (bear), recession (bear), Fed +200bp (bear), copper supercycle (bull — the cover risk), leaching/growth (bull) — full matrix in `outputs/FCX_structured.json` `tail_risks`.

## §12 Catalyst calendar & verification
Copper-price trajectory (continuous) · Grasberg Blocks 2&3 ramp (Q2'26, Q2 earnings ~2026-08-05) · US Section 232 copper review (~2026-06-30) · Manyar restart + Indonesia export permit (~2026-09-30) · leaching scale-up. **34 web/data verification calls**; load-bearing specifics independently re-verified (FY25/Q1'26 financials via XBRL, copper price, Grasberg mud-rush + ramp, MIND ID + MoU, unit-cost guide, Section 232, consensus, price). The de-bias is the only change vs v1: **base anchored to independent mid-cycle fair value, not spot.** Programmatic gates **G1–G20 all pass** (G16 N/A non-bank; **G15 + G20 now PASS** — non-Hold rating, load-bearing variance with S1/S2 evidence, ~19pp consensus differentiation, surviving variance_attack); see `outputs/FCX_verification_gates.json`.

---
*Source matrix: `outputs/FCX_source_tags.json` · Scenarios: `outputs/FCX_scenarios.json` · Structured: `outputs/FCX_structured.json` · v1 Hold archived: `outputs/archive/FCX_v1_hold/`. GAAP financials verified against SEC XBRL companyfacts (primary).*
