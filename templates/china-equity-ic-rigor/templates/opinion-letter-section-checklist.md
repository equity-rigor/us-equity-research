# Investment opinion letter — 12-section checklist

This is the canonical structure for the institutional version. Every section is mandatory; if a section is empty, justify why (typically you don't get to skip).

## §0 — Cover / metadata

- Ticker + name
- Author
- Date
- Current price (with date stamp)
- Market cap, ADV (5-day), beta
- Source data cutoff date

## §1 — Headline (executive summary)

Single page max. Required content:

- 12-month 中位预期收益 (point value)
- 情景加权区间 (low/high)
- 信号倾向 (e.g. 中度偏空 / 中性轻偏空 / 中性 / 中性轻偏多 / 中度偏多)
- **Source-conditional flag if any top-3 anchor is S3 or weaker**
- 默认仓位动作 (持有 / 减仓 -25% / 减仓 -50% / 加仓 +25% etc.)
- 重新评估触发 (≤3 events)
- 一句话核心论点

## §2 — Source stratification box (mandatory)

Top-5 anchors with:
- Anchor name
- S-level (S1-S5 or Pending)
- Source citation
- Promotion path (how it would graduate to S2 if S3-S5)

## §3 — Company / industry context

- Business model 1 paragraph
- Revenue mix by segment (latest year, with source S1)
- Position in industry
- Why this stock is in the universe right now

## §4 — Anchor evidence (per top-anchor deep dive)

For each top-3 anchor:
- What the anchor is (specific claim)
- Source level + citation
- Why it matters for the thesis
- What would falsify it
- How it links to scenario probabilities

## §5 — Five-scenario valuation core

§5.1 5-scenario table (probability × EPS × PE × price × return × anchors × source)
§5.2 Anchor weighting impact table
§5.3 EPS path verification (each scenario's EPS reconciles to bear/bull bridge)
§5.4 Headline calculation (Σ P×R = mid; P10/P90 = range)

## §6 — Three-method valuation reconcile

§6.0 GM taxonomy box (5 GM types)
§6.1 EPS × PE (already in §5.1; cross-reference here)
§6.2 SOTP — segment-by-segment with revenue → GP → OP → NI columns
§6.3 Multi-multiple bear (P/B / EV/EBITDA / FCF yield)
§6.4 Reconcile table — which method for which scenario, why
§6.5 Bear bridge (three-layer: soft / clean / strong)
§6.6 Bull bridge (mirror)

## §7 — What-would-reverse triggers

Tiered or single-threshold triggers with:
- Signal (specific)
- Source channel
- Threshold + denominator
- Window
- Action mapping

Both bear→bull triggers AND bull→bear triggers (symmetric).

## §8 — A0 tail risk mapping

For each tail (3-5 bear, 2-3 bull):
- Trigger
- Probability shift across 5 scenarios (must sum to 0)
- Δ headline post-shift
- Worst/best-case scenario value

## §9 — Position sizing

- σ + horizon-scaled (annual / quarterly / monthly / weekly 1σ)
- E[R], Sharpe (with R_f cited)
- Kelly + conviction multiplier rationale
- Specific position action
- Re-sizing trigger

## §10 — Catalyst calendar

- Date / window
- Event type (earnings / industry data / regulator / company-specific)
- What you're watching for
- Expected impact direction + magnitude

Format as a sortable table by date.

## §11 — Caveats / known limitations

- Anchor verification status (Pending items)
- Cross-section consistency known issues
- Data gaps
- What you'd want to look at if more time

## §12 — Appendix

- Sell-side consensus snapshot (cited)
- Historical multiple bands (with source)
- Comp set analysis (5+ peers)
- Disclosures / IP

## Cross-checks before signing off

Before claiming the institutional version is locked:

1. All verification gates from SKILL.md pass
2. PM rubric score 9.0+ (run `references/pm-redteam-rubric.md` mentally)
3. EPS year consistent across all tables (FY+1 vs FY+2)
4. All specific numbers source-tagged at first appearance
5. Headline-conditionality matches strongest-anchor source level
6. GM taxonomy declared + consistent throughout
7. SOTP reconciles + monotonic + sums to consolidated
8. Bear bridge layered + sum verified
9. What-would-reverse has denominators
10. A0 prob shifts sum to zero
11. Position sizing translates to specific action

If any fail, fix at source (build script) and rebuild.
