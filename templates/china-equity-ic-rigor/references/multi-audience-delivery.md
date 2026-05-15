# Multi-audience delivery — institutional / IC pre-read / IC debate / retail

## What this solves

A single memo cannot serve four audiences. The institutional version is too dense for IC pre-read. The pre-read is too compact for verbal debate. None of them are usable for retail. The pattern is: build the institutional version first as the **single source of truth**; derive the others. **Numbers must match across all four**; only language compresses.

## The four versions

### Institutional version (full, 12-section)

The full memo. ~25-40 pages. Audience: PM, sector specialist, IC committee for deep prep.

Format: docx with structured tables, full source citations, all gates passing.

Naming: `<ticker>_投资意见书_<author>.docx`

Sections (see `templates/opinion-letter-section-checklist.md` for full list):
1. Headline
2. Source stratification box
3. Company / industry context
4. Anchor evidence
5. Five-scenario valuation
6. Three-method reconcile + bear bridge + GM taxonomy
7. What-would-reverse triggers
8. A0 tail mapping
9. Position sizing
10. Catalyst calendar
11. Caveats
12. Appendix

### IC pre-read (concise, ≤4 page)

For IC committee pre-meeting reading. ~3-4 pages. Audience: PM committee members reviewing 10+ memos before IC.

Format: docx, light tables, dense prose, no appendix.

Naming: `<ticker>_精简版_<author>.docx`

Required content:
- Headline (1 paragraph)
- Source stratification box (kept; this is what they'll challenge)
- Five-scenario table (kept; with all columns)
- Three-method reconcile (kept; in compact form)
- Bear bridge (kept; layered)
- What-would-reverse triggers (kept; ≤6 entries)
- A0 tails (kept; ≤6 entries)
- Position sizing (kept; with action)

Removed:
- Industry context narrative
- Anchor evidence build-up
- Catalyst calendar
- Appendix

Discipline: **no number changes from institutional**. If you find a number wrong while building pre-read, fix institutional first, then re-derive pre-read.

### IC debate script (verbal-form)

For IC presentation. Audience: presenter (you) standing in front of committee.

Format: docx with timing markers, talking points, Q&A bank.

Naming: `<ticker>_IC_Debate_Script_<author>.docx`

Required structure:
1. **Company fundamentals** (2 min) — what does the company do, why does this matter, what's the setup
2. **Research methodology** (1 min) — anchors used, source levels, scenario framework
3. **Logic chain** (3 min) — anchor → scenario → headline, walked through verbally
4. **Anchor evidence** (4 min) — specific numbers, source citations, conviction
5. **Valuation** (2 min) — three-method reconcile result + headline number
6. **Caveats / what would reverse** (1 min) — denomination
7. **Recommendation + position** (1 min) — specific action

After each section, list 2-3 likely PM challenges with prepared answers. The Q&A bank should cover ~8 challenges total, sorted by likelihood.

Use **timing markers** at section starts (3 min / 5 min / 10 min variants if presenter wants flexibility).

### Retail / 非专业版 (zero-jargon)

For individual investors, family members, or non-finance professionals. Audience: someone who doesn't know what EPS is.

Format: docx, narrative prose, zero formula language.

Naming: `<ticker>_零售版_投资意见书_<author>.docx` + `<ticker>_零售_对话Script_<author>.docx`

The retail version has TWO docs:
- The opinion letter equivalent (no jargon)
- A Q&A script anticipating typical retail questions ("现在能买吗?", "国家会扶持吗?", "卖方都给买入,你和他们谁对?")

## Translation glossary (institutional → retail)

This is the lookup that drives the retail version. The full glossary is in `templates/retail-translation-glossary.md`. Selected entries:

| Institutional term | Retail translation |
|---|---|
| 减仓 -25% | 卖一部分 (大约四分之一) |
| 中位预期收益 -12.4% | 平均来说股价大概率下跌 12% 左右 |
| 情景加权区间 [-15%, -3%] | 几种可能性按概率平均，多数情况股价下跌 3% 到 15% |
| 锚点 (anchor) | 关键事件 / 关键信号 |
| σ (volatility) | 这只股票一般起落多大 |
| Sharpe | 风险调整后回报，越高越值得做 |
| Kelly | 用数学公式算出该投多少 |
| EPS × PE | 公司每股能赚多少 × 市场愿意给多少倍 |
| 源等级 S1 | 公司年报里写的 (最可信) |
| S2 | 公司公告里写的 (可信) |
| S3 | 公司在投资者会议上说的 (中等) |
| S4 | 卖方分析师说的 (有偏差) |
| S5 | 行业研究机构说的 (有偏差) |
| Pending | 还没核实的 (不能依赖) |
| Source-conditional 中性轻偏多 | 我倾向看好但前提是几个关键消息要兑现 |
| 默认持有 | 你已经买了的话，先不要动 |
| 默认减仓 | 你已经买了的话，建议先卖一部分 |

## Common retail Q&A patterns

The retail Q&A script should anticipate ~15 of these:

- "现在能买吗?"
- "为什么不能买? (or 为什么我应该买?)"
- "中位 -12% 是什么意思? 一定会跌吗?"
- "卖方都说买入, 你和他们谁说得对?"
- "国家会扶持这个行业吗? 政策会救它吗?"
- "[名分析师/基金经理] 都买了, 我能跟着买吗?"
- "我已经买了, 怎么办? 现在卖晚了吗?"
- "我不卖会怎样?"
- "[竞争对手] 怎么样?"
- "你是不是太悲观/乐观了?"
- "如果我什么都不做会怎样?"
- "明天能涨吗?"
- "未来 1 年最坏会怎样?"
- "有没有内部消息?"
- "我应该多关注什么?"

For each, the answer should:
1. Stay zero-jargon
2. Map to the institutional finding
3. Caveat appropriately ("我不能保证, 这是基于现有信息的判断")
4. Direct to actionable behavior

## Building order

The right order is:

1. **Institutional first** (Phases 0-4 of SKILL.md)
2. **Lock institutional**: passes all gates, scores 9.0+
3. **IC pre-read** (compress; verify numbers identical)
4. **IC debate script** (verbalize; build Q&A bank)
5. **Retail version** (translate; build retail Q&A)

Doing them in parallel before institutional is locked guarantees you'll have to redo them when institutional moves. We learned this the expensive way over multiple rounds.

## Number-consistency discipline

Maintain a "key numbers manifest" at the top of the build script for each derivative version, drawn from the institutional version:

```js
// drawn from institutional v3.0 (locked at 8.8 / 9.0+)
const HEADLINE_RETURN_MID = -0.124;   // 中位 -12.4%
const HEADLINE_RANGE = [-0.15, -0.03]; // 情景加权
const CONVICTION_TAG = "中度偏空";
const ACTION = "减仓";
const CURRENT_PRICE = 35.53;
// etc.
```

Then every derivative version's build script imports these constants. Any change to institutional propagates automatically when derivatives are rebuilt.

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| Different headline numbers in IC pre-read vs institutional | erodes trust; PM will check |
| IC debate script reading off institutional verbatim | sounds robotic; misses verbal compression |
| Retail version still uses "EPS" without translation | loses audience |
| Retail Q&A doesn't anticipate "明天会涨吗" | fails to address how retail thinks |
| Adding new analysis in IC pre-read not in institutional | violates "single source of truth" |
| Retail version has full source citations | overwhelms; instead use "据公司财报" / "据行业研究" |

## Format-level disciplines

### Docx column widths

Every table must have column widths summing to PAGE_W = 9000 in the shared `_docx_helpers.js`. The validator catches mismatches before render. Common pattern is 7-column tables with widths {1400, 1100, 1100, 1300, 1000, 1600, 1500}.

### Naming conventions

- `<ticker>_投资意见书_<author>.docx` — institutional
- `<ticker>_精简版_<author>.docx` — IC pre-read
- `<ticker>_IC_Debate_Script_<author>.docx` — IC debate
- `<ticker>_零售版_投资意见书_<author>.docx` — retail letter
- `<ticker>_零售_对话Script_<author>.docx` — retail Q&A

### Build script naming

- `build_<ticker>_truly_honest.js` — institutional
- `build_<ticker>_concise.js` — IC pre-read
- `build_<ticker>_ic_debate.js` — IC debate
- `build_<ticker>_retail.js` — retail letter
- `build_<ticker>_retail_qa.js` — retail Q&A

### Output discipline

After every build:
1. Verify file produced (check size)
2. Provide `computer://` link to the user
3. Summarize 1-3 lines what's new vs prior version

## Worked example structure (300699 final set)

For ticker 300699 the full deliverable was:

| File | Pages | Purpose |
|---|---|---|
| 300699_投资意见书_谷泓毅.docx | 25-40 | institutional, full, 9.0+ |
| 300699_精简版_谷泓毅.docx | 4 | IC pre-read |
| 300699_IC_Debate_Script_谷泓毅.docx | 6 | IC debate (verbal + Q&A) |
| 300699_零售版_投资意见书_谷泓毅.docx | 4 | retail letter |
| 300699_零售_对话Script_谷泓毅.docx | 5 | retail Q&A (15 common questions) |

All five share these constants: HEADLINE_RETURN_MID = -0.124, RANGE = [-0.15, -0.03], CONVICTION = "中度偏空", ACTION = "减仓", PRICE = 35.53.

Identical structure for BOE.
