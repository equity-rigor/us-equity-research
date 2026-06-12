# Energy Transfer LP (NYSE: ET) — IC Memo (v2, DE-BIASED rebuild)

**Rating: BUY** (marginal, source-conditional) · **12-mo PT $20.88** (range $14.70–$28.35) · **Expected return +11.5%** (prob-weighted)
**As of:** 2026-06-09 · **Price:** $19.06 (S4: 2026-06-09 close) · **Sector:** Energy › Oil & Gas Storage & Transportation (Midstream MLP)
**Mandate sizing:** modest overweight / yield-carry. *De-biased rebuild; v1 Buy archived at `outputs/archive/ET_v1_buy/`.*

> **Headline (source-conditional MARGINAL Buy, softened by the de-bias):** ET at $19.06 carries a probability-weighted 12-month expected return of **+11.5%** to a base-case PT of **$20.88** — an **independent fair value** (DCF $20.50 / SOTP $21.00 / comps $21.45 → ~$20.9, **+9.5% vs spot**). The de-bias **softens** ET from the prior +15.4% Buy to a **marginal Buy at the Buy/Hold boundary**: its **DCF (+7.6%) sits only modestly above spot**, and the base case (+9.5%) is right on the line — so unlike APD (DCF +22%), ET's Buy leans on the **right-skewed distribution** (a heavy bull weight) as much as on the base. The genuine support is the **~7% distribution yield + deleveraging + a growth pipeline**; but the Street's ~$23.5 PT (+23%) looks full and **we sit below consensus**. **CONDITIONAL on** distribution growth and project-pipeline delivery.

---

## §1 Thesis in brief
This de-biased rebuild **softens, but does not flip,** the Buy — the most nuanced of the six. ET is a high-yield (~7%) diversified midstream MLP (intrastate/interstate gas, NGL, crude, midstream) deleveraging with a sizeable organic + M&A growth pipeline, valued on price-to-distributable-cash-flow (P/DCF). When the base is anchored to independent fair value (~$20.9, +9.5%) rather than the spot-anchored 7.5x P/DCF, the call softens to a **marginal Buy** (weighted +11.5%, base +9.6%). The diagnostic: ET's **DCF (+7.6%) is only modestly above spot** — between the Holds (DCFs below spot) and APD (DCF +22%) — so the Buy is partly carried by the elevated base multiple and a right-skewed distribution, *not* purely by fundamentals. The view is **source-conditional** on distribution growth and pipeline delivery; the ~7% yield provides real carry, but the Street's +23% PT is full. **Conditional on** those, +11.5% expected → a marginal Buy that sits a hair above the Hold line.

## §2 The five-scenario framework (DCF/unit × P/DCF; base anchored to fair value)
| Scenario | Prob | DCF/unit | P/DCF | PT | Return |
|---|---:|---:|---:|---:|---:|
| strong_bear | 8% | $2.45 | 6.0x | $14.70 | −22.9% |
| bear | 20% | $2.65 | 6.8x | $18.02 | −5.5% |
| **base** | **37%** | **$2.86** | **7.3x** | **$20.88** | **+9.6%** |
| bull | 27% | $3.00 | 8.0x | $24.00 | +25.9% |
| strong_bull | 8% | $3.15 | 9.0x | $28.35 | +48.7% |

**Weighted expected return +11.5%; P10/P90 [−22.9%, +48.7%].** **HEADLINE CONDITIONALITY:** source_conditional. The de-bias lowered the base P/DCF from 7.5x to 7.3x and trimmed bull/strong_bull. Note the **right skew** (bull weight 0.27): it pulls the weighted return (+11.5%) above the base (+9.6%) — which is *why* ET stays a marginal Buy rather than flipping to Hold. (Per `outputs/ET_scenarios.json`; G1/G4/G5 verified. MLP P/DCF uses `multiple_type:"Other"` per the framework.)

## §3 Three-method valuation reconcile (independent)
- **DCF: ~$20.50 (+7.6%)** — only modestly above spot (the key data point distinguishing ET from APD).
- **SOTP: ~$21.00** — gas/NGL/crude/midstream segments net of debt + GP economics. Monotonicity holds (G3).
- **Comps (P/DCF): ~$21.45** — 7.5x DCF/unit.
- **Independent weighted fair value ~$20.9 (+9.5%).** Just above spot — a marginal Buy, not the solid Buy the v1 spot-anchored base implied.

## §4 Earnings quality & §5–§6
**GAAP/non-GAAP parallel (reconciliation: present).** MLP economics are best read on Distributable Cash Flow / unit and distribution coverage, not GAAP net income (G11 reconciliation present; G12 FCF/DCF definition disclosed). The declared variance V1 (sizing 2.11pp, S1/S2 evidence) drives the below-consensus stance; with a Buy rating it remains load-bearing and **G15 + G20 PASS** (~14pp differentiation vs the Street's +23% PT, surviving variance_attack). Load-bearing risks: commodity/volume sensitivity, distribution-growth execution, leverage, K-1 tax structure.

## §7–§10 (unchanged from v1)
Regulatory / positioning / triggers per v1. Triggers: stay/upgrade on DCF/unit growth + coverage >1.8x + deleveraging to target; downgrade to Hold on flat distribution growth or a DCF/unit guide cut.

## §11 Quant overlay
**Barra factor tags** (match `quant_overlay.factor_tags`): **Value +1.4**, **Size +1.1**, **Liquidity +0.8**, **Low-Vol +0.6**, **Growth +0.4**, **Momentum +0.3**, **Quality −0.3**. A deep-value, large, liquid MLP — the Value tilt is the main exposure. **Capacity:** 30-day ADV $320M (S4: 30-day avg); days-to-exit per `quant_overlay.capacity`. 6-tail A0 map (shifts sum to zero) in `outputs/ET_structured.json`.

## §12 Verification
The de-bias re-anchored the base to independent fair value (~$20.9, +9.5%) and **softened ET to a marginal Buy** (+11.5% weighted, +9.6% base) — it does not flip to Hold only because of the right-skewed distribution, which the report flags as the load-bearing assumption. Programmatic gates **G1–G20 all pass** (G16 N/A non-bank; G15 + G20 PASS, marginal Buy); see `outputs/ET_verification_gates.json`. v1 Buy archived: `outputs/archive/ET_v1_buy/`.
