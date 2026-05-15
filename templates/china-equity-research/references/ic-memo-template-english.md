# IC Memo Template (English)

The English IC memo is the institutional deliverable. Structure forces explicit articulation of rating, sizing, thesis, risks, and decision triggers.

---

## Required Structure

```markdown
# Investment Committee Memo: [Company Name] ([TICKER])

**Author**: [Author / PM]
**Date**: [Date]
**Mandate**: [Long-only / Hedge fund / Other]
**Horizon**: [Months]
**Stage**: [Final IC memo / Initiation / Update]

## RECOMMENDATION

**[BUY / HOLD / SELL] / [Overweight / Equal-weight / Underweight]**

12-month price target: [PT]
24-month price target: [PT]
Stop discipline: [Stop level + condition]

[One-paragraph rationale for the rating]

**Asymmetry**: [Bear PT / Base PT / Bull PT] vs. current price [X]. [Specific asymmetry math.]

## INVESTMENT THESIS

[One-paragraph framing]

**Leg 1 — [Title]**: [Specific evidence and quantification]

**Leg 2 — [Title]**: [Specific evidence and quantification]

**Leg 3 — [Title]**: [Specific evidence and quantification]

[Continue with as many legs as the thesis requires; typically 3-5]

## VALUATION FRAMEWORK

### Scenario probabilities and per-share IV

| Scenario | Probability | NI to parent FY[X]E | Per-share IV | Driver |
|---|---|---|---|---|
| Bull | [%] | [$] | [PT] | [Specific drivers] |
| Base | [%] | [$] | [PT] | [Specific drivers] |
| Bear | [%] | [$] | [PT] | [Specific drivers] |

**Probability-weighted IV: [PT]**

### Methodology triangulation

- DCF central: [PT]
- DCF bear: [PT]
- SOTP: [PT]
- Peer multiples: [PT]
- **Triangulated final IV range**: [Range] (weighting: X% peer / Y% DCF / Z% SOTP)

### Position sizing across mandate types

| Mandate type | Recommended position | vs. Benchmark | Rationale |
|---|---|---|---|
| Standard A-share whole-market portfolio | [%] | [Benchmark + delta] | [Why] |
| Sector / themed portfolio | [%] | [Benchmark + delta] | [Why] |
| Concentrated specialty fund | [%] | [Benchmark + delta] | [Why] |
| Pair-trade structure | [Subject + Pair sizing] | [Pair benchmark / N/A] | [Why] |

## KEY FINANCIAL DATA (verified, primary-source)

### FY[X] actuals
[Hard numbers with source citation]

### Q[X] actuals
[Hard numbers with source citation]

### Forward forecast
[NI / FCF / capex trajectory next 3 years]

### Specific contractual / regulatory items
[Identified contingent obligations, regulatory designations, etc.]

## RISKS AND KILL CRITERIA

### Tier 1 — Auto-exit triggers (any → exit immediately)

1. [Specific binary regulatory event]
2. [Specific binary customer event]
3. [Specific binary geopolitical event]
[etc.]

### Tier 2 — Position-cut triggers (any → reduce by half)

1. [Specific quarterly miss threshold]
2. [Specific cycle / pricing trigger]
3. [Specific commercial pipeline trigger]
[etc.]

### Tier 3 — Watch / re-evaluate triggers

1. [Subtler change-of-mind catalysts]
[etc.]

## MONITORING PLAN

### Weekly
[Specific data series to track Monday morning, ~15 min]

### Monthly
[Specific items, ~30 min]

### Quarterly (after results)
[Full re-underwrite, ~4 hours]

### Key dated events

| Date | Event | Significance |
|---|---|---|
| [Date] | [Event] | [Why it matters] |

### Re-underwrite triggers

Schedule explicit re-underwrite at:
- [Specific dated milestone 1]
- [Specific dated milestone 2]

## RED TEAM POSTURE (FINAL)

**Bear PT range**: [Range]

**Concession from Red Team**: [Specific points where bear case yields]

**Defended bear points**: [Bullet list of bear arguments that survive]

**Falsification criteria** (3 of 5 fires → bear concedes):
1. [Specific measurable event 1]
2. [Specific measurable event 2]
[etc.]

**Recommended weight (Red Team's view)**: [Position size]

## FINAL ADJUDICATION

[How the PM weighed bull vs. bear vs. valuation vs. forensic vs. peer analysis to arrive at the final recommendation. This is where the disagreements between specialists are explicitly resolved.]

**Path to upsizing**:
- [Specific catalyst → Add X pp]
- [Specific catalyst → Add X pp]

**Path to position cut**: any Tier 1 or Tier 2 trigger from §Risks

## OPEN QUESTIONS / WHAT WOULD CHANGE THE VIEW

[Specific verifiable items that, if resolved, would change conviction or directional call. Typically 5-10 items, ranked by importance.]

For [Item 1]: [What we'd want to learn] [Source / how to verify]

## APPENDICES

### Appendix A: Document map
[List all phase deliverables and where they're saved]

### Appendix B: Source links (verified primary)
[List all primary sources used, with URLs]

### Appendix C: Verification report reference
[Link to verification report; summarize verification status]
```

---

## Key Quality Standards

**Rating + sizing must be explicit and explained**. A "Buy" with limited conviction is half-weight. A "Hold" can be 0% (avoid) or 1% (small show position). State both.

**Position sizing across mandate types is mandatory**. Different funds have different benchmarks. Articulate the recommendation for at least 3 mandate types.

**Bear case must be present and not strawmanned**. Even on a Buy recommendation, the Red Team's strongest case should be visible.

**Open questions section forces intellectual honesty**. Every IC memo has gaps. List them explicitly. The 4-6 most important should drive the next research cycle.

**Cite specific source URLs in appendix**. Every material number should be traceable. The verification report is the supporting documentation.

---

## What NOT to Include

- **Process commentary**: How many phases, what was wrong with v1/v2, intellectual humility statements. These belong in internal documentation, not the IC memo. The IC reader cares about the conclusion.
- **Self-promotion**: "Our framework is rigorous because..." Just be rigorous.
- **Excessive hedging**: "Could be either bull or bear" without commitment is useless. Adjudicate.
- **Padding**: Length is not value. A 4,000-word IC memo done well beats an 8,000-word one with filler.
