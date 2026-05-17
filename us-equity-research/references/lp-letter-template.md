# LP Letter Template (US)

NET-NEW for the US skill (per D4 — replaces the China retail and Chinese-language variants). Audience variant `lp_letter` per memo.json.

Audience: qualified purchasers / accredited investors / institutional LPs. Out of scope for FINRA Rule 2210 retail-comms compliance. This is a quarterly fund-letter format, not a single-stock IC memo — but the buy-side rigor still threads through: attribution, change-in-view, position adjustments, catalyst look-ahead, risk disclosure.

Format: prose-heavy (NOT tables), 1-2 pages, tight quarterly cadence. Jargon level: institutional-LP-appropriate. Uses "alpha", "factor exposure", "drawdown", "asymmetry" without explanation; explains "source-conditional" if invoked.

Output as Markdown (.md). No PDF render in initial scope per D15 open question; PDF is Phase G+ extension.

---

## Required structure (rendered)

```markdown
# [Period — e.g. Q1 2026] LP Letter — [Fund Name]

[Date — typically 30-45 days after period close]

[Optional: opening salutation]

## Period overview

[One paragraph — 4-6 sentences. State fund performance vs benchmark for the period (e.g. "Up +X.X% net vs S&P 500 +Y.Y%, an outperformance of Z bps"). State YTD if mid-year. Brief positioning vs prior period: were we adding net exposure, taking it down, rotating between sectors. Avoid market-timing brag; the LP cares about how the book is set up, not whether you "called the bottom".]

## Top contributors and detractors

[Attribution — top 3 each side. NOT a trade blotter — one or two sentences each, focused on the thesis driver, not the entry/exit price.]

**Contributors**:

- **[Position 1]** added +[X] bps. [One sentence on what drove the move — anchor hit, catalyst confirmed, multiple re-rating, beat-and-raise. Cite the source date if it was a specific print or event.]
- **[Position 2]** added +[X] bps. [Same pattern.]
- **[Position 3]** added +[X] bps. [Same pattern.]

**Detractors**:

- **[Position 1]** cost −[X] bps. [One sentence on what went wrong. If thesis broke, say so. If macro headwind, say so. Don't blame "the market".]
- **[Position 2]** cost −[X] bps.
- **[Position 3]** cost −[X] bps.

## Change in view

[Positions where the thesis has materially shifted since the prior letter. This is the section that demonstrates intellectual honesty — LPs notice when the same view is repeated quarter after quarter without acknowledging contrary evidence. 1-2 paragraphs.]

- **[Position]**: We [upsized / downsized / exited] following [specific observable]. Our prior letter [stated / implied] [specific claim]; that has been [confirmed / falsified / shifted] by [evidence with source date]. The revised view is [one sentence].
- **[Position]**: [Same structure if a second material change.]

If no material change: state explicitly. "Coverage thesis is unchanged this quarter; the work continues to validate." Don't fabricate change for the sake of having a section.

## Position adjustments

[New positions, exits, sizing changes — with brief rationale. NOT a trade blotter ("we bought 500 shares of X on Tuesday at $Y"). Focus on the strategic shape of the book.]

- **New**: [Position] initiated at [size, e.g. "1.5% NAV"] following [thesis driver, anchor S-level]. [Catalyst path in one line.]
- **Exits**: [Position] closed. [Why — thesis confirmed and priced-in, or thesis broken, or capacity issue, or better redeployment.]
- **Resized**: [Position] [increased / reduced] from [X%] to [Y%]. [Why.]

If quiet quarter: "Limited turnover this period; portfolio shape is consistent with prior letter."

## Catalyst look-ahead

[Next quarter — 3-5 catalysts that move the book. Forward-looking, not backward attribution. Specific dates where possible.]

- **[Date or window]** — [Position]: [Event — earnings print, FDA decision, investor day, regulatory deadline]. [What we're watching for; how it ties to our thesis.]
- **[Date or window]** — [Position]: [Event.]
- **[Date or window]** — [Position]: [Event.]
- [Sector / macro catalyst if relevant — e.g. "Fed rate decision [date]: portfolio is positioned [long duration / short duration / neutral]"]

## Risk disclosures

[Current portfolio risk concentrations and how we manage them. Acknowledge tail exposure explicitly per A0 tail mapping discipline. 1-2 paragraphs.]

Concentration: top-5 positions = [%] NAV; top-10 = [%]. Sector tilt: [overweight X by Y bps vs benchmark]. Factor tilts (Barra-style per quant overlay framework): [e.g. "long Quality, modestly long Momentum, neutral Value, short Size — i.e. large-cap bias"].

Tail risk acknowledgment: the portfolio is sensitive to [specific A0 event class — NBER_recession / Fed_rate_shock / sector_regulatory_action / tariff_trade_war / sanctions_export_control / commodity_shock]. Worst-case stress per overlay: [stock-portfolio % impact under Fed +200bp / oil −20% / recession dummy]. We monitor [specific observables] and have [trim triggers / hedges / option overlays] sized for [stated dollar loss tolerance].

## Signature

[PM signature]
[Title]
[Fund Name]
[Date]

---

**Disclosures**: This letter is for qualified purchasers / accredited investors / institutional LPs only. Past performance is not indicative of future results. Positions referenced are illustrative; the fund holds many positions not discussed. Performance figures are net of fees unless stated otherwise. Out of scope for FINRA Rule 2210 retail communications rules (institutional audience only). [Standard institutional LP disclaimer paragraph as per fund offering documents.]
```

---

## Audience-tone notes

- **Confident but humble**. State the call; admit when the call was wrong.
- **Explain what didn't work as openly as what did**. Detractors section is not optional even in a strong quarter. LPs lose trust faster on hidden losses than on disclosed ones.
- **Flag changes-in-view explicitly**. The change-in-view section is the credibility section. Even if the change is small, surface it.
- **Don't bury bad attribution**. If a detractor cost 100bps, name it. Don't hide it in aggregate "macro headwind" language.
- **Quarterly cadence**. Letter goes out 30-45 days after period close. Tighter than that risks pre-empting filings; looser than that and LPs are reading stale material.
- **Don't promise future returns**. Forward-looking section is catalyst calendar, not return forecast. Compliance-clean by construction.

---

## Anti-patterns (do not write)

- **Trade blotter style**: "On 1/15 we purchased 5,000 shares of XYZ at $124.50, on 1/22 we trimmed 1,500 shares at $131.20..." LPs do not want a transaction log. They want the strategic shape.
- **Avoiding losses**: "The market was volatile and our positions were temporarily affected." Specifically: which positions, how much, why.
- **Overuse of jargon**: This is institutional, not academic. "Convexity" is fine; "negative skew with positive kurtosis tilted toward..." is not. Use words that the LP's allocator (not necessarily a PM) understands.
- **Promise future returns**: "We expect to generate alpha over the coming quarter from..." Forward-looking sections should be catalyst-driven, not return-projection-driven. SEC compliance hygiene + actual epistemic honesty both point the same way here.
- **Process bragging**: "Our 5-specialist research framework continued to identify..." LP cares about results, not choreography.
- **Repetition of prior letter**: If the thesis is unchanged, say so in one line. Do not re-litigate.

---

## Format discipline

- Prose-heavy. Tables only for the attribution section if absolutely needed; the body of the letter should read like a letter, not a slide deck.
- 1-2 pages max. If running long, cut the catalyst look-ahead first (LPs can find that in the catalyst calendar separately) before cutting attribution.
- Markdown output. PDF render is not in initial scope per D15.
- File path: `outputs/<fund_name>_LP_letter_<period>.md`
- Plural-position letters (covering multiple holdings) are the norm. Single-position LP communications are rare; use IC memo or earnings flash instead.

---

## Composition note

The LP letter is NOT derived mechanically from the IC memo. It is a separate authored artifact. The PM picks 3+3 names to highlight from the book; the rigor framework provides the source-stratified evidence per name when the PM is drafting attribution.

If the user requests "draft the Q[N] LP letter for [fund]" without naming positions, the skill prompts the PM for: (a) the top contributor / detractor list (typically from book attribution dashboard, not from the skill); (b) which positions had material change-in-view; (c) the catalyst calendar look-ahead pulled from `outputs/<ticker>_*.md` files across coverage.
