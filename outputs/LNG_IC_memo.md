# Cheniere Energy, Inc. (NYSE: LNG) — IC Memo (v2, DE-BIASED rebuild)

**Rating: HOLD** (source-conditional) · **12-mo PT $243.88** (range $144.50–$352.00) · **Expected return +0.7%** (prob-weighted)
**As of:** 2026-06-09 · **Price:** $239.40 (S4: 2026-06-09 close) · **Sector:** Energy › Oil & Gas Storage & Transportation
**Mandate sizing:** benchmark-weight. *De-biased rebuild; v1 archived at `outputs/archive/LNG_v1_hold/`.*

> **Headline (source-conditional Hold, CONFIRMED by the de-bias):** LNG at $239.40 carries a probability-weighted 12-month expected return of **+0.7%** to a base-case PT of **$243.88** — an **independent fair value** (DCF $225 / SOTP $262 / comps $253 → ~$244, ~flat vs spot). The notable finding: anchoring the base on fundamentals rather than "consensus EPS × current multiple" **barely moves LNG** (v1 base $253.63 → $243.88), because its **DCF was already only ~6% below spot**. So the prior Hold was a **genuine fair-value call, not a spot-anchoring artifact** (unlike VST/FCX, whose DCFs sat 12–27% below spot and flipped to Sell). **CONDITIONAL on** the ~90%-contracted take-or-pay book holding its fixed liquefaction fees through the mid-2030s and the FY2026 guidance raise proving durable into the global LNG supply wave; two-sided → Hold.

---

## §1 Thesis in brief
This de-biased rebuild **confirms the Hold** (it does not flip). Cheniere is a ~90%-contracted, IG-rated, buyback-compounding LNG cash-flow machine; the contracted annuity supports value **close to the current price even on normalized assumptions**, while the largest LNG supply wave in history (~193 mtpa 2024–28) caps upside. The de-bias test — anchor the base on independent fair value, not the current multiple — moves LNG only ~−4% (to ~$244), because its **DCF ($225) was already near spot**. That is the diagnostic: LNG's v1 Hold was earned on fundamentals, not manufactured by spot-anchoring. The view remains **source-conditional** on the contracted book holding its fixed fees and the FY2026 raise (a partly spread-driven beat) proving durable; the open/merchant slice is tiny (<1 mtpa in 2026), so the risk is two-sided around fair value. **Conditional on** those, +0.7% expected → Hold.

## §2 The five-scenario framework (FY27E EPS × P/E; base anchored to fair value)
| Scenario | Prob | FY27E EPS | P/E | PT | Return |
|---|---:|---:|---:|---:|---:|
| strong_bear | 10% | $17.00 | 8.5x | $144.50 | −39.6% |
| bear | 22% | $18.50 | 10.5x | $194.25 | −18.9% |
| **base** | **38%** | **$19.51** | **12.5x** | **$243.88** | **+1.9%** |
| bull | 22% | $20.50 | 14.0x | $287.00 | +19.9% |
| strong_bull | 8% | $22.00 | 16.0x | $352.00 | +47.0% |

**Weighted expected return +0.7%; P10/P90 [−39.6%, +47.0%].** **HEADLINE CONDITIONALITY:** source_conditional (top-3 anchors include the FY2026 EBITDA + DCF guides (S3) → conditional per G7). The de-bias lowered the base multiple from 13.0x to 12.5x and trimmed the bull/strong_bull multiples — a small move, because the base was already near fair value. (Full bridges in `outputs/LNG_scenarios.json`; G1/G4/G5 verified.)

## §3 Three-method valuation reconcile (independent)
- **DCF: ~$225** (only ~6% below spot — the key data point) — 10y DCF on Distributable Cash Flow, WACC 7.36% (beta 1.05 (S4: 5y weekly vs S&P 500); g 2.25%).
- **SOTP: ~$262** — Sabine Pass + Corpus Christi (incl Stage 3) + Marketing, net of debt + CQP minority. Monotonicity holds (G3).
- **Comps: ~$253** — 10.2x FY27E EBITDA $7.8B.
- **Independent weighted fair value ~$244 (~flat vs spot).** All three cluster near spot — LNG is genuinely fairly valued, which is why the de-bias confirms rather than flips.

## §4 Earnings quality (S1: XBRL companyfacts, CIK 0000003570)
**GAAP/non-GAAP parallel (reconciliation: present).** GAAP is non-informational (ASC 815 unrealized derivative MtM; Q1'26 ~$3.5B non-cash net loss vs ~$2.3B Consolidated Adj EBITDA); underwrite on Consolidated Adjusted EBITDA / Distributable Cash Flow (G11 reconciliation present; G12 FCF = OCF − capex, SBC ~0.8% of revenue (S1: XBRL) and immaterial). KPMG clean opinion; no restatement/going-concern. Unchanged by the de-bias — only the multiple anchor changed.

## §5 Risks & §6 Consensus variance
Load-bearing risks (unchanged): global LNG oversupply 2026–28 (JKM toward $7–8/MMBtu), marginal-fee recontracting (~$2/MMBtu vs legacy ~$3), premium-multiple/rate sensitivity, crowded long. The declared downward consensus variance V1 (FY2027 durability + multiple, sizing 2.4pp, S1/S3 evidence) is carried for narrative; **G15/G20 are n_a (Hold)**. The de-bias doesn't change the variance — it just confirms the base sits near fair value.

## §7–§10 Regulatory, positioning, triggers (unchanged from v1)
DOE export pause reversed (adds supply); SPL Expansion FERC/DOE pending; no BIS/OFAC/CFIUS (US exporter). Crowded long (96% Street Buy), short interest ~1.5% float. Triggers: cover/bull on SPL Expansion FID + new SPAs ≥$2.50/MMBtu or FY27 EBITDA ≥$8.0B; bear on FY27 EBITDA guide <$7.0B or a sub-$2.00/MMBtu fee print or JKM–HH <$5/MMBtu for 3 quarters.

## §11 Quant overlay
**Barra factor tags** (match `quant_overlay.factor_tags`): **Quality +1.0**, **Size +1.0**, **Growth +0.8**, **Liquidity +0.4**, **Value −0.2**, **Low-Vol −0.2**, **Momentum −0.3**. **Capacity:** 30-day ADV $470M (S4: 30-day avg); days-to-exit 10/20/30% = 2.7 / 1.3 / 0.9 days. Beta 1.05 (S4: 5y weekly). 6-tail A0 map (shifts sum to zero) in `outputs/LNG_structured.json`.

## §12 Verification
The de-bias re-anchored the base to independent fair value (~$244) and CONFIRMED the Hold — the diagnostic that LNG's v1 Hold was genuine (DCF already near spot), not a spot-anchoring artifact. Programmatic gates **G1–G19 all pass** (G15/G16/G20 N/A: Hold rating, non-bank); see `outputs/LNG_verification_gates.json`. v1 archived: `outputs/archive/LNG_v1_hold/`.
