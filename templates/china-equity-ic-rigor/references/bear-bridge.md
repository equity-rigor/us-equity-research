# Bear EPS bridge — three-layer construction

## What this solves

PMs do not believe a bear EPS unless they can see, line by line, which assumption did the work. "Bear EPS ¥0.22 because conditions are bad" is not a bear case — it is an opinion. A bear EPS bridge starts at consensus / base EPS, applies a series of named, quantified adjustments, and lands on the bear number. The reader can disagree with any single adjustment and re-do the math.

The three-layer structure (soft / clean / strong) lets the reader see the conviction gradient. Soft layer = adjustments most market participants would accept. Clean layer = adjustments only a few participants make. Strong layer = adjustments unique to your bear thesis. Each layer carries a probability weighting in your scenario distribution.

## Required structure

The bear bridge is a column-form or row-form table:

```
| Adjustment                              | Layer   | EPS impact | Cumulative EPS | Source/anchor       |
|-----------------------------------------|---------|------------|----------------|---------------------|
| Base / consensus EPS                     | —       | —          | 0.34           | S4: Wind n=12       |
| Soft 1: 风电业务 GM −2pp (cycle bottom)  | Soft    | −0.03      | 0.31           | S2: 1Q26 季报趋势   |
| Soft 2: 应收账款减值计提 +0.5%          | Soft    | −0.02      | 0.29           | S5: 行业账期延长     |
| Soft total                              |         | **−0.05**  | **0.29**       |                     |
| Clean 1: 客户 A 价格让步 3-5%           | Clean   | −0.03      | 0.26           | S3: IR + S5: 渠道   |
| Clean 2: 财务费用回升 (利率)            | Clean   | −0.01      | 0.25           | S2: 季报负债结构    |
| Clean total                             |         | **−0.04**  | **0.25**       |                     |
| Strong 1: 包头一期减值 ¥X 亿           | Strong  | −0.04      | 0.21           | S5: 项目进展        |
| Strong 2: 风电客户集中度爆雷           | Strong  | −0.03      | 0.18           | tail event          |
| Strong total                            |         | **−0.07**  | **0.18**       |                     |
| **Bear EPS (强空)**                      |         |            | **0.18**       |                     |
| **Mid-bear EPS (空头, soft+clean only)** |         |            | **0.25**       |                     |
```

## Layer definitions

### Soft layer

Adjustments that are **already in motion or empirically observed in recent reports**. Most market participants would mark to these if asked.

Examples:
- Cycle-trough margin compression for cyclicals when the cycle has clearly turned
- Working capital build when 1Q working capital cycle days have visibly extended
- FX translation hits when CNY has already moved
- Volume mix shift when channel data already shows it

Rule: if a sell-side analyst not constructing a bear case would still mark to this, it's soft.

### Clean layer

Adjustments that are **plausibly coming based on visible inputs but have not yet shown in reported financials**. These are the conviction-adjusted bear case.

Examples:
- Customer concentration risk where the customer has signaled price negotiation but it hasn't hit price yet
- Capacity coming online that will pressure pricing in 2 quarters
- Capex deferral that suggests management losing confidence
- Subsidy rolloff that's been announced but not yet reflected

Rule: 一般卖方不会做这个调整，但如果你给一个 PM 看你的逻辑链他会接受它。

### Strong layer

Adjustments unique to your bear thesis. These are the **non-consensus calls** — where the rest of the market disagrees with you.

Examples:
- Specific asset impairment you forecast that management doesn't acknowledge
- Demand collapse on a structural basis (e.g. share loss to a new competitor)
- Tail events with non-trivial probability (regulator action, lawsuit, key customer loss)
- Quality-of-earnings adjustments that reveal hidden trouble

Rule: this is the layer that justifies *your* bear vs the market's bear. If your strong layer is empty, you don't have a non-consensus view.

## Mapping to scenarios

The three layers map to the 5-scenario distribution (see `five-scenario-framework.md`):

- **基础**: base EPS, none of the bridge applied → probability ~50%
- **空头 (mid-bear)**: base EPS minus soft+clean layers → probability ~20%
- **强空 (deep-bear)**: base EPS minus all three layers → probability ~5-10%

Symmetric construction for bull side: the bear bridge has a mirror — bull bridge — where you start at base and add soft / clean / strong upward adjustments. 多头 = base + soft+clean. 强多 = base + all three layers.

## How PMs challenge a bear bridge

Common PM challenges (and what to be ready for):

1. **"Where does adjustment X come from?"** — every adjustment must have a source tag. If the source is S3-S5, the adjustment is acceptable but the *probability* on that scenario should be lower than if all adjustments were S1-S2.
2. **"Are you double-counting?"** — soft and clean must be mutually exclusive. If "GM −2pp" (soft) already incorporates "customer price pressure", you can't then add "客户 A 价格让步 3-5%" (clean) without showing they hit different lines.
3. **"What's the time horizon?"** — bear EPS for FY+1 vs FY+2 vs FY+3 will differ. Be explicit which year the bridge is computing.
4. **"What about offsetting positives?"** — a bear bridge that ignores known cost-side positives (e.g. raw material tailwind) is one-sided. Either include them or note they're insufficient to offset.

## Worked example: 300699 final bear bridge (FY+2 = 2027E)

```
Base 2027E EPS                                                      ¥0.51 (S4: Wind n=8 mean)
  Soft 1: 风电业务 -10% revenue (cycle pressure)                    -0.05
  Soft 2: 复合材料 GM -1pp (raw material adjusted)                  -0.02
                                                Soft cumulative:    ¥0.44
  Clean 1: Vestas 让价 3-5%                                         -0.04
  Clean 2: 应收减值 +¥X 亿 (账期 +30 天)                            -0.02
                                                Clean cumulative:   ¥0.38
  Strong 1: 包头一期减值                                            -0.04
  Strong 2: 风电客户 集中度爆雷 (tail)                              -0.03
                                                Strong cumulative:  ¥0.31
                                                                      
                                                空头 EPS (soft+clean): ¥0.38
                                                强空 EPS (all):        ¥0.31
```

Verify: 0.51 − 0.05 − 0.02 − 0.04 − 0.02 − 0.04 − 0.03 = 0.31 ✓
Verify: 0.51 − 0.05 − 0.02 − 0.04 − 0.02 = 0.38 ✓

These numbers feed directly into the 5-scenario table EPS column.

## The bear bridge box (mandatory)

Every memo with a meaningful bear case (≥10% probability on 空头+强空) must include the bear bridge as a standalone table in §6.x. It should be visually clear which layer each adjustment sits in (use shading or section breaks).

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| "Bear EPS ¥0.22, 30% lower than base" — no decomposition | unreviewable; PM cannot disagree with anything specific |
| All adjustments lumped together (no layers) | reader can't separate "obvious" from "non-consensus" |
| Strong layer empty (only soft + clean) | you have a market-consensus bear, not a differentiated view |
| Soft and clean overlapping (double-counted) | bridge is mathematically unsound |
| Bear bridge applied to wrong year (e.g., bridge for FY+2 used in FY+1 scenario) | inconsistent time horizon |
| No upside cross-check (only bear bridge, no bull bridge) | one-sided framework biases probability assignment |
