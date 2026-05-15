# Tail-risk mapping (A0) — probability shift × valuation impact

## What this solves

Every memo has a "risks" section. The bad version is a generic list ("regulatory risk, customer concentration, technology shift"). The good version says, for each tail event: (1) the trigger that would activate it, (2) how it shifts the 5-scenario probabilities, (3) the resulting headline drift, (4) the worst-case scenario value if the tail crystallizes.

This is the A0 mapping. It belongs in §8 (or wherever risks live) and it pre-empts the IC challenge "what about tail X."

## Required structure

```
| Tail event    | Trigger                                  | Prob shift                                | Δ headline | Worst-case scenario value |
|---------------|------------------------------------------|-------------------------------------------|------------|---------------------------|
| 大客户违约    | 公告披露 ≥X% 违约 / 仲裁                | 强空 +10pp at 基础 expense; 空头 +5pp     | -7%        | 强空 ¥1.98 → -52%        |
| 政策黑天鹅     | 关键产品被列入限制 / 海关重大调整         | 强空 +5pp; 空头 +10pp at 基础 expense     | -4%        | 强空 ¥1.98 → -52%        |
| 技术替代       | 关键客户公开测试替代方案 / 专利诉讼       | 强空 +3pp; 空头 +7pp at 基础 expense      | -3%        | 强空 ¥1.98 → -52%        |
```

## Required dimensions

For each tail event, specify:

### 1. Trigger

What would have to happen for this tail to be considered crystallized? Same discipline as `what-would-reverse.md` — specific source channel + numerical threshold.

### 2. Probability shift across scenarios

This is the core analytic content. The tail event doesn't just "change the probability of bad outcomes" — it **redistributes probability mass between specific scenarios**. The redistribution should:

- Sum to zero (probability conservation)
- Reflect the magnitude of the tail (large tails shift mass into 强空 directly; smaller tails shift into 空头)
- Be the same direction whether it's a bear-tail or bull-tail event

Example for a "大客户违约" tail:
- 强空: +10pp (this is exactly the world it describes)
- 空头: +5pp (cycle deepens)
- 基础: -10pp (no longer modal)
- 多头: -3pp (almost impossible if customer defaults)
- 强多: -2pp
- Sum: 0 ✓

### 3. Δ headline (post-tail expected return)

Recompute Σ(P_scenario × return_scenario) using the post-shift probabilities. The Δ vs current headline is the headline impact.

If current headline is +0.5% and post-tail is -7%, you state the impact as "Δ headline -7.5pp" or just "post-tail headline -7%".

### 4. Worst-case scenario value

If the tail crystallizes and 强空 is realized, what's the price? Cite the 强空 row from the 5-scenario table. This is the "max loss" reference number.

## Asymmetry: bear tails vs bull tails

A complete A0 table has both. PMs especially appreciate explicit bull tails (they keep you from anchoring on bear) — but bull tails are usually harder to model because real upside surprises are non-linear.

```
| Bull tail event      | Trigger                                  | Prob shift                          | Δ headline | Best-case  |
|----------------------|------------------------------------------|-------------------------------------|------------|------------|
| 大客户独家份额扩大    | 公告 / 财报披露 share >Y%                | 强多 +10pp at 基础-多头 expense     | +12%       | 强多 ¥6.00 → +44% |
| 政策强催化           | 国务院/部委指定支持 + 资金落地           | 强多 +5pp; 多头 +5pp                | +8%        | 强多 ¥6.00 → +44% |
```

## Tail count discipline

Memos with 8+ tails listed look unfocused. Best practice:

- 3-5 bear tails (the ones that actually move headline)
- 2-3 bull tails
- Anything more goes into a separate "watching list" annex

The tails should be **identifiable, specific events** — not "macroeconomic downturn" (too broad) but "specific customer announces price cut" (concrete).

## Threshold for inclusion

A tail belongs in A0 if:

- Probability of the trigger ≥3% over 12 months (low-prob is OK, but not noise)
- Δ headline impact ≥3pp (otherwise it's not actually moving the case)
- Identifiable trigger source

If a tail fails any of these, move it to "minor risks" / annex.

## Worked example: 300699 final A0

```
| Bear tail                  | Trigger                                | Prob shift                                  | Δ headline | 强空 |
|----------------------------|----------------------------------------|---------------------------------------------|------------|------|
| Vestas 单一客户大幅减单    | 2026 订单 -30% YoY 公开披露            | 强空 +8pp / 空头 +7pp / 基础 -10pp / 多头 -5pp | -8%       | ¥X   |
| 包头一期大额减值           | 单次减值 ¥Z 亿 (>3 亿)                | 强空 +5pp / 空头 +5pp / 基础 -10pp           | -5%       | ¥X   |
| 复合材料技术替代加速       | 客户公开转向 [替代方案] / 专利败诉    | 强空 +3pp / 空头 +5pp / 基础 -8pp / 多头 -0pp | -3%       | ¥X   |
| Bull tail                  | Trigger                                | Prob shift                                  | Δ headline | 强多 |
| 客户 A 复购量 ≥2024 顶峰   | 2026 营收明显回升                      | 强多 +5pp / 多头 +10pp / 基础 -10pp / 空头 -5pp | +6%       | ¥X   |
| 政策强支持                 | 风电补贴回归 / 海军大单                | 强多 +3pp / 多头 +5pp / 基础 -5pp / 空头 -3pp  | +3%       | ¥X   |
```

Each row: trigger specific, prob shift sums to zero, headline impact computed, worst/best-case from scenario table.

## How A0 connects to position sizing

The A0 table feeds position sizing in two ways:

1. **Range widening**: if A0 has high-impact tails on both sides, the headline range [P10, P90] widens. Position sizing should respect the widened range.
2. **Asymmetric tails**: if bear-tail Δ headline is -8% but bull-tail Δ headline is +3%, the asymmetry argues for smaller position even if base-case return is positive.

Position sizing math see `position-sizing.md`.

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| Generic tails ("regulatory risk", "execution risk") | not actionable |
| Tail listed without prob shift | shows no analytic content |
| Tail prob shifts that don't sum to zero | math error |
| Only bear tails on a bear thesis | asymmetric framework |
| Δ headline not computed | reader can't gauge how much each tail matters |
| 10+ tails | unfocused; signals you don't know which matter |
