# Air Products and Chemicals, Inc. (NYSE: APD) — IC Memo (v2, DE-BIASED rebuild)

**Rating: BUY** (source-conditional, high conviction) · **12-mo PT $353.80** (range $200.00–$448.00) · **Expected return +18.5%** (prob-weighted)
**As of:** 2026-06-09 · **Price:** $282.35 (S4: close) · **Sector:** Materials › Industrial Gases · **FYE:** Sep 30
**Mandate sizing:** +150bps active vs S&P 500. *De-biased rebuild; v1 archived at `outputs/archive/APD_v1_buy/`.*

> **Headline (source-conditional Buy, CONFIRMED by the de-bias):** APD at $282.35 carries a probability-weighted 12-month expected return of **+18.5%** to a base-case PT of **$353.80** — an **independent fair value** (DCF $345 / SOTP $365 / comps $355 → ~$354, **+25% vs spot**). This is the key contrast with the Holds: **APD's DCF (+22%) and SOTP (+29%) both sit ABOVE spot**, so the prior Buy was **never a spot-anchoring artifact** — anchoring the base on independent fundamentals *confirms* it. Activist-installed management (Eduardo Menezes, ex-Linde, CEO since Feb-2025) is cutting capex from a ~$7.0B FY2025 peak toward ~$4.0B, the ~$3.7B FY2025 hydrogen charges are behind it, **free cash flow inflects positive in FY2027**, and APD trades at a ~25–28% forward-P/E discount to Linde. We sit **~9–10pp above the consensus PT-implied return**. **CONDITIONAL on** the FY2027 FCF inflection and no further >$1.0B impairment.

---

## §1 Thesis in brief
This de-biased rebuild **confirms the Buy** — the most important contrast in the set. When you anchor the base on independent fair value instead of "consensus EPS × the current multiple," the Holds (VST/CEG/FCX) move *down* (their DCFs were below spot) and one flips to Sell; **APD moves nowhere**, because its **DCF ($345, +22%) and SOTP ($365, +29%) were already above spot**. The Buy is independently supported by fundamentals, not by spot-anchoring. APD is an industrial-gas oligopoly mid-turnaround: capex rolling off ($7B→$4B), FY2025 hydrogen charges taken, FCF inflecting from −$3.8B toward positive in FY2027, trading at a wide discount to Linde with an activist-installed operator restoring discipline. The view is **source-conditional** on the FCF inflection and no further large impairment. **Conditional on** those, +18.5% expected → Buy.

## §2 The five-scenario framework (FY27E adjusted EPS × P/E; base anchored to fair value)
| Scenario | Prob | FY27E EPS | P/E | PT | Return |
|---|---:|---:|---:|---:|---:|
| strong_bear | 10% | $12.50 | 16.0x | $200.00 | −29.2% |
| bear | 22% | $13.50 | 19.0x | $256.50 | −9.2% |
| **base** | **40%** | **$14.50** | **24.4x** | **$353.80** | **+25.3%** |
| bull | 20% | $15.25 | 26.5x | $404.12 | +43.1% |
| strong_bull | 8% | $16.00 | 28.0x | $448.00 | +58.7% |

**Weighted expected return +18.5%; P10/P90 [−29.2%, +58.7%].** **HEADLINE CONDITIONALITY:** source_conditional (top-3 anchors include the FY2026 guide (S3) + the LIN-discount valuation (S4) → conditional per G7). The de-bias barely changed the base (multiple 24.5x → 24.4x) — because fair value was already above spot. (Full bridges in `outputs/APD_scenarios.json`; G1/G4/G5 verified.)

## §3 Three-method valuation reconcile (independent — all ABOVE spot)
- **DCF: ~$345 (+22%)** — the fundamental anchor sits well above spot, WACC 6.96% (beta 0.75 (S4: 5y weekly vs S&P 500); g 2.5%); the sharp FCF inflection as capex normalizes drives it.
- **SOTP: ~$365 (+29%)** — Americas / Asia / Europe at 13–14x, plus clean-H2 optionality, less net debt. Monotonicity holds (G3).
- **Comps: ~$355** — 24.5x FY27E adjusted EPS $14.50 (half-gap re-rate to Linde).
- **Independent weighted fair value ~$354 (+25%).** All three above spot — the de-bias *confirms* the Buy.

## §4 Earnings quality (S1: XBRL companyfacts, CIK 0000002969)
**GAAP/non-GAAP parallel (reconciliation: present).** FY2025 GAAP was a loss (−$1.74) on ~$3.7B project-exit charges vs adjusted EPS $12.03; underwrite on adjusted EPS / Consolidated Adjusted EBITDA (G11 reconciliation present; G12 FCF = OCF − capex, SBC ~0.6% of revenue (S1: XBRL) and immaterial). The genuine flag is the debt-funded dividend until the FY2027 FCF inflection. KPMG clean; A/A2 (negative outlook). Unchanged by the de-bias.

## §5 Risks & §6 Consensus variance
Load-bearing risks (unchanged): residual hydrogen impairment tail (NEOM/Louisiana), FCF inflection fails, valuation/rate sensitivity, execution, Linde out-executes. The load-bearing variance V1 (FCF-inflection re-rate, **sizing 2.4pp, S1/S2 evidence**) drives the non-consensus Buy. **Stress-test (adjudication trail):** an isolated red-team attacked V1 on **base-rate sanity** ("activist turnarounds re-rate only sometimes"); it survived **modified** (probability trimmed 65→60%, re-rate capped at half-gap). **G15 + G20 PASS** (9.1pp consensus differentiation, S1/S2 evidence, surviving attack).

## §7–§10 Regulatory, positioning, triggers (unchanged from v1)
45V/45Q clean-H2 credits underpin NEOM/Louisiana economics; no BIS/OFAC/CFIUS. Mantle Ridge won 3 board seats; ~39% Hold cohort (the variance target). Triggers: bull on FY2027 FCF positive + capex ≤$4.0B + LIN gap <5 turns or NEOM/Yara FID by Dec-2026; bear on a >$1B impairment or FY2027 EPS guide <$13.50 or capex re-acceleration >$4.5B.

## §11 Quant overlay
**Barra factor tags** (match `quant_overlay.factor_tags`): **Size +0.9**, **Quality +0.8**, **Low-Vol +0.8**, **Momentum +0.6**, **Value +0.5**, **Growth +0.2**, **Liquidity +0.2**. **Capacity:** 30-day ADV $340M (S4: 30-day avg); days-to-exit 10/20/30% = 3.5 / 1.8 / 1.2 days. Beta 0.75 (S4: 5y weekly). 6-tail A0 map (shifts sum to zero) in `outputs/APD_structured.json`.

## §12 Verification
The de-bias re-anchored the base to independent fair value (~$354, +25%) and **CONFIRMED the Buy** — APD's DCF/SOTP were already above spot, so it was never a spot-anchoring artifact (the clean contrast with the Holds). Programmatic gates **G1–G20 all pass** (G16 N/A non-bank; G15 + G20 PASS); see `outputs/APD_verification_gates.json`. v1 archived: `outputs/archive/APD_v1_buy/`.
