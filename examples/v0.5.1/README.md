# Examples — v0.5.1 flagship: MU (Micron Technology)

End-to-end memo run from 2026-06-06 demonstrating the framework's full output across all 20 verification gates, the 5-scenario probabilistic framework, the isolated R-v2 attack, and the PM red-team iteration cycle. This is the framework's most current public example and the artifact to point a skeptical reader at.

## Important disclosure: this is a v0.4.0-era run, not v0.5.1

The MU run was executed on 2026-06-06 against the v0.4.0 plugins, BEFORE the v0.5.1 release shipped the verifier-reachability fix (Sprint 4 Item 8). The user ran Claude Code from a directory where the plugin's verifier scripts at `scripts/verify_*.py` were not on a reachable path. Per the framework's anti-degradation discipline that v0.5.1 adds, the orchestrator should have STOPPED at that point and reported the error. Instead — because this run pre-dated the discipline — it gracefully degraded to LLM-analytical gate evaluation and proceeded.

The manifest documents the degradation honestly:

> "Manifest hand-assembled because plugin scripts/write_manifest.py + schemas/ are absent in working dir; conforms to schemas/manifest.json shape."

And the red-team round 1 document discloses it again:

> "The plugin's scripts/verify_*.py are not present in this build, and the memo was authored via the base us-equity-research workflow ... Gates were therefore evaluated **analytically** against the memo + JSON, not by script execution."

This honest disclosure is what surfaced the bug to the maintainer in the first place. Sprint 4 Item 8's bundled-scripts fix + the SKILL.md anti-degradation preamble (also v0.5.1) prevent this silent degradation going forward. **Future runs from properly-installed v0.5.1+ plugins will execute the actual Python verifier scripts and the gate statuses will reflect script exit codes, not LLM self-assessment.**

This example is committed here despite the lineage because:

1. It is the framework's most analytically complete public output.
2. It demonstrates the red-team iteration mechanism working as designed (formal score went from 7.5 in round 1 to 8.9 in round 2 after structural fixes).
3. The honest disclosure of degradation is itself an artifact worth preserving — the framework's own provenance discipline caught its own packaging defect.
4. The analytical content is independent of how the gate statuses were determined. A v0.5.1+ re-run would change the gate evaluation method but not the underlying analytical work.

## What this example demonstrates

**Output convention.** v0.5.1+ consolidated structured.json (introduced in Sprint 4 Item 9) with `memo_metadata`, `recommendation`, `source_tags`-style inline structure, `scenarios`, `consensus_variance`, `gm_taxonomy`, `bear_eps_bridge`, `what_would_reverse`, `quant_overlay`, `position_sizing`, and `red_team_g20` all in a single file rather than five split sidecars.

**5-scenario probabilistic framework.** strong_bear / bear / base / bull / strong_bull with EPS, multiple, target price, probability, and narrative. Probabilities sum to 1.00. Probability-weighted expected value of $626 vs. $864 spot = −27.5%. Headline rating is SELL (low-moderate conviction 3/5) with explicit derivation from EV per the rubric's rating bands.

**GM taxonomy box (T1-T5).** Consolidated GAAP 74.4% (T1) tagged separately from non-GAAP 74.9% (T1 non-GAAP), segment GMs (T2: CDBU 74.3% / CMBU 74.2% / AEBU 68.3%), modeled normalized 44-45% (T4), marginal/incremental ~90%+ (T5). Every GM mention in the memo carries its tier tag on first use.

**Three-layer bear EPS bridge (soft/clean/strong).** Soft layer (ASP/mix reversion, −$12, reversible) → clean layer (depreciation cliff, −$5, irreversible regardless of demand) → strong layer (HBM4 share/price give-back, −$3, structural). Plus edge-case analysis if ASP holds. Shows the bridge isn't a single driver walk but a layered reversibility story.

**Anchor weighting + A0 tail map.** §7 has the sensitivity table showing how a 10pp probability shift across scenarios moves the EV (most sensitive to strong_bull weight at +$55/10pp; even max-bullish shift leaves EV $681, still 21% below spot). §12 has the A0 tail map with 6 tail events and shifts per scenario that sum to 0.0 per row (mass-conservation, B9).

**Quant overlay with numeric Barra z-scores.** Value −1.5 (trap), Quality −0.5, Momentum +2.7, Growth +1.8, Size +2.5, Low-Vol −2.0, Liquidity +1.5. Plus capacity (ADV $5-10B/day, 0.71/0.36/0.24 days-to-exit at 10/20/30% participation, max_position_constrained_by_adv not binding). Plus buyback-offset-to-SBC ratio ≈ 0.

**Five-mandate position sizing.** Long-only large-cap (UW −30 to −50 bps), long-only SMID (N/A, mega-cap out of universe), L/S HF (small net short via pair, 1.5-2% gross), sector specialty (UW vs SOX, −100 to −150 bps on MU), pair-trade (LONG SK Hynix 000660.KS / SHORT MU, 1:1 beta-neutral, 1-1.5% gross/leg — the recommended highest-conviction structure).

**Isolated R-v2 adversarial attack with model diversity.** R-v2 ran with `attacker_context_isolation: true` and `attacker_model: "claude-sonnet-4-6"` (different from the writer). The attack failed/demoted 5 claims and propagated 2 factual corrections:
- "Insider 10b5-1 selling = bearish" → dropped (10b5-1 plans carry no directional signal)
- "Broadcom selloff = AI capex plateau" → inverted (Broadcom AI revenue grew +143% YoY; selloff was valuation/software, not demand)
- "Deferred tax asset release flattered NI" → refuted by 10-Q Note 15 (14.7% effective rate is Pillar Two, a headwind, not a one-time benefit)

**PM red-team iteration arc.** Round 1 scored the memo at formal **7.5** (G19 cap due to missing manifest) with analytical raw 8.2; identified 4 bottleneck bugs at the 6.5-7.0 band (B4 GM taxonomy box missing, B9 A0 weighting/shift table missing, B6 bear bridge not layered, B13 factor exposure qualitative instead of numeric). Round 2 verified all 4 fixes applied and rescored to **8.9** with the cap lifted. Demonstrates the rubric's "push from N to N+1" mechanism working as designed.

## Files

| File | Size | Content |
|---|---|---|
| `MU_IC_memo.md` | 24K | 13-section institutional IC memo in Markdown |
| `MU_structured.json` | 13K | Consolidated machine-readable representation (memo + source_tags + scenarios + all sub-blocks) |
| `MU_manifest.json` | 5K | Provenance manifest: run_id, phase timing, 40-call web log, 15-agent provenance, output file SHA-256 |
| `MU_redteam_round_1.md` | 10K | PM red-team round 1 — gate sweep, B1-B14 scorecard, push-to-8.5 fix list |
| `MU_redteam_round_2.md` | 6K | PM red-team round 2 — re-evaluation after fixes applied, rescored to 8.9 |

## What this example is NOT

- **Not investment advice.** The analytical work is structural demonstration. The author is not a buy-side employee. Any directional view is a calibration artifact.
- **Not a backtest result.** The 8.9 rubric score grades structural completeness and gate compliance. It does not measure whether the trade made money.
- **Not a fully programmatically-verified run.** The gate statuses were judged analytically by the LLM because the v0.4.0 install path didn't bundle the verifier scripts. v0.5.1+ runs will execute the actual Python scripts. The honest disclosure is preserved in the manifest and round 1 doc.
- **Not the only example.** See `examples/` parent directory for the v0.1.x calibration set (NVDA, JPM, MRK, XOM, DLR) that was used for the original Phase E framework calibration. Those memos exercise only G1-G14 and are explicitly grandfathered.

## Re-running

To produce a fresh v0.5.1+ run with programmatically-verified gates:

```
/plugin install us-equity-research@us-equity-research
/plugin install us-equity-ic-rigor@us-equity-research
```

Then in a Claude Code session run from the cloned repo (so `${CLAUDE_PLUGIN_ROOT}/scripts/...` resolves):

```
/us-equity-ic-rigor:ic-memo MU
```

The v0.5.1+ orchestrator will execute the verifier scripts, write a real manifest via `write_manifest.py`, and produce a `MU_verification_gates.json` with `evaluation_method: "programmatic_script"` per gate.

## Reproducibility caveats

The framework has non-deterministic agent dispatch (LLM sampling variance, WebSearch result ranking variance). Two runs on the same ticker on the same day produce different memos. The verification gates verify structural consistency, not run-to-run reproducibility. A fresh MU run today would produce a different but structurally-compliant memo, possibly with a different rating, different probability weights, and different anchor tags. Treat the score (8.9) and rating (SELL) as exemplary, not canonical.

## Why this is the flagship

The deep-research report of v0.4.0 published 2026-06-06 criticized the framework: *"the modern framework is described as if validated, but the public examples are explicitly pre-modern."* The MU run answers that critique directly. It exercises G15 (consensus variance), G17 (revision velocity), G19 (provenance manifest with hand-assembled disclosure), and G20 (view defensibility with isolated R-v2). It demonstrates the red-team iteration arc. It is honest about its degradation. It is the public artifact that v0.4.0's design claimed but did not previously have.
