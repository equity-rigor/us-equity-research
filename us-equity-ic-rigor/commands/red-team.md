---
description: PM red-team an existing IC memo — runs all 20 verification gates (G1-G20) against outputs/{TICKER}_structured.json, scores the memo against pm-redteam-rubric-us.md (1-10 scale, B1-B17 bug categories), produces gate-failure list + score-band assessment + push-from-N-to-N+1 actionable fixes
argument-hint: "[ticker] [optional: target score, e.g. 8.5 or 9.0]"
allowed-tools:
  - Read
  - Write(outputs/**)
  - Edit(outputs/**)
  - Bash(cat *)
  - Bash(ls *)
  - Bash(python3 *)
  - Bash(python *)
  - Bash(grep *)
  - Bash(head *)
  - Bash(tail *)
  - Task
---

Load the `us-equity-ic-rigor` skill and run Phase 4 (PM red-team) on the existing memo for the ticker provided.

If a ticker is provided, look for `outputs/{TICKER}_IC_memo.md` + `outputs/{TICKER}_structured.json` + `outputs/{TICKER}_manifest.json` (v0.5.0+ consolidated convention). For grandfathered v0.4.x memos, also accept the split-file form with separate `outputs/{TICKER}_scenarios.json` + `outputs/{TICKER}_source_tags.json` sidecar files. If any required file is missing, instruct the user to run `/us-equity-ic-rigor:ic-memo {TICKER}` first — DO NOT silently re-run Phase 0-3.

If a target score is provided (e.g. "8.5" or "9.0"), use it as the gate threshold. Otherwise default to ≥8.5 per D20.

Workflow per `references/pm-redteam-rubric-us.md` Phase 4:

**Step 1 — Mechanical gate sweep**: Run all 20 `${CLAUDE_PLUGIN_ROOT}/scripts/verify_*.py` against the structured JSON outputs. Report pass/fail per gate with the specific line/section that failed. The 20 gates:

- G1 — EPS × multiple rows multiply exactly (no rounding lies)
- G2 — Segment GM reconciles to consolidated within tolerance (±50bp industrials / ±5bp banks NIM per D24)
- G3 — SOTP monotonicity (NI ≤ Pre-Tax ≤ OP ≤ GP for industrials; NI ≤ Pre-Tax ≤ PPNR ≤ Total Revenue for banks per D24)
- G4 — Scenario probabilities sum to exactly 1.00
- G5 — Bear EPS bridge reconciles to base via line-item delta walk
- G6 — No unsourced specifics (every number tagged S1-S5 or Pending)
- G7 — Headline conditionality: if any top-3 anchor is S3 or weaker, headline must be source-conditional
- G8 — No mixed GM definitions (consolidated vs segment vs adj-ex-one-time used consistently within a row); GM taxonomy box T1-T5 present
- G9 — What-would-reverse triggers have numerical denominators (not "deterioration in X" but "X declines >Y% over Z quarters")
- G10 — Anchor weighting impact table present + A0 tail map shifts sum to zero per tail event
- G11 — Non-GAAP figures accompanied by GAAP reconciliation (US-specific, B11)
- G12 — SBC included in FCF or flagged explicitly excluded + buyback-offset-to-SBC ratio (US-specific, B12)
- G13 — Barra factor exposure stated as numeric z-scores (Value/Quality/Momentum/Growth/Size/Low-Vol/Liquidity, B13)
- G14 — Capacity / ADV / days-to-exit at 10/20/30% participation stated + max_position_constrained_by_adv (B14)
- G15 — Consensus variance declared with sized scenario impact OR headline self-labels "consensus-anchored" (v0.2.0, B15)
- G16 — Bank discipline (AOCI + CET1 + NIM + stress capital) when sector=Banks (v0.2.0, B16)
- G17 — Earnings revision velocity disclosed when n_analysts ≥ 5 (v0.2.0, B17)
- G18 — Quant overlay cross-document consistency: prose factor mentions match structured block ±0.2 (v0.3.0)
- G19 — Plugin 1 → Plugin 2 provenance manifest with SHA-256 file-hash integrity (v0.3.0; caps memo at 7.5 on fail or hand_authored=true)
- G20 — View defensibility: for any score >8.5, three conjunctive conditions (differentiation magnitude ≥8pp, S1/S2 evidence on load-bearing variance, surviving variance_attack with isolation + model diversity); v0.4.0 graduated rigor for >9.0 (v0.3.0+)

If a verifier script cannot be reached (file not found, permission denied, import error), DO NOT degrade to LLM-analytical gate evaluation. STOP, report the error to the user with the exact command and exact error message, and follow the SKILL.md anti-degradation preamble protocol.

**Step 2 — Rubric score**: Score the memo 1-10 across all B1-B17 bug categories from `pm-redteam-rubric-us.md`. Report the lowest-scoring band as the bottleneck. Memo passes iff overall ≥ target (default 8.5). Mechanical-math gate failures (G1, G3, G15, G16) cap the score at 7.0; revision velocity (G17) caps at 7.5; provenance (G19) caps at 7.5 on fail or hand_authored=true; view defensibility (G20) caps at 8.5 on fail.

**Step 3 — Push-from-N-to-N+1 fixes**: For each bug category scoring below target, produce a specific actionable edit (filename, line number, before/after diff). Order by score-gain-per-effort.

**Output**: write `outputs/{TICKER}_redteam_round_{N}.md` (N = round number, increments each call) with: gate sweep table (all 20 gates including grandfathered status for older schema versions), rubric scorecard (B1-B17), bottleneck identification, ordered fix list. Do not modify the original memo — that is the user's call after reviewing.

This is a red-team, not a cheerleader. If the memo is mechanically broken (gates failing), say so plainly. If the memo is mechanically clean but the thesis is weak (no edge attribution, consensus reproduction, hand-wavy catalysts, S4-anchored bull thesis), say that too — those are not gate failures but they are real PM kill triggers.
