# Position sizing — vol math, Sharpe, Kelly, conviction adjustment

## What this solves

A memo that ends with "建议减仓" (recommend reduce) without specifying *how much* is half a memo. PMs need to know: 25%? 50%? Out entirely? The answer comes from a chain that connects scenario distribution → expected return + variance → Sharpe → Kelly → conviction-adjusted position. This file specifies that chain.

We use **conviction-adjusted Kelly**, not raw Kelly. Raw Kelly is mathematically optimal under perfectly known distributions, which is never the case in equity research. Conviction adjustment scales position by how much you trust your scenario probabilities — typically 0.25× to 0.5× Kelly.

## Step 1: Compute expected return and volatility from scenarios

Using the 5-scenario table (see `five-scenario-framework.md`):

```
E[R] = Σ(P_i × R_i)
Var[R] = Σ(P_i × (R_i - E[R])²)
σ = √Var[R]
```

Worked example (BOE final scenarios, returns vs current ¥4.17):

```
| Scenario | P    | R       | P×R      | R - E[R]  | (R-E[R])²  | P×(R-E[R])² |
|----------|------|---------|----------|-----------|------------|-------------|
| 强多      | 5%   | +43.9%  | +2.20%   | +43.4%    | 0.1884     | 0.00942     |
| 多头      | 20%  | +20.9%  | +4.18%   | +20.4%    | 0.0416     | 0.00832     |
| 基础      | 50%  | +6.0%   | +3.00%   | +5.5%     | 0.00302    | 0.00151     |
| 空头      | 20%  | -20.9%  | -4.18%   | -21.4%    | 0.0458     | 0.00916     |
| 强空      | 5%   | -52.5%  | -2.63%   | -53.0%    | 0.2809     | 0.01405     |
| Sum      |      |         | +2.57%   |           |            | 0.04246     |
```

E[R] = 2.57% (12-month expected return)
σ = √0.04246 = 20.6% (12-month vol)

Wait — this gives a different number from BOE's headline +0.5%. The difference is because BOE's actual scenario probabilities and returns differ; the example above is illustrative. The discipline is the same.

## Step 2: Time-scaling vol

Annual σ → other horizons:

```
σ_quarterly = σ_annual / √4 = σ_annual / 2
σ_monthly   = σ_annual / √12 ≈ σ_annual / 3.46
σ_weekly    = σ_annual / √52 ≈ σ_annual / 7.21
```

For BOE example with σ = 20.6%:
- Quarterly 1σ = 10.3%
- Monthly 1σ = 5.95%
- Weekly 1σ = 2.86%

Embed this in the memo so the reader knows the noise floor for evaluating short-term moves.

## Step 3: Sharpe ratio

```
Sharpe = (E[R] - R_f) / σ
```

R_f for A-shares, use the 1Y AAA corporate yield or the 10Y CGB depending on convention. Typical R_f at writing was ~2.5%.

For BOE example (E[R] = 2.57%, σ = 20.6%, R_f = 2.5%):
- Sharpe = (2.57% - 2.5%) / 20.6% = 0.003

Note the very low Sharpe — that's the BOE neutral case. For 300699 (bear), expected return was -12.4%; Sharpe was strongly negative.

## Step 4: Raw Kelly

```
Kelly_full = (E[R] - R_f) / σ²
```

For a normal-ish distribution this gives the position size that maximizes long-run geometric growth. It's wildly aggressive when conditions are favorable, and (importantly) goes negative when E[R] < R_f.

For BOE example: Kelly_full = (2.57% - 2.5%) / 0.0426 = 0.016 ≈ 1.6% allocation. (Tiny — because expected return barely above risk-free.)

For 300699 with E[R] = -12.4%, Kelly_full is strongly negative, indicating a short or zero allocation.

## Step 5: Conviction adjustment

Raw Kelly assumes perfect knowledge of E[R] and σ. We never have that. Apply a conviction multiplier:

| Scenario probabilities source | Conviction | Multiplier |
|---|---|---|
| All anchors S1-S2, history rich, multi-cycle data | High | 0.5×  |
| Mix of S1-S3, recent data only | Medium | 0.25–0.35× |
| S3-S5 dominant, source-conditional headline | Low | 0.10–0.20× |
| Heavy tails, A0 events with non-trivial probability | Reduce further | × 0.5× of above |

Final position = Kelly_full × conviction multiplier.

For BOE (low conviction, source-conditional, heavy tails): Kelly_adjusted = 0.016 × 0.15 = 0.0024 ≈ 0.2% allocation. In practice this rounds to "trivial position" which translates to "default 持有" for an existing holder — i.e., do nothing aggressive.

For 300699 (medium conviction, bear thesis with S1-S2 anchors): Kelly_adjusted is negative ≈ -2-5%, which translates to "default 减仓" for an existing long.

## Step 6: Translation to action

Map conviction-adjusted Kelly to a specific action:

| Kelly_adj         | Action for existing long | Action for fresh entry |
|-------------------|--------------------------|------------------------|
| +5% to +15%      | 加仓                     | 建仓 5-15%             |
| +1% to +5%       | 持有 / 不加              | 小仓位 1-5%            |
| -1% to +1%       | 持有 (中性)               | 不建仓                  |
| -5% to -1%       | 持有 / 小幅减仓           | 不建仓                  |
| -15% to -5%      | 减仓 25-50%               | 不建仓 / 短              |
| < -15%            | 大幅减仓 / 离场           | 短                      |

The exact thresholds are specific to fund mandate. The discipline is to translate, not to skip.

## Required memo content

A memo with full position sizing has:

1. **σ + horizon-scaled vol** (annual / quarterly / monthly / weekly 1σ) — gives reader sense of noise floor
2. **Sharpe** — single number for risk-adjusted return at headline horizon
3. **Kelly + conviction multiplier rationale** — why we're using e.g. 0.15× rather than 0.5×
4. **Final action** — specific % position adjustment
5. **Re-sizing triggers** — when to revisit the size (typically tied to anchor verification milestones from `what-would-reverse.md`)

## Sample disclosure language for memo

> "**仓位建议**: 12M σ ≈ 20.6% (季度 10.3% / 月 5.95% / 周 2.86%). E[R] +2.57%, Sharpe ≈ 0.003 (vs 1Y AAA R_f 2.5%). 由于核心锚点 (L1/L2/B2) 三个均为 S3-S5 等级，conviction multiplier 取 0.15×；调整后 Kelly ≈ 0.2% (trivial)。**默认持有，不加仓不减仓**。再评估触发: 1Q26 季报披露 OLED IT 出货占比 ≥10% / 半年报 LCD 价格弹性印证 (L1)，任一兑现升级至 conviction 0.25×。"

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| "建议减仓" with no specific % | unactionable |
| Kelly without conviction adjustment | over-aggressive in real conditions |
| Same Kelly for source-conditional and unconditional headlines | conviction not respected |
| Skipping vol disclosure | reader can't gauge noise floor |
| Sharpe quoted without R_f base | not reproducible |
| No re-sizing trigger | position becomes stale without observable update path |

## Volatility note for conditional headlines

When a memo has source-conditional headline, the σ from scenario distribution **understates** true uncertainty because it doesn't include anchor-verification uncertainty. Practical adjustment:

- Inflate σ by 1.2-1.5× for source-conditional headlines
- Or add a "headline branching" outer scenario where unconditional bull / unconditional bear branches each have their own scenario tree

The latter is cleaner but adds a doc-level table. The former is a quick adjustment.
