# Critical Review — us-equity-research + us-equity-ic-rigor (v0.4.0)

Reviewer lens: senior L/S institutional PM / CIO deciding whether to run a book through this framework. Authored 2026-05-31.

**Method.** Four independent reviewers each read a different slice cold — no shared context, no knowledge of prior findings — covering (1) research process & agent architecture, (2) valuation / scenarios / sizing / risk, (3) evidence / gates / rubric / epistemology, (4) the actual output memos. Their conclusions were then cross-checked against a direct read of the NVDA memo and the five committed output memos (NVDA, JPM, MRK, XOM, DLR) plus their structured JSON. The four reviews converged independently, which raises confidence that the issues below are structural rather than an artifact of one viewpoint.

---

## Verdict

This is an **exceptional editor and a dangerous judge.** As a single-name diligence and red-team discipline it is genuinely strong — the arithmetic floors, the forensic/regulatory dominance hierarchy, the falsification triggers, and the three-method downside flooring are better than most sell-side. But it is mislabeled. It is a **deep single-name long-valuation engine wearing an L/S portfolio costume**, and its central deliverable — a precise 6–10 score — measures whether a memo will *survive an IC meeting*, not whether a *trade will make money*. The framework's own documentation concedes this ("a 9.0 does not mean the view is right"; "no backtest of the 20 gates against historical names"), yet the entire workflow is built to "push from 8.x to 9.x." The result is a machine that reliably manufactures institutional-grade confidence around what is, empirically, the consensus view.

The most damning finding is empirical, not theoretical: **the framework's anti-consensus apparatus has never run on its own output.** All five showcase memos are `schema_version 0.1.0` and pass the 14-gate set; G15 (consensus variance), G18/G19, and G20 (view defensibility) — every gate built across v0.2.0 → v0.4.0 specifically to stop consensus-hugging and verify edge — are not applied to a single committed memo. And those memos are consensus: JPM's base EPS is the Visible Alpha median to the cent, NVDA's is within a cent, two of the five are negative-Kelly "Holds" sized to benchmark. The team has spent four releases hardening gates that have never touched a real memo, while the real memos are exactly the behavior those gates were meant to catch.

---

## Core issues, ranked

### 1. It scores the memo, not the trade — and the score is unbacktested but consumed as confidence. [SEVERE]

`us-equity-ic-rigor/SKILL.md` is explicit: the gates and rubric grade "mechanical correctness and structural completeness… **A 9.0 does not mean the view is right**… not predictive value," and "there is no backtest of the 20 gates against historical names." Yet ≥8.5 is the Phase E *success criterion*, the bands are labeled "IC-grade hardness / IC-ready," and the whole skill is a loop to raise the number. A single 6–10 score with those labels will be read by any PM as a confidence signal no matter the disclaimer. The product sold is "this will survive IC"; the product the reader infers is "this is a good trade." Those are different things under one number, with zero demonstrated correlation to P&L or hit rate. This is the root error from which most of the others follow.

### 2. Consensus is the only yardstick — and empirically the output *is* consensus. [SEVERE]

Edge is defined as `your_number − consensus_number` (`consensus-variance-us.md`), and G20 *requires* the headline to differ from consensus by ≥8pp to score >8.5. Three structural consequences:

- **No consensus-independent anchor exists anywhere.** The "three-method valuation" is explicitly "three lenses on the same business"; the DCF discounts the same scenario EPS paths, which are themselves benchmarked to consensus. There is no from-primitives intrinsic estimate. So **correlated-wrong is undetectable by construction** — if the Street and the analyst share the same flawed prior (the usual case at cycle turns), the framework has no orthogonal ruler to catch it.
- **The ≥8pp rule rewards manufactured differentiation.** An analyst who correctly agrees with a fairly-priced Street is capped at 8.5; one who fabricates an 8pp gap clears the bar. The framework half-knows this (it warns that >60% variance hit-rate means you are manufacturing variances) but the gate still mechanically rewards the behavior.
- **Empirically, the output hugs consensus** (verified, all five v0.1.0 memos):

  | Name | Base EPS | Street median | Rec / base return | PT vs Street |
  |------|----------|---------------|-------------------|--------------|
  | NVDA | $6.50 | VA $6.52 (n=15) | Buy +15–17% | $260 vs DCF $258 / comps $268 |
  | JPM | $22.50 | VA $22.50 (n=22) | Hold +4.6% | $326 vs consensus PT $331–345 |
  | XOM | $7.50 | FactSet $7.60 (n=22) | Hold +4.5% | $112.50, +3.7% |

  These are the Street numbers. The declared "variances" are the known bull/bear case (NVDA: $725B hyperscaler capex — the single most-discussed number in the market; JPM: Basel III disadvantage — the universal bear talking point; XOM: a $0.7B Pioneer synergy that is rounding error on a $7.50 base). And none of it ran the gates designed to flag it.

### 3. "L/S" is cosmetic — shorts are unpriced, the book is invisible, factors are asserted. [SEVERE for an L/S mandate]

- **Short mechanics are never priced into the decision.** Borrow cost / `stock_loan_rate_bps`, days-to-cover, utilization, squeeze and recall risk are captured as *reporting fields* but never subtracted from expected return before Kelly. The Kelly numerator `(E[R] − R_f)` ignores 200–2000bp of carry. A short sized off this framework systematically over-sizes hard-to-borrow names. Capped-upside/unlimited-loss convexity is unmodeled; the "short math" is just a smaller NAV cap.
- **There is no book-level risk.** The correlation overlay is an admitted placeholder (`live_wired: false`, `book_file_path: "n/a"`). There is no contribution-to-risk, no portfolio VaR, no vol target, no netting. Sizing is standalone Kelly, blind to whether the name triples the book's AI/Growth/Momentum beta.
- **Factor exposures are asserted, not regressed — and only reported, not neutralized.** The framework concedes the Barra z-scores "are not regression outputs… directional estimates the analyst asserts," and G13 checks only presence and [-3,+3] range. Yet those guessed z-scores feed a crowding discount that can *halve* a position. Real arithmetic on fabricated inputs, aggregatable into nothing.
- **Sizing is Kelly × a hand-picked fudge factor.** Every memo computes a Kelly fraction, then multiplies by a "conviction multiplier" of **0.125 — the same 0.125 in every name**, "midpoint selected" by assertion, regardless of whether raw Kelly is +52% (NVDA), −0.8% (JPM), or −1.9% (XOM). The Kelly math is decorative; the actual sizing decision is the unexaminable 0.125.

### 4. It is not a portfolio process — no origination, throughput can't sustain a book, no live-book layer. [HIGH]

- **No origination.** Every entry point requires a ticker; screening/funnel is explicitly out of scope (`design/skill-composition.md` marks idea-generation "Skip — we're deep single-name research, not screening"). For a PM, name selection *is* the alpha; this addresses the cheap part of the funnel and ignores the expensive one.
- **Throughput is incompatible with a real book.** ~2 hours of orchestrated execution per name, ~19 specialist dispatches, and compounding web-call floors (FS alone "minimum 60 tool calls"). Rigor is all-or-nothing — no light/maintenance tier. A 60–120 name book cannot be initiated, let alone re-underwritten quarterly, at this cadence.
- **"Monitoring" is one-shot, not position-aware.** Triggers are populated once at build; they fire identically whether you hold 30bp or 300bp; there is no portfolio aggregation layer.

### 5. The gates check form, not correctness — gameable, and there is no "no-opinion" exit. [HIGH]

Of the 20 gates, G1–G5 are arithmetic tautologies, G6–G14/G18 are presence/formatting checks, G15/G20 are differentiation-magnitude checks, G19 is a file hash. **None tests whether a forecast is good.** A motivated analyst passes all 20 by taking the Street number, shading it exactly 8pp, writing one plausible "triangulation point," filling the taxonomy boxes, making the columns multiply, asserting factor z-scores, and staging one rebutted R-v2 attack. Every gate green, score 9.0, view worthless. The NVDA memo is the proof of concept: its headline applies a 40× *non-GAAP* multiple to "$6.50 non-GAAP EPS," while its own §6.0 bridge labels that same $6.50 as **GAAP** and shows non-GAAP at **$6.65** — a mislabeled denominator under the only Buy in the set — and **G1 passes anyway**, because 6.50 × 40 = 260 is arithmetically correct. The gate verifies the multiplication, not the number. Separately, the framework almost never says "no edge / pass" — the only honest exit (consensus-anchored Hold) is framed as a scoring penalty, so a "push to 9.0" workflow always lands on a rateable view, corrupting the base rate that makes selectivity valuable.

### 6. The product does not survive a PM's read. [HIGH]

Judged as finished memos a PM would act on:

- **NVDA** — the GAAP/non-GAAP $6.50 denominator inconsistency sits under the entire valuation; the "edge" is consensus capex the PM already owns elsewhere.
- **JPM** — the memo argues itself into a Hold ("multiple expansion has already happened… roughly fair") and still prints a +8.5% PT below the consensus PT range; **raw Kelly −0.8%**, sized to benchmark.
- **XOM** — a levered WTI bet wearing a synergy costume; +3.7% base; **raw Kelly −1.9%**; the memo concedes "conviction is in the symmetric falsification framework, not in directional return" — i.e., there is no trade.

Negative Kelly means *don't own it*; resolving that to "default to benchmark weight" is incoherent in an L/S book (there is no benchmark weight) and hides the signal the math is giving.

---

## Genuine strengths (calibration — keep these)

1. **The PM-synthesis adjudication hierarchy** (forensic/regulatory dominate and can veto to Hold; industry is base-case; positioning/channel move size not direction) is real cognitive discipline most "AI research" hand-waves.
2. **Arithmetic-integrity + first-use sourcing (G1–G6)** are a cheap, high-value competence floor — they catch the embarrassing, model-killing errors before IC. This layer earns its keep.
3. **What-would-reverse triggers** (numeric threshold + unit + observable channel + date) are genuine falsification discipline a PM can monitor — better than most sell-side.
4. **Three-method downside flooring** (never average; multi-multiple bear floor) genuinely pressure-tests downside rather than rubber-stamping a target.
5. **Intellectual honesty.** The Scope & Limitations sections pre-empt most of these criticisms in writing. That candor is real — but a documented flaw is still a flaw, and in places the honesty *launders* the problem rather than fixing it.

---

## Meta-diagnosis: right philosophy, wrong target

The framework's design instincts — isolated red team, falsification triggers, evidence stratification, adversarial review — are sound. They have simply been pointed at the wrong target. The machinery polices the memo's *internal consistency* and its *deviation from consensus*; it does not test the *view's correctness* or the *portfolio's risk*. So it has become superb at preventing embarrassment and producing publishable artifacts, and structurally incapable of detecting being wrong-with-the-Street or mis-sizing into a book. The recent sprints (v0.2.0–v0.4.0, including the adversarial-isolation work) have deepened the editor while leaving the judge and the portfolio layer unbuilt — and have not been exercised on a single real memo.

---

## What I would require before running capital decisions through it

In priority order:

1. **A consensus-independent estimate.** One agent builds the load-bearing number bottoms-up from primitives *without* seeing the Street figure; the variance is computed against it. Without this, "edge" is undefined and correlated-wrong is invisible. (Highest leverage; addresses Issues 1, 2, 5.)
2. **A real L/S risk layer.** Borrow cost into E[R] before Kelly; a book-level factor/correlation/contribution-to-risk aggregation; short-specific sizing and kill criteria. Replace the universal 0.125 fudge with a risk-budgeted size. (Addresses Issue 3.)
3. **Re-baseline the showcase outputs to current schema** and actually run G15–G20 on them. If the flagship memos fail the consensus-variance and view-defensibility gates (they will), that is the most useful signal the framework can produce about itself. (Addresses Issue 2's empirical core.)
4. **Separate the two products.** Report a "mechanical-integrity: PASS" (the competence floor, honest and useful) distinctly from any "view-quality" claim — and stop emitting a single 6–10 number that conflates them until there is a backtest. (Addresses Issue 1.)
5. **Add an origination front-end and a light maintenance tier**, or scope the tool honestly as a deep-dive for a handful of high-conviction names rather than a book engine. (Addresses Issue 4.)
6. **Add a respectable "no edge / pass" output** so the system can decline, preserving the base rate that makes selectivity worth anything. (Addresses Issue 5.)

---

## Appendix — verified empirical exhibits

- **Showcase memos are pre-gate.** `outputs/{NVDA,JPM,MRK,XOM,DLR}_structured.json` all carry `schema_version: "0.1.0"`; memos report "14 of 14 gates pass" (JPM 13/14, G2 n/a). G15–G20 not run on any.
- **Consensus laundering.** Base EPS = Street median (JPM $22.50 = VA median exactly; NVDA $6.50 vs $6.52; XOM $7.50 vs $7.60).
- **Negative-Kelly Holds.** JPM raw Kelly −0.83%, XOM raw Kelly −1.91%, both ×0.125 → ~0% → "default to benchmark weight." NVDA raw Kelly 52.4% × 0.125 → 6.55% (same multiplier).
- **Gate checks form not correctness.** NVDA §1 calls $6.50 "non-GAAP" and applies a non-GAAP 40× multiple; §6.0 labels $6.50 "GAAP" and shows non-GAAP $6.65. G1 passes (6.50 × 40 = 260).
- **Self-admitted placeholders.** Factor z-scores "asserted, not regression outputs"; correlation overlay `live_wired: false`.
