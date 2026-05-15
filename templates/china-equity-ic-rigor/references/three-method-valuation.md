# Three-method valuation reconciliation

## The core discipline

EPS×PE, SOTP, and multi-multiple are **three lenses on the same business** — they are not three independent fair values to average. Treating them as three fair values to average produces nonsense (you'd be averaging a forward earnings view, a sum-of-parts view, and a cycle-trough view; the average has no economic meaning).

The right framing:

- **EPS × PE** is the primary valuation. It is what you defend in IC. It is the headline.
- **SOTP** is a *cross-check* for segment-level internal consistency. If your scenario EPS doesn't reconcile to a defensible SOTP, your scenario EPS is wrong.
- **Multi-multiple bear** (P/B, EV/EBITDA, FCF yield) is a *floor check* — it answers "if the market loses faith in EPS entirely, where does the stock find support?"

When the three methods disagree, do NOT average. Instead, identify which method's assumption is doing the work and which scenario the disagreement implies. A 30% spread between EPS×PE bear case and multi-multiple bear case usually signals one of three things:

1. The bear-case EPS has too much hidden cost-cutting baked in (EPS×PE looks too high vs P/B floor)
2. The asset base has stale book value (P/B floor is too high vs forward earnings)
3. The market is pricing a regime change EPS×PE doesn't capture (FCF yield says worse than P/E says)

Identify which one and write it as the "valuation reconcile" subsection.

## Method 1: EPS × PE (primary)

See `five-scenario-framework.md` for the scenario construction. Key disciplines:

- Forward EPS year must be consistent across rows (FY+1 or FY+2; pick one and stick with it; we typically use FY+2 for cyclical stocks because it captures a meaningful cycle pivot).
- PE must reflect both growth quality AND scenario-specific risk premium.
- Each row's price = EPS × PE (mechanical, not narrative).

## Method 2: SOTP — what it's actually for

SOTP is the **internal consistency check**. Build the SOTP using the same EPS path you used in EPS×PE, decompose it segment-by-segment, and verify:

1. Σ(segment NI) ≈ company NI (within rounding + minority interest)
2. Per-segment NI < per-segment OP < per-segment GP < per-segment Revenue (monotonic)
3. Per-segment GM consistent with what GM taxonomy says (see `gm-taxonomy.md`)
4. Per-segment OP margin within historical bands

If any of these fail, your scenario EPS path is fictional. SOTP is not generating new information — it's auditing the EPS you already have.

### SOTP table required columns

```
| 业务分部 | 营收 | 毛利率 | 毛利 | 销管研费用 | 营业利润 | 所得税 | 净利润 | 估值倍数 | 分部估值 |
```

The middle columns (营收 → 毛利 → 营业利润 → 净利润) must reconcile mechanically. If they don't, fix the segment assumption, not the column.

The 估值倍数 / 分部估值 columns at the right side are **for cross-comparing implied multiples**, not for summing to a fair value. Common usage: show that your sum-of-parts implied EV is within ±15% of EV×PE-method EV; if it's not, either segments are mispriced or company-level valuation is mispriced — investigate which.

### Pitfall: SOTP NI > SOTP GP

This was the BOE Round 11 / 300699 Round 11 bug. It happens when the modeler estimates segment NI directly (top-down) without forcing it through the GP→OP→NI mechanical chain. To prevent: ALWAYS construct SOTP bottom-up via the column sequence above. NI should be the final number you compute, not an input.

### Pitfall: segments don't sum to consolidated

Common: segment revenues sum to consolidated within ±2%, but segment NI sums to 80% of consolidated NI because corporate overhead / unallocated wasn't modeled. Fix: include a "其他/未分配" row that absorbs the difference, with a one-line explanation (typically "总部费用 + 内部抵消 + 投资收益").

## Method 3: Multi-multiple bear (floor check)

Apply when constructing the bear / 强空 scenarios. The question this method answers: in a true downside, what is the stock worth on metrics that don't depend on forward earnings?

### Three multiples to triangulate

**P/B floor**:
- Best for: capital-intensive cyclicals (panels, materials, basic industry).
- Formula: BVPS × historical-trough P/B (cite trough year and value).
- Caveat: if there's impairment risk in the bear, mark down the BV first.

**EV/EBITDA trough**:
- Best for: mid-cycle / high-leverage names.
- Formula: (forward EBITDA in bear) × historical-trough EV/EBITDA, then back into equity value.
- Caveat: EBITDA is not cash; if working capital is unwinding, FCF is worse.

**FCF yield**:
- Best for: capex-heavy companies where reported earnings overstate cash generation.
- Formula: bear FCF / market cap. Compare to peer / risk-free rate + ERP.
- Caveat: cyclical names have negative FCF in trough; use mid-cycle FCF for floor.

### When to apply which

| Situation | Multiple | Why |
|---|---|---|
| Capital-heavy cyclical (BOE, panel, steel) | P/B | trough P/B has historical anchor |
| High-leverage industrial (chem, transport) | EV/EBITDA | strips out leverage noise |
| Capex-heavy with cash distortion (semis, panels) | FCF yield | catches cash burn missed by P/E |
| Asset-light brand (consumer, services) | none of these — stay with EPS×PE |

### Triangulation example (BOE 强空 floor)

- P/B floor: BVPS ¥3.5 × trough P/B 0.7 (2018 trough) = ¥2.45
- EV/EBITDA: bear EBITDA ¥320 亿 × 4x EV/EBITDA = EV ¥1280 亿; subtract net debt ¥600 亿 → equity ¥680 亿 / 38 亿股 = ¥1.79
- FCF yield: bear FCF ¥80 亿 / 8% required yield = ¥1000 亿 / 38 亿股 = ¥2.63
- Range: [¥1.79, ¥2.63], midpoint ¥2.21
- EPS×PE 强空 was ¥1.98 — sits within multi-multiple range, **floor consistent**.

If EPS×PE 强空 had said ¥3.50 while multi-multiple says [1.79, 2.63], that's a red flag: bear EPS too generous, bear PE too generous, or both. Re-bridge.

## The three-method reconcile table (mandatory in §5.7)

```
| 方法            | 基础情景值 | 空头情景值 | 强空情景值 | 锚点逻辑           |
|-----------------|-----------|-----------|-----------|--------------------|
| EPS × PE        | ¥4.42    | ¥3.30    | ¥1.98    | 基础 0.34×13      |
| SOTP            | ¥4.30    | ¥3.40    | ¥2.10    | 分部加总          |
| 多倍数 (P/B)    | —        | —        | ¥2.45    | 0.7x trough BV    |
| 多倍数 (EBITDA) | —        | —        | ¥1.79    | 4x trough         |
| 多倍数 (FCF)    | —        | —        | ¥2.63    | 8% yield           |
| **采用值**       | ¥4.42    | ¥3.30    | ¥1.98    | EPS×PE primary     |
```

Bottom row is what flows to the headline. The other rows are the audit trail showing why EPS×PE ¥1.98 in 强空 is defensible.

## What to do when methods disagree by >15%

1. Identify the disagreement (e.g. EPS×PE 强空 ¥1.98 vs P/B floor ¥2.45)
2. Locate the source of disagreement: usually it's a difference in how aggressively the bear narrative is bitten off. P/B doesn't believe earnings will collapse; EPS×PE assumes they will.
3. Add a "valuation reconcile" subsection that names the disagreement and resolves it: "EPS×PE 强空 implies a 35% earnings decline; P/B floor implies the market would not let it fall that far. We use EPS×PE because [reason — e.g. recent precedent, structural shift, tighter capacity discipline] suggests P/B is anchored on a structurally healthier era."
4. Use the disagreement to inform conviction: methods agreeing tightens conviction; methods disagreeing widens the headline range.

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| "FV = (EPS×PE + SOTP + multi-multiple) / 3" | averaging incompatible methods; produces non-economic number |
| Citing only EPS×PE without SOTP | no internal consistency check |
| SOTP at headline level only (no segment breakdown) | useless — doesn't audit anything |
| Multi-multiple in 基础 scenario | floor methods only inform downside; using them in base inflates pessimism |
| Using BV without segment-level impairment in bear | overstates floor in real downside |
