# Consensus Variance — Where the Edge Is

This file codifies the discipline that separates "we ran a clean process" from "we have a non-consensus view that pays." Every IC-grade memo with a non-Hold rating must declare at least one specific **consensus variance** — a numerical disagreement with the FactSet (or Visible Alpha / Bloomberg EE / IBES) consensus on a specific line item, supported by S1-S3 evidence, with a quantified contribution to scenario weights. Memos that cannot declare such a variance must label themselves "consensus-anchored" in the headline and accept the corresponding scoring cap.

Verified by Plugin 2 gate **G15**. Schema-backed by the `consensus_variance` block in `memo.json` and the `consensus_variance` field in `source_tags.json`.

## The principle

Sell-side consensus is S4 — second-weakest in the S1-S5 stack (see `source-stratification-us.md`). It is a useful base rate, not a truth claim. The structural biases are documented: sell-side overestimates EPS at cycle peaks and underestimates at troughs, anchors to last-print management guidance, herds toward median dispersion, and is structurally slow to recalibrate after regime changes (rate cycles, IRA implementation, BIS export control resets, deposit-beta normalization, GLP-1 demand revisions).

If your memo's top-3 anchors are all S4 (FactSet PT median, Visible Alpha EPS, sell-side rating distribution), you are by definition consensus-anchored — the headline conditionality rule forces `range_only` per `source-stratification-us.md`. G15 enforces the operational extension: a non-Hold rating without at least one declared S1-S3 consensus variance is overclaim. You cannot rate Buy / Strong Buy / Sell / Strong Sell on a name whose every load-bearing input is just the Street median.

The discipline is **forced specificity**. "We think NVDA is more expensive than consensus" is rejected. "We model FY27 datacenter revenue at $215B vs Visible Alpha median $232B because the Q4 FY26 hyperscaler capex guidance from the four largest customers (MSFT $96B, GOOGL $84B, META $66B, AMZN $115B; sum $361B, +12% YoY vs Street modeling +28%) does not support the Street's implied DC revenue trajectory" is accepted. The variance is a number, it has S2/S3 evidence, it ties to a specific scenario weighting impact.

## Variance taxonomy

Every declared variance must be classified as one of five types. The type determines what evidence is required to pass G15.

**Type 1 — Revenue variance.** Disagreement with consensus on FY1 / FY2 / FY3 revenue, segment revenue, geography revenue, or product-line revenue.

  Required evidence: at least one S3 (earnings call / mgmt guidance) or S2 (8-K, 10-Q) citation supporting your number, plus a triangulating data point that consensus does not appear to be weighing — a customer capex disclosure (S2 hyperscaler 10-Q), a channel datapoint (S5 Yipit / Earnest / Placer), a regulator disclosure (S2 FDA / FCC docket affecting addressable market), a pricing decision (S3 mgmt commentary on net realized price). The triangulation point is the actual "edge" claim — it explains *why* you see something consensus has not yet priced.

  Common patterns:
   - Hyperscaler capex Σ vs implied DC GPU revenue (NVDA / AVGO / AMD)
   - Net new logo additions vs implied revenue growth (CRM / NOW / DDOG)
   - Same-store sales vs implied comp acceleration (CMG / SBUX / DPZ)
   - Subscriber additions vs implied ARPU (DIS / NFLX / SPOT)
   - Backlog conversion vs implied book-to-bill ramp (LMT / RTX / BA)

**Type 2 — Margin variance.** Disagreement with consensus on GM / op margin / EBITDA margin / FCF margin at consolidated or segment level.

  Required evidence: explicit bridge from consensus margin to your margin, with each step cited. Bridge items typically include: mix shift (S2/S3 segment disclosure), input cost path (S5 commodity curve or S2 supply contract), price realization (S3 mgmt commentary), SBC % of revenue trajectory (S1 10-K Note + S2 10-Q updates), restructuring tail (S2 8-K + S3 mgmt timeline), tariff pass-through (S5 USTR rate + S3 mgmt commentary). For banks: NIM bridge (deposit beta, asset repricing, mix shift) — see `phase-1-deep-dive-us.md` FS bank section.

  Anti-pattern: "we think margins compress because the cycle is rolling over." Rejected — no specific bridge step.

  Acceptance pattern: "we model FY27 GM 71.2% vs Visible Alpha median 73.8%, bridged as -150bp mix (DC GPU mix declining from 78% to 71% of segment as networking inflects per Q4 FY26 call S3), -80bp pricing (Blackwell-to-Rubin ASP step of only +8% vs consensus implied +18% per Q1 FY27 transcript S3), +30bp manufacturing yield (3nm-to-2nm yield uplift per latest CapEx disclosure S2)." Each step has a citation.

**Type 3 — Multiple variance.** Disagreement with consensus on the appropriate forward multiple (P/E, EV/EBITDA, P/B, P/AFFO, EV/Sales, etc.).

  Required evidence: an explicit peer-set re-rating thesis, with the peer set named and the re-rating mechanism specified. Multiple variance is the highest-fluff category — most analyst notes lean on "multiple compression" or "re-rating to peer median" without specifying *why* the re-rating happens *now* vs in 18 months. G15 forces the mechanism.

  Acceptance examples:
   - "MRK should trade at 14.5x FY27 EPS vs Street 13.0x because IRA Round 2 list (expected Federal Register publication 2026-Q4 per S2 CMS docket) likely excludes Keytruda — pharma peer set ex-LLY currently 13.5x, MRK 7-8% discount to peer median for IRA overhang; if Keytruda excluded, discount unwinds to 0-3%."
   - "JPM should trade at 1.95x TBV vs Street 1.75x because deposit beta normalizes 6 months earlier than peer median per Q1 FY26 call commentary on deposit mix (S3) — peer set BAC/C/WFC re-rated 8-12% on similar deposit normalization signals in 2024-2025; precedent: WFC re-rating Q3 2024 +14% over 90 days."
   - "AAPL should trade at 26x FY27 EPS vs Street 28x because services growth deceleration (16% → 11% on Google AI revenue-share renegotiation, S3 Q1 FY27 commentary) re-rates services-multiple-implied component of SOTP from 35x to 27x."

  Rejection pattern: "we think the multiple is too high" / "valuation looks stretched" / "trades at premium to historical." None of these are mechanisms; they are restatements of price.

**Type 4 — Scenario-weight variance.** Disagreement with consensus on the probability of bear / base / bull outcomes — distinct from disagreement on the value of the base case.

  Required evidence: a base-rate analysis showing peer or analog historical outcome distribution that differs from what consensus is implying via dispersion. Consensus PT dispersion gives the implied scenario distribution; if Street PT range is $80-$145 with median $108, the implied bear-to-bull spread is ±25% — your weight variance must argue this spread is wrong.

  Acceptance pattern: "Street is implying 30% probability of a $145+ bull outcome. We model 12% because the FY27 Hopper-to-Blackwell transition has 4 historical analogs (NVDA Pascal-to-Volta 2018, Volta-to-Ampere 2020, Ampere-to-Hopper 2023, plus AMD Vega-to-RDNA 2019); in 3 of 4, the transition produced 12-24 months of mid-cycle ASP compression before re-acceleration. Bull case requires the 1-of-4 'clean transition' outcome; base rate says ~25% probability not 30%, and within bull case the path is 12-month delay not snap-up."

  Rejection pattern: "we just think bear is more likely than Street does" (no base rate).

  This type also covers what-would-reverse asymmetry: if your bear case requires a specific catalyst (FDA CRL, BIS Entity List addition, antitrust block) that consensus is pricing at 5% and base rate says 35%, that's a scenario-weight variance.

**Type 5 — Timing / catalyst variance.** Disagreement with consensus on *when* something happens, not whether.

  Required evidence: specific date or window, plus the operational mechanism that fixes the timing. Most commonly used for biotech (PDUFA dates, AdCom outcomes), regulatory (HSR Second Request → consent decree timeline, FERC docket resolution), monetary (Fed pivot timing), capacity (fab ramp dates, capacity expansion completion).

  Acceptance pattern: "Consensus models Pioneer synergy run-rate of $3B/yr by Q4 FY27. We model Q2 FY28 — 6 months later — because the integration timeline disclosed Q1 FY26 (S3 CFO commentary at $0.7B run-rate Q1) implies linear ramp to $3B requiring 9 more quarters, not 6. NPV impact: -2.3% on base case; -8% on bull case which currently assumes synergies in run-rate by FY28 dividend reset decision."

  Rejection pattern: "we think it's going to take longer than people think." No date, no mechanism.

## Evidence-required matrix

| Variance type | Required S-level | Required components |
|---|---|---|
| Revenue | At least 1× S2 or S3 | Specific number, named source, triangulation point not in Street model |
| Margin | At least 1× S2 + 1× S3 | Bridge from consensus margin to yours, each step cited |
| Multiple | At least 1× S2 OR S3 + peer history | Named peer set, named re-rating mechanism, historical precedent (date + magnitude) |
| Scenario-weight | At least 1× S5 base-rate study OR 3+ historical analogs | Base rate from analog set, distribution implied by consensus dispersion |
| Timing | At least 1× S2 or S3 docket / mgmt timeline | Specific date or window, operational mechanism |

Variances supported only by S4 (FactSet consensus, sell-side notes) or only by S5 (alt-data without filing-level confirmation) fail G15. The discipline is: *if your variance is only supported by something other analysts are also reading, you don't have a variance — you have a reading*.

## Sizing rule

Each declared variance must specify its contribution to scenario weights. The formula is:

```
sizing_impact_pp = variance_magnitude_pct × probability_of_being_right_pct × scenario_sensitivity
```

Where:
- `variance_magnitude_pct` = your number vs consensus number, as % difference
- `probability_of_being_right_pct` = your subjective probability, range-bound 5%-95%
- `scenario_sensitivity` = % NPV impact per 10% change in the line item (taken from anchor `sensitivity_pct` in the source-tags schema)

The product is the percentage-point shift in the relevant scenario probability vs the consensus-implied scenario probability. Variances with `sizing_impact_pp < 2.0` are decorative — they don't move the headline — and should not be declared as load-bearing.

Example: Pioneer synergy timing variance for XOM. Magnitude = 20% (6 months later out of 30-month timeline). Probability of being right = 60% (mgmt has narrow track record on synergy timing, mixed on M&A integration). Scenario sensitivity = 8% (per A7 NPV sensitivity in base case). Impact: 20% × 60% × 8% = 0.96pp shift — *below threshold, decorative.* Either size up the variance (timing matters more than +8% NPV sensitivity captures, e.g., because dividend coverage breaks) or drop it from the variance block.

## Anti-patterns (G15 will reject)

**1. Generic directional claim.** "We think Street is too bullish." No magnitude, no line item, no evidence.

**2. Repackaged base case.** Stating your base case as a variance from consensus when it numerically matches consensus median. If your FY27 EPS is $7.50 and Street median is $7.45, your "variance" is +0.7% — within noise of Street dispersion. Not a variance.

**3. Multi-quarter handwave.** "Margins will compress over time." No bridge, no period.

**4. Anchor on dispersion.** "Street range is wide, so there's an opportunity." Wide dispersion means analysts disagree; it does not mean *you* have edge. The variance must specify the direction *and* the evidence that places you on one side of the dispersion.

**5. S4-only support.** "We disagree with Visible Alpha consensus based on FactSet's revisions trend." Both are S4. Not a variance — both inputs are the same source class.

**6. "Consensus is anchoring on outdated data."** Often true, often unprovable. The variance must point to the specific S1-S3 source consensus has not incorporated *and* the operational reason the incorporation will happen.

**7. Variance as conviction restatement.** "Buy rating reflects our above-consensus view." Buy rating reflects expected return. If the rating exists without a numerical variance, the rating is consensus-anchored — G15 fails and the headline must reflect that.

## What G15 enforces

G15 is gated on `recommendation.rating` from `memo.json`:

- If rating ∈ {Hold}: G15 = n_a (consensus-anchored Hold is a valid rating, no variance required).
- If rating ∈ {Strong Buy, Buy, Sell, Strong Sell}:
  - Memo must have ≥1 entry in `consensus_variance` block with all required fields (`type`, `magnitude_pct`, `evidence_refs` linking to ≥1 citation per the evidence matrix above, `sizing_impact_pp`).
  - `sizing_impact_pp` of at least one declared variance must be ≥2.0 (i.e., load-bearing).
  - At least one declared variance must have its supporting citations at S1, S2, or S3 — not all-S4 or all-S5.
- If no qualifying variance exists, G15 fails and `blocks_score_above` = 7.0 (memo cannot score above 7.0 / 10 even if all other gates pass).

Exception: if the memo's `headline_conditionality` from `source_tags.json` is `range_only` *and* the memo explicitly self-labels in the headline as "consensus-anchored" (per the convention in `source-stratification-us.md` Rule 1), G15 = n_a for any rating. This is the honest path — admit no edge, accept the scoring cap, do not pretend.

## Operational workflow integration

The A-Consensus specialist is dispatched in Phase 2 alongside A2/A3/A3-Peers/R/A6 (six agents total in Phase 2 from v0.2.0). The A-Consensus prompt forces the analyst to:

1. Pull the FactSet (or Visible Alpha / Bloomberg EE) consensus snapshot — median FY1/FY2/FY3 revenue, EPS, EBITDA; PT median + dispersion; rating distribution; revision history.
2. For each of revenue / margin / multiple, identify whether your model materially differs (>2% on revenue/EPS, >50bp on margin, >5% on multiple).
3. For each material disagreement, classify the variance type and pull the S1-S3 supporting evidence.
4. Quantify the sizing impact using the formula above.
5. If no material disagreement exists, explicitly declare "consensus-anchored" and adjust the headline before PM synthesis.

The A-Consensus output feeds directly into:
- `source_tags.json`'s `consensus_variance` field (machine-readable)
- The "Consensus Variance" section of the IC memo template (human-readable, see `ic-memo-template-us.md`)
- A7's scenario-weighting in Phase 3 (variance sizing impact updates the prior scenario probabilities)
- R-v2's red team challenge — Red Team is required to attack each declared variance specifically.

## Special cases

**No coverage / sub-3 analysts.** If the name has fewer than 3 covering sell-side analysts, "consensus" is too thin to be a meaningful baseline. G15 is `n_a`; the memo must instead declare an explicit "no consensus baseline" in the source-stratification block. Replace the consensus-variance discipline with peer-implied benchmarking (use closest GICS sub-industry peers' multiples and growth rates as the implicit consensus).

**Deep illiquid micro-cap.** Similar — pre-revenue biotech, post-bankruptcy emergent equity, recent IPO without analyst initiation. G15 = n_a; document the alternative benchmarking method.

**Time-arb thesis.** Sometimes the variance is "consensus will agree with us in 6 months." This is a Type 5 (timing) variance — the operational mechanism is the specific S1-S3 catalyst (earnings, FDA decision, regulator order) that forces the recalibration. Cannot be left vague.

**Pair-trade.** Variance must be declared on the spread, not on each leg. If you're long NVDA / short AMD, the variance is about the differential — e.g., "we model Blackwell-to-MI400 share differential as 78%/22% vs Street's implied 72%/28% based on Q1 FY27 hyperscaler procurement disclosures." Apply the discipline once to the spread, not twice to each side.

**Activist / event-driven.** Variance type 4 (scenario-weight) is the natural fit for activist names — the disagreement is "Street prices a 15% probability of board change; we price 45% given the proxy filing S2 + voting recommendation S3 from ISS." Standard discipline applies.

## Calibration: how often should you declare a variance vs go consensus-anchored?

Honest base rate from running this discipline across the v0.1.x self-test set (NVDA / JPM / MRK / XOM / DLR):

- Names where a defensible non-Hold variance can be declared: roughly 30-50% in normal markets. The other 50-70% are honestly consensus-anchored — Hold rating, range-only headline. This is the *correct* base rate. If your hit rate of declared variances exceeds 60% across your coverage, you are likely manufacturing variances to avoid Hold ratings — a known PM-grade failure mode.

- Variance types frequency: Revenue (~25%), Margin (~25%), Multiple (~30%), Scenario-weight (~15%), Timing (~5%). Multiple variance is the easiest to manufacture (most fluffy) and should be scrutinized most aggressively by Red Team v1 and v2.

- Sizing impact distribution: most declared variances produce 2-5pp scenario shifts (mid-conviction); 5-10pp shifts are conviction trades (size up); >10pp shifts should be examined for over-claim and either substantiated with stronger evidence or down-weighted.

## What this discipline does *not* solve

This file forces a structured place to claim edge. It does not generate edge. The actual identification of where consensus is wrong is irreducibly the analyst's craft — it requires reading the same source data consensus reads but seeing what they did not see, or pulling a primary source consensus has not pulled. G15 ensures that *when* an edge claim is made, it is specific, evidence-backed, and sized. G15 cannot ensure the edge is real. That falls to the verification phase, the red team, and the PM's judgment.

The honest framing: G15 is a *quality gate*, not an *alpha gate*. It catches the most common LLM and junior-analyst failure mode (decorative variance language without numerical content) and forces explicit "consensus-anchored" labeling when no real variance exists. Memos that pass G15 are not automatically alpha-generating; they are at minimum non-fraudulent in their edge claims.

## Cross-references

- `source-stratification-us.md` — S1-S5 taxonomy, headline conditionality rule
- `phase-2-continuation-us.md` — A-Consensus specialist prompt (v0.2.0)
- `ic-memo-template-us.md` — Consensus Variance section (v0.2.0)
- `phase-3-valuation-us.md` — How variance sizing flows into A7 scenario weighting and R-v2
- Plugin 2 `verification_gates.json` — G15 definition
- Plugin 2 `scripts/verify_consensus_variance.py` — G15 verifier
