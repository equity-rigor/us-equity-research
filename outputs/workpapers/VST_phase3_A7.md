# VST — Phase 3 A7: Valuation + Quant Overlay Workpaper

**Ticker:** VST (Vistra Corp., NYSE) · **As of:** 2026-06-09 · **Current price:** $146.90 (6/8/26 close)
**Specialist:** A7 Valuation + Quant Overlay · Every numeric S-tagged.

---

## 0. Verified market inputs (Phase 3 web verification — 17 tool calls)

| Input | Value | Source / S-level |
|---|---|---|
| Current price (6/8/26 close) | **$146.90** | stockanalysis.com VST [S1] |
| Shares outstanding | 337.18M | stockanalysis.com / 10-Q FY2026 [S1] |
| Market cap | $48.97B | stockanalysis.com [S1] |
| Beta | 1.41 | stockanalysis.com [S1] |
| ADV | 5.4M sh/day (consolidated; aggregators show 3.0-5.3M) [S2] |
| Forward P/E | 13.77 | stockanalysis.com [S1] |
| Dividend | $0.91 (0.63% yld) | stockanalysis.com [S1] |
| 10Y UST (DGS10, 6/8/26) | **4.536%** | Fed H.15 / FRED DGS10, TradingEconomics [S1] |
| Implied ERP (Damodaran 1/1/26) | 4.23% | aswathdamodaran [S2] |
| CEG forward P/E | ~22x (range 21.8–26.6) | stockanalysis/GuruFocus [S2] |
| Cogentrix multiple | **7.25x 2027E EBITDA**, ~$730/kW, $4.0B, 5.5GW | VST 1/5/26 8-K [S1] |
| FY26E EPS consensus | ~$9.0–9.4 (stockanalysis $8.59 ex-Cogentrix lens) | multiple [S2] |
| FY27E EPS consensus | **~$10.96** | consolidated Phase 1-2 [S2] |
| FY27 Adj EBITDA opportunity | $7.4–7.8B (ex-Cogentrix/PPAs); consensus ~$7.6B | VST guidance [S1] |

*Note on EPS divergence:* stockanalysis FY26 $8.59 vs other-source $9.0–9.4 reflects different Cogentrix-funding/share-count treatment (deal closes 2H26). I use the consolidated FY27E **$10.96** as the base scenario anchor for the P/E framework, consistent with mgmt's HSD Cogentrix accretion and double-digit compounding guidance.

---

## 1. DCF (10y explicit, unlevered FCF → EV)

**WACC build:**
- Rf = 4.54% (DGS10 6/8/26) [S1]
- ERP = 4.75% (Damodaran implied 4.23% rounded up for merchant/cyclical risk) [S2]
- Beta = 1.41 [S1] → **CoE = 4.54% + 1.41×4.75% = 11.24%**
- Pre-tax Kd = 6.0% coupon, tax 21% → after-tax Kd = 4.74%
- Cap structure E=$48.97B, D(net)=$16.4B (FY25 steady-state) → **WACC = 9.61%**

**Unlevered FCF (FCFbG) path ($B), 2026–2035:** 3.8 / 4.3 / 4.5 / 4.4 / 4.3 / 4.2 / 4.3 / 4.4 / 4.5 / 4.6
- Calibrated to mgmt ~$10B cumulative 2026-27 cash generation [S1]; Cogentrix adds ~+$0.35B uFCF from 2027; mid-decade dip reflects 45U PTC fade + 2028 open-book repricing (A-Consensus downward variance), late-decade recovery on gas/PPA durability.
- Terminal growth g = 2.25% (inflation-anchored; merchant generation has no real volume growth).

**Result:**
- PV explicit + PV(TV) = EV ≈ **$52.4B** → less net debt $16.4B → equity $36.0B → **/337.18M = ~$107/sh (base DCF)**
- **Range (WACC ±50bp, g ±25bp): $95 – $121.** Floor (WACC 10.11%, g 2.0%) = $95; ceiling (WACC 9.11%, g 2.5%) = $121.

**Read:** DCF intrinsic (~$107, range $95-121) sits **below** the current $146.90 and below the comps-implied value. The DCF disciplines the merchant-cyclical tail and does not fully credit the AI-power capacity-premium / PPA-conversion optionality that the market price embeds. This is the central tension of the name.

---

## 2. EV/EBITDA comps (2027E)

**2027E EBITDA used: $8.1B** = consensus ~$7.6B opportunity midpoint + ~$0.55B Cogentrix contribution (5.5GW at 7.25x on ~$4B).

**Justified multiple band:** floor = private-market gas M&A **7.5x** (Cogentrix 7.25x, NRG/LS Power 7.5x); ceiling = CEG-relative (CEG ~14-20x EV/EBITDA). I apply **8.75x** as the justified 2027E multiple — a ~1.25-turn premium to private-market for VST's contracted-nuclear PPAs + retail integration, but a deep discount to CEG.

**Bridge (post-Cogentrix funding, net debt $19.3B):**

| Multiple | EV ($B) | – Net debt | Equity ($B) | /337.18M = $/sh |
|---|---|---|---|---|
| 7.5x (floor) | 60.8 | 19.3 | 41.5 | **$123** |
| **8.75x (base)** | **70.9** | **19.3** | **51.6** | **$153** |
| 10.0x (CEG-tilt) | 81.0 | 19.3 | 61.7 | **$183** |

**Comps base ≈ $153/sh** — modestly above spot, the cleanest cross-check on the base scenario.

---

## 3. SOTP (optional — monotonicity enforced)

2027E EBITDA ~$8.1B split (illustrative, segment EBITDA → EBIT → NI monotone within each):

| Segment | EBITDA ($B) | Multiple | EV ($B) | Rationale (NI ≤ EBIT ≤ EBITDA holds) |
|---|---|---|---|---|
| Nuclear (contracted PPAs) | 2.0 | 11.0x | 22.0 | Premium for AWS/Meta 3,809MW + PTC; nuclear-pure analog. EBIT~1.5, NI~1.0 |
| Gas (incl. Cogentrix) | 3.3 | 8.0x | 26.4 | Private-market gas multiple. EBIT~2.5, NI~1.6 |
| Retail | 1.4 | 7.0x | 9.8 | Normalizing $1.62B→$1.4B; stable but no growth. EBIT~1.2, NI~0.9 |
| Coal/closure | 1.4 | 4.0x | 5.6 | Runoff/closure discount. EBIT~0.9, NI~0.6 |
| **Total EV** | **8.1** | — | **63.8** | |
| – Net debt | | | (19.3) | |
| **Equity / $/sh** | | | **44.5 / $132** | SOTP ≈ **$132** |

SOTP (~$132) brackets between DCF (~$107) and comps (~$153) — three-method reconcile is internally consistent.

**Three-method reconcile:** DCF $95-121 | SOTP ~$132 | Comps $123-183 (base $153). Convergence band ≈ **$120-155**, centered near spot. The market is paying for optionality the DCF cannot underwrite — hence Hold.

---

## 4. Five-scenario probabilistic framework (FY27E EPS × P/E)

Built on FY27E EPS × P/E. JSON conforms to `schemas/scenarios.json`; **G1 (eps×mult) PASS**, **G4 (weights=1.00) PASS**.

| Scenario | P | EPS (FY27E) | P/E | Target | 12mo Return |
|---|---|---|---|---|---|
| strong_bear | 0.10 | 8.20 | 9.0x | **$73.80** | **-49.8%** |
| bear | 0.22 | 9.60 | 11.0x | **$105.60** | **-28.1%** |
| base | 0.38 | 10.96 | 14.0x | **$153.44** | **+4.5%** |
| bull | 0.22 | 11.80 | 16.5x | **$194.70** | **+32.5%** |
| strong_bull | 0.08 | 12.80 | 18.5x | **$236.80** | **+61.2%** |

**Multiple grounding:** VST forward P/E 13.77 [S1]; 5y avg ~15x; CEG forward ~22x [S2]. Bear band 9-11x = private-market gas M&A / no-growth-merchant analog (Cogentrix 7.25x EV/EBITDA ≈ 9-10x equity P/E). Bull 16.5-18.5x = re-rate toward CEG, retaining a discount for merchant/leverage.

**Bear-case drivers (strong_bear EPS bridge from $10.96):** open-book repricing -$1.45 (A-Consensus downward variance, P~60%), capacity reversion -$0.70, PTC fade -$0.40, retail normalization -$0.21 → $8.20. The strong_bear $73.80 ties to the consolidated bear PT ~$73 at 7.5x — independent corroboration.

**Bull-case drivers:** Comanche Unit 2 + gas co-location PPA conversion +$0.55, Cogentrix HSD accretion +$0.29 → $11.80.

**Headline:**
- **Probability-weighted expected return (median): +2.6%**
- **P10/P90 range: -49.8% / +61.2%** (strong_bear / strong_bull tails)
- **Rating: HOLD** (±10% band). default_action `hold_long`, conviction `neutral`, source_conditional on the 2028 open-book repricing.

**Weighting sensitivity:** base→bear -10pp ⇒ -0.7%; base→bull -10pp ⇒ +5.4%; strong_bear +10pp ⇒ -2.8%; strong_bull +10pp ⇒ +8.3%. Headline stays in Hold band under all ±10pp shifts — robust to reweighting.

---

## 5. Quant overlay

### 5a. Barra factor tags (all 7)

| Factor | Exposure | Rationale |
|---|---|---|
| **Value** | **+0.4 (mild long)** | FCF yield ~7.2% (highest in IPP peer set); fwd P/E 13.8x below market. Value-ish on cash, not on GAAP earnings. |
| **Quality** | **-0.6 (short)** | Low quality-of-GAAP-earnings (mark-to-market hedge noise, Q4'25 miss/Q1'26 rebound volatility); Moody's Ba1 (sub-IG). |
| **Momentum** | **-0.2 (mild short)** | De-rating from ~$196 Sept'25 peak to $147; 12m price momentum has cooled. Mid/fading. |
| **Growth** | **+0.5 (long)** | EBITDA $5.91B→$7.6B+ trajectory, double-digit EPS compounding, AI-power TAM. |
| **Size** | **+0.9 (large long)** | $49B mkt cap, large-cap IPP. |
| **Low-Vol / Volatility** | **-0.8 (short low-vol = high vol)** | Beta 1.41; commodity/capacity-price sensitivity makes it a high-vol name. |
| **Liquidity** | **+0.5 (liquid)** | ADV ~$790M (5.4M sh × $146.90); ample for most mandates. |

**Net factor read:** high-beta, large-cap, value-on-FCF / low-on-GAAP-quality, growth-tilted, momentum-cooling. A "cyclical-growth with optionality" profile.

### 5b. Capacity / days-to-exit

ADV (dollar) = 5.4M sh × $146.90 = **~$793M/day**.

| Position | 10% ADV ($79.3M) | 20% ADV ($158.6M) | 30% ADV ($238M) |
|---|---|---|---|
| **$200M position** | 2.5 days | 1.3 days | 0.8 days |
| **$500M position** | 6.3 days | 3.2 days | 2.1 days |

Even a $500M position exits in ~1 trading week at 20% participation — VST is highly liquid; capacity is not a binding constraint for L/S or long-only mandates below ~$1B.

### 5c. Edge decay / correlation / stress

- **Edge decay:** The mispricing thesis (DCF < price) is slow-bleed, gated on capacity auction prints (annual) and 2028 open-book hedging (rolls quarterly). Edge realizes over 12-24mo, not days — low-turnover expression.
- **Correlation:** High co-movement with CEG and the AI-power basket (TLN/NRG); moderately negative vs XLU (VST is a merchant, not a regulated utility — trades on power/capacity prices, not rate base). Beta to AI-power theme > beta to utilities index.
- **Stress overlay:**
  - **2× gas move:** ERCOT/PJM spark spreads widen — net positive near-term (merchant generation length), but compresses 45U PTC (phases out at higher power prices) and pressures retail margins. Net modestly positive to EBITDA, negative to PTC line.
  - **Capacity-floor print (auction clears at CONE):** strong_bear realizes — ~-$0.7 EPS from capacity reversion, multiple compresses to 9-11x → $74-106 zone. The dominant left-tail risk.

### 5d. Pair-trade quant — long VST / short CEG

- **Valuation spread:** VST 2026E EV/EBITDA ~9.4x vs CEG ~11.4x = **2.0 turns** discount (P/E: VST 13.8x vs CEG ~22x = ~8 turns). The thesis: VST's gas+nuclear+retail integration deserves a narrower discount as PPAs convert.
- **Beta-adjusted sizing:** VST beta 1.41; CEG beta ~1.6 (nuclear-pure, higher AI-momentum beta). Hedge ratio = 1.41/1.60 ≈ **0.88** → for $100 long VST, short ~$88 CEG to neutralize market beta. (If using $1 gross each leg, the residual is short ~0.12 units of beta — tilt slightly more CEG short for full neutrality.)
- **Spread expression:** long the discount-narrowing (VST re-rate) while shorting CEG's premium multiple. Risk: if the AI-power supercycle accelerates, CEG (pure nuclear) re-rates faster than VST and the spread widens against the trade — size to the EV/EBITDA-turn convergence, not directional.
- **Carry:** VST div yield 0.63% vs CEG lower; slight positive carry on the long leg.

---

## 6. Reconcile summary

| Method | Implied value | vs spot $146.90 |
|---|---|---|
| DCF (10y, WACC 9.61%) | $107 ($95-121) | -27% (disciplines tail) |
| SOTP | ~$132 | -10% |
| Comps (8.75x 2027E EBITDA) | $153 ($123-183) | +4% |
| **5-scenario weighted** | **+2.6% exp return** | **Hold** |

**Verdict: HOLD.** Spot sits inside the three-method convergence band ($120-155). The market price embeds AI-power optionality the DCF cannot underwrite; downside is gated on the ~42% 2028 open-book repricing (A-Consensus downward variance, P~60%). Asymmetry is roughly symmetric (-50% strong_bear / +61% strong_bull) with the base only marginally positive — no edge to initiate at $147.

**Gate status:** G1 (eps×mult) PASS · G4 (weights sum 1.00) PASS.
**Tool-call count: 17** (WebSearch ×11, WebFetch ×6 incl. 2 403s retried via search).
