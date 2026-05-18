# PM red-team rubric (US)

## What this is

A scoring rubric and bug catalog calibrated for US institutional buy-side IC memos. Use it when:

- Red-teaming your own (or another model's) draft.
- The user reports a numerical score and asks "what would push this from 8.x to 9.x."
- Deciding whether a memo is IC-ready (≥8.5 per **D20** Phase E success criteria).

The rubric is intentionally tight — it tracks what actually moves PM scores in practice, not aspirational quality dimensions. The 14 verification gates G1-G14 (10 inherited from China + 4 US-specific per D13) are the mechanical floor; this rubric is the human discipline layered on top.

## Score bands

### 6.0–7.5 — structural / mechanical bugs

The memo fails at least one of these:

- **Math doesn't reconcile**: EPS × multiple ≠ scenario price (G1); segment GM × revenue ≠ consolidated GP (G2); SOTP NI > GP (G3 inversion); bear bridge doesn't sum (G5).
- **Sourcing absent**: specific numbers appear without S1-S5 tags (G6).
- **Headline-anchor mismatch**: unconditional headline on weak (S3-S5) anchors (G7).
- **Internal contradiction**: same number cited differently in two sections without reconciliation.

These are mechanical bugs. They never get past 7.5 until fixed. Run the verification scripts.

**To get to 7.5+**: run all 14 verification gates from `schemas/verification_gates.json`; fix every gate failure; re-run.

### 7.5–8.5 — narrative coherence + scenario discipline

Math passes. Now the issues are analytical:

- **Scenario probabilities lazy** (10/20/40/20/10 default not justified by anchors).
- **Anchor weighting impact table missing** (G10) — PM cannot see how sensitive headline is to a single probability shift.
- **GM taxonomy not declared** (G8) — "gross margin" used loosely without T1/T2/T3/T4/T5 mapping per `gm-taxonomy-us.md`.
- **Bear bridge missing layers** — bear EPS shown without soft/clean/strong decomposition per `bear-bridge-us.md`.
- **What-would-reverse triggers without numerical denominators** (G9) — directional handwave instead of measurable threshold.
- **Anchor sensitivity not shown** — reader cannot tell which anchor moves headline most.

**To get to 8.5+**: add missing structures (taxonomy box, anchor weighting, layered bridge, denominators on triggers).

### 8.5–9.0 — IC-grade hardness

Structures are in place. Issues are sharper:

- **A0 tail mapping incomplete** — bear tails listed but no bull tails; or shifts don't sum to zero (G10/B9).
- **Three-method valuation reconcile missing** — only EPS × P/E, no DCF cross-check, no multi-multiple floor.
- **Source-conditional language inconsistent** — top anchors have S3 elements but headline reads unconditional in one paragraph, conditional in another.
- **Cross-section consistency** — numbers in §3 and §6 within rounding but not explicitly reconciled.
- **Position sizing skipped** (B10) — Sharpe and Kelly mentioned conceptually but not translated to specific %/bps per `position-sizing-us.md`.
- **Action mapping vague** — "trim" without specifying −25%? −50%?
- **Non-GAAP/GAAP gap unreconciled** (G11/B11) — US-specific.
- **SBC not deducted from FCF without explicit flag** (G12/B12) — US-specific.
- **Factor exposure unstated** (G13/B13) — US-specific.
- **Capacity / ADV / days-to-exit unstated** (G14/B14) — US-specific.

**To get to 9.0+**: add the missing hardness (full A0, three-method reconcile, conditional language audit, position sizing math, specific action, non-GAAP reconciliation, FCF/SBC discipline, factor tags, capacity disclosure).

### 9.0+ — IC-ready

All 14 gates passed. All structures present. Issues are subtle:

- **Edge-case completeness** — does the bear bridge handle the case where soft adjustments cancel each other?
- **Forward-looking inflation guard** — are forward EPS years consistent across all tables (FY26E vs FY27E vs CY26E confusion)?
- **Audience derivative consistency** — do IC pre-read / IC debate script / LP letter numbers exactly match institutional source-of-truth per `multi-audience-delivery-us.md`?
- **Catalyst calendar present** — does the memo tell the reader when to look for trigger updates per `monitoring-framework-us.md`?

Polish-level fixes. Memo is defensible at 9.0 even without them.

## Bug catalog (in order of frequency observed)

### B1 — EPS × Multiple column doesn't multiply (G1)

The most common bug. Modeler computes scenario prices by reverse-engineering from a target return rather than from EPS × multiple discipline.

**Detection**: for each scenario row, multiply EPS × multiple; compare to listed price; flag any divergence >0.5%.

**Fix**: rebuild the scenario table starting from EPS path × multiple assumptions; let the price column be the output.

### B2 — Segment GM × revenue ≠ consolidated GP (G2)

Modeler quotes segment GMs from notes and consolidated GM from income statement; doesn't verify they reconcile.

**Detection**: compute Σ(segment_revenue × segment_GM) / Σ(segment_revenue); compare to consolidated GM; require ≤50bp delta.

**Fix**: add "Other / unallocated" row reconciling the residual; or fix the segment assumption that's wrong.

**Scope methodology note**: G2 applies to **LTM and forward (projected/modeled) periods** — the canonical current and forward-cycle mosaic that the memo's valuation anchors on. **Historical period segment reconciliation is informational only**, because real 10-K disclosures routinely diverge from weighted consolidated GM by 50-150bp due to corporate allocation differences, "Other / Unallocated" buckets, source-filing rounding, and segment-definition changes mid-year. Historical mismatches surface in the memo as forensic flags but do NOT trip G2 / B2. See `gm-taxonomy-us.md` G2-scope paragraph for the canonical statement.

### B3 — SOTP NI > GP (G3 inversion)

Modeler estimates segment NI directly without going through GP → OP → NI mechanical chain.

**Detection**: in SOTP table, check NI ≤ OP ≤ GP ≤ Revenue for every segment.

**Fix**: rebuild SOTP bottom-up via column sequence Revenue → GM → GP → OpEx → OP → Tax → NI.

### B4 — Mixed GM definitions without taxonomy box (G8)

Memo uses "gross margin" for T1 consolidated in one place, T2 segment in another, T3 sub-segment in another. PM challenge: "Are you saying GM is 8%, 18%, or 35%?"

**Detection**: scan for every "gross margin" / "GM" instance; tag each with its taxonomy type.

**Fix**: insert GM taxonomy box per `gm-taxonomy-us.md`; tag every instance at first mention.

### B5 — Headline unconditional on weak anchors (G7)

Top-3 anchors are S3-S5 but headline reads as confident point estimate.

**Detection**: classify top-3 anchors per `source-stratification-us.md`; check headline language for source-conditional patterns A-D.

**Fix**: rewrite headline using one of the four source-conditional English patterns.

### B6 — Bear EPS not bridged (G5)

Bear EPS appears as a number with no soft/clean/strong decomposition.

**Detection**: search for bear EPS / Strong Bear EPS; look for adjacent bridge table.

**Fix**: build three-layer bridge per `bear-bridge-us.md`.

### B7 — What-would-reverse without numerical denominator (G9)

Triggers are directional ("if margins recover") not numerical ("≥75.0% GAAP gross margin for two consecutive quarters on revenue ≥$X B").

**Detection**: read each trigger; check for specific number AND denominator base.

**Fix**: rewrite triggers per `what-would-reverse-us.md`.

### B8 — Cross-version stale numbers

Earlier round number persists in a section that wasn't updated when institutional was re-derived.

**Detection**: search for old version's headline number; verify all instances updated.

**Fix**: global search-and-replace; verify by reading relevant sections; rebuild derivative variants per `multi-audience-delivery-us.md` source-of-truth discipline.

### B9 — A0 tail probability shifts don't sum to zero (G10)

Modeler shifts probability but doesn't conserve mass.

**Detection**: for each A0 row, sum the five probability shifts; should be 0.0 within ±0.1pp.

**Fix**: re-balance shifts so they sum to zero; ensure direction matches event severity per `tail-risk-mapping-us.md`.

### B10 — Position sizing absent

Sharpe and Kelly mentioned conceptually but not translated to specific %/bps allocation.

**Detection**: search for "Sharpe" / "Kelly" / "position" / "weight"; verify a specific bps or %-NAV appears for each of five mandate types per **D3**.

**Fix**: add full sizing chain per `position-sizing-us.md`.

### B11 — Non-GAAP / GAAP gap not reconciled (G11, US-specific)

US filers report both GAAP and non-GAAP. Analysts often anchor to non-GAAP (because management does) without reconciling SBC + acquired intangible amortization + restructuring + other adjustments.

**Detection**: search for "non-GAAP" or "adjusted" EPS / EBITDA / operating income; check for adjacent reconciliation table or bridge to GAAP.

**Fix**: insert reconciliation table per Reg G + Item 10(e). At minimum, show:
- GAAP EPS
- + SBC per share
- + amortization of acquired intangibles per share
- + restructuring per share
- + other one-time per share
- = Non-GAAP EPS

Cross-reference `forensic-accounting-checklist-us.md` for non-GAAP discipline.

**Example**: NVDA memo cites "non-GAAP EPS $X" without bridge to GAAP — adds back ~10% SBC and amortization headwind missed. Fix: mandatory reconciliation table at first non-GAAP citation. GAAP-to-non-GAAP delta as % of NI flagged if >25% sustained (per `schemas/memo.json` `forensic_flags.non_gaap_to_gaap_delta_pct_ni_5y_avg`).

### B12 — SBC not deducted from FCF without explicit flag (G12, US-specific)

Common pattern: bull case cites "FCF" without disclosing SBC is excluded. "FCF" definitions vary (OCF − capex, OCF − capex − SBC, EBITDA − capex, etc.); without explicit definition, the headline is opaque on real dilution.

**Detection**: search for "FCF" / "free cash flow"; verify the definition is stated AND SBC treatment is disclosed.

**Fix**: insert FCF definition line at first use:
> "FCF defined as OCF − capex − SBC (i.e., SBC treated as a real cost), $X B for FY24 (S1: NVDA 2024 10-K Item 8 Cash Flow Statement reconciliation). Buyback offset to SBC ratio: $Y / $Z = N.NN."

Buyback-offset-to-SBC ratio <1.0 means dilution masked by ASR; this is a structural red flag per `forensic-accounting-checklist-us.md`. Schema field: `financials.fcf_includes_sbc_addback` (boolean) and `buyback_offsets_sbc_ratio` (number).

**Example**: TSLA memo cites "$Y B FCF" without flagging SBC ~$Z B excluded. Unflagged disclosure violates G12. Fix: state FCF definition explicitly; show SBC line separately; compute buyback offset ratio.

### B13 — Factor exposure unstated (G13, US-specific, per D13)

Memo lacks Barra-style factor tags. Without factor decomposition, the PM cannot tell what the position adds at the book level — and the analyst cannot anticipate factor-reversal events.

**Detection**: search §11 (Quant Overlay) for `factor_tags` with Value / Quality / Momentum / Growth / Size / Low-Vol / Liquidity z-scores.

**Fix**: insert factor table per `schemas/memo.json` `quant_overlay.factor_tags` schema. Each on -3 to +3 z-score (typically estimated by regressing name returns against factor portfolios or sourcing from Barra / Axioma / MSCI if available).

**Example**: AAPL memo without Barra tags (would typically score: Quality +1.5, Low-Vol +0.8, Size +2.7, Liquidity +0.5, Momentum +0.4, Value −0.7, Growth +0.2). Without these, a Quality+Low-Vol-tilted book cannot tell whether adding AAPL doubles down on existing factor exposure or diversifies.

### B14 — Capacity / ADV / days-to-exit unstated (G14, US-specific, per D13)

Position sizing without capacity check is theory; a thin-trade name cannot be liquidated at thesis-break without market impact.

**Detection**: search §11 (Quant Overlay) for `capacity` with `adv_30d_usd_m`, `days_to_exit_10pct_participation`, etc.

**Fix**: insert capacity table per `schemas/memo.json` `quant_overlay.capacity` schema. Include ADV (30-day average daily dollar volume), days-to-exit at 10% / 20% / 30% participation against the recommended position size, and the implied `max_position_constrained_by_adv_pct_nav`.

**Example**: SMID-cap with $50M ADV → cannot absorb 1% of $5B fund (= $50M position) without 10 days of 10% participation. Memo must surface this explicitly and cap absolute position such that days-to-exit at 10% participation ≤5 days (or accept higher participation rate with disclosed market-impact cost).

## Score-to-fix lookup table

| Reported score | Most likely bug class                        | Action                                                                  |
|----------------|---------------------------------------------|-------------------------------------------------------------------------|
| 6.0–6.5        | B1, B2, B3 (mechanical)                     | Run verification scripts G1, G2, G3                                     |
| 6.5–7.5        | B1-B5 mix                                   | Scripts G1-G7 + headline conditionality review                          |
| 7.5–8.0        | B5, B6                                      | Source-conditional rewrite + bear bridge add (G7, G5)                   |
| 8.0–8.5        | B4, B7, B8                                  | Taxonomy box + denominators on triggers + stale-number sweep (G8, G9)   |
| 8.5–8.8        | B9, B10                                     | A0 completeness + position sizing (G10 + sizing math)                   |
| 8.5–8.8        | B11, B12                                    | Non-GAAP reconciliation + FCF/SBC disclosure (G11, G12)                 |
| 8.8–9.0        | B13, B14                                    | Factor tags + capacity disclosure (G13, G14) — required per D13         |
| 8.8–9.0        | polish                                      | Catalyst calendar + audience derivative consistency                     |
| 9.0+           | edge cases                                  | Only matters if going LP-facing or external-audit-grade                 |

## Working a red-team round end-to-end

1. **Read the user's challenge or score.** Identify whether it's a specific item ("EPS × multiple wrong in scenario row 3 of NVDA memo") or a band ("8.0, push to 9.0").
2. **Map to bug class.** Specific challenge → fix that. Band → run gates G1-G14 against the structured memo JSON and identify which fail.
3. **Locate the source.** Find the section in the memo Markdown; find the cell in `outputs/<ticker>_structured.json`.
4. **Fix the math / source / language at the source.** Don't patch the artifact; fix the underlying numbers/structure in the structured JSON or memo Markdown.
5. **Rebuild the artifact.** Re-derive any downstream audience variants per `multi-audience-delivery-us.md` constants block.
6. **Re-verify the gate.** Re-run the relevant verification script(s). If G1, re-run `verify_eps_pe.py`. If G11, re-run `verify_non_gaap.py`. If G13/G14, re-run `verify_quant_overlay.py`.
7. **Report what changed and what gate now passes.** The user is testing whether you patch cleanly or flinch.

## Don't defend the broken version

When a PM points out a bug, the wrong response is to argue for why it's actually OK. The right response is acknowledge → fix → ship. Defending the broken version costs trust faster than the bug itself.

Exception: if the user's challenge is *itself* wrong (e.g., they're miscomputing the multiplication), gently correct with the actual math. But this is rare; usually they're right.

## What 9.0+ actually feels like

When a memo hits 9.0+:

- Reader can re-derive every specific number from the cited source (EDGAR, FRED, Visible Alpha, etc.).
- Reader can challenge any single assumption and immediately find which scenario row or anchor it lives in.
- Reader can predict, before reading the headline, what the headline will say from the anchor strengths in the Source Stratification Box.
- Reader leaves IC able to hold the position through the next earnings without needing to update their mental model.
- All five mandate-type sizings tie back to the same E[R], σ, Sharpe, conviction-adjusted Kelly; differences are mandate-cap and benchmark-driven, not assumption-drift.
- All 14 verification gates exit 0.
- The IC pre-read, IC debate script, and LP letter (per `multi-audience-delivery-us.md`) have identical numbers, only language compressed.

That's the bar. It's high, but achievable in 6-10 rounds with the rubric.

## Cross-references

- **Verification gates schema**: `schemas/verification_gates.json` — G1-G14 definitions.
- **Memo umbrella schema**: `schemas/memo.json` — `forensic_flags`, `quant_overlay`, `gm_taxonomy`, `position_sizing` definitions.
- **Source discipline**: `source-stratification-us.md` — S1-S5 + Pending taxonomy, headline conditionality.
- **GM discipline**: `gm-taxonomy-us.md` — T1-T5 plus non-GAAP/GAAP parallel.
- **Bridge discipline**: `bear-bridge-us.md` — soft/clean/strong layer decomposition.
- **Trigger discipline**: `what-would-reverse-us.md` — numerical denominator rule.
- **A0 discipline**: `tail-risk-mapping-us.md` — 6 standing + 2-3 idiosyncratic + bull tails.
- **Sizing math**: `position-sizing-us.md` — Kelly / conviction / mandate translation.
- **Audience derivatives**: `multi-audience-delivery-us.md` — source-of-truth rule.
- **Monitoring**: `monitoring-framework-us.md` — re-sizing triggers and catalyst calendar.
- **Forensic checklist**: `forensic-accounting-checklist-us.md` — B11/B12 hooks.
- **Open decisions**: D1 (5-band rating), D3 (mandate types), D6 (conviction range), D12 (A0 catalog), D13 (quant overlay mandatory), D20 (score ≥8.5 for Phase E pass).
