# FCX IC Memo — PM Red-Team, Round 2 (DE-BIASED rebuild)

**Date:** 2026-06-11 · **Verdict: PASS — 8.7/10 · Rating FLIPPED Hold → SELL/Underweight** · all 19 gates pass (G15 + G20 now affirmatively pass)

## The experiment
Round 1 (v1) rated FCX **Hold, weighted −2.5%, base PT ≈ spot ($66)**. The red-team flagged a construction bias: the base case was anchored to "consensus EPS × the current multiple," which pins fair value to spot and produces a near-zero Hold. v2 re-runs the valuation **leading with an independent, mid-cycle-copper fair value** and lets the rating fall where it lands.

## Result — it flips
| | v1 (spot-anchored) | v2 (fair-value-anchored) |
|---|---|---|
| Base PT | $66.23 (≈ spot) | **$57.09** (independent FV) |
| Base return | +0.05% | **−13.8%** |
| Weighted ER | −2.5% | **−11.0%** |
| Rating | Hold | **Sell / Underweight** |
| Fair value vs spot | (DCF $58 down-weighted) | DCF $58 / NAV $60 / norm-comps $54 → **$57.5, −13%** |
| G15 / G20 | n/a (Hold) | **PASS** (19.3pp consensus differentiation, S1/S2 evidence, variance_attack survived) |

**The single driver of the flip:** v1 applied ~7.7x to **peak-copper** FY27 EBITDA ($13.5B) → $66 = spot; v2 applies the same through-cycle 7.5x to **normalized mid-cycle** EBITDA ($11.5B) → $54, and weights DCF/NAV at the mid-cycle deck. Nothing about the company changed — only the anchor.

## What this proves about the clustering
~8.5pp of the −2.5%→−11.0% swing was **pure construction bias** (spot anchoring + auto-discounting the below-spot DCF). The residual is a genuine judgment call: **how likely is copper to mean-revert vs. stay elevated over 12 months?** v2's base assumes partial reversion (Goldman's 2026-decline call, China property, record supply) — defensible but not certain. If you believe the structural deficit holds copper >$6/lb for 12+ months, the v1 Hold is back in play. The framework now surfaces that as the explicit load-bearing assumption (the `timing_arbitrage` variance_attack) rather than burying it in a spot-anchored base.

## Honest caveats
- The flip is **partly mechanical** (de-biasing) and **partly a real copper view** — separable now, which was the point.
- B2/B3 (modeled segment cash margin) unchanged; the mid-cycle EBITDA normalization is an analyst estimate.
- Sized as **Sell/Underweight + long-SCCO/short-FCX**, not Strong Sell — the structural-deficit timing tail is respected.

*Gate logs: `outputs/FCX_verification_gates.json` · v1 Hold archived: `outputs/archive/FCX_v1_hold/`.*
