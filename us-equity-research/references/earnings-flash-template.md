# Earnings Flash Template (US)

NET-NEW for the US skill (per D10). Audience variant `earnings_flash` per memo.json. T+30min post-print structured rapid response.

This is the **operational rapid response** — written within 30 minutes of the earnings call ending. Pre-rehearsed via `earnings-prep-template.md`, executed with verified actuals. The subsequent post-print 8-12 page DOCX earnings update is delegated to `equity-research:earnings-analysis` per `tool-composition-us.md` and runs on a T+24-48h cadence.

Output as Markdown (.md). File path: `outputs/<TICKER>_earnings_flash_<quarter>.md`.

---

## Required structure (rendered)

```markdown
# Earnings Flash — [TICKER] [Q[N] FY[NN]] — [T+X min]

**Author**: [Author]
**Print received**: [YYYY-MM-DD HH:MM ET]
**Call ended**: [YYYY-MM-DD HH:MM ET]
**Flash published**: [YYYY-MM-DD HH:MM ET] (T+[X] minutes from call end)
**Audience variant**: `earnings_flash`
**Source data cutoff (this flash)**: [transcript timestamp / press release timestamp]

## Headline (1 line)

[BEAT / MISS / IN-LINE] vs consensus. Revenue [+X% or −X%] / EPS [+X% or −X%]. Stock reaction [pre-market / after-hours]: [%]. Thesis impact: [confirmed / weakened / shifted / broken].

[One additional sentence on the most important takeaway — typically guidance trajectory or a specific KPI move.]

## Top-3 metrics table

| Metric | Actual | Consensus | Variance | Source |
|---|---|---|---|---|
| Revenue ($M) | [actual] | [consensus] | [+X%] or [−X%] | (S2: [TICKER] [period] earnings release, 8-K Item 2.02 filed [date]) |
| EPS diluted (non-GAAP, $) | [actual] | [consensus] | [+X%] or [−X%] | (S2: same) and (S4: [Visible Alpha / Yahoo Finance] consensus refreshed [date]) |
| [Primary segment KPI, e.g. NVDA Datacenter rev $M] | [actual] | [consensus] | [+X%] | (S2: 10-Q Note 4 if filed concurrently; otherwise press release supplemental) |

Source tags per D16 regex. Variance must be both absolute and percentage.

## KPI movers

[Which segment KPIs moved most; mix shift signal. Bullet 3-5 items. Each ties to a thesis leg.]

- **[KPI 1]**: [actual] vs consensus [expected]. [What this signals — leg confirmation or breakage.]
- **[KPI 2]**: [actual] vs consensus.
- **[KPI 3]**: [actual] vs consensus.
- **Mix shift signal**: [e.g. "Higher-margin segment grew faster than lower-margin; GM mix tailwind worth ~50bp"]

## Guidance update

**CRITICAL**: Verify guidance against the EARNINGS CALL TRANSCRIPT, NOT the press release. Per delta matrix §11 / `verification-protocol-us.md` — companies sometimes give differently-shaped guidance on the call (e.g. wider range, qualitative tone) vs in the 8-K Item 7.01 supplemental release.

| Period | Prior guidance (last quarter) | New guidance (this print) | Verified via |
|---|---|---|---|
| Next quarter ([Q[N+1]]) | [revenue $X-$Y / EPS $A-$B] | [new revenue $X-$Y / EPS $A-$B] | (S3: [TICKER] [Q[N]] earnings call transcript, [date], minute [MM:SS]) |
| Full year (FY[NN]) | [prior FY range or "not given"] | [new FY range or "maintained" or "withdrawn"] | (S3: same; cross-reference 8-K Item 7.01 if range differs) |
| Long-term targets | [if applicable] | [if applicable] | (S3: same) |

Embedded vs raised vs cut:
- Revenue guide: [maintained / raised / lowered / withdrawn] — by [%]
- EPS guide: [same] — by [%]
- Margin guide: [if given]
- Capital allocation: [buyback pace, dividend, M&A commentary changes]

**Point estimate vs range**: did management shift from range to point or vice versa? Tighter range = higher confidence; wider range = lower confidence.

**FY vs NTM**: which horizon is the guide most relevant to? Some companies guide only next quarter; others guide FY; the framing matters.

## Stock reaction read

| Read | Value | Interpretation |
|---|---|---|
| Pre-market or after-hours move | [%] | [vs implied move below] |
| Implied move from prep (front-month straddle) | ±[%] | [from earnings-prep template] |
| Reaction vs implied | [reaction / implied ratio] | [<1 = market absorbed within expectation; >1 = surprise; >>1 = repricing event] |
| Historical reaction to similar prints (e.g. beat-and-raise) | median ±[%] | [is this print's reaction in line with history?] |

Citation example: `(S5: pre-market quote via [Bloomberg / Yahoo Finance / TradingView] at [HH:MM ET])`

If reaction wildly different from implied move:
- Reaction > implied × 1.5 → repricing event; market is shifting the multiple, not just the EPS
- Reaction < implied × 0.5 → market was complacent or had different expectation than published consensus; check whisper alignment

## Thesis impact

[Which of the 5 scenarios in `outputs/<TICKER>_scenarios.json` shifts? Which thesis pillars are affected? Conviction tag change? New top-3 anchor strength?]

- **Scenarios affected**: [base case probability rises from X% to Y%; bear probability falls from A% to B%]; or [strong_bear probability rises from X% to Y% — invoke kill_memo workflow if Tier 2 trigger fires]
- **Pillars affected**: [Leg 1 confirmed by KPI X / Leg 2 weakened by guidance cut]
- **Conviction tag change**: [high_conviction → moderate_conviction] or [source_conditional → high_conviction if S3 anchor graduated to S2 via the print]
- **New top-3 anchor strength**: [the print itself becomes an S2 anchor; promotion path from prior S3 transcript is complete]
- **Updated headline**: [revised 12-month median expected return + range]

## What-would-reverse trigger fires (if any)

[Did this print fire any trigger from §7 of the IC memo per `what-would-reverse-us.md`?]

- **Bear-to-bull reverse**: [yes / no — if yes, cite the specific threshold from IC memo §7 that the print confirms]
- **Bull-to-bear reverse**: [yes / no — if yes, cite the threshold breached]
- **Tier 1 auto-exit**: [yes / no — if yes, name the trigger and direct to exit immediately]
- **Tier 2 position-cut**: [yes / no — if yes, name the trigger and the cut size]
- **Tier 3 watch**: [yes / no — if yes, name the trigger and the re-evaluate timeline]

## Action recommendation by mandate (per D3)

Pre-rehearsed gradient from earnings-prep template, now executed with verified actuals:

| Mandate type | Recommended action | Sizing change | Rationale |
|---|---|---|---|
| Long-only large-cap | [add / hold / trim / exit] | [±X bps active vs S&P 500] | [one-line why] |
| Long-only SMID | [add / hold / trim / exit] | [±X bps active vs Russell] | [one-line] |
| L/S hedge fund | [add long / hold / trim long / cover long / initiate short] | [gross + net adjustment] | [one-line] |
| Sector specialty | [add / hold / trim / exit] | [±X bps active vs sector ETF] | [one-line] |
| Pair-trade | [widen / hold / tighten / invert] | [pair ratio change] | [one-line] |

If material (>1% NAV impact for any mandate), action takes effect at open next session. If pre-market move >2σ vs implied, consider partial execution overnight.

## Kill memo handoff trigger

[Per D10: if pre-announcement-negative pattern (8-K Item 7.01 pre-print) OR beat/miss > −5% with quality breakdown (margin compression + guidance cut + KPI miss simultaneously) → invoke `kill_memo` template per `multi-audience-delivery-us.md`.]

- Pre-announcement detected? [yes / no]
- Beat/miss magnitude vs consensus: [%]
- Quality breakdown (any 2 of 3): margin compression > [bp]? guidance cut > [%]? primary KPI miss > [%]?
- **→ Kill memo invoked**: [yes / no]. If yes, the analyst opens the kill_memo template within T+90 minutes of the call ending and routes the position to exit workflow.

## Sources

- [TICKER] [Q[N]] earnings release (8-K Item 2.02), filed [date], URL: [edgar.sec.gov/...]
- [TICKER] [Q[N]] earnings call transcript, [date], [provider — Motley Fool / SeekingAlpha / AlphaSense]
- Consensus refresh as of [date], [Visible Alpha / Yahoo Finance / etc.]
- Prior guidance reference: [TICKER] [Q[N−1]] earnings call transcript, [date]

## Next steps

- T+24-48 hours: full 8-12 page DOCX earnings update is delegated to `equity-research:earnings-analysis` per `tool-composition-us.md`. This flash is the input to that.
- Update `outputs/<TICKER>_scenarios.json` with verified actuals (Phase 4 verification re-run)
- Refresh `outputs/<TICKER>_structured.json` so the next 14-gate verification reflects the print
- If Tier 1/2 trigger fired: open kill_memo flow
- If thesis upsized: update IC memo §Recommendation with new conviction tag and §Position sizing with new mandate-by-mandate recommendations
```

---

## Time discipline

- **T+30 min** ≠ T+30 days. This is a rapid response after the call ends, not a deep-dive post-mortem.
- The flash is intentionally **structured but brief** — 1-2 pages, written in 20-30 minutes from the actuals.
- Subsequent steps:
  - T+24-48h: full earnings update report — delegated to `equity-research:earnings-analysis` per `tool-composition-us.md`
  - T+1 week: IC memo refresh if material thesis shift
  - T+ next quarter: full re-underwrite per `monitoring-framework-us.md`

## Source ladder discipline

- 8-K Item 2.02 (earnings release) is **S2** — same-day primary source
- Earnings call transcript is **S3** — authoritative for guidance per `verification-protocol-us.md`
- 10-Q (if filed concurrently with print) is **S2** — promotes the S3 transcript anchor to S2 for segment specifics
- Pre-market / after-hours price quote is **S5** — market-implied, not management-confirmed

**Critical**: verify guidance against the transcript, NOT just the press release. Per delta matrix §11.

## Unit confusion checks

- $M vs $B — 10× error; for large-cap names where consensus is sometimes reported in $B, double-check the units on every actual vs consensus comparison
- Basis points vs percent — 100× error; for margin numbers, decide upfront whether you're reporting in bp or %
- GAAP vs non-GAAP — companies report both; consensus is typically non-GAAP for tech, GAAP for some industrials/financials; explicit label required per `forensic-accounting-checklist-us.md`

## Composition with the broader cycle

- `earnings_prep` (night before) sets up the scenario gradient
- `earnings_flash` (T+30 min, this template) executes with verified actuals
- `equity-research:earnings-analysis` (T+24-48h) produces the polished DOCX update — delegated, not duplicated here
- IC memo refresh (week+) integrates the print into the structured JSON and re-runs the 14-gate verification

The flash is the **handoff artifact** between rapid response and the deeper update.
