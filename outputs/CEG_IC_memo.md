# Constellation Energy Corporation (Nasdaq: CEG) — IC Memo (v2, DE-BIASED rebuild)

**Rating: HOLD** (source-conditional, cautious) · **12-mo PT $233.55** (range $168.00–$356.50) · **Expected return −3.6%** (prob-weighted)
**As of:** 2026-06-11 · **Price:** $247.12 (S4: 2026-06-11 close) · **Sector:** Utilities › Independent Power Producers
**Mandate sizing:** benchmark-weight / modest underweight. *De-biased rebuild; v1 archived at `outputs/archive/CEG_v1_hold/`.*

> **Headline (source-conditional cautious Hold, SHARPENED by the de-bias):** CEG at $247.12 carries a probability-weighted 12-month expected return of **−3.6%** to a base-case PT of **$233.55** — an **independent fair value** (DCF $215 / SOTP $245 / comps $256 → ~$234, **−5% vs spot**). The de-bias **sharpens** CEG from the prior +3.0% Hold to a clearly cautious **~−4% Hold**: its **DCF sits −13% below spot**, so the premium-nuclear multiple is doing real work — but it **does not flip to Sell**, because the de-rate is **already ~40% done** (off the $412 high to a 52-week low), leaving fair value only ~5% below spot. **CONDITIONAL on** the FY2026 guide + >20% base-EPS-CAGR holding post-Calpine and hyperscaler PPA conversions resuming under the June-2026 PJM/FERC framework; two-sided → Hold (cautious).

---

## §1 Thesis in brief
This de-biased rebuild **sharpens, but does not flip,** the Hold. CEG is the highest-quality IPP — the largest US nuclear fleet (~32.4-GW, scaled by Calpine to ~60-GW), cleanest balance sheet (IG), 45U floor — but premium-priced on partly **cyclical-peak earnings** (PJM cleared at the FERC cap $329–333/MW-day, the FERC EL25-49 BTM restriction, Calpine gas dilution). Anchoring the base on independent fair value rather than the current ~19x multiple moves CEG to ~$234 (−5%): its **DCF ($215) is −13% below spot**, confirming the multiple carries real premium — yet the ~40% drawdown already taken keeps fair value only modestly below spot, so the disciplined call is a **cautious Hold (~−4%)**, not a Sell. The view is **source-conditional** on the >20% CAGR holding and PPA conversions resuming. **Conditional on** those, −3.6% expected → Hold, modest underweight.

## §2 The five-scenario framework (FY27E EPS × P/E; base anchored to fair value)
| Scenario | Prob | FY27E EPS | P/E | PT | Return |
|---|---:|---:|---:|---:|---:|
| strong_bear | 12% | $12.00 | 14.0x | $168.00 | −32.0% |
| bear | 25% | $12.75 | 16.0x | $204.00 | −17.4% |
| **base** | **36%** | **$13.50** | **17.3x** | **$233.55** | **−5.5%** |
| bull | 20% | $14.50 | 20.0x | $290.00 | +17.4% |
| strong_bull | 7% | $15.50 | 23.0x | $356.50 | +44.3% |

**Weighted expected return −3.6%; P10/P90 [−32.0%, +44.3%].** **HEADLINE CONDITIONALITY:** source_conditional (top-3 anchors include the FY2026 guide (S3) → conditional per G7). The de-bias lowered the base multiple from 19.0x to 17.3x (≈ the current FY27E forward, no longer assuming a re-rate) and trimmed bull/strong_bull. (Full bridges in `outputs/CEG_scenarios.json`; G1/G4/G5 verified.)

## §3 Three-method valuation reconcile (independent)
- **DCF: ~$215** (−13% below spot — shows the premium is real) — WACC 8.17% (beta 1.09 (S4: 5y weekly vs S&P 500); g 2.25%).
- **SOTP: ~$245** — nuclear (contracted) + Calpine gas + retail, net of debt + NCI. Monotonicity holds (G3).
- **Comps: ~$256** — 13.2x FY27E Adjusted EBITDA $8.5B.
- **Independent weighted fair value ~$234 (−5% vs spot).** Below spot, but only modestly — the ~40% drawdown already discounted much of the premium, which is why this sharpens rather than flips.

## §4 Earnings quality (S1: XBRL companyfacts, CIK 0001868275)
**GAAP/non-GAAP parallel (reconciliation: present).** GAAP is derivative-distorted (FY25 GAAP EPS $7.40 vs Adjusted Operating EPS $9.39); underwrite on Adjusted Operating Earnings (G11 reconciliation present; G12 FCF = OCF − capex, SBC ~0.3% of revenue (S1: XBRL) and immaterial). The real flag is hedge-collateral OCF volatility (−$5.3B FY23 → +$4.2B FY25). PwC clean; IG; no restatement. Unchanged by the de-bias.

## §5 Risks & §6 Consensus variance
Load-bearing risks (unchanged): premium de-rate on cyclical-peak earnings, FERC EL25-49 BTM restriction, Calpine integration/bought-at-peak, hyperscaler AI-capex cut, 45U sunset 2032. The declared downward variance V1 (premium durability, sizing 2.16pp, S2 evidence) is carried; **G15/G20 n_a (Hold)**. The de-bias confirms the base sits modestly below fair value.

## §7–§10 Regulatory, positioning, triggers (unchanged from v1)
FERC EL25-49: FTM blessed, BTM restricted (PPAs "paused"); PJM compliance June-2026 the key catalyst. PJM capacity at the cap (only down). Crowded long (76% Buy), stale PTs being cut. Triggers: cover/bull on a new FTM PPA + >20% CAGR reaffirmed or BRA >$300/MW-day; bear on FY27 EPS guide <$13.0 or a PPA repriced/delayed or BRA <$250/MW-day.

## §11 Quant overlay
**Barra factor tags** (match `quant_overlay.factor_tags`): **Size +1.0**, **Liquidity +0.8**, **Growth +0.7**, **Quality +0.3**, **Low-Vol −0.5**, **Value −0.6**, **Momentum −1.1**. **Capacity:** 30-day ADV $1.0B (S4: 30-day avg); days-to-exit 10/20/30% = 2.0 / 1.0 / 0.7 days. Beta 1.09 (S4: 5y weekly). 6-tail A0 map (shifts sum to zero) in `outputs/CEG_structured.json`.

## §12 Verification
The de-bias re-anchored the base to independent fair value (~$234) and SHARPENED the Hold to a cautious ~−4% (DCF −13% below spot), without flipping to Sell (de-rate already ~40% done). Programmatic gates **G1–G19 all pass** (G15/G16/G20 N/A: Hold, non-bank); see `outputs/CEG_verification_gates.json`. v1 archived: `outputs/archive/CEG_v1_hold/`.
