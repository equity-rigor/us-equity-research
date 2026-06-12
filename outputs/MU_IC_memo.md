# Micron Technology, Inc. (Nasdaq: MU) — IC Memo (0.6.0, fair-value-anchored)

**Rating: STRONG SELL / UNDERWEIGHT** (source-conditional) · **12-mo PT $702** (range $340–$1,360) · **Expected return −29.7%** (prob-weighted)
**As of:** 2026-06-11 · **Price:** $995.87 (S4: 2026-06-11 close) · **Sector:** Information Technology › Semiconductors (Memory) · **FYE:** late-Aug
**Mandate sizing:** −100bps underweight / avoid; **long-SK-Hynix / short-MU** is the cycle-neutral expression. *Fair-value-anchored from the start; replaces the older-version MU build.*

> **Headline (source-conditional Strong Sell, anchored to through-cycle fair value):** MU at $995.87 carries a probability-weighted 12-month expected return of **−29.7%** to a base-case PT of **$702**, against an **independent through-cycle fair value of ~$552** (mid-cycle EPS $40–48 × a cyclical 12–14x; **−45% vs spot**) and even a consensus PT of **~$829 (−17%, already below spot)**. This is the definitive fair-value-anchored case: MU looks "cheap" at ~16.7x FY2026E EPS ($59.82) or ~9x FY2027E — but that is **peak-cycle memory earnings**. On mid-cycle/normalized EPS at a cyclical-appropriate multiple, fair value is ~$550–700, not ~$1,000. On **price-to-book (~6.5x)** — the reliable cyclical anchor — MU trades **above its historical *peak* band (~3x)**, richer than at any prior memory peak. The stock is parabolic (+770–910% over 1yr, 52-wk low $103); the AI/HBM supercycle is real, but capitalizing a multi-sigma peak (Q2'26 GM 74.9%, Q3 guide ~81%) as a plateau is the trap. **CONDITIONAL on** the memory cycle mean-reverting toward mid-cycle over 12–24 months. Sized **Underweight + a relative short vs the HBM leader** (MU trades at a *premium* to #1 SK Hynix), **not** an aggressive outright short — the cycle is still rising and shorting a parabola is dangerous.

---

## §1 Thesis in brief
This 0.6.0 build is **fair-value-anchored from the start** — and that is the entire call. Micron is the #2 HBM supplier (~21–24% behind SK Hynix) and a genuine AI-memory beneficiary; the franchise is structurally better post-HBM (higher margins, multi-year contracts, a disciplined 3-player oligopoly). But the numbers are a multi-sigma peak: FY2026 consensus EPS ~$59.82 (vs FY2023 trough −$5.34 and FY2024 $0.70), Q2'26 GAAP gross margin 74.9% (vs ~22% in FY2024), on DRAM prices that rose ~+90% then ~+60% in consecutive quarters. **The de-bias:** value the cyclical on **normalized mid-cycle EPS** (~$40–48, crediting HBM; $30–40 per Wells Fargo) at a cyclical multiple → fair value ~$550–700. On P/B (~6.5x), MU is above its historical *peak*. And tellingly, the 44-analyst average PT ($829) is already **17% below spot** — the marginal buyer is above even the Street. The view is **source-conditional** on the cycle reverting; the timing tail (the cycle is still rising) is the bull leg and the reason this is sized Underweight, not an aggressive short. **Conditional on** mean-reversion, −29.7% expected → Strong Sell.

## §2 The five-scenario framework (cycle-position EPS × cyclical P/E; base anchored to fair value)
| Scenario | Prob | EPS | P/E | PT | Return |
|---|---:|---:|---:|---:|---:|
| strong_bear | 18% | $40 (mid-cycle, glut) | 8.5x | $340 | −65.9% |
| bear | 25% | $50 (normalizing) | 11.0x | $550 | −44.8% |
| **base** | **30%** | **$60 (FY26-peak)** | **11.7x** | **$702** | **−29.5%** |
| bull | 20% | $70 (cycle extends) | 14.0x | $980 | −1.6% |
| strong_bull | 7% | $80 (supercycle) | 17.0x | $1,360 | +36.6% |

**Weighted expected return −29.7%; P10/P90 [−65.9%, +36.6%].** **HEADLINE CONDITIONALITY:** source_conditional (top-3 anchors include normalized mid-cycle EPS (S3) → conditional per G7). The base de-rates the multiple on FY26-peak EPS to $702 — a **partial** reversion that lands *above* through-cycle fair value (~$552) because the cycle hasn't rolled within 12 months. Left-skewed: a glut/down-leg is the high-probability path from a peak; the bull tail is the cycle extending. (Full bridges in `outputs/MU_scenarios.json`; G1/G4/G5 verified.)

## §3 Three-method valuation reconcile (independent, NOT peak-anchored)
- **Normalized comps (primary): ~$672** — mid-cycle EPS ~$48 (crediting HBM vs Wells Fargo $30–40) × a cyclical 14.0x. The ~$60 FY26E / $112 FY27E *peak* EPS are NOT the valuation denominator.
- **DCF: ~$580** — 10y DCF on **normalized** mid-cycle FCF (mid-cycle ~30% margins against fixed ~$25B+ capex), WACC 13.73% (beta 2.17 (S4: 5y weekly vs S&P 500) — the high beta is punitive).
- **P/B cyclical anchor: ~$320** — book ~$75/share × a generous through-cycle ~4.3x P/B. Current ~6.5x P/B is **above** MU's historical *peak* (~3x). Monotonic segment SOTP cross-check holds (G3).
- **Independent through-cycle fair value ~$552 (−45%).** Bear/trough floor $190–300 (P/B reversion; FY2023 EPS was *negative*). The spot-anchored "cheap at ~9–17x forward P/E" inverts to Strong Sell once the denominator is normalized.

## §4 Earnings quality (S1: XBRL companyfacts, CIK 0000723125)
**GAAP/non-GAAP parallel (reconciliation: present).** The "flag" here is not accounting — it is **cyclicality**: GAAP EPS swung −$5.34 (FY23, *negative* gross margin) → $0.70 (FY24) → $7.59 (FY25) → ~$60 (FY26E); gross margin −9% → 75%. Do **not** capitalize a single peak print; underwrite on **mid-cycle/normalized** earnings (G11 reconciliation present; G12 FCF = OCF − capex, SBC ~1.2% of revenue (S1: XBRL); note peak-margin FCF (~$30B FY26E) is a peak artifact — at mid-cycle ~30% margins the fixed ~$25B+ capex eats most of it, and a trough inverts to a burn). Net cash ~+$4.4B; PwC clean opinion; no restatement/going-concern.

## §5 The load-bearing risks (now to the short)
1. **Cycle keeps running / supercycle extends (the cover risk).** Q3'26 guided a record; HBM sold out CY2026; momentum (+770–910%, IV ~100%). The peak may not roll within 12 months; **overvaluation is not a catalyst** — this is why it's sized Underweight, not an aggressive short. *Cover: FY2027 EPS consensus holds >$80 with DRAM ASP still rising.*
2. **HBM4 share gain / structurally higher normalized earnings.** If Micron takes decisive HBM4 share from SK Hynix and AI floors memory demand, normalized EPS is higher than we model.
3. **(Confirming the short) memory glut 2027–28** — Samsung qualifies HBM4, DRAM ASP turns negative, the 3–4x wafer-trade-ratio snaps into a commodity oversupply, CXMT commoditizes legacy DRAM, AI-capex digests → EPS reverts toward mid-cycle/trough.

## §6 Consensus variance (load-bearing for the Strong Sell)
**V1 — DOWNWARD load-bearing variance on the memory-cycle position / normalized earnings** (~65% conviction, sizing **3.9pp** = 30%×65%×20%/10000). Consensus rates MU 89% Buy on peak FY2026E EPS, yet its **own average PT ($829) is 17% below spot**. We mark FY2026 EPS as a multi-sigma peak (75% margins vs ~25–30% mid-cycle; FY2023 was −$5.34, S1/S2), normalized EPS at ~$40–48 → through-cycle fair value ~$552, and P/B (~6.5x) above the historical *peak* (~3x, S4). Our PT-implied return (−29.5%) is ~13pp below even the below-spot consensus. **Stress-test (adjudication trail):** an isolated red-team attacked V1 on **timing-arbitrage** ("the cycle is still rising; HBM is structurally different; don't short a parabola"); it survived **modified** — we raised normalized EPS to ~$48 (crediting HBM), set the 12-month base *above* through-cycle fair value, and sized the position Underweight + a relative short, not an aggressive outright short. **G15 + G20 PASS** (12.7pp differentiation, S1/S2 evidence, surviving attack).

## §7 Regulatory & §8 Positioning
US BIS export controls (CXMT curbed); CHIPS Act up to $6.4B for Idaho/NY fabs; China 2023 sales restriction (geopolitical). Passive-dominated ownership (BlackRock ~7.8%, Vanguard ~7.5%); short interest only ~3.3% float, DTC ~0.8 (no squeeze fuel either way); IV ~100% (S4); S&P 500 / Nasdaq-100 / SOX. Net insider selling. The average PT below spot is the key sentiment tell.

## §9 Pair-trade & sizing
**Long SK Hynix / short MU**, dollar-neutral beta-adjusted ~1.00:0.85 — long the **cheaper HBM leader** (~6x fwd P/E, ~3x P/B) vs short the pricier **#2** (~16.7x, ~6.5x P/B). Cycle-neutral; the edge is MU's premium-to-the-leader + its single-vintage AI-peak earnings capitalized at a *higher* multiple than the franchise that actually leads HBM. Size **small** and manage tightly around the Q3'26 print (both legs high-beta). Directional: **−100bps underweight / avoid** at $996; for an L/S book a **modest** MU short (net −1.5% NAV), **not aggressive** given the parabolic momentum + cycle-still-rising. Re-enter long only on a de-rate <$600 with demand intact.

## §10 What-would-reverse
→ Cover/Bull: FY2027 EPS consensus holds >$80 **and** DRAM ASP still rising; **or** Samsung HBM4E qualification slips past 2026 with AI capex >+30%. → Confirm short: DRAM ASP turns **negative** in any CY2027 quarter; **or** HBM pricing cut >10% as Samsung qualifies; **or** FY2027 consensus EPS <$40; **or** DRAM inventory >8 weeks.

## §11 Quant overlay & A0 tail map
**Barra factor tags** (match `quant_overlay.factor_tags`): **Momentum +2.5**, **Growth +1.8**, **Size +1.2**, **Liquidity +1.0**, **Quality 0.0**, **Value −1.5**, **Low-Vol −2.0**. The profile screams late-cycle momentum: extreme **Momentum** + extreme negative **Low-Vol** (beta 2.17 (S4: 5y), IV ~100%) + deeply negative **Value** — shorting it leans hard against Momentum, the main risk to the trade. **Capacity:** 30-day ADV $40B (S4: 30-day avg) — among the most liquid in the market; days-to-exit at 10/20/30% = 0.3 / 0.2 / 0.1 days. **Stress overlay:** Fed +200bp −28%; memory glut 2027 −65%; AI-capex digestion −55%; recession −55%. **A0 tail map** (6 tails; shifts sum to zero per row): glut, AI-capex digestion, recession, rate shock (bear); supercycle-extends, HBM4-share-gain (bull) — full matrix in `outputs/MU_structured.json`.

## §12 Verification
This 0.6.0 build anchors the base to an independent **through-cycle** fair value (~$552; 12-month base $702 on partial reversion), NOT to peak FY2026 EPS × the current multiple — the methodology that makes the most-cyclical large-cap look "cheap" at a peak. **36 web/data verification calls**; load-bearing specifics independently re-verified (FY23–25 financials via XBRL, Q2'26 print, DRAM/NAND + HBM pricing, mid-cycle EPS framework, P/B history, consensus PT below spot). Programmatic gates **G1–G20 all pass** (G16 N/A non-bank; **G15 + G20 PASS** — non-Hold, S1/S2-evidenced load-bearing variance, 12.7pp consensus differentiation, surviving variance_attack); see `outputs/MU_verification_gates.json`.

---
*Source matrix: `outputs/MU_source_tags.json` · Scenarios: `outputs/MU_scenarios.json` · Structured: `outputs/MU_structured.json` · Workpapers: `outputs/workpapers/`. GAAP financials verified against SEC XBRL companyfacts (primary). Phases 0–3 + Verification complete.*
