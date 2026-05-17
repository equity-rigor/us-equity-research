# IC Debate Script — Template (US)

Verbal-form template for the `ic_debate_script` audience variant (per memo.json). Use as the starting structure for `outputs/<ticker>_IC_debate_<author>.md`. Replace bracketed placeholders. Keep the timing markers — they enforce a discipline of brevity. NVDA as the running example where useful.

This is the talk track; the written rigor lives in `opinion-letter-section-checklist-us.md` and the deliverable shape in `ic-memo-template-us.md`.

---

```markdown
# [TICKER] [Company Name] — IC Debate ([Author])

**Position recommendation**: [action by mandate, e.g. "Long-only large-cap: initiate +50 bps active vs S&P 500" or "L/S: 3% long, beta-neutral via SOXL hedge"]
**Conviction tag**: [high_conviction / moderate_conviction / low_conviction / source_conditional / reactive]
**12M median expected return**: [%]
**Current price**: $[price] ([date])
**Strongest anchor S-level**: [S1 / S2 / S3 / S4 / S5] → headline is [unconditional / source-conditional]
```

---

## §1 — Company fundamentals (2 minutes)

[Company] is [one-sentence positioning — what they do, in plain English]. Revenue mix [latest filed period, S1-tagged]:

1. [Segment 1] — [%] of revenue — [one-line role in the franchise]
2. [Segment 2] — [%] of revenue — [one-line role]
3. [Segment 3] — [%] of revenue — [one-line role]
... (continue for 3-5 segments)

**Why now**: [the specific catalyst, mispricing, or change-in-view that brought this to IC today — one sentence. Examples: "Hopper-to-Blackwell transition closing this quarter creates a 2-quarter ASP step that consensus has not modeled" / "Pre-announce risk this Friday given AVGO supplier signal"]

---

## §2 — Research methodology (1 minute)

I used the 5-scenario probabilistic framework (strong_bear / bear / base / bull / strong_bull) layered with three-method valuation reconcile (EPS × multiple primary; SOTP cross-check; multi-multiple bear floor).

Source stratification: I have [n] core anchors. [m] are S1-S2 (audited 10-K / 10-Q / 8-K). [n−m] are S3-S5 (transcripts, consensus, alt-data). **Strongest top-3 anchor is [S-level]** → headline is [unconditional / source-conditional].

Every specific number is source-tagged at first appearance per the D16 regex pattern. Full citation map is in the appendix.

---

## §3 — Logic chain (3 minutes; anchor → implication → scenario)

The argument runs in three steps:

**Anchor 1** — [name] ([S-level]) → implication: [one sentence on what this anchor commits us to]
**Anchor 2** — [name] ([S-level]) → implication: [one sentence]
**Anchor 3** — [name] ([S-level]) → implication: [one sentence]

Bring all three into the 5-scenario table:

| Scenario | Probability | EPS | Multiple | Target | Return | Anchor weight |
|---|---|---|---|---|---|---|
| strong_bull | [%] | [$] | [x] | [$P] | [%] | [which anchors load here] |
| bull | [%] | [$] | [x] | [$P] | [%] | |
| base | [%] | [$] | [x] | [$P] | [%] | |
| bear | [%] | [$] | [x] | [$P] | [%] | |
| strong_bear | [%] | [$] | [x] | [$P] | [%] | |

Weighted = Σ(P × R) = **[%]**. Range [P10, P90] = **[low%, high%]**. That's the headline.

---

## §4 — Anchor evidence deep dive (4 minutes)

**Anchor 1 — [name]**:
- Data: [specific number with unit + period] ([S-level citation, D16 format])
- Why it matters: [which scenario it loads probability into, and by how much]
- Risk: [specific observable that would falsify this anchor]

**Anchor 2 — [name]**:
[Same three-line structure]

**Anchor 3 — [name]**:
[Same three-line structure]

If any anchor is S3 or weaker: state the promotion path. "This anchor is S3 from the FY24Q4 earnings call. It graduates to S2 at the next 10-Q on [date]; if confirmed, base case probability rises from [%] to [%]."

---

## §5 — Valuation (2 minutes)

**Primary — EPS × multiple**: base scenario [EPS $X] × [multiple_type, e.g. "30x P/E"] = $[price]. Multiple band check: historical 5-year [percentile rank] per `valuation-discipline-us.md`.

**Cross-check — SOTP**: segment-by-segment sum = $[price]. Reconciles to consolidated within ±[bp]; G3 monotonicity holds.

**Strong_bear floor — multi-multiple**: [P/B $X | EV/EBITDA $Y | FCF yield $Z] — sector-branched per D8. Range $[low]-$[high]. This is the strong_bear scenario floor, NOT a weighted-average input.

→ Headline price target [$P] with scenario-weighted range [$low, $high]. Methods are not averaged; they cross-check.

---

## §6 — Caveats / what would reverse (1 minute)

What would change my view (numerical denominators per G9):

1. [Bear-reverse trigger 1]: [specific number + denominator + window] → action [trim/exit]
2. [Bear-reverse trigger 2]: [specific number + denominator + window] → action
3. [Bull-reverse trigger 1]: [specific number + denominator + window] → action [add/upsize]

A0 tail risks (top 3 from `tail-risk-mapping-us.md`):

- [Bear tail, e.g. NBER_recession / Fed_rate_shock / sector_regulatory_action]: probability [%], headline impact [−%]
- [Bear tail 2]: [%] / [−%]
- [Bull tail]: [%] / [+%]

Probability shifts sum to zero across the 5 scenarios per G10.

---

## §7 — Recommendation + position (1 minute)

**Rating**: [Strong Buy / Buy / Hold / Sell / Strong Sell] per D1 bands.

**Sizing by mandate type** (per D3):

- Long-only large-cap (S&P 500 bench): [+/− X bps active]; conviction-adjusted [X% of NAV]
- Long-only SMID (Russell): [+/− X bps]
- L/S hedge fund: [X% gross long, single-name long cap Y%]
- Concentrated specialty / sector fund: [X% of NAV vs sector ETF]
- Pair-trade: [long X / short Y / structure: dollar_neutral or beta_neutral; expected spread return Z%]

Math: σ_annual = [X%]; Sharpe = [Y] using R_f = [%] (FRED `DGS10` as of [date]); Kelly = [Z%]; conviction multiplier = [m×] given [rationale]; final position = [Kelly × m].

Re-sizing trigger: [specific event → adjustment].

---

## Q&A bank — 8 likely PM challenges

### Q1: Challenge core anchor strength
**Likely form**: "Your anchor 1 is just management commentary on the call — that's S3. Why are you levering on it?"
**A**: Accept-and-redirect. "Correct, anchor 1 is S3. That's why the headline carries the source-conditional flag. The promotion path is the next 10-Q on [date]. If the S3 anchor is falsified before then, base case probability drops by [Y pp] and the headline shifts to [revised %]. We are not levering on it; we are weighting it appropriately."

### Q2: Challenge probability distribution
**Likely form**: "You've got base case at 45%. Why isn't bear scenario higher given the macro setup?"
**A**: "The five-scenario probability distribution is anchored to the source-stratified anchor weights, not subjective gut. See §5.2 anchor weighting impact: if I move base from 45% to 35% and reload bear to 30%, the headline shifts from [%] to [%]. That sensitivity is the relevant number. The distribution chosen reflects [specific evidence], not optimism bias."

### Q3: Challenge EPS path / bridge
**Likely form**: "Your bear EPS is $X. Walk me through the bridge from base."
**A**: "Base EPS is $[Y]. Bear bridge has three layered adjustments per `bear-bridge-us.md`. Soft layer: [revenue miss step] = [−$delta] from [S3 anchor]. Clean layer: [GM compression step] = [−$delta] from [S2 anchor]. Strong layer: [tax/SBC normalization] = [−$delta]. Sum = $[Y − bear $X]. Reconciles to scenario table within rounding."

### Q4: Challenge multiple assumption
**Likely form**: "30x P/E for base case — historical band is 18-35x. Why aren't you using mid-cycle?"
**A**: "Historical 5-year percentile is [rank]th per `valuation-discipline-us.md`. In the base scenario, [specific growth/margin profile] justifies [percentile] of band, not mid-cycle. In the bear scenario, multiple compresses to [lower percentile] which is consistent with prior cycle troughs. The multi-multiple floor (§5) cross-checks at $[X] using EV/EBITDA, which is independent of the P/E re-rating debate."

### Q5: Versus sell-side consensus
**Likely form**: "Consensus has FY26 EPS at $X. You have $Y. Where are you different and why?"
**A**: "Consensus median per [S4 source — Visible Alpha n=42 / Yahoo Finance aggregator] is $X with range $[low]−$[high]. I'm at $Y, which is at the [percentile] of the consensus range. The delta is driven by [specific anchor] — sell-side has not yet modeled [specific event]. If they roll forward at the next [10-Q / Investor Day], consensus likely converges to my number. That's the asymmetric setup."

### Q6: Competitor / industry tail
**Likely form**: "What if [competitor X] takes share / what if industry growth halves?"
**A**: "Both are mapped. Competitor share loss above [%] is in the strong_bear scenario (probability [%]); industry growth half-out is the `commodity_shock` or sector demand tail in §6, probability-shift mapped to [scenarios]. Headline impact under either tail: [−X%]. Position re-sizing trigger fires at [observable threshold]."

### Q7: Tail event / A0
**Likely form**: "If [tariff_trade_war / Fed_rate_shock / FDA action] happens, you're stuck."
**A**: "That tail is mapped in §6 per `tail-risk-mapping-us.md`. Event class [name]; probability [%]; worst-case price impact [−X%]; worst-case EPS haircut [−Y%]. Re-sizing trigger fires before the tail materializes if [pre-event observable] is hit. We don't get caught flat-footed; we're sized for the tail."

### Q8: Position sizing too aggressive / too conservative
**Likely form**: "[X%] of NAV is too high given the bear case" OR "if conviction is high, why only [X%]?"
**A**: "Sizing math is in §7. Kelly = [Z%]; conviction multiplier = [m×] per D6 (S1-S2 dominant → 0.50×; mixed S3 → 0.25-0.35×; source-conditional → 0.10-0.20×). Capacity check from quant overlay: ADV is $[X]M, days-to-exit at 10% participation = [N] days. The sized recommendation respects both Kelly and capacity. If PM wants to override, the trigger should be conviction or capacity, not feel."

---

## Timing variants

- **3-minute version**: §1 (compressed) + §3 (compressed) + §7. Use when PM says "give me the gist".
- **5-minute version**: §1 + §2 + §3 + §5 + §7. Full logic chain without deep dive on anchors.
- **10-minute version**: full §1-§7 in order. Default.
- **15-minute version**: full §1-§7 + Q&A bank pre-handled.

---

## Presenter notes

- **Don't hand-wave key numbers** — if PM catches a number you cannot tie to a source, credibility collapses. Be ready to cite §2 directly.
- **Accept-and-redirect when challenged** — "You're right, that anchor is S3. That's why the headline carries the conditional flag. Here's what graduates it."
- **"I don't know — I'll follow up" is acceptable** — better than confabulation. Note the open question; circle back same-day.
- **Voice pacing** — anchor sections (§4) slow; valuation section (§5) faster (technical, audience knows the framework); recommendation (§7) deliberate (this is the ask).
- **Bring the page** — even verbal, have the §0 cover slide visible. Date stamp + current price + strongest anchor S-level is the single screen PM needs in front of them.
- **End on the ask** — last sentence is the position recommendation by mandate. No trailing hedge.
