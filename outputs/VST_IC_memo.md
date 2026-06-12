# Vistra Corp. (NYSE: VST) — IC Memo (v2, DE-BIASED rebuild)

**Rating: SELL / UNDERWEIGHT** (source-conditional) · **12-mo PT $124.94** (range $69.70–$217.60) · **Expected return −14.2%** (prob-weighted)
**As of:** 2026-06-09 · **Price:** $146.90 (S4: 2026-06-08 close) · **Sector:** Utilities › Independent Power Producers
**Mandate sizing:** −50bps underweight; relative short within the IPP sleeve. *De-biased rebuild; v1 Hold archived at `outputs/archive/VST_v1_hold/`.*

> **Headline (source-conditional Sell/Underweight, anchored to fair value):** VST at $146.90 carries a probability-weighted 12-month expected return of **−14.2%** to a base-case PT of **$124.94** — an **independent fair value** (DCF $107 / SOTP $132 / de-rated comps $130 → ~$125, **−15% vs spot**), **not** the spot-anchored ~14x forward P/E that produced the prior near-zero Hold. The v1 Hold held VST's elevated ~14x AI-power multiple on FY27E EPS; de-anchored to the **through-cycle / private-market band** (~11x — VST itself bought Cogentrix at ~7.25x EV/EBITDA, and NRG/LS Power gas marked ~7.5x), fair value is ~15% below spot. **CONDITIONAL on** the ~35% open 2028 generation book repricing toward the EIA base and PJM capacity reverting off the FERC cap; **cover toward Hold** on a sub-$120 entry or a >$300/MW-day PJM 2028/29 BRA print. Sized **Sell/Underweight, not Strong Sell** — the AI-power-demand + PPA-conversion timing tail is genuine.

---

## §1 Thesis in brief
This is a **de-biased rebuild** and a **rating flip** (Hold → Sell/Underweight). The only methodological change: anchor the base on an **independent fair value**, not on VST's current elevated multiple. VST is a high-quality integrated IPP — cheapest large merchant on EV/kW, hedged by a ~5M-customer retail book, with 20-year investment-grade hyperscaler PPAs (AWS, Meta) (S2: VST 8-Ks). But at $146.90 it sits near the high on peak AI-power capacity prices (PJM cleared at the FERC cap $333.44/MW-day, S1), and on **normalized through-cycle earnings** the franchise is worth **~$125 — about 15% below spot**: DCF $107, SOTP $132, comps de-rated to the private-market gas band $130. The prior Hold reached ~$153 only by holding a ~14x forward P/E; VST's **own capital allocation marks private fair value below the public multiple** (Cogentrix ~7.25x), and a ~35%-open 2028 book at PJM-capacity-at-the-cap is a peak-on-peak. Strip the spot-anchor and the asymmetry is adverse. The view is **source-conditional** on the open-book repricing and capacity reverting off the cap — the disciplined base. The AI-power-demand + PPA-conversion tail is real and capacity-scarcity is sticky on *timing*, so this is sized **Sell/Underweight + a relative short**, not a Strong Sell. Cover: sub-$120 or a >$300 BRA.

## §2 The five-scenario framework (FY27E EPS × P/E; base anchored to fair value)
| Scenario | Prob | FY27E EPS | P/E | PT | Return |
|---|---:|---:|---:|---:|---:|
| strong_bear | 13% | $8.20 | 8.5x | $69.70 | −52.6% |
| bear | 25% | $9.60 | 10.0x | $96.00 | −34.6% |
| **base** | **34%** | **$10.96** | **11.4x** | **$124.94** | **−14.9%** |
| bull | 20% | $11.80 | 14.0x | $165.20 | +12.5% |
| strong_bull | 8% | $12.80 | 17.0x | $217.60 | +48.1% |

**Weighted expected return −14.2%; P10/P90 [−52.6%, +48.1%].** **HEADLINE CONDITIONALITY:** source_conditional. The change vs v1: the base de-rates VST's multiple from ~14x to the ~11.4x through-cycle/private-market band rather than holding the peak AI-power multiple, so the base lands at fair value (−14.9%) not spot. Left-skewed because de-rate-to-private-market is the more likely path from a peak. (Full bridges in `outputs/VST_scenarios.json`; G1/G4/G5 verified.)

## §3 Three-method valuation reconcile (independent, normalized)
- **DCF: ~$107** (the fundamental anchor) — 10y FCFbG, WACC 9.61% (β 1.41 (S4); g 2.25%). Well below spot; the contracted cash-flow value strips the AI-power optionality premium.
- **SOTP: ~$132** — East (PJM nuclear+capacity+Meta), Texas (Comanche+AWS), Retail, West, net of debt. Monotonicity holds (G3).
- **Comps (de-rated): ~$130** — 8.0x 2027E EBITDA toward the **private-market gas band** (~7.25–7.5x VST/NRG paid), not the spot-anchored 8.75x.
- **Independent weighted fair value ~$125 (−15%).** Bear floor $53–74 (private-market 7.5x on a normalized 2028) anchors strong_bear.

All three fundamental methods land **below spot** once the AI-power multiple premium is removed — the entire difference vs the v1 Hold.

## §4 Earnings quality (S1: XBRL companyfacts, CIK 0001692819)
**GAAP/non-GAAP parallel (reconciliation: present).** GAAP net income is non-informational — dominated by ASC 815 unrealized hedge mark-to-market (FY25 GAAP NI $944M vs Ongoing Adj EBITDA $5,912M, ~6.3x). Underwrite on Adj EBITDA / FCFbG (G11 non-GAAP reconciliation present; G12 FCF = OCF − capex, SBC ~0.6% of revenue (S1: XBRL) and immaterial). Earnings quality is high (Deloitte clean opinion; no restatement/going-concern); the real tail is **hedge-collateral liquidity** (a 2x forward move could demand $3–4B vs ~$2.8B dry powder). The de-bias doesn't change earnings quality — only the multiple anchor.

## §5 The load-bearing risks (now to the short)
1. **AI-power demand stays strong / capacity prices hold (the cover risk).** PJM-at-the-cap + signed PPAs + the open 2028 book can keep the premium for 12+ months; overvaluation is not a catalyst. *Cover: >$300 BRA or sub-$120 entry.*
2. **PPA conversion (Comanche Unit 2 / gas co-location).** A >$100/MWh 15yr+ PPA on un-signed MW is the dominant bullish reverse.
3. **(Confirming the short) 2028 open-book reprices down + capacity reverts off the cap toward the $179.55 floor** → −$0.6 to −0.9B EBITDA (modal) to −$1.4–2.3B (tail).

## §6 Consensus variance (load-bearing for the Sell)
**V1 — DOWNWARD load-bearing variance on the 2028 open book + the multiple** (~60% conviction, sizing **2.16pp** = 18%×60%×20%/10000, S1 evidence). The Street is ~88% Buy with a PT median ~$230 (>+50% above spot); our independent fair value (~$125) is far below. **Stress-test (adjudication trail):** an isolated red-team attacked V1 on **timing-arbitrage** ("AI-power scarcity is sticky"); it survived **modified** — VST's own private mark (Cogentrix ~7.25x), the DCF ($107) and SOTP ($132) are all below spot and PJM-at-the-cap is peak, so fair value is below spot regardless of the open-book call. Sized Sell/Underweight, not Strong Sell.

## §7–§8 Regulatory & positioning (unchanged from v1)
FERC co-location (EL25-49): VST's Meta deal is FTM, AWS in ERCOT — low BTM exposure. EPA deregulatory pivot; PJM cap/collar binds through 2029/30. Export-control/sanctions N/A (US utility). Crowded long → unwind risk; SI ~4% float, DTC ~2.3 (cheap borrow). PT median ~$230 being trimmed while estimates hold.

## §9 Pair-trade & sizing
**−50bps underweight** vs S&P 500 (don't own at the high above fair value). For an L/S book, a **modest VST short** (net −1.5% NAV) or a relative short vs the cohort — **not aggressive** given the AI-power timing tail. The prior long-VST/short-CEG pair is *off* (de-biased, VST is the richer/short candidate now, and CEG is also above its own fair value). Re-enter long <$120 or on a >$300 BRA.

## §10 What-would-reverse
→ Cover: PJM 2028/29 BRA >$300/MW-day **or** a Comanche Unit 2 / gas co-location PPA >$100/MWh 15yr+ **or** stock <$120. → Confirm short: BRA <$250/MW-day **or** 2027 Adj EBITDA guide <$7.0B **or** margin posting >$2.8B/6mo.

## §11 Quant overlay
**Barra factor tags** (match `quant_overlay.factor_tags`): **Size +0.9**, **Growth +0.5**, **Liquidity +0.5**, **Value +0.4**, **Momentum −0.2**, **Quality −0.6**, **Low-Vol −0.8**. **Capacity:** 30-day ADV $793M (S4: 30-day avg); days-to-exit 10/20/30% = 6.3 / 3.2 / 2.1 days. Beta 1.41 (S4: 5y) — shorting it leans against a high-beta utility. 6-tail A0 map (shifts sum to zero) in `outputs/VST_structured.json`.

## §12 Verification
The de-bias is the only change vs v1 (base anchored to independent fair value, not spot). Programmatic gates **G1–G20 all pass** (G16 N/A non-bank; **G15 + G20 now PASS** — non-Hold, load-bearing variance with S1 evidence, ~71pp consensus differentiation, surviving variance_attack); see `outputs/VST_verification_gates.json`. v1 Hold: `outputs/archive/VST_v1_hold/`.
