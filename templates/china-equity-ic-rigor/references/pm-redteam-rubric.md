# PM red-team rubric

## What this is

A scoring rubric and bug catalog calibrated against ~23 actual rounds of PM-style red-team review across two memos (光威复材 300699 Round 1-13, 京东方A 000725 Round 1-10). Use this when:

- You're red-teaming your own (or another model's) draft
- The user gives you a numerical score and asks "what would push this from 8.x to 9.x"
- You're deciding whether a memo is IC-ready

The rubric is intentionally tight — it tracks what actually moves PM scores in practice, not aspirational quality dimensions.

## Score bands

### 6.0–7.5 — structural / mechanical bugs

The memo has at least one of these failures:

- **Math doesn't reconcile**: EPS × PE ≠ price in scenario table; segment GM × revenue ≠ consolidated GP; SOTP NI > GP; bear bridge doesn't sum.
- **Sourcing absent**: specific numbers (revenue figures, GM percentages, share figures) appear without S1-S5 tags.
- **Headline-anchor mismatch**: unconditional headline on weak (S3-S5) anchors.
- **Internal contradiction**: same number cited differently in two places (e.g. seg GM 17% in §3, 18% in §6 with no reconciliation).

These are mechanical bugs. They should never get past 7.5 until fixed. Fix them before any narrative-level critique.

**To get to 7.5+**: run all verification gates from SKILL.md; fix every gate failure; re-run.

### 7.5–8.5 — narrative coherence + scenario discipline

Math passes. Now the issues are analytical:

- **Scenario probabilities lazy** (10/20/40/20/10 default not justified by anchors)
- **Anchor weighting impact table missing** — PM can't see how sensitive headline is to one probability shift
- **GM taxonomy not declared** — terms like "毛利率" used without specifying T1/T2/T3
- **Bear bridge missing layers** — bear EPS shown without soft/clean/strong decomposition
- **What-would-reverse triggers without numerical denominators**
- **Anchor sensitivity not shown** — reader can't tell which anchor moves headline most

**To get to 8.5+**: add the missing structures (taxonomy box, anchor weighting, layered bridge, denominators on triggers).

### 8.5–9.0 — IC-grade hardness

Structures are in place. Issues are sharper:

- **A0 tail mapping incomplete** — bear tails listed but no bull tails; or shifts don't sum to zero
- **Three-method valuation reconcile missing** — only EPS×PE, no SOTP cross-check, no multi-multiple floor
- **Source-conditional language inconsistent** — top anchors have S3 elements but headline is unconditional
- **Cross-section consistency**: numbers in one section don't quite match another (within rounding but not reconciled)
- **Position sizing skipped** — Sharpe and Kelly mentioned but not translated to specific position
- **Action mapping vague** — "减仓" without specifying how much (-25%? -50%?)

**To get to 9.0+**: add the missing hardness (full A0, three-method reconcile, conditional language, position sizing math, specific action).

### 9.0+ — IC-ready

All gates passed. All structures present. Issues are subtle:

- **Edge-case completeness** — does the bear bridge handle the case where soft adjustments cancel each other?
- **Forward-looking inflation guard** — are forward EPS years consistent across all tables?
- **Audience derivative consistency** — do the IC pre-read numbers exactly match institutional?
- **Catalyst calendar present** — does the memo tell the reader when to look for trigger updates?

These are polish-level fixes. The memo is defensible at 9.0 even without them.

## Common bug catalog (in order of frequency observed)

### B1 — EPS × PE column doesn't multiply

The most common bug. Modeler computes scenario prices by reverse-engineering from a target return rather than EPS × PE.

**Detection**: for each row, multiply EPS × PE; compare to listed price; flag any divergence >¥0.05.

**Fix**: rebuild the scenario table starting from EPS path × PE assumptions; let the price column be the output.

**Real instance**: BOE Round 2 — every scenario row failed this; major rebuild.

### B2 — Segment GM × revenue ≠ consolidated GP

Modeler quotes segment GMs from notes and consolidated GM from income statement; doesn't verify they reconcile.

**Detection**: compute Σ(segment_revenue × segment_GM) / Σ(segment_revenue); compare to consolidated GM.

**Fix**: add 其他/未分配 row for unallocated; or fix the segment assumption that's wrong.

**Real instance**: BOE Round 6 — added explicit reconciliation table showing 1,330×17% + 420×9% + 220×19% + 76×22% = ¥322.4亿 / 2,046 = 15.8% ≈ reported 15.5%.

### B3 — SOTP NI > GP

Modeler estimates segment NI directly without going through the GP→OP→NI mechanical chain.

**Detection**: in SOTP table, check NI ≤ OP ≤ GP ≤ Revenue.

**Fix**: rebuild SOTP bottom-up via column sequence Revenue → GM → GP → SG&A → OP → Tax → NI.

**Real instance**: 300699 Round 11 — rebuilt entire SOTP.

### B4 — Mixed GM definitions

Memo uses "毛利率" for T1 in one place, T2 in another, T3 in another. PM challenge: "Are you saying GM is 8% or 18% or 35%?"

**Detection**: scan for every "毛利率" instance; tag each with its type.

**Fix**: insert GM taxonomy box (see `gm-taxonomy.md`); tag every instance at first mention.

**Real instance**: BOE Round 7 — inserted §6.0 taxonomy box.

### B5 — Headline unconditional on weak anchors

Top-3 anchors are S3-S5 but headline reads as confident point estimate.

**Detection**: classify top-3 anchors; check headline language.

**Fix**: rewrite headline using one of the 4 source-conditional patterns (see `source-stratification.md` §3).

**Real instance**: BOE Round 10 — converted to "source-conditional 中性轻偏多".

### B6 — Bear EPS not bridged

Bear EPS appears as a number with no decomposition.

**Detection**: search for bear EPS / 强空 EPS; look for bridge table immediately adjacent.

**Fix**: build three-layer bridge per `bear-bridge.md`.

**Real instance**: 300699 Round 9.

### B7 — What-would-reverse without denominator

Triggers are directional ("if margins recover") not numerical ("≥18.5% on revenue ≥X").

**Detection**: read each trigger; check for specific number AND denominator base.

**Fix**: rewrite triggers per `what-would-reverse.md`.

**Real instance**: 300699 Round 7-8.

### B8 — Cross-version stale numbers

Earlier round number persists in a section that wasn't updated.

**Detection**: search for old version's headline number; verify all instances updated.

**Fix**: global search-and-replace; verify by reading relevant sections.

**Real instance**: BOE Round 3 (multiple stale targets), 300699 Round 5-6.

### B9 — A0 tail prob shifts don't sum to zero

Modeler shifts probability but doesn't conserve mass.

**Detection**: for each A0 row, sum the probability shifts; should be 0.

**Fix**: re-balance the shifts.

### B10 — Position sizing absent

Sharpe and Kelly mentioned conceptually but not translated to a specific position size.

**Detection**: search for "Sharpe" / "Kelly" / "仓位"; verify a specific % allocation appears.

**Fix**: add position sizing per `position-sizing.md`.

## Score-to-fix lookup

| Reported score | Most likely bug class | Action |
|---|---|---|
| 6.0–6.5 | B1, B2, B3 (mechanical) | run verification scripts |
| 6.5–7.5 | B1-B5 mix | scripts + headline review |
| 7.5–8.0 | B5, B6 | source-conditional rewrite + bridge add |
| 8.0–8.5 | B4, B7, B8 | taxonomy + denominators + stale sweep |
| 8.5–8.8 | B9, B10 | A0 completeness + position sizing |
| 8.8–9.0 | polish | catalyst calendar + audience derivative consistency |
| 9.0+ | edge cases | only matters if going public-facing |

## Working a red-team round end-to-end

1. **Read the user's challenge or score**. Identify whether it's a specific item ("EPS × PE wrong in row 3") or a band ("8.0").
2. **Map to bug class**. Specific challenge → fix that. Band → run gates and identify which fail.
3. **Locate the source**. Find the build script (typically `build_<ticker>_truly_honest.js` or equivalent), find the section.
4. **Fix the math/source/language at the source**. Don't patch the artifact; fix the build.
5. **Rebuild the artifact**. Run `node build_*.js`.
6. **Verify the fix passed the gate**. If it's a math fix, re-run `verify_eps_pe.py`. If it's source-conditional, re-read the headline.
7. **Report what changed and what gate now passes**. The user is testing whether you patch cleanly or flinch.

## Don't defend the broken version

When a PM points out a bug, the wrong response is to argue for why it's actually OK. The right response is acknowledge → fix → ship. Defending the broken version costs trust faster than the bug itself.

The exception: if the user's challenge is *itself* wrong (e.g. they're miscomputing the multiplication), gently correct them with the actual math. But this is rare; usually they're right.

## What 9.0+ actually feels like

When a memo hits 9.0+, the experience is:

- Reader can re-derive every specific number from sources
- Reader can challenge any single assumption and immediately find which scenario row it lives in
- Reader can predict, before reading the headline, what the headline will say from the anchor strengths
- Reader leaves IC able to hold the position through the next earnings without needing to update mental model

That's the bar. It's high, but achievable in 6-10 rounds with the rubric.
