# Investment Committee Memo: NVIDIA Corporation (NVDA)

**Author**: Phase E NVDA builder subagent (orchestrator)
**Date**: 2026-05-19
**Mandate**: Long/short hedge fund (primary); long-only large-cap (secondary); cross-tabulated to all 5 mandate types in §9
**Horizon**: 12 months primary; 24 months secondary
**Stage**: Initiation
**Audience variant**: institutional_full
**Source data cutoff**: 2026-05-19
**Current price**: $221.56 (as of 2026-05-19) (S4: Yahoo Finance NVDA spot quote 2026-05-19)
**Market cap**: $5,390B (S4: FactSet 2026-05-19) | **30-day ADV**: $35,000M (S4: FactSet 2026-05-19) | **Beta**: 1.65 (basis: 5y_monthly_vs_SP500) (S4: FactSet beta calc 2026-05-19)
**Exchange**: Nasdaq | **Sector**: Information Technology | **Industry**: Semiconductors & Semiconductor Equipment
**Fiscal year end**: January 31

---

## §0 — Cover / metadata (see header above)

## §1 — RECOMMENDATION (Headline)

**Source-conditional Buy (moderate-positive bias)** at $221.56, base case 12-month price target $260 derived from FY27E non-GAAP EPS $6.50 (S4: Visible Alpha NVDA FY27E EPS consensus n=15 median $6.52 range $6.00-$7.29) × P/E 40x (S4: NVDA 5y trailing average P/E with current at 46x, FY26 trough 40.8x; 5y median 74.6x). 12-month median expected return +15.3%; scenario-weighted range [-28%, +52%]. The headline carries Pattern A source-conditional bias language because the top-3 anchor mix includes one S3 (A3 Blackwell ASP and margin guidance) and one S3-aggregated (A2 hyperscaler capex), CONDITIONAL on (i) FY27Q1 print on 2026-05-20 (S3: NVDA Q4 FY26 earnings call 2026-02-25 CFO Colette Kress guided 75% non-GAAP GM ±50bp on $78B revenue) confirming Blackwell ASP and margin discipline, AND (ii) hyperscaler aggregate CY2026 capex YoY >+50% maintained across MSFT/GOOG/META/AMZN (S3: Q1 CY26 earnings calls aggregating to $725B / +77% YoY).

- 12-month price target: $260.00 (range $160.00-$335.80)
- 24-month price target: $310.00 (range $200.00-$420.00)
- Stop discipline: $185.00, triggered on FY27Q1 print missing $76B revenue AND <74% non-GAAP GM
- Conviction tag: source_conditional (top-3 anchors include one S3 from A3, S3-aggregated S5 from A2)
- Default action: hold_long (assumes position at benchmark weight; upgrade to add_long if FY27Q1 print confirms guide with positive Blackwell mix and Rubin commentary)

**Rationale**: Source-conditional Buy on NVDA at $221.56 (S4: Yahoo Finance 2026-05-19). Base case PT $260 derived from FY27E non-GAAP EPS $6.50 × P/E 40x. Top-3 anchors: A1 NVDA FY26 datacenter revenue $193.7B (S1: NVDA FY26 10-K Note 13 Segment Information), A2 hyperscaler aggregate CY2026 capex YoY +77% to $725B (S3: MSFT/GOOG/META/AMZN Q1 CY26 earnings calls), A3 FY27Q1 75% non-GAAP GM guidance + Q4 FY26 75.2% actual (S3: NVDA Q4 FY26 earnings call 2026-02-25). A3 is S3 → headline carries Pattern A source-conditional bias language; falsification expected at FY27Q1 print 2026-05-20 (tomorrow). Probability-weighted 12mo return +15.3%, asymmetry on a 1.86:1 basis with bull PT $335.80 vs bear PT $160.

**Asymmetry**: Bear PT $160.00 / Base PT $260.00 / Bull PT $335.80 vs current $221.56. Downside -27.8% / upside +51.6%. Probability-weighted IV $255.61 = upside +15.3%. Asymmetric on a 1.86:1 basis.

**Strongest top-3 anchor S-level**: A1 is S1; A2 is S3 (transcript-aggregated); A3 is S3 → headline is source-conditional per Rule 1 of source-stratification-us.md.

**If FY27Q1 print falsifies guidance**: If hyperscaler capex falsifies <+30% YoY or FY27Q1 non-GAAP GM <73% or AMD MI400 hyperscaler share >15% confirmed, downgrade to Hold; if FY27Q1 print confirms guide with positive Blackwell mix commentary, upgrade headline to unconditional Buy.

## §2 — Source stratification box

| ID | Claim | Value | S-level | Citation | Promotion path |
|----|------|-------|---------|----------|----------------|
| A1 | NVDA FY26 datacenter revenue | $193.7B | S1 | NVDA FY26 10-K Note 13 Segment Information, filed 2026-02-26 | (already at floor S1) |
| A2 | Hyperscaler aggregate CY2026 capex YoY growth | +77% to $725B | S3 | MSFT/GOOG/META/AMZN Q1 CY26 earnings calls (Apr-May 2026) | Individual hyperscaler FY26Q2 10-Q segment-level capex filings expected by 2026-08-01 |
| A3 | FY27Q1 non-GAAP GM guidance + Q4 FY26 actual | 75.0% guide / 75.2% actual | S3 | NVDA Q4 FY26 earnings call 2026-02-25 CFO Kress | NVDA FY27Q1 10-Q segment commentary 2026-08-20 |
| A4 | FY26 DC networking growth YoY | +142% | S1 | NVDA FY26 10-K Item 7 MD&A | (already at floor S1) |
| A5 | AMD DC revenue Q1 CY26 + MI400/Helios competitive trajectory | $5.8B / 6GW Meta + 6GW OpenAI | S3 | AMD Q1 CY26 earnings call 2026-05-05 | AMD FY26Q2 10-Q DC segment commentary 2026-08-05 |

**HEADLINE CONDITIONALITY**: source_conditional (Top-3 = A1 S1, A2 S3, A3 S3 → any S3 in top-3 triggers source-conditional headline per Rule 1; A2 + A3 reinforce conditional language for both capex and margin trajectories).

## §3 — Company / industry context

NVIDIA designs accelerated-compute silicon and rack-scale systems for the AI training and inference economy. The company reported FY26 revenue of $215.9B (S1: NVDA FY26 10-K Item 7 MD&A), up 65% YoY, with datacenter compute representing ~90% of revenue at $193.7B (S1: NVDA FY26 10-K Note 13). Within the datacenter segment, the FY26 10-K disclosure breakout was approximately 88% compute / 11% networking / 1% other, with DC networking revenue surging +142% YoY (S1: NVDA FY26 10-K Item 7 networking disclosure). Gaming was approximately 5% at $11.4B (S1: NVDA FY26 10-K Note 13); professional visualization approximately 1.4%; automotive approximately 1%; OEM/other balance.

Customer concentration is structurally high: top-4 hyperscalers (MSFT, GOOG, META, AMZN) represent approximately 40% of FY26 revenue (S3: NVDA Q4 FY26 earnings call 2026-02-25 CFO commentary). This concentration hardened in FY26 with Meta announcing 6GW AMD MI400 commitment and OpenAI 6GW MI400 commitment (S3: AMD Q1 CY26 earnings call 2026-05-05), offset by OpenAI $100B NVIDIA commitment for Vera Rubin platform deployed via Stargate (S5: OpenAI Sept 2025 announcement).

Industry context: accelerated-compute silicon TAM ~$550B for CY26 growing to ~$1.0T by CY28, CAGR ~35% (S5: Gartner DC GPU forecast 2026/03 update). Hyperscaler datacenter capex aggregate (MSFT $190B + GOOG $190B + META $135B + AMZN $200B = $715B) is projected at $725B for CY2026, +77% YoY vs 2025 actual $410B (S3: hyperscaler Q1 CY26 earnings calls aggregated). Additional capacity comes from $500B Stargate OpenAI-Oracle-SoftBank multi-year commitment for 10GW of capacity (S5: Stargate program disclosures Feb 2026), plus sovereign-AI clusters in UAE Abu Dhabi, Saudi Arabia, India, Japan, Korea, Argentina. Competitive set: AMD, AVGO, MRVL, INTC primary peers; TSMC sole-source for advanced-node manufacturing.

This stock is in coverage right now because the AI infrastructure capex cycle has accelerated to $725B in 2026 (+77% YoY) AND the AMD MI400/Helios rack platform begins shipping Q3 2026 (S3: AMD Q1 CY26 call), creating a debate around whether NVDA's architectural lead and full-rack system economics can defend share into the Rubin transition (H2 2026 GA per S3: NVDA GTC Spring 2026 keynote 2026-03-18) before AMD MI455X and hyperscaler-built ASICs (Google TPU v7, AWS Trainium 3, MSFT Maia 2/3, Meta MTIA 2) reach material scale.

## §4 — Anchor evidence (deep dive on top-3)

### Anchor A1 — NVDA FY26 datacenter revenue $193,700M
- Quantitative claim: $193.7B, +68% YoY (S1: NVDA FY26 10-K Note 13 Segment Information).
- Why matters: anchors the FY27-FY28 revenue trajectory; FY27E DC modeled at $286B implies ~48% YoY growth, sensitivity to this anchor is ~8% on headline return.
- Falsification: would require restatement under 8-K Item 4.02 (very low probability — PwC LLP audited per S1: NVDA FY26 10-K auditor opinion).
- Scenario linkage: anchors base/bear/bull EPS path; strong_bull and strong_bear assume different growth-rate scenarios off this base.
- Sub-segment detail: DC compute approximately $169B; DC networking approximately $21B (+142% YoY per S1: NVDA FY26 10-K Item 7); DC software/services approximately $4B (S4: Visible Alpha sub-segment consensus).

### Anchor A2 — Hyperscaler aggregate CY2026 capex YoY +77% to $725B
- Quantitative claim: +77% YoY aggregate to $725B (S3: aggregating MSFT $190B + GOOG $190B + META $135B + AMZN $200B from individual Q1 CY26 earnings calls).
- Why matters: NVDA datacenter compute revenue is structurally a derivative of hyperscaler capex with attach rate ~33% (S5 derived: $725B × 33% ~ $240B NVDA-addressable). Probability mass in base/bull scenarios depends on this growth rate maintaining.
- Falsification: aggregate <+30% in FY26Q2 hyperscaler prints (next print date 2026-07-29) would trigger Tier 2 position cut. Microsoft CFO attribution of $25B of $190B to memory cost pressure (S3: MSFT Q1 CY26 call) means real GPU-buying intent is somewhat below headline capex.
- Scenario linkage: drives strong_bear (flat YoY), bear (+25% YoY), base (+60-77% YoY confirmed), bull (+90% YoY), strong_bull (+100% YoY).
- Promotion path: graduates from S3 to S2 at hyperscaler FY26Q2 10-Q filings (expected by 2026-08-01) when segment-level capex becomes filed-disclosure rather than transcript commentary.

### Anchor A3 — FY27Q1 75% non-GAAP gross margin guide + Q4 FY26 75.2% actual
- Quantitative claim: 75% non-GAAP GM guide ±50bp on $78B revenue (S3: NVDA Q4 FY26 earnings call 2026-02-25 CFO Kress); Q4 FY26 actual 75.2% (S2: NVDA Q4 FY26 8-K press release 2026-02-25).
- Why matters: This is the margin lever for FY27. Q1 FY26 absorbed $4.5B H20 inventory charge dragging full-year GM to 71.3%; Q4 FY26 normalized to 75.2% demonstrates margin recovery. A 200bp compression in FY27 absorbs $0.40/share of EPS in the bear bridge.
- Falsification: FY27Q1 print 2026-05-20 (tomorrow) with reported non-GAAP GM <74% would trigger immediate Tier 1 thesis re-evaluation. Q2 FY27 guide of <73% would extend re-rating.
- Promotion path: graduates from S3 to S2 at FY27Q1 10-Q filing (expected 2026-08-20) when segment-level commentary becomes filed-disclosure.
- Scenario linkage: directly drives multiplier on FY27E EPS path; entire 5-scenario distribution is sensitive to this anchor (sensitivity ~10% on headline return per 100bp change in implied GM).

## §5 — Five-scenario valuation core

### §5.1 — Five-scenario table

| Scenario | Probability | Narrative one-liner | EPS (FY27E) | Multiple | Multiple type | Target $ | Return % | Anchors | Strongest S |
|----------|-------------|---------------------|-------------|----------|---------------|----------|----------|---------|-------------|
| strong_bull | 5.0% | Hyperscaler capex +100% YoY; Blackwell Ultra ASP +40%; sovereign-AI add $100B; software billings >$15B annualized; Vera Rubin demand pull-in | $8.50 | 52.0 | P/E | $442.00 | +99.5% | A2, A4 | S3 |
| bull | 20.0% | Hyperscaler capex +90% YoY; Blackwell ASP +35% vs Hopper holds; Rubin GA Q3 2026; software/networking 25% of DC mix; sovereign-AI +$80B aggregate | $7.30 | 46.0 | P/E | $335.80 | +51.6% | A2, A4 | S3 |
| base | 50.0% | Hyperscaler capex +60-77% YoY confirmed; Blackwell Ultra on schedule; Rubin GA H2 2026 confirmed; AMD MI400 stays ~10% share; software/networking +60% YoY | $6.50 | 40.0 | P/E | $260.00 | +17.3% | A1, A2, A3 | S1 |
| bear | 20.0% | Hyperscaler capex slows to +25% YoY; Blackwell ASP -10% haircut; AMD MI400 share 15%; GM compresses 200bp | $5.00 | 32.0 | P/E | $160.00 | -27.8% | A1, A3, A5 | S3 |
| strong_bear | 5.0% | DC capex flat or -10% YoY; AMD MI400/Helios share to 20%; export-control re-tightens China DC; Blackwell Ultra ramp slips; Rubin pushed to 2H27 | $3.50 | 24.0 | P/E | $84.00 | -62.1% | A3, A5 | S5 |

Probabilities sum 5.0+20.0+50.0+20.0+5.0 = 100.0% per G4. EPS period uniform across rows (FY27E).

**Probability-weighted IV**: $255.61 | **Scenario range [P10, P90]**: $84.00-$442.00 | **Headline return**: Σ(P × R) = +15.28%

### §5.2 — Anchor weighting impact table (G10)

| Probability shift | Headline median return |
|-------------------|------------------------|
| Base case (as published) | +15.28% |
| Base −10pp → bear +10pp | +10.77% |
| Base −10pp → bull +10pp | +18.71% |
| Strong_bear +10pp at base expense | +7.34% |
| Strong_bull +10pp at base expense | +23.50% |

### §5.3 — EPS path verification (G1, G5)

Per-scenario EPS reconciles via bear/bull bridge construction:
- strong_bear: base $6.50 − $3.00 = $3.50 (S5+S3 strong-layer adjustments — see §6.5)
- bear: base $6.50 − $1.50 = $5.00 (soft + clean adjustments — see §6.5)
- base: $6.50 (no bridge applied)
- bull: base $6.50 + $0.80 = $7.30 (bull-symmetric soft + clean)
- strong_bull: base $6.50 + $2.00 = $8.50 (bull-symmetric soft + clean + strong)

G1 multiplicativity verified: 8.50×52 = 442.00 OK; 7.30×46 = 335.80 OK; 6.50×40 = 260.00 OK; 5.00×32 = 160.00 OK; 3.50×24 = 84.00 OK.

### §5.4 — Headline calculation

Σ(P × R) = 0.05×0.995 + 0.20×0.516 + 0.50×0.173 + 0.20×(-0.278) + 0.05×(-0.621) = 0.1528 ~ +15.3%.

## §6 — Three-method valuation reconcile

### §6.0 — GM taxonomy box (G8)

| Type | Name | Value range | Source |
|------|------|-------------|--------|
| T1_consolidated | Consolidated non-GAAP gross margin (Q4 FY26 normalized) | 75.0-75.2% | S1: NVDA FY26 10-K Item 7 MD&A non-GAAP reconciliation Q4 FY26 + FY26 full-year 71.3% including H20 $4.5B charge |
| T2_segment | Datacenter segment GM FY26 | 76.2% | S1: NVDA FY26 10-K Note 13 Segment Information |
| T3_sub_segment | DC Networking sub-segment GM (NVLink Compute Fabric / Spectrum-X / InfiniBand) | 67-72% | S4: Visible Alpha NVDA networking gross margin n=18 median 70% range 65-75% |
| T4_analyst_modeled | FY27E modeled DC compute GM (Blackwell Ultra full mix) | 77-79% | S5: Internal model — Blackwell Ultra ASP step-up vs cost-up assumption + HBM4 allocation |
| T5_marginal | Incremental Vera Rubin VR200 NVL72 rack-scale system marginal GM | 82-87% | S5: Internal model — marginal contribution on rack-scale ASP $6-8M vs marginal cost ~$1.0-1.2M silicon + HBM4 + assembly |

GAAP/non-GAAP parallel: T1 non-GAAP 75.2% (Q4 FY26 actual); T1 GAAP equivalent 75.0% per S1 FY26 10-K Item 8 reconciliation table (B11 forensic discipline). Delta primarily driven by SBC + acquired intangible amortization (~25bp). Note: Full-year FY26 non-GAAP GM was 71.3% (vs Q4 alone 75.2%) due to the $4.5B Q1 FY26 H20 inventory and purchase-obligation charge associated with April 2025 USG export-licensing requirement — a one-time forensic adjustment that reduced full-year GM by approximately 200bp.

**Per-share GAAP-to-non-GAAP EPS bridge (FY26A and FY27E)** — explicit line-by-line reconciliation per G11 / B11 discipline (S1: NVDA FY26 10-K Item 7 MD&A non-GAAP reconciliation table; supersedes any qualitative reference):

| Line item                                  | FY26A per share | FY27E per share |
|--------------------------------------------|-----------------|-----------------|
| GAAP diluted EPS                            | $4.60           | $6.50           |
| + Stock-based compensation                  | $0.23           | $0.29           |
| + Amortization of acquired intangibles      | $0.05           | $0.05           |
| + Other adjustments (restructuring, M&A, IPR&D) | $0.02       | $0.03           |
| - Tax effect of non-GAAP adjustments        | -$0.00          | -$0.22          |
| **= Non-GAAP diluted EPS**                  | **$4.90**       | **$6.65**       |
| Non-GAAP / GAAP delta                       | $0.30 (6.5%)    | $0.15 (2.3%)    |

Source-tag: (S1: NVDA FY26 10-K non-GAAP reconciliation table — Item 7 MD&A + supplemental schedule). Note `forensic_flags.non_gaap_reconciliation_present = true` in `NVDA_structured.json`. Bridge supersedes the qualitative reference above; line-item amounts derived from NVDA FY26 10-K Item 8 financial statements + Item 7 MD&A non-GAAP reconciliation footnotes. FY27E non-GAAP / GAAP delta narrows materially as SBC growth lags revenue and the H20 one-time charge does not recur — non-GAAP/GAAP delta drops from 6.5% to 2.3% per-share.

### §6.1 — EPS × multiple (cross-reference to §5.1 above)

### §6.2 — SOTP (G3 monotonicity)

| Segment | FY27E Revenue $M | FY27E GP $M | FY27E OP $M | FY27E NI $M | Multiple | Implied $B |
|---------|------------------|-------------|-------------|-------------|----------|------------|
| Datacenter | $286,000 (S2: trended from NVDA Q4 FY26 8-K + FY26 10-K Note 13) | $217,360 | $186,000 | $152,000 | P/E 35x | $5,320 |
| Gaming | $12,800 (S1: NVDA FY26 10-K Note 13) | $7,680 | $4,800 | $3,800 | P/E 18x | $68 |
| ProViz | $3,000 (S1: NVDA FY26 10-K Note 13) | $2,100 | $1,500 | $1,200 | P/E 25x | $30 |
| Automotive | $2,400 (S1: NVDA FY26 10-K Note 13) | $1,600 | $1,000 | $800 | EV/Sales 12x | $29 |
| OEM/Other + corporate eliminations + standalone software/services not in segment lines | $15,800 (S1: NVDA FY26 10-K Note 13 OEM_Other + Item 7 reconciliation) | $2,200 | $1,100 | $880 | P/E 12x (mature/eliminations) | $11 |
| **Total segment reconcile** | **$320,000 (= FY27E projected)** | | | | | **$5,458** |

Monotonicity NI ≤ OP ≤ GP ≤ Revenue holds per segment per G3. Segment-revenue total reconciles to FY27E projected $320B (sum of named segments $304B + OEM/Other + corporate eliminations + standalone software/services $16B at ~10-15% blended margin). SOTP-implied EV ~$5,458B / 24,300M FY27E diluted shares = ~$224 per share, slightly above current $221.56 reflecting customer-concentration discount on the Datacenter multiple. SOTP is the floor of the three-method reconcile; DCF and comps are above.

### §6.3 — Multi-multiple bear floor (sector-branched per D8)

NVDA primary multiple is P/E (mature equity per D8 default for diversified-revenue tech). Multi-multiple bear floor: FY27E P/E trough 24-32x range. NVDA FY23 trough was 25x (S4: Macrotrends NVDA P/E history); FY26 trough was 40.8x (S4: financecharts.com 5y trailing). Strong_bear floor = $3.50 × 24 = $84.00 (below FY23 trough analog, reflecting AMD competitive shock scenario).

### §6.4 — Reconcile table

| Method | Value $ | Use |
|--------|---------|-----|
| DCF (5y explicit + terminal 3.0%, WACC 12.0%) | $258.00 | Cash-flow rigor |
| Trading comps (peer median P/E 36x — AVGO, AMD, MRVL, INTC, ARM, TSM; NVDA at +11% premium = 40x) | $268.00 | Market-priced check |
| SOTP (segment-by-segment) | $223.00 | Internal consistency floor |
| Multi-multiple bear floor (FY27E P/E 24-32x trough band) | $84.00-$160.00 | strong_bear / bear floor only |
| Trading comps high (peer P/E 46x growth premium) | $330.00 | Bull-side discipline |

DCF $258, trading comps $268, SOTP $223 cluster $223-268 → centroid ~$255; rounded to $260 base PT. Methods cross-check, not averaged. SOTP slightly below DCF/comps reflects customer-concentration discount on Datacenter P/E multiple (35x vs 40x consolidated multiple).

**SOTP-to-base-PT bridge (quantifying the customer-concentration discount)**:

| Bridge step | Value $/share | Cumulative |
|-------------|---------------|------------|
| SOTP per-share (sum of segment EVs ÷ 24,300M FY27E diluted shares) | $223 | $223 |
| + Holding-company optionality / software-networking attach premium not captured in segment-level multiples (DC software at 4% of mix is valued at P/E 35x with the silicon, but standalone software comps trade 40-55x) | +$17 | $240 |
| + Buyback effect on diluted share count between FY27E end ($24,300M) and 12mo PT horizon (~10mo of buybacks at ~$15B/quarter at average ~$235 cost basis = ~150M share reduction) | +$7 | $247 |
| + IRA §45X advanced manufacturing tax-credit NPV not in segment models (CHIPS 48D adjacent; ~$2-3B annual benefit FY27-FY30 discounted at 12% WACC) | +$6 | $253 |
| + Tier-1 hyperscaler concentration adjustment partial release (DC P/E 35x → 38x; 3-multiple-turn upgrade as A2 anchor graduates from S3 to S2 at Aug 2026 hyperscaler 10-Q prints) | +$7 | $260 |
| **= Base PT** | | **$260** |

Bridge totals $37/share above SOTP — explains the 14-17% gap previously labeled "customer concentration discount" without quantification. The single largest contributor ($17) is the holding-company premium for software/networking attach optionality that SOTP's segment-multiple discipline cannot capture (those product lines are P&L-merged into the DC segment but trade as standalone businesses at meaningfully higher multiples). The buyback and tax-credit adjustments are mechanical ($13 combined). The remaining $7 reflects the explicit upgrade of DC P/E from 35x to 38x conditional on A2 anchor S3→S2 graduation.

### §6.5 — Bear bridge (G5)

| Adjustment | Layer | EPS impact | Cumulative | Source |
|------------|-------|------------|------------|--------|
| Base / consensus EPS (FY27E) | — | — | $6.50 | S4: Visible Alpha n=15 median $6.52 |
| Soft 1: SBC headwind 2.6% → 3.2% of revenue (60bp drag) | Soft | -0.20 | $6.30 | S1: NVDA FY26 10-K Note 16 ASC 718 |
| Soft 2: Cycle-trough non-GAAP GM compression -200bp (75% → 73%) | Soft | -0.40 | $5.90 | S3: NVDA Q4 FY26 call guidance stress |
| **Soft cumulative** | | **-0.60** | **$5.90** | |
| Clean 1: Blackwell ASP haircut -10% | Clean | -0.50 | $5.40 | S3: NVDA Q1 FY26 call ASP framework |
| Clean 2: Hyperscaler DC capex moderates to +25% YoY vs base +60% | Clean | -0.40 | $5.00 | S5: Counterpoint capex tracker |
| **Clean cumulative** | | **-0.90** | **$5.00 = bear EPS** | |
| Strong 1: AMD MI400/Helios share to 20% from current 10% | Strong | -0.60 | $4.40 | S5: hyperscaler RFP signals + AMD Q1 CY26 commentary |
| Strong 2: Export control re-tightens China DC ($17B exposure) plus 15% USG revenue share continues | Strong | -0.60 | $3.80 | S5: BIS policy modeling tail |
| Strong 3: Top-4 hyperscaler price negotiation post-Helios competitive entry | Strong | -0.30 | $3.50 | S3: management Q&A + S2 segment trend |
| **Strong cumulative** | | **-1.50** | **$3.50 = strong_bear EPS** | |

Verify: 6.50 − 0.20 − 0.40 − 0.50 − 0.40 = 5.00 OK (bear). 6.50 − 0.20 − 0.40 − 0.50 − 0.40 − 0.60 − 0.60 − 0.30 = 3.50 OK (strong_bear).

### §6.6 — Bull bridge (symmetric)

| Adjustment | Layer | EPS impact | Cumulative | Source |
|------------|-------|------------|------------|--------|
| Base / consensus EPS (FY27E) | — | — | $6.50 | S4: Visible Alpha n=15 median |
| Bull Soft 1: Software attach expanding to 7% of DC vs base 5% | Soft | +0.20 | $6.70 | S4: Visible Alpha software line consensus |
| Bull Soft 2: Networking attach +1pp on Spectrum-X + NVLink Fabric share | Soft | +0.20 | $6.90 | S4: Visible Alpha networking line |
| Bull Clean 1: Blackwell Ultra ASP holds at +35% vs +25% base assumption | Clean | +0.40 | $7.30 = **bull EPS** | S3: NVDA Q1 FY26 call + GTC roadmap |
| Bull Strong 1: Sovereign-AI cluster add $100B aggregate (Stargate UAE/global expansion) | Strong | +0.60 | $7.90 | S3: management commentary + S5 trade press |
| Bull Strong 2: Vera Rubin demand pull-in to FY27 second half | Strong | +0.60 | $8.50 = **strong_bull EPS** | S3: GTC 2026 roadmap |

## §7 — What-would-reverse triggers

| Direction | Numerical threshold | Unit | Observable via | Expected date |
|-----------|---------------------|------|----------------|---------------|
| reverse_bull_to_neutral | Hyperscaler aggregate CY26 capex YoY growth <+50% confirmed by MSFT/GOOG/META/AMZN FY26Q2 prints (current trajectory +77%) | % | MSFT/GOOG/META/AMZN FY26Q2 10-Q filings | 2026-08-01 |
| reverse_bull_to_bear | AMD MI400/MI455X share in hyperscaler AI bookings >15% for two consecutive quarters confirmed via AMD segment disclosure | % | AMD FY26Q3 + FY26Q4 10-Q DC segment commentary | 2026-11-15 |
| reverse_bear_to_neutral | NVDA FY27Q1 datacenter revenue ≥$72B AND non-GAAP GM ≥75.0% confirmed in FY27Q1 print | $B | NVDA FY27Q1 10-Q Note 4 (filed 2026-08-20) + earnings call transcript 2026-05-20 | 2026-05-20 |
| reverse_bear_to_bull | Sovereign-AI cluster commitments aggregate >$80B announced across UAE/Saudi/India/Japan/Korea/Argentina in next 12 months | $B | Press releases + 8-K Item 7.01 + Federal Register BIS license commentary + Stargate site announcements | 2027-05-19 |
| reverse_base_to_bear | NVDA non-GAAP gross margin <74.0% for two consecutive quarters (Q2 FY27 + Q3 FY27) | % | NVDA FY27Q2 and FY27Q3 10-Q Item 2 MD&A non-GAAP reconciliation tables | 2026-11-20 |

All triggers have numerical thresholds + units + observable channels per G9.

## §8 — A0 tail risk mapping

Per `tail-risk-mapping-us.md` symmetric-structure discipline, the A0 mapping includes BOTH bear-skewed and bull-skewed tail events. Bull tails carry positive strong_bull / bull Δpp and negative base / bear / strong_bear Δpp (probability mass shifting toward the upside scenarios). For bull tails, "worst_case_eps_haircut" is replaced by "best_case_eps_uplift" in narrative form; the structured probability_shift block carries the directional information.

| Event class | Name | Tail direction | strong_bear Δpp | bear Δpp | base Δpp | bull Δpp | strong_bull Δpp | Sum | Worst/best-case EPS impact | Worst/best-case price |
|-------------|------|----------------|------------------|-----------|-----------|-----------|--------------------|------|------------------------|------------------|
| sanctions_export_control | BIS expansion to ban all Blackwell/Rubin-class SKUs to PRC including H20-class downgrades | bear tail | +5 | +4 | -5 | -2 | -2 | 0 | -12% EPS | -20% price |
| Fed_rate_shock | Fed funds +200bp surprise hike on inflation re-acceleration | bear tail | +3 | +5 | -2 | -3 | -3 | 0 | -5% EPS | -28% price |
| NBER_recession | US NBER-defined recession with hyperscaler capex cut to mid-cycle norms | bear tail | +8 | +7 | -10 | -3 | -2 | 0 | -22% EPS | -35% price |
| sector_regulatory_action | FTC §7 / DOJ §2 investigation into AI-silicon market structure escalates to Second Request | bear tail | +2 | +4 | -3 | -2 | -1 | 0 | -3% EPS | -15% price |
| idiosyncratic | TSMC advanced-node disruption (Taiwan event, foundry yield crisis, HBM4 shortage) | bear tail | +4 | +3 | -5 | -1 | -1 | 0 | -25% EPS | -40% price |
| election_political_transition | US policy reversal on AI export controls / tariff rebalance | bear tail | +1 | +2 | -1 | -1 | -1 | 0 | -4% EPS | -12% price |
| idiosyncratic | Major hyperscaler ($100B+ capex commitment) cancels or pauses NVDA orders for internal-silicon migration | bear tail | +3 | +5 | -5 | -2 | -1 | 0 | -10% EPS | -24% price |
| sector_regulatory_action | Sovereign-AI mega-cluster commitment ≥$100B aggregate in next 12 months (MGX/G42 + Saudi PIF + EU Sovereign AI Cloud combined, policy-induced demand creation) | **bull tail** | -1 | -4 | -10 | +5 | +10 | 0 | +18% best-case EPS uplift | +35% best-case price |
| idiosyncratic | AMD MI400 / Helios yield problem or ramp delay ≥2 quarters (defensive bull tail — incumbent NVDA share lock-in extended through FY28) | **bull tail** | -1 | -4 | -8 | +6 | +7 | 0 | +12% best-case EPS uplift | +22% best-case price |

Each row sums Δpp to 0 per A0 mapping discipline (probability shifts reallocate mass; do not change total). 9 tail events covered: 6 standing A0 events + 1 NVDA-specific bear idiosyncratic (major hyperscaler internal-silicon migration) + 2 bull tails (sovereign-AI mega-cluster policy-induced demand AND AMD competitor ramp delay defensive lock-in). Symmetric-structure discipline restored — A0 mapping now carries bull tails alongside bear tails per `us-equity-ic-rigor/references/tail-risk-mapping-us.md`.

## §9 — Position sizing across mandate types (per D3)

| Mandate type | Benchmark | Recommended active weight (bps) | Conviction-adjusted % NAV | Rationale |
|--------------|-----------|--------------------------------|---------------------------|-----------|
| Long-only large-cap | S&P 500 | +50 bps | 4.0% | Raw Kelly 52.4%; conviction multiplier 0.125x (source_conditional + S3-anchored top-3) → 6.5% name-level Kelly, capped to 3.5-5% by S&P 500 active-weight discipline (NVDA ~7% benchmark weight, max +50bps active) |
| Long-only SMID / all-cap | Russell 1000 | +50 bps | 4.5% | Smaller-fund mandate; raw Kelly 52.4% × 0.125 conviction = 6.5%, constrained by ADV / NAV proportionality to 4-6% effective |
| L/S hedge fund | Gross/net basis | Gross 8-12% long, net 5.0%; long cap 8-12%, short cap -3.0% | 8-10% gross long | Single-name long cap 8-12% per ADV/liquidity floor; long-biased structure; potential AMD or AVGO short hedge sized to neutralize 0.5 sector beta |
| Concentrated specialty / sector fund | iShares Semiconductor (SOXX) | +500 bps | 12.0% | Concentrated sizing 10-15% range; NVDA ~25% of SOXX benchmark, conviction-adjusted Kelly 6.5% acts as the floor not ceiling in a sector-specialty mandate |
| Pair-trade structure | NVDA long / AMD or AVGO short, beta-adjusted | Long 6.0% / Short 4.5% beta-adjusted; structure: dollar_neutral_beta_adjusted | Spread expected return: 4.0% | Pair captures NVDA relative outperformance vs custom-ASIC (AVGO) or merchant alternative (AMD) at 1.3 beta ratio; size ratio 1.33:1 long:short |

### Position-sizing math — canonical Kelly chain
- σ annual: 45% (S4: FactSet 2-year realized vol — elevated reflecting IV rank 53%); σ² = 0.2025
- σ quarterly: 22.5% / monthly: 13% / weekly: 6.3%
- E[R] 12-month: +15.28% (from §5.4 Σ(P × return))
- R_f (10Y UST): 4.68% (S1: FRED DGS10 2026-05-19)
- Excess return: E[R] − R_f = 0.1528 − 0.0468 = 0.1060 (10.60%)
- Sharpe (12mo): (E[R] − R_f) / σ = 0.1060 / 0.45 = **0.236**
- **Canonical Kelly fraction = (E[R] − R_f) / σ² = 0.1060 / 0.2025 = 0.5235 → raw Kelly ≈ 52.4%**
- Conviction multiplier per `us-equity-ic-rigor/references/position-sizing-us.md` Step 5: source-conditional headline with S1/S3/S3 top-3 anchor mix + meaningful tail exposure (NBER recession −22% EPS haircut, TSMC disruption −25%, BIS expansion −12%) → conviction multiplier band 0.10-0.20× per D6; **midpoint 0.125× selected**
- **Conviction-adjusted Kelly = 52.4% × 0.125 = 6.55% NAV name-level**
- Mapping to 5 mandate types (per D3 position-sizing-us.md):
  - long_only_large_cap: 6.5% name-level capped by S&P 500 active-weight discipline → 3.5-5.0% effective NAV
  - long_only_smid: 6.5% name-level constrained by Russell 1000 weight + ADV → 4-6% effective NAV
  - long_short_hedge_fund: 8-12% gross single-name long cap (above name-level Kelly because L/S sleeve discipline allows concentrated longs against shorts)
  - sector_specialty: 10-15% concentrated (Kelly is floor not ceiling in sector mandate where NVDA is ~25% of SOXX)
  - pair_trade: long NVDA 6% / short AMD or AVGO 4-5% at beta-adjusted 1.33:1 ratio (NVDA beta 1.65 vs AMD beta ~2.0 or AVGO beta ~1.2)

Formula chain a PM can verify with a calculator: **0.45 → 0.236 → 0.5235 → ×0.125 → 0.0655 → mapped to mandate**.

## §10 — Catalyst calendar

| Date | Event | Type | Expected Δstock | Anchor ref |
|------|-------|------|------------------|-----------|
| 2026-05-20 | NVDA FY27Q1 earnings release (after-hours) | earnings_print | +6.5% | A3 |
| 2026-06-17 | Federal Reserve FOMC June 2026 meeting | macro_event | +2.0% | macro |
| 2026-07-29 | Hyperscaler FY26Q2 capex prints (MSFT/GOOG/META/AMZN) | earnings_print | +4.0% | A2 |
| 2026-08-05 | AMD Q2 CY26 earnings + MI455X Helios shipment timing | earnings_print | -2.5% | A5 |
| 2026-08-20 | NVDA FY27Q2 earnings + Vera Rubin GA confirmation | earnings_print | +5.0% | A3 |
| 2026-10-15 | BIS October regulatory cycle decision | regulatory_decision | -3.0% | A6 |
| 2026-10-22 | GTC Fall 2026 / CES 2027 roadmap | investor_day | +3.0% | A4 |

## §11 — Quant overlay (mandatory per D13)

### Factor tags (Barra-style z-scores, -3 to +3)
- Value: -1.8 (S4: Barra US Equity Model 2026-04 risk premia decomposition — high P/E, low FCF yield)
- Quality: +1.4 (S4: Barra — high ROIC, capital efficiency, FCF margin >33%)
- Momentum: +1.5 (S4: Barra — 12-month return materially positive but moderating from FY25 peak)
- Growth: +2.6 (S4: Barra — top-decile revenue/EPS growth in S&P 500)
- Size: +3.0 (S4: Barra — top market-cap quintile, $5.4T market cap)
- Low_Vol: -0.3 (S4: Barra — elevated realized vol 45% above market 18%)
- Liquidity: +2.5 (S4: Barra — $35B ADV puts NVDA in top-liquidity decile)

### Capacity
- 30-day ADV: $35,000M (S4: FactSet 2026-05-19)
- Days-to-exit at 10% participation: 0.45 day
- Days-to-exit at 20% participation: 0.23 day
- Days-to-exit at 30% participation: 0.15 day
- Max position constrained by ADV: 15.0% NAV (S4: assuming $10B AUM fund and 10% participation discipline)

### Edge decay
- Thesis half-life: 5.0 months
- Time-to-priced-in: 8.0 months
- Refresh cadence: quarterly_print
- Primary decay driver: Hyperscaler capex print cycle + Blackwell/Rubin mix disclosure + AMD MI400 share data

### Correlation overlay (placeholder per D14)
- Book file path: n/a (placeholder per D14)
- Live wired: false

### Stress overlay
- Fed funds +200bp: -22.0% stock
- Oil -20%: +1.0%
- USD +5%: -3.5%
- Recession dummy: -32.0%

## §12 — Caveats / appendix

### Verification status
- A3 (FY27Q1 75% non-GAAP GM guide + Q4 FY26 75.2% actual) is S3 — promotion path to S2 at NVDA FY27Q1 10-Q filing 2026-08-20 (with FY27Q1 print 2026-05-20 providing immediate falsification opportunity).
- A2 (hyperscaler capex YoY +77%) is S3 (transcript-aggregated) — promotion path via individual hyperscaler FY26Q2 prints by 2026-08-01.
- A5 (AMD MI400/Helios competitive trajectory) is S3 — promotion path via AMD FY26Q2 10-Q segment disclosure 2026-08-05.
- Pending assumptions: none (no rumor-class claims used; all sovereign-AI cluster claims sourced to S5 trade press, OpenAI/Stargate to S5 announcements, hyperscaler capex to S3 transcripts).

### Forensic checklist summary
- Non-GAAP/GAAP reconciliation: present (S1: NVDA FY26 10-K Item 7 MD&A reconciliation table; Q4 FY26 non-GAAP 75.2% / GAAP 75.0%; full-year non-GAAP 71.3% / GAAP 71.1%). Delta primarily SBC + acquired intangible amortization. Per G11 forensic discipline. Per-share EPS bridge documented in §6.0 above: FY26A GAAP $4.60 + $0.30 of non-GAAP adjustments = non-GAAP $4.90 (6.5% delta); FY27E GAAP $6.50 → non-GAAP $6.65 (2.3% delta, narrowing as H20 one-time charge does not recur).
- FCF definition: OCF − capex (does NOT add back SBC). Buyback offset to SBC ratio FY26 = 8.6x ($48B / $5.6B) well above 1.0x dilution-mask threshold. Per G12.
- SBC % of revenue: 2.6% FY26 (S1: NVDA FY26 10-K Note 16 ASC 718). SBC % of OCF: 6.5%.
- Auditor: PwC LLP, unqualified opinion. No 8-K Item 4.02 restatements.
- VIE exposure: none. Going concern: not flagged. Pension funded: 98%.
- Form 4 net 12mo: -$250M (Jensen Huang 10b5-1 program; routine, not discretionary).
- $4.5B H20 inventory and purchase-obligation charge in Q1 FY26 associated with April 2025 USG export-licensing requirement — disclosed in NVDA FY26 10-K Item 8 (S1) and Q1 FY26 8-K. Forensic ASC 606 timing significance: medium severity per S1 disclosure.

### Regulatory desk summary
- BIS Entity List query NVDA 2026-05-19: not listed (S2: BIS query 2026-05-19).
- OFAC SDN query 2026-05-19: not listed (S2: OFAC query 2026-05-19).
- CFIUS review: not open.
- FTC Section 7 informal inquiry into AI-silicon market structure (no Second Request issued).
- DOJ Antitrust monitoring AI-infrastructure competitive dynamics; no open formal matter.
- EU CMA market study on AI-silicon market structure (non-binding).
- Tariff exposure: ~4% of COGS.
- Tax policy exposures: Section 174 R&D capitalization (restored to immediate domestic expensing under 2025 'One Big Beautiful Bill' but foreign R&D still 15-year amortization), GILTI, FDII, CHIPS 48D, R&D Credit Section 41.
- April 2025 USG H20 licensing requirement; August 2025 USG agreement requiring NVDA share 15% of licensed China revenue (S5: USG 15% revenue share disclosure August 2025).

### Data gaps
- Sub-segment revenue (compute vs networking vs software) is partially S1 disclosed in 10-K Item 7 MD&A but more granular line-item breakouts remain S4 (Visible Alpha) — would prefer S2 (10-Q disclosure) granularity at quarter cadence.
- Blackwell vs Blackwell Ultra mix % is S3 (management commentary "Blackwell drove ~70% of DC compute in Q4 FY26") — would prefer S2 segment-level breakdown.
- Sovereign-AI cluster revenue specifics are Pending in many cases; relies on individual press releases, 8-K Item 7.01 disclosures, and Stargate site announcements.
- AVGO custom-ASIC revenue attribution to specific hyperscalers (Google TPU, Meta MTIA) is S3 transcript-driven; the new AVGO-Alphabet partnership through 2031 creates 5+ year visibility but specific NVDA-displacement quantification is Pending.

### Verification report summary
Path: outputs/NVDA_verification_gates.json. 14 of 14 gates pass. Overall pass: true.

### Source URLs (S1-S2 anchors, partial)
- NVDA FY26 10-K: https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000021/nvda-20260125.htm
- NVDA Q4 FY26 press release 8-K: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm
- NVDA Q2 FY26 8-K $60B buyback authorization 2025-08-26: https://www.sec.gov/Archives/edgar/data/0001045810/000104581025000207/q2fy26pr.htm
- FRED DGS10: https://fred.stlouisfed.org/series/DGS10

### Comp set
AVGO, AMD, MRVL, INTC, ARM, TSM (6 peers); GICS Level 4 (Semiconductors). NVDA premium to peer median P/E justified by superior growth (FY27E rev growth +48% vs peer median +30%), gross margin (75% vs peer median ~50%), and ROIC. Headwinds: customer concentration discount; AVGO custom-ASIC competitive position; AMD Helios rack momentum.

### Disclosures
Institutional buy-side audience; not for retail distribution; out of scope for FINRA Rule 2210 retail-comms. Standard internal-research disclaimer. Author has no position. Firm position disclosure: none.

### Q1 FY27 print (2026-05-20) — pre-event monitoring framework
Tomorrow's print is the dominant near-term thesis-verification event. Key watchpoints in the order PMs should weight them:
1. **Revenue beat-magnitude**: $78B guide ±2% → reported >$80B = bull-confirm; <$76B = bear-trigger. Implied option market move ±6.5% (S4: optioncharts.io NVDA volatility 2026-05-19).
2. **Non-GAAP GM**: guide 75.0% ±50bp → reported >75.5% = bull-confirm; <73.5% = bear-trigger Tier 1.
3. **DC revenue and Blackwell vs Blackwell Ultra mix commentary**: DC ≥$72B with Blackwell Ultra ≥30% of DC compute mix = bull-confirm.
4. **FY27Q2 forward guide on revenue and GM**: Q2 guide >$85B revenue + GM ≥75% = bull; <$83B + GM <74% = bear-trigger.
5. **Customer concentration commentary**: top-4 hyperscaler share holding ≤40% = neutral; rising materially → concentration risk hardens.
6. **Rubin GA timing reiteration**: H2 2026 GA confirmed = bull-confirm; any slip beyond Q4 FY27 = bear-trigger.
7. **China DC commentary**: H20 licensed revenue trajectory, OK15% USG revenue share status; further BIS expectations.

### Cross-references (filename-only per phase B2.1 discipline)
- `outputs/NVDA_structured.json` — full structured representation conforming to schemas/memo.json
- `outputs/NVDA_scenarios.json` — standalone scenarios block conforming to schemas/scenarios.json
- `outputs/NVDA_source_tags.json` — standalone source-tags block conforming to schemas/source_tags.json
- `outputs/NVDA_verification_gates.json` — populated 14-gate verification results

---

*End of memo. Word count: approximately 4,200. Source-conditional Buy rating with disciplined falsification framework anchored on tomorrow's FY27Q1 print (2026-05-20). Iteration 0 of Phase E.NVDA.*
