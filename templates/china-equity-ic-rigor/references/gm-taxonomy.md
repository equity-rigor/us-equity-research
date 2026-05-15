# GM taxonomy — five distinct gross margin concepts

## The problem this solves

In a single memo about BOE, you might see "毛利率 8-10%", "毛利率 17-18%", "毛利率 30-35%" all appear within three pages. PMs read this and conclude one of two things: either you're contradicting yourself, or you're sloppy. Both kill the memo.

The reality is that these are three different concepts pointing to three different cuts of the same business. The fix is not to pick one — it's to label them rigorously. This file specifies the five distinct GM concepts you'll encounter, the discipline for using them in a single doc, and the **GM taxonomy box** every memo must contain.

## The 5 GM types

### Type 1: Consolidated GM (合并毛利率)

- 定义: company-level total GP / total revenue, as reported in 利润表.
- 来源: S1 (年报) / S2 (季报).
- 用途: highest-level aggregate metric, useful for tracking trend and comparing to peer at company level.
- 例 (BOE): 2024 合并毛利率 15.5%, 2025E 14-16%.
- 特征: 一个数. 它不告诉你哪个业务在赚钱、哪个在烧钱.

### Type 2: Segment GM (分部毛利率)

- 定义: per-business-segment GP / revenue, as reported in 分部信息附注.
- 来源: S1 (年报附注) / S2 (季报，如披露).
- 用途: 看哪个分部在贡献毛利、哪个在拖累.
- 例 (BOE): 2024 显示器件 17%, IoT 9%, 传感器 19%, 智慧系统 22%.
- 关键约束: **Σ(segment_revenue × segment_GM) / Σ(segment_revenue) 必须 ≈ Type 1 合并毛利率，差异 ≤50bp**. 如果对不上，要么分部数据错，要么有未分配业务（公司层面对内交易、总部费用），需要单独标出.

### Type 3: Sub-segment / product-line GM (业务线毛利率)

- 定义: 某分部内具体产品线的毛利率，公司未必正式披露，多见于 IR 沟通或卖方拆分.
- 来源: S3 (IR) / S4 (卖方拆分) / S5 (行业数据).
- 用途: 解释 segment GM 内部 mix shift，理解 cyclical vs structural.
- 例 (BOE 显示器件分部内): LCD TV 毛利 8-10% (2024), OLED 智能手机 30-35% (2024), OLED IT 模组 待证（卖方拆分）.
- 关键约束: 用作 mix shift 解释，不要拿 sub-segment GM 直接对标 consolidated 给读者看（会引发"毛利率到底是 10% 还是 35%"的认知混乱）.

### Type 4: Analyst-modeled GM (卖方/我方模型毛利率)

- 定义: 卖方或我方 forward 模型对未来期间的毛利率假设，可能落在 segment 或 sub-segment 层级.
- 来源: S4 (卖方一致) / 自有模型.
- 用途: 在 EPS 桥 / scenario 表中作为输入参数.
- 例: 我方 2027E 显示器件分部毛利率假设 17.5% (基础情景), 19% (多头), 14% (空头).
- 关键约束: 必须明确这是 forward modeled，不是历史报告. 用 "假设" / "我方预测" 而不是 "毛利率为".

### Type 5: Marginal GM (边际毛利率)

- 定义: 增量营收的毛利率，通常用于讨论 mix shift 影响 (e.g. 新增 OLED IT 出货的边际毛利).
- 来源: 推导 (S3 IR commentary + S5 行业 + 内部假设) — 几乎从来不是 S1.
- 用途: 解释为什么 Q-on-Q 毛利率变化与 revenue mix 变化方向一致.
- 例: BOE OLED IT 模组边际毛利 25-30% (基于 BOE-V 设备折旧 + 韩国厂占比测算), vs LCD TV 边际毛利 5-8%.
- 关键约束: **永远是测算值不是 reported**, 必须明确标注 "marginal/边际" 字样, 并写明推导路径.

## The GM taxonomy box (mandatory; place near §6.0)

```
| 类型 | 名称           | 范围            | 来源                    |
|------|----------------|-----------------|-------------------------|
| T1   | 合并毛利率      | 14-16%          | S1: 2024 年报           |
| T2   | 分部毛利率      | 9% - 22%        | S1: 2024 年报附注 §X    |
| T3   | 业务线毛利率    | 8-10% / 30-35% | S3: IR / S5: 卖方拆分    |
| T4   | 模型假设毛利率   | 17.5% (基础)    | 自有 forward 假设         |
| T5   | 边际毛利率      | 25-30%          | 推导 (S3+S5)             |
```

读者一眼看清: 8-10% 是 T3 (LCD TV sub-segment), 14-16% 是 T1 (consolidated), 17-18% 是 T2 (显示器件分部), 30-35% 是 T3 (OLED phone). 不再混淆.

## Reconciliation discipline — the segment GM weighted check

每次出现 segment GM 列表 (T2)，必须配套 reconciliation 行：

```
| 分部       | 营收 (¥亿) | 分部 GM | 分部 GP (¥亿) |
|-----------|-----------|---------|--------------|
| 显示器件    | 1,330     | 17%     | 226.1        |
| IoT       | 420       | 9%      | 37.8         |
| 传感器      | 220       | 19%     | 41.8         |
| 智慧系统    | 76        | 22%     | 16.7         |
| **合计**    | **2,046** |         | **322.4**    |
| 隐含合并 GM |           |         | 322.4/2,046 = 15.8% |
| 公司报告    |           |         | 15.5%       |
| 差异        |           |         | 30bp (在 ±50bp 容差内) |
```

If the difference exceeds ±50bp, one of three things is happening:

1. **Segment data is incomplete** — there's an unallocated bucket. Add an "其他/未分配" row explaining what's there (typically internal eliminations, corporate, investment income).
2. **GM figures are mismatched periods** — full-year revenue ≠ full-year GP for some segments (e.g. one is annualized from H1). Fix by aligning periods.
3. **GM figures from different sources/cuts** — e.g. you mixed an S3 IR sub-segment GM into an S1 segment GM list. Fix by re-checking source levels.

If you can't get within ±50bp without forcing it, **you don't understand the segment economics yet**. Stop, re-read the 分部信息附注, ask why.

## How GM types interact in a memo

A typical narrative sequence:

1. Open with T1 (合并 GM) trend — reader gets aggregate context.
2. Decompose into T2 (segment GM) — reader sees mix.
3. Within key segment, explain via T3 (sub-segment GM) — reader sees what's driving.
4. Build forward via T4 (modeled GM) — reader sees your assumptions.
5. Stress-test via T5 (marginal GM) — reader sees sensitivity.

Every sentence with a GM number must implicitly tag which type it is. If the reader has to guess, you've failed.

## Anti-patterns (these will fail PM red-team)

| Anti-pattern | Why wrong | Fix |
|---|---|---|
| "毛利率 8-10%" 不说哪一层 | reader can't tell if T1, T2, or T3 | "LCD TV 业务线毛利率 (T3) 8-10%" |
| Quoting T3 sub-segment GM without showing it sums consistent with T2 | partial picture, may mislead | always pair T3 with the T2 it sits within |
| Using T4 forward GM in same sentence as T1 historical without flagging | reader can't tell what's reported vs assumed | "公司 2024 合并 GM 15.5%; 我方 2027E 假设 (T4) 16.0%" |
| T5 marginal GM presented without derivation | unverifiable | "边际 GM 推导: BOE-V 折旧 ¥X 亿 + IT 模组单价 ¥Y → 边际 ~25-30%" |
| Segment GM × revenue weighted ≠ consolidated, no explanation | broken reconciliation | add 其他/未分配 row OR fix the assumption |

## Worked example: BOE Round 7 fix

Before fix, the memo had:
- "毛利率 8-10%" (intended: LCD TV business line, T3)
- "毛利率 17-18%" (intended: 显示器件 segment, T2)
- "毛利率 30-35%" (intended: OLED smartphone module, T3)
- "公司毛利率 15.5%" (T1)

PM challenge: "Are you saying the consolidated GM is 8% or 18% or 35%? You realize these are all in the same memo?"

Fix: insert §6.0 GM taxonomy box (the table above), then go back through the memo and tag every GM number with its type at first mention. Round 7 score: 8.0 → 8.3.

Round 6 had a related but distinct issue: segment GM × revenue didn't reconcile to T1. We rebuilt the segment GM bridge (LCD 17% / OLED 9% / Sensors 19% / Smart 22% on revenue mix → weighted 15.8%, vs reported 15.5%, within tolerance). That alone moved 7.5 → 8.0.

These two fixes — taxonomy box + segment reconciliation — are the canonical pattern for any cyclical multi-segment industrial.
