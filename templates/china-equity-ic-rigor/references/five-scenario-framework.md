# Five-scenario probabilistic framework

## Why five (not three, not seven)

Three scenarios (bear/base/bull) under-resolves: real PM disagreement is between "tail-bear" and "ordinary-bear", and between "ordinary-bull" and "blow-off-bull". Two scenarios collapse those distinctions. Seven scenarios over-resolves: once you're allocating <10% probability mass to each tail, the difference between 5% and 8% is noise, and the table becomes too wide to read in IC.

Five scenarios — 强空 / 空头 / 基础 / 多头 / 强多 — cleanly separates "this is the modal case" from "this is what a tail looks like" on each side. Probabilities typically distribute roughly 5-20-50-20-5 for a strong-conviction view, 10-25-30-25-10 for a low-conviction view.

## Required structure

Every memo's §5 (valuation core) contains a 5-scenario table with these columns:

| Column | Required | Notes |
|---|---|---|
| 情景 | yes | 强空/空头/基础/多头/强多 |
| 概率 | yes | sum to 1.00 (allow ±0.01 rounding display) |
| 一句话叙事 | yes | what world this scenario describes |
| EPS (FY+1 or FY+2) | yes | year must be consistent across rows |
| PE | yes | the PE you're applying in this scenario |
| 目标价 | yes | = EPS × PE, **must actually multiply** |
| 涨跌幅 | yes | vs current price |
| 关键锚点 | yes | which anchor(s) drive this scenario |
| 源标记 | yes | strongest anchor's S-level |

The most-failed gate: 目标价 column not actually = EPS × PE. PMs verify with a calculator. The script `scripts/verify_eps_pe.py` automates this check.

## Probability assignment discipline

Probabilities must reflect:

1. **Anchor strength in each scenario**: a scenario whose narrative depends on S3-S5 anchors should carry less mass than one whose narrative is consistent with S1-S2 trajectories. If 强多 needs an unverified rumor, 强多 probability ≤10%.
2. **Path dependence**: 强多 and 强空 should be reachable only through specific identifiable paths (not just "things go well"). If you cannot describe what would have to happen for 强多 to be realized in 12 months, 强多 probability is too high.
3. **Symmetry check**: |P(强多) − P(强空)| should reflect actual asymmetry of the setup. Symmetric tails for asymmetric situations is lazy.

Common probability mistakes:

- **Anchoring on consensus**: "卖方一致 buy → 多头 +20pp probability" is wrong if your underlying anchors don't support consensus.
- **Tail inflation for narrative drama**: 强多 / 强空 over 15% each on a non-binary stock is rare; usually one tail dominates.
- **Linear ladder (10/20/40/20/10)**: this is the default lazy distribution. The actual distribution should be informed by what anchors you have.

## EPS path discipline per scenario

Each scenario's EPS must be derivable from the bear bridge (or its bull-symmetric equivalent — see `bear-bridge.md`). The reader must be able to:

1. Start from base EPS
2. See which adjustments are applied (named, line-by-line)
3. Land on the scenario EPS

If you cannot show this bridge, the scenario EPS is hand-waving. PMs catch this in the form of "where does EPS ¥0.40 in 强多 come from?" and the right answer is "base ¥0.34 + 面板价格 +6% impact +0.04 + OLED IT mix +¥0.02 = ¥0.40 (S3 IR + S5 Omdia anchored)".

## PE multiple discipline per scenario

Each scenario's PE must be:

1. **Justified by historical range**: cite the multiple's 5-year band (1σ from mean).
2. **Reflective of scenario growth/quality profile**: 多头/强多 PE > 基础 only if growth or ROE differs in that scenario; otherwise applying a higher PE in a higher-EPS scenario is double-counting.
3. **Bound by peer comp at sector level**: within ±20% of sector peer median for that scenario's growth profile.

Common PE multiple mistakes:

- **Same PE in all scenarios**: under-resolves. The PE *should* differ across scenarios because risk premium differs.
- **Higher PE × higher EPS in bull**: only valid if quality / cyclical position differs; otherwise double-counting.
- **Floor PE = 0.5x current PE without justification**: in a true 强空, PE compression is real, but cite the historical analog (e.g. 2018 trough trough PE).

## Scenario narrative ↔ anchor consistency

Each scenario row's "关键锚点" column must list the specific anchors driving it. The narrative must be consistent with those anchors.

Example (BOE 基础 scenario):

| 情景 | 概率 | 叙事 | EPS | PE | 目标价 | 涨跌 | 锚点 | 源 |
|---|---|---|---|---|---|---|---|---|
| 基础 | 50% | LCD TV 平稳; OLED IT 缓启动; B2 投产推迟到 2026Q4 | 0.34 | 13.0 | 4.42 | +0.5% | L1 (S5), L2 (S3), B2 (S3) | mixed S3/S5 → conditional |

The reader can trace: anchors L1+L2+B2 → 叙事 → EPS path → PE band → 目标价. If any link breaks (e.g. EPS ¥0.34 doesn't follow from those anchors), the scenario is incoherent.

## Scenario weighting impact table (mandatory adjacent table)

Right after the 5-scenario table, include the **anchor weighting impact table** (this is what gets challenged in IC):

> "若 [基础] 概率 −10pp, [空头] 概率 +10pp, headline 中位收益从 +0.5% 变 to −1.7%; if 强空 +10pp at 基础 expense, 中位 −5.4%."

Reason: PMs ask "what's the variance of your headline if your probabilities are slightly wrong?" Having this in the doc preempts the question.

## Aggregating to headline

Headline 中位 = Σ(P_scenario × return_scenario)

Headline 区间 = [P10, P90] of the discrete distribution (sort scenarios by return; cumulate probabilities; find 10th/90th percentile).

Note: with 5 discrete scenarios, P10/P90 will land *on* a scenario boundary unless you interpolate. Standard practice in our memos: cite [worst-case return, best-case return] of scenarios within the 10-90 mass, and call out tails separately.

## Scenario probabilities → conviction strength

Map probabilities to a conviction tag for the headline:

| Distribution | Conviction tag |
|---|---|
| 50%+ on one direction (bull or bear), tails balanced | 中度偏[多/空] |
| 35-50% on one direction | 中性轻偏[多/空] |
| Mass split 30-30-30 across base/bull/bear | 中性 |
| One tail >15% | 注意 [tail] 风险 |

The conviction tag flows into the default action:
- 中度偏空 → 减仓 (-25-50%)
- 中性轻偏空 → 持有 (-0-25% nibbling)
- 中性 → 持有
- 中性轻偏多 → 持有 / 不加仓
- 中度偏多 → 加仓 (+25-50%)

Position sizing math is in `position-sizing.md`.

## What a fully-realized 5-scenario table looks like (BOE final)

```
| 情景 | 概率 | 叙事一句话                                   | 2027E EPS | PE  | 目标价 | 涨跌    | 锚点         |
|------|------|----------------------------------------------|-----------|-----|--------|---------|--------------|
| 强多 | 5%   | OLED IT 起量 + LCD 价格 +10%                  | 0.40      | 15  | 6.00   | +43.9%  | L2,L1 兑现   |
| 多头 | 20%  | OLED IT 部分起量 + LCD 价格 +5%               | 0.36      | 14  | 5.04   | +20.9%  | L2 部分兑现  |
| 基础 | 50%  | LCD 平稳 + OLED IT 缓启动 + B2 推迟           | 0.34      | 13  | 4.42   | +6.0%   | mixed        |
| 空头 | 20%  | LCD 价格 -5% + OLED IT 不及预期               | 0.30      | 11  | 3.30   | -20.9%  | L1 反转      |
| 强空 | 5%   | LCD -10% + OLED IT 失败 + 折旧 +¥30 亿        | 0.22      | 9   | 1.98   | -52.5%  | L1+L2 反转   |
                                                                                  P-weighted: +0.5%
```

Verify: each row's PE × EPS = 目标价. Verify: P sum = 1.00. Verify: 涨跌 calculated from current price ¥4.17.
