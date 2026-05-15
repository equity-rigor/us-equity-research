# IC debate script — template

Use as starting template for `<ticker>_IC_Debate_Script_<author>.docx`. Replace bracketed placeholders. Keep timing markers.

---

# [Ticker] [Company] — IC 报告 (谷泓毅)

**仓位建议**: [action] | **信号倾向**: [conviction tag] | **12M 中位**: [%] | **当前价**: ¥[price]

---

## 第 1 段 (2 分钟) — 公司基本面

[Company] 是 [一句话定位 — what does the company do, in plain Chinese]. 主要业务分 [n] 个分部:

1. [分部1] (营收占比 X%) — [1 句话角色]
2. [分部2] (营收占比 Y%) — [1 句话角色]
...

**核心争论点**: [是什么让这只股票值得 IC 时间 — 即"why now"]

---

## 第 2 段 (1 分钟) — 研究方法

我用了 5 情景概率框架 (强空/空头/基础/多头/强多), 加 3 估值法 reconcile (EPS×PE 主, SOTP 一致性核验, 多倍数 floor).

源等级: 我标注的核心锚点 [n] 个, 其中 S1-S2 [m] 个, S3-S5 [n-m] 个 → **headline 为 [conditional / unconditional]**.

如果 PM 想看具体源, 我每个数字第一次出现都带源标记 (S1/S2/S3/S4/S5).

---

## 第 3 段 (3 分钟) — 逻辑链 (anchor → scenario → headline)

我的核心逻辑是这样:

**锚点 1**: [name] (S[level]) → 这告诉我们 [implication]
**锚点 2**: [name] (S[level]) → 这告诉我们 [implication]
**锚点 3**: [name] (S[level]) → 这告诉我们 [implication]

把这三个锚点带入 5 情景:

- 强多 (P=[X]%, EPS [Y], PE [Z], 目标 [P]): [一句话 condition]
- 多头 (P=[X]%, ...): ...
- 基础 (P=[X]%, ...): ...
- 空头 (P=[X]%, ...): ...
- 强空 (P=[X]%, ...): ...

加权 = [%]. 区间 [low%, high%]. 这是 headline.

---

## 第 4 段 (4 分钟) — 锚点证据 (deep dive 强论据)

**锚点 1 — [name]**:
- 数据: [number with source]
- 解读: [why this matters specifically]
- 风险: [what would prove this wrong]

**锚点 2 — [name]**:
[同样三段]

**锚点 3 — [name]**:
[同样三段]

---

## 第 5 段 (2 分钟) — 估值

EPS × PE 法: 基础 [EPS] × [PE] = ¥[price]
SOTP 法: 分部加总 = ¥[price] (cross-check, [agree/disagree by X%])
多倍数 (强空 floor): [P/B] = ¥[X], [EV/EBITDA] = ¥[Y], [FCF] = ¥[Z], 范围 [low, high]

→ 采用 EPS × PE 主, SOTP/多倍数 cross-check. headline ¥[price] / [%].

---

## 第 6 段 (1 分钟) — 警告 / 何时改变看法

什么会让我改变看法 (numerical denominators):

1. [Trigger 1]: [specific number + window] → [action]
2. [Trigger 2]: [specific number + window] → [action]
3. [Trigger 3]: [specific number + window] → [action]

A0 tail 风险:
- [Bear tail]: 概率 [%], headline 影响 [-%]
- [Bull tail]: 概率 [%], headline 影响 [+%]

---

## 第 7 段 (1 分钟) — 建议 + 仓位

**建议**: [action with %]

具体: σ_annual = [X%] / Sharpe = [Y] / Kelly = [Z%]; 由于 [conviction reasoning], conviction multiplier = [m×]; 调整后 [action].

如果 IC 决定上仓位, 我建议 sizing [n%]; 如果决定不动, 默认 [hold/cut/add].

---

## Q&A 准备 (8 个 likely challenges)

### Q1: [最有可能的 PM 第一问 — 通常是质疑核心锚点]
**A**: [accept what's valid + redirect to data]

### Q2: [质疑概率分布]
**A**: [explain why this distribution given anchors]

### Q3: [质疑 EPS path / 桥]
**A**: [walk through bridge]

### Q4: [质疑 PE 假设]
**A**: [cite historical band + scenario logic]

### Q5: [比较 sell-side consensus]
**A**: [where you agree, where you don't, why]

### Q6: [What about competitor X / industry trend Y]
**A**: [direct answer + show you've considered]

### Q7: [Tail event question]
**A**: [point to A0 mapping]

### Q8: [Position sizing — too aggressive / too conservative]
**A**: [point to conviction multiplier rationale]

---

## 时间长度备选

- **3 分钟版**: §1 (1 min) + §3 + §5 + §7 (compressed) — 仅 PM 问"give me the gist"
- **5 分钟版**: §1 + §2 + §3 + §5 + §7 — full logic chain without deep dive
- **10 分钟版**: 全部 §1-§7
- **15 分钟版**: 全部 §1-§7 + Q&A bank

---

## 演讲提示 (presenter notes)

- **不要 hand-wave 关键数字** — 如果 PM 抓到一个不能立即对号入座的数字, 信任度断崖
- **被挑战时不要防御** — 接受 + 重定位. "你说得对, 这个是 S3, 所以我标了 source-conditional headline"
- **如果不知道答案就说不知道** — "这个我没数据, 我会会后查并 follow up"
- **声音节奏** — 锚点段落慢一点 (这是要被 IC 记住的); 估值段落可以快 (技术性强)
