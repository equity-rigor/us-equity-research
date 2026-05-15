# What-would-reverse — falsification triggers with denominators

## What this solves

Every directional view (bear, bull, neutral) needs an explicit falsification condition. Without it, the view is unfalsifiable opinion. With a vague one ("if margins recover"), it's still unfalsifiable — "recover" has no value. The discipline is:

> A trigger that survives PM challenge has a **measurable signal**, a **numerical threshold**, a **observation window**, and an **action mapping**.

## Required structure

Each memo's §7 (or equivalent) contains a "What would reverse this view" table:

```
| Signal              | Source channel       | Threshold (denominator)    | Window     | Action if hit               |
|---------------------|----------------------|----------------------------|------------|-----------------------------|
| 4Q seg GM (T2)      | 1Q26 季报附注         | ≥18.5% on revenue ≥¥X 亿   | by 4/30/26 | Upgrade base from 中性偏空  |
|                                                                                                                  |
|                       to 中性偏多, headline +5%; cap further sell at      |
|                                                                                                                  |
|                       current weight                                       |
| OLED IT 出货占比     | 半年报分部 + 公司表态   | ≥10% / 季                  | by 9/30/26 | Upgrade L2 anchor S3→S2;   |
|                                                                                                                  |
|                       weight 多头 +10pp at 基础 expense; +5% headline       |
```

Not every entry is identical — but every entry must have all four elements (signal / source / threshold / window / action).

## What makes a good trigger

### Specific source channel

Not "if the company beats" — what report? Annual? Quarterly? Pre-announcement? Investor day? You need to specify the *exact* document or call where the signal appears.

### Numerical threshold (denominator)

This is the most-failed gate. "If margins recover" → fail. "If 4Q segment GM ≥18.5%" → pass. The threshold should be:

- A **specific number** (≥18.5%, not "improvement")
- Tied to a **denominator base** when applicable ("18.5% on revenue ≥¥X 亿" — because GM at low volume is meaningless)
- **Observable from public sources** — not "if management says so internally"

### Observation window

When does the trigger expire? "By 1Q26 results release" / "by 9/30/26 if half-year results show". An open-ended trigger lets you delay action indefinitely.

### Action mapping

What specifically do you do when the trigger hits? Not "rethink view" — *what* rethink? This must specify:

- Which scenario probabilities shift, and by how many percentage points
- What the new headline becomes
- What position action you take (cap sell / start nibbling / re-enter / cut)

## Symmetric construction (both directions)

If your view is bear, you need bull triggers (what would force you to abandon bear). If your view is neutral, you need both. If your view is bull, you need bear triggers.

A bear-only trigger table on a bear thesis is asymmetric and looks like bias. The discipline of writing the "what would force me to give this up" trigger is what keeps you from anchoring on your view.

### Bear thesis: bull triggers required

> "If 1Q26 segment GM ≥18.5% AND volume ≥¥X 亿, then thesis is broken. Action: cover any remaining short / cap further sell, re-rate to base, prepare framework for 中性偏多 if 半年报 confirms."

### Bull thesis: bear triggers required

> "If OLED IT 季度出货占比 maintains ≤6% through 4Q26, OR if Apple OLED 屏占比 confirmed <2%, action: downgrade to neutral, cut position by 30%."

### Neutral thesis: both required

> "Upgrade trigger: [...]. Downgrade trigger: [...]."

## Tiered triggers (most informative pattern)

Single-threshold triggers are coarse. Tiered triggers map signal magnitude to action magnitude:

```
| Signal level     | Threshold              | Action                                                |
|------------------|------------------------|-------------------------------------------------------|
| Confirming bear  | seg GM <13% any 季    | hold or extend short                                  |
| Mild reversal    | seg GM 13-15.5%       | cap further sell; observe 1 more quarter              |
| Strong reversal  | seg GM 15.5-18%       | cut bear position 50%, reassess weights               |
| Full reversal    | seg GM ≥18% on volume | exit bear, prepare to flip                            |
```

This is more informative than a single trigger and easier to operationalize.

## Trigger denominator gotchas

A common failure: triggers with implicit denominators. Three patterns:

1. **GM without volume base**: "GM ≥X%" can be hit by collapsing low-margin volume rather than expanding margin. Fix: "GM ≥X% on revenue ≥Y."
2. **Yoy growth without base**: "Revenue growth ≥10%" off a depressed base may not signify strength. Fix: "Revenue growth ≥10% AND absolute revenue ≥Y 亿."
3. **Margin without product mix**: "Segment GM ≥17%" can be hit by mix shift to a non-strategic high-margin product. Fix: "Segment GM ≥17% AND OLED IT 出货占比 ≥X%."

## Worked example: 300699 final triggers

```
| Signal                       | Source                      | Threshold                                      | Window     | Action                                              |
|------------------------------|-----------------------------|------------------------------------------------|------------|-----------------------------------------------------|
| Vestas 续约                  | 公司公告                    | 2027 续签且单价不低于 2024 水平 −3%            | 4/30/27   | Cap further sell; re-rate to 基础-空头 boundary    |
| 风电业务收入                 | 1Q27 季报                   | YoY +5% AND 绝对值 ≥¥X 亿                      | 4/30/27   | Cut bear position 30%; weights 基础+5pp/空头-5pp   |
| 应收账款周转天数             | 半年报附注                  | <120 天 (vs 当前 168)                          | 9/30/27   | Cap any further sell; reassess Customer A          |
| 包头一期减值                 | 任何公告                    | 单次减值 ≥¥X 亿 (公开)                         | open       | Confirm bear; weights 强空 +5pp                     |
```

Reader can: (a) see exactly what to look for, (b) know where to look, (c) measure when it happens, (d) act.

## Worked example: BOE final triggers (神性 source-conditional)

Because BOE's headline was source-conditional (top anchors S3-S5), the triggers prioritize **anchor verification** alongside fundamental signals:

```
| 信号                           | 来源                         | 阈值                                             | 窗口        | 行动                                       |
|--------------------------------|------------------------------|--------------------------------------------------|-------------|--------------------------------------------|
| L1 LCD 价格弹性 (mix)         | 半年报 + Omdia 月报         | LCD TV ASP YoY ≥-3% on 出货量稳定               | 9/30/26    | L1 anchor S5→S3+; +2% headline             |
| L2 OLED IT 季度出货占比        | 季报分部                    | ≥10%                                            | 4/30/27    | L2 anchor S3→S2; +5% headline              |
| B2 BOE-V 投产时点              | 公司公告                    | 投产 ≤2026Q4 AND 1Q27 出货 ≥X 万平               | 4/30/27    | B2 anchor S3→S2; 基础 prob +5pp           |
| 苹果 OLED iPad 屏占比          | 供应链 + 公司表态            | ≥3% 经第三方机构 (Omdia/CINNO) 确认             | 12/31/26   | 多头 prob +5pp; 强多 prob +2pp            |
| Apple Watch / iPhone 屏占比   | 供应链                       | 显著进展（>当前份额）                            | 9/30/26    | 多头 prob +3pp                             |
```

Note the anchor-verification triggers ("L2 anchor S3→S2") — these directly tie to whether the source-conditional headline can be unconditionalized. This is the BOE-specific pattern.

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| "If conditions improve" | unmeasurable; what is "conditions"? |
| "If margins recover to historical" | which historical? what specific number? |
| Threshold without source channel | reader can't verify when it's hit |
| Single trigger covering 12 months with no gradient | binary; doesn't match how information arrives |
| Action = "reassess" | not actionable; what does reassess mean? |
| Bear thesis with no bull triggers (or vice versa) | asymmetric; looks like bias |
| Denominator missing (GM without volume base) | trigger can be hit in bad way and look like good signal |
