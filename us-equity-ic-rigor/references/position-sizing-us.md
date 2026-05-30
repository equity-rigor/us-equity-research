# Position sizing — vol math, Sharpe, Kelly, conviction adjustment, mandate translation (US)

## What this solves

A memo that ends with "recommend reduce" without specifying *how much* is half a memo. PMs need to know: 25 bps active weight? 200 bps? Out entirely? Long $10M and short $5M? The answer comes from a chain that connects scenario distribution → expected return + variance → Sharpe → Kelly → conviction-adjusted position → mandate-specific action.

Per **D6**, we use **conviction-adjusted Kelly**, not raw Kelly. Raw Kelly is mathematically optimal under perfectly known distributions, which is never the case in equity research. Conviction adjustment scales position by how much we trust our scenario probabilities — typically 0.10× to 0.50× Kelly. Per **D3**, we express the result across **five mandate types**.

Position sizing hooks **gate G14** (capacity / ADV / days-to-exit) and informs **G13** (factor exposure) via the quant overlay. Both must be present in every institutional memo per **D13**.

## Step 1 — Expected return and volatility from scenarios

Using the 5-scenario table per `five-scenario-framework-us.md`:

```
E[R]   = Σ(P_i × R_i)
Var[R] = Σ(P_i × (R_i − E[R])²)
σ      = √Var[R]
```

Worked example (NVDA illustrative, returns vs current price):

```
| Scenario      | P    | R       | P × R    | R − E[R]  | (R − E[R])²  | P × (R − E[R])² |
|---------------|------|---------|----------|-----------|--------------|-----------------|
| Strong Bull   | 10%  | +44.0%  | +4.40%   | +29.5%    | 0.08703      | 0.00870         |
| Bull          | 25%  | +28.0%  | +7.00%   | +13.5%    | 0.01823      | 0.00456         |
| Base          | 35%  | +12.0%  | +4.20%   | -2.5%     | 0.00063      | 0.00022         |
| Bear          | 20%  | -10.0%  | -2.00%   | -24.5%    | 0.06003      | 0.01201         |
| Strong Bear   | 10%  | -42.0%  | -4.20%   | -56.5%    | 0.31923      | 0.03192         |
| Sum           | 100% |         | +9.40%   |           |              | 0.05741         |
```

E[R] = **+9.4%** (12-month expected return)
σ = √0.05741 = **24.0%** (12-month vol)

Probabilities are illustrative; real scenario weighting follows the five-scenario discipline.

## Step 2 — Time-scaling vol

Annual σ → other horizons (assumes IID-like log returns over the horizon):

```
σ_quarterly = σ_annual / √4   = σ_annual / 2
σ_monthly   = σ_annual / √12  ≈ σ_annual / 3.46
σ_weekly    = σ_annual / √52  ≈ σ_annual / 7.21
```

For NVDA example with σ = 24.0%:
- Quarterly 1σ = 12.0%
- Monthly 1σ = 6.94%
- Weekly 1σ = 3.33%

Embed this in the memo so the reader knows the noise floor when evaluating short-term moves.

## Step 3 — Sharpe ratio

```
Sharpe = (E[R] − R_f) / σ
```

**R_f for US**: 10Y UST yield from FRED `DGS10`, verified daily (per `valuation-discipline-us.md`). Typical R_f at writing was ~4.3%.

For NVDA (E[R] = 9.4%, σ = 24.0%, R_f = 4.3%):
- Sharpe = (9.4% − 4.3%) / 24.0% = **0.21**

This is a modest Sharpe — institutional buy-side typically wants Sharpe ≥0.5 at the name level before considering it a primary book position. NVDA at this level qualifies as a satellite or tactical position, not a core long.

## Step 4 — Raw Kelly

```
Kelly_full = (E[R] − R_f) / σ²
```

For a normal-ish distribution this gives the position size that maximizes long-run geometric growth. It is wildly aggressive under favorable conditions and (importantly) **goes negative when E[R] < R_f** — indicating a short or zero allocation.

For NVDA: Kelly_full = (9.4% − 4.3%) / 0.0574 = **0.089 ≈ 8.9% of NAV**.

For a bearish thesis where E[R] = −8%, σ = 28%: Kelly_full = (−8% − 4.3%) / 0.0784 = −1.57 → strongly negative, indicating short bias.

## Step 5 — Conviction adjustment (per D6)

Raw Kelly assumes perfect knowledge of E[R] and σ. We never have that. Apply a conviction multiplier:

| Scenario probability source                                                 | Conviction         | Multiplier  |
|-----------------------------------------------------------------------------|--------------------|-------------|
| All top-3 anchors S1-S2, multi-cycle data                                   | High               | 0.50×       |
| Mix of S1-S3, recent data only                                              | Medium             | 0.25–0.35×  |
| S3-S5 dominant, source-conditional headline                                 | Low                | 0.10–0.20×  |
| Heavy tail exposure per `tail-risk-mapping-us.md` (asymmetric Δ headlines)  | Reduce further     | × 0.5× of above |

**Source-conditional headline σ inflation**: when the memo headline is source-conditional, the σ computed from the scenario distribution **understates** true uncertainty because the scenario probabilities themselves are conditional on anchor verification. Inflate σ by **1.2–1.5×** before computing Kelly to reflect this anchor-verification uncertainty.

For NVDA (medium conviction — A1 is S1, A2 is S5 with dispersion, A3 is S3 transcript; source-conditional headline; tail-risk asymmetry meaningful per A0 table):
- Base multiplier: 0.25× (S1-S3 mix)
- Tail discount: × 0.5 (asymmetric A0, bear aggregate −24pp vs bull +15pp)
- Final conviction multiplier: **0.125×**
- σ inflation: ×1.3 → adjusted σ = 31.2% → adjusted σ² = 0.0974 → adjusted Kelly_full = (9.4% − 4.3%) / 0.0974 = **0.052**
- Conviction-adjusted Kelly = 0.052 × 0.125 = **0.65% of NAV** — still modest.

This is the **name-level Kelly**; mandate-specific caps and capacity then re-shape it.

## Step 6 — Translation to action by mandate type (per D3)

Per **D3**, every IC memo expresses sizing across five mandate types. The mandate determines the cap and the relevant benchmark.

### Mandate type 1 — Long-only large-cap (benchmark: S&P 500)

- Active weight in basis points vs S&P 500 weight.
- `max_weight_pct_nav` typically 3-7% for a high-conviction single name; mandate concentration limits often cap at 5%.
- Example: NVDA at ~6% of S&P 500. Conviction-adjusted Kelly 0.65% → active weight = +0.65pp = **+65 bps overweight** vs benchmark. In NAV terms, hold NVDA at ~6.65% (benchmark 6.0% + active 0.65pp).
- If conviction were higher (Kelly 4%), active weight would cap at +400 bps but mandate ceiling could constrain to +250-300 bps.

### Mandate type 2 — Long-only SMID (benchmark: Russell 3000 or Russell 1000/2000)

- Active weight vs Russell benchmark weight.
- Typically 1-5% of NAV for a single name (smaller absolute size; more capacity-constrained).
- ADV constraint is more binding: a $300M ADV name caps absolute dollar exposure for any fund >$5B.
- Example for a SMID name with NVDA-equivalent conviction: active weight +50-150 bps subject to ADV cap.

### Mandate type 3 — L/S hedge fund (no single-stock benchmark; gross/net exposure)

- Single-name long cap typically **5-10% of NAV** at cost; 12-15% at market (cushion for the long working).
- Single-name short cap typically **2-5% of NAV** (higher hurdle because of borrow + asymmetric loss tail).
- Gross exposure target 150-200%, net 30-80%.
- Example: NVDA at Kelly_adj 0.65% in a 150% gross / 50% net L/S fund → single-name long at ~6-7% of NAV (5× the long-only equivalent because of leverage), with a paired short on a beta-correlated peer (AMD, AVGO) at 2-3% to harvest the relative-value alpha and neutralize sector beta.

### Mandate type 4 — Sector-specialty (benchmark: sector ETF, e.g. SOXX for semis)

- Active weight vs sector ETF weight.
- Can run more concentrated: 5-15% of NAV for a single name is normal at sector funds (concentration is the value proposition).
- Example: NVDA at ~25% of SOXX. Conviction-adjusted positions might be 15-30% of NAV — but mandate concentration limits and SEC diversification rules cap.

### Mandate type 5 — Pair trade (benchmark: pair spread)

- Long ticker + short ticker with explicit neutrality structure.
- Structures: **dollar-neutral** (equal $ on each leg), **beta-neutral** (β-weighted dollar), **value-neutral** (book-value-weighted), **ratio** (units-based).
- Example: long NVDA / short AMD (1.3 NVDA : 1.0 AMD beta-neutral). Sizing: 4% NAV long NVDA, 3% NAV short AMD (beta-weighted). Expected spread return harvested if NVDA outperforms AMD on relative-value or share-gain thesis.

## Capacity constraint per G14 — ADV and days-to-exit

**G14** requires `quant_overlay.capacity` fields populated and the recommended position size respected.

`schemas/memo.json` `quant_overlay.capacity` requires:
- `adv_30d_usd_m` — 30-day average daily dollar volume
- `days_to_exit_10pct_participation`, `_20pct`, `_30pct`
- `max_position_constrained_by_adv_pct_nav`

Formula: `days_to_exit = (position_size_usd) / (adv_usd × participation_pct)`.

Common participation thresholds (avoid market impact):
- **10% of ADV** — passive, no impact
- **20% of ADV** — moderate impact
- **30% of ADV** — meaningful impact; reserved for forced liquidation

Examples:

- **NVDA**: ADV ~$30 B → a $1B fund holding 5% (=$50M) exits in <1 day at 10% participation. **Not capacity-constrained**.
- **SMID-cap $400M ADV** (e.g. a mid-tier SaaS): a $5B fund holding 1% (=$50M) exits in 1.25 days at 10% participation. **Manageable**.
- **Thin-trade $50M ADV**: a $5B fund holding 1% (=$50M) exits in 10 days at 10% participation. **Capacity-binding** — cap absolute dollar exposure such that days-to-exit ≤5 at 10% participation; this often forces position below name-level Kelly.

Rule per G14: any position where `days_to_exit_10pct_participation` >5 days must explicitly state the capacity cap and the implied days-to-exit at each of 10% / 20% / 30% participation. PMs need this for portfolio-level risk-budget reporting.

## Factor exposure (G13) and conviction discount

Per **G13** and `quant_overlay.factor_tags`, each memo must declare Barra-style factor exposures (Value, Quality, Momentum, Growth, Size, Low-Vol, Liquidity) on a -3 to +3 z-score scale.

**Why this matters for sizing**: a name with concentrated factor exposure (e.g., NVDA at peak in 2023-2024: high Momentum, high Growth, low Quality on FCF-yield basis, mega Size, low Liquidity-risk) accumulates **factor crowding risk**. In a factor-aware mandate (most institutional book-aware funds), conviction should be discounted when the name is **already a factor crowd** because the marginal position adds little factor-orthogonal alpha and is exposed to factor-reversal events (e.g., 2022 Momentum crash).

Conviction discount for factor crowding:
- Single factor with |z| >2.0: discount conviction multiplier by 0.7×
- Two factors with |z| >1.5: discount by 0.6×
- Three or more factors with |z| >1.5: discount by 0.5×

NVDA at writing (per the canonical fixture in `quant-overlay-us.md` §"7 Barra-style factors"): Momentum +1.8, Growth +2.5, Size +3.0, Liquidity +2.0, Quality +1.2, Value −1.5, Low-Vol +0.2. Four factors with |z| > 1.5 (Momentum +1.8, Growth +2.5, Size +3.0, Liquidity +2.0) — well above the 3-factor threshold → conviction multiplier additionally × 0.5. Stacked on the prior 0.125× → **0.063×**. Conviction-adjusted Kelly = 0.052 × 0.063 = **0.33% of NAV**. **Cross-doc consistency (G18, v0.3.0)**: any memo using this skill must keep the Barra z-scores consistent between the structured `quant_overlay.barra_factor_tags` block in `memo.json` and any Markdown narrative reference, within ±0.2 tolerance. Pre-v0.3.0 versions of this file carried divergent NVDA values (Momentum +2.3 / Growth +2.0 / Size +2.5 / Liquidity +0.5) which contradicted `quant-overlay-us.md`; reconciled as of v0.3.0 to the canonical set.

## Re-sizing triggers

Position size is not static. Re-evaluate when:

- Any top-3 anchor graduates from S3 to S2 (per `source-stratification-us.md`) — upgrade conviction multiplier by one notch.
- Any A0 trigger fires per `tail-risk-mapping-us.md` — re-compute headline, σ, Kelly.
- Realized return moves >1σ_monthly without thesis change — capture the gain or cover the loss (do not let position drift).
- A what-would-reverse milestone per `what-would-reverse-us.md` is met or missed — flip the thesis, re-size.

Tie each re-sizing trigger to a dated event on the catalyst calendar (per `monitoring-framework-us.md`).

## Required memo content for sizing section

A memo with full position sizing has:

1. **σ + horizon-scaled vol** — annual / quarterly / monthly / weekly 1σ. Reader gets noise floor.
2. **Sharpe** — single number for risk-adjusted return at headline horizon, with R_f base disclosed.
3. **Raw Kelly + conviction multiplier rationale** — why we're using e.g. 0.125× rather than 0.50×.
4. **σ inflation for source-conditional headlines** — if applied, disclosed.
5. **Factor crowding discount** — if applied, disclosed with factor z-scores.
6. **Conviction-adjusted Kelly** — single number, % NAV.
7. **Mandate-specific translation** — all five mandate types with specific bps / NAV % / pair structure.
8. **Capacity disclosure** — ADV, days-to-exit at 10/20/30%, max constrained position.
9. **Re-sizing triggers** — tied to anchor verification milestones and A0 events.

## Sample disclosure language for memo

> "**Position sizing.** 12M σ = 24.0% (Q 12.0% / M 6.9% / W 3.3%). E[R] = +9.4%; Sharpe = 0.21 (vs FRED DGS10 R_f 4.3%). Raw Kelly = 0.089 (8.9% NAV). Source-conditional headline σ inflation ×1.3 → adjusted σ² = 0.097, adjusted Kelly = 0.052. Conviction multiplier 0.125× (S1-S3 anchor mix per Source Stratification box; heavy A0 tail asymmetry per §8 — × 0.5 tail discount). Factor crowding discount × 0.5 (Momentum +1.8, Growth +2.5, Size +3.0, Liquidity +2.0 per §11 Quant Overlay; four factors above |z| = 1.5 threshold). **Conviction-adjusted Kelly = 0.33% NAV**.
>
> **By mandate:**
> - Long-only large-cap (S&P 500): +33 bps active weight (NVDA at ~6.33% NAV vs ~6.0% bench).
> - Long-only SMID (Russell 1000): +60 bps active vs ~5.5% bench → 6.1% NAV; ADV not binding.
> - L/S HF: 2.5% NAV long, paired with 1.5% NAV short on AMD (1.3:1 beta-neutral).
> - Sector-specialty (SOXX): +200 bps active (12% NAV vs 25% benchmark — underweight despite long, because benchmark is concentrated).
> - Pair trade: long NVDA / short AMD, dollar-neutral 3% gross each leg.
>
> **Capacity (G14):** ADV $30B → at 10% participation, $1B fund 5%-NAV position exits in <1 day. Not capacity-constrained.
>
> **Re-size triggers:** (i) FY26Q1 10-Q DC segment commentary confirming Blackwell mix ≥40% upgrades conviction to 0.20× → re-size by +50% from current 0.125×. (ii) Hyperscaler aggregate FY26 capex falsifies <+10% → flip thesis, re-size to short / zero. (iii) BIS rule expansion per A0 fires → immediate trim per `monitoring-framework-us.md` Tier 1."

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| "Recommend reduce" with no specific % or bps | Unactionable; G14 fails |
| Kelly without conviction adjustment | Over-aggressive vs real-world uncertainty; ignores D6 |
| Same Kelly for source-conditional vs unconditional headlines | Conviction not respected; σ understated |
| Skipping vol disclosure | Reader cannot gauge noise floor |
| Sharpe quoted without R_f base | Not reproducible; verify against FRED DGS10 |
| No re-sizing triggers | Position becomes stale without observable update path; monitoring framework fails |
| Position size with no capacity check | G14 fails; cannot size thin-trade names responsibly |
| Single mandate type only | Violates D3 — every memo expresses across five mandates |
| Same active weight regardless of mandate | Ignores benchmark weight differences; SMID name in long-only large-cap is materially different sizing problem than in sector specialty |
| Factor exposure stated but not used in sizing | G13 + sizing decoupling; PM cannot tell book-level integration |
| ADV cap not disclosed for thin-trade names | Cannot liquidate at thesis-break; downside opacity |
