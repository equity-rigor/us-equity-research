# Source stratification (S1–S5 + Pending)

## Why this matters

The single fastest way to fail a PM challenge is to put a specific number in a headline anchor without being able to point at where it came from. "The market expects X" / "industry sources suggest Y" gets you killed. Source stratification forces you to grade every number on a 6-level scale and forces the headline language to match the strongest anchor's grade. If your three top anchors are all S3, your headline is *not* "中度偏空 / 默认减仓" — it is "**source-conditional** 中性轻偏多 / 默认持有 (待 [anchors] 兑现)".

This is not pedantry. It is what kept us from publishing a strong directional view on BOE based on three unverified rumors (Apple supply share, OLED IT capacity, BOE-V production date) that all turned out to be S3 IR commentary, not S1 audit.

## The 6 levels

### S1 — audited financials / 经审计年报

- 定义: 经四大或国内 A 类会计师事务所审计的年报、半年报（如审）、招股说明书。
- 例子: 公司 2024 年报营收 ¥X 亿、毛利率 Y%、应收账款周转 Z 天。
- 红队抗压: 最强。可以直接做 headline anchor。
- 仍要核验的事: 表内 vs 附注口径是否一致；非经常损益是否做调整；分部数据是否按事业部一致披露。

### S2 — unaudited public filing

- 定义: 公司公开披露但未经审计的文件 — 季报、月度经营数据公告、投资者关系活动记录表（公开文档）、临时公告、问询函回复。
- 例子: 1Q26 营收 +X% (季报)、设备订单 ¥Y 亿 (公告)、回应交易所问询的细分销量。
- 红队抗压: 较强。可以做 headline anchor 但需要标注 "据 [公告日期] 公告"。
- 注意: 季报口径常常与年报不严格一致 (应计 vs 现金、内部抵消)；月度数据未审。

### S3 — IR commentary / management guidance

- 定义: 公司投资者关系电话会、业绩说明会、分析师交流口径、官方微博/微信公众号披露的细节。包括公司表态但未进入正式公告的指引。
- 例子: "公司表示 2026 年风电业务毛利率回升至 25%"; "据公司 IR 回复，光威风电下半年订单见底"。
- 红队抗压: 弱。**不应单独做 headline anchor**；可以作为 narrative 支撑。
- 默认语言: "据公司表示"、"管理层指引"、"IR 沟通显示"。
- 危险: IR 经常给"区间偏乐观"的口径，特别是周期下行期。把 IR 口径当 fact 是 round-N PM review 必杀。

### S4 — sell-side consensus / broker estimates

- 定义: 卖方分析师覆盖、Wind/Bloomberg consensus、主要券商目标价。
- 例子: "Wind 一致预期 2026 EPS ¥0.34"; "中金目标价 ¥4.50"。
- 红队抗压: 中等，但只能用作**锚点带 (anchor band)** 不能用作点估计。
- 默认语言: "卖方一致预期 X (range Y–Z)"; 必须给出 range 和样本数。
- 危险: 卖方 EPS 在周期顶点系统性偏乐观，在底部系统性偏悲观；用 mean 而不是 median 容易被异常值拖偏。

### S5 — industry data / channel checks

- 定义: 行业协会数据、第三方咨询机构 (Omdia, Counterpoint, IDC, IHS, CINNO, TrendForce 等)、供应链调研、专家电话纪要、海关进出口数据。
- 例子: "Omdia 2026 年 LCD TV 面板出货量预计 +X%"; "供应链反馈苹果 OLED iPad 屏幕份额 BOE 1.4%"。
- 红队抗压: 弱-中。**必须标明数据源 + 不确定带宽**。
- 默认语言: "据 [机构] 数据"; "供应链反馈"; "渠道调研显示 [范围]"。
- 危险: 第三方机构经常彼此打架 (Omdia vs CINNO 对面板出货差 >5%)；供应链调研有 confirmation bias。

### Pending — 未核实

- 定义: 未能溯源、模型截止日之后的具体数字、媒体报道未经公司或第三方独立确认的"消息"。
- 例子: "传 BOE 收购 LGD 广州厂"; "市场预期苹果折叠屏 2027 上市"。
- 红队抗压: 零。**绝不做 headline anchor**。
- 文档处理: 如果必须出现，加 `(Pending — 未核实, 不作为锚点)` 标记。

## Decision rules

### Rule 1 — Headline conditional gate

定义"top-3 anchors"为支撑 headline 方向最强的三个具体数字。

- 三个全是 S1-S2 → headline 可以是 unconditional ("中度偏空 / 默认减仓")
- 任何一个是 S3 → headline 必须是 source-conditional ("中性轻偏空 / 默认持有，待 [anchor] 通过 [核验路径] 兑现升级至 [stronger view]")
- 任何一个是 S4-S5 → headline 给区间不给点估计；情景表写明 "consensus-anchored"
- 任何一个是 Pending → 该 anchor 不进 headline 计算，单独放在 "未核实假设" 段

### Rule 2 — First-use citation gate

每个具体数字（营收、毛利率、份额、产能、客户占比、单价等）**首次出现时必须带源标记**。

格式:
- `(S1: 2024 年报 §3.2)`
- `(S2: 2026-04-15 季报)`
- `(S3: 2026-Q1 IR 沟通)`
- `(S4: Wind consensus, n=12, range 0.30-0.41, median 0.34)`
- `(S5: Omdia 2026/03)`
- `(Pending — not used as anchor)`

### Rule 3 — S3 promotion path

S3 数据可以"升级"成 S2 if:
- 出现在后续公告中 (e.g. 季报披露分部数据印证了 IR 之前的口径) → S2
- 经过两次以上独立来源交叉印证 → S3+ (但仍不到 S2)
- 仅一次 IR 口径未出现在任何正式公告 → 仍是 S3，不能促成 unconditional headline

### Rule 4 — Cross-cutoff verification

对 model knowledge cutoff (May 2025) 之后的具体数字:
- 必须 web search 验证
- 引用至少一个 S1-S2 或权威机构 (Reuters/Bloomberg/官方)
- 找不到独立验证 → 降级为 Pending

### Rule 5 — Strongest-link, not weakest-link

S1-S2 数据**不会被** S3-S5 的相邻数据拖累。例: 营收 S1 + 毛利率拆分 S3 → 整体毛利率 S1 (营收口径), 分部毛利率 S3 (拆分口径)。两者可以共存于同一文档，分别标注。

## Source-conditional headline language patterns

When top-3 anchors include S3 or weaker, use these patterns:

### Pattern A — "Source-conditional [bias]" (when overall direction is moderate but key anchors are weak)

> "**Source-conditional 中性轻偏多 / 默认持有**。本意见的中位预期收益 +0.5% 假设 [anchor1: S3]、[anchor2: S3]、[anchor3: S5] 均在未来 [timeframe] 内向 S2 升级。若任一锚点在核验中证伪，下调至 [revised view]。"

### Pattern B — "若…则" (when the directional view is conditional on a specific event)

> "**基础情景中性偏空（中位 -3%）；若 4Q26 OLED IT 出货占比经季报披露 ≥10%，则升级至中性轻偏多。**"

### Pattern C — "Conditional on [audit-equivalent]" (when waiting for an upcoming filing)

> "本意见以 1Q26 季报口径为基础。9 月半年报披露后将 [specific anchors] 升级至 S2 并重估意见。"

### Pattern D — Confidence-interval headline (when consensus-anchored)

> "12M 中位预期收益 +0.5%，情景加权区间 [-2%, +3%]，**该区间下沿由 S4 卖方一致 EPS ¥0.34 (range 0.30-0.41) 决定**；若实际 EPS 落在 25% 分位 (¥0.31) 以下，下沿移至 -8%。"

## Worked examples from the actual memos

### 300699 case (final round)

Top-3 anchors: 风电业务收入下滑 -X% (S1: 2024 年报), 碳梁出口客户集中 (S2: 2024 招股 §业务集中风险), Vestas 份额 (S5: 行业调研)

→ 因为含一个 S5，headline 给了 source-conditional 区间 [-15%, -3%]，中位 -12.4%；不写"目标价 ¥X" 而是写 "12M 中位 ¥35.53, 区间…"

### BOE case (final round)

Top-3 anchors: L1 LCD TV 价格弹性 (S5: Omdia + 公司表态混合), L2 OLED IT 份额 (S3: IR), B2 BOE-V 投产时点 (S3: IR)

→ 三个全部 S3-S5，整篇用 Pattern A. Headline: "Source-conditional 中性轻偏多 / 默认持有 / 中位 +0.5% / 区间 [-2%, +3%]"

这就是为什么 BOE 不能写"中度偏多" — 锚点强度根本不支持。

## Anti-patterns (will fail PM red-team)

| Anti-pattern | What's wrong | Fix |
|---|---|---|
| "市场预期 EPS ¥0.34" 没有源 | unsourced consensus claim | "Wind 一致 EPS ¥0.34 (n=12, range 0.30-0.41) (S4)" |
| "公司毛利率有望回升至 18%" | wishful + no source | "公司 IR 表示 2027 毛利率目标 17-18% (S3); 卖方平均 16.2% (S4)" |
| "据传苹果新机型采用 BOE 屏" | unsourced rumor in headline thesis | 移到 "未核实假设" 段; 标 Pending; 不进 valuation |
| "目标价 ¥4.50" with all S3 anchors | over-precise on weak anchors | 改区间 + 加 conditional 语言 |
| 公司年报营收 + 卖方 EPS 混合做点估计 | mixing source levels into a single number | 分别标注；如果用合成口径，标 "blend (S1 营收 + S4 EPS path)" |

## Source stratification box (insert near top of every memo)

每份意见书前 2 页内必须有一个表，列出 top-5 anchors + 它们的源等级 + 是否升级路径已识别。模板见 `templates/opinion-letter-section-checklist.md` §2。
