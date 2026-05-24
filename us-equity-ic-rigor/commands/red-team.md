---
description: PM red-team an existing IC memo — runs all 14 verification gates (G1-G14) against outputs/{TICKER}_*.json, scores the memo against pm-redteam-rubric-us.md (1-10 scale, B1-B14 bug categories), produces gate-failure list + score-band assessment + push-from-N-to-N+1 actionable fixes
argument-hint: "[ticker] [optional: target score, e.g. 8.5 or 9.0]"
---

Load the `us-equity-ic-rigor` skill and run Phase 4 (PM red-team) on the existing memo for the ticker provided.

If a ticker is provided, look for `outputs/{TICKER}_IC_memo.md` + `outputs/{TICKER}_structured.json` + `outputs/{TICKER}_scenarios.json` + `outputs/{TICKER}_source_tags.json` + `outputs/{TICKER}_verification_gates.json`. If any are missing, instruct the user to run `/us-equity-ic-rigor:ic-memo {TICKER}` first — DO NOT silently re-run Phase 0-3.

If a target score is provided (e.g. "8.5" or "9.0"), use it as the gate threshold. Otherwise default to ≥8.5 per D20.

Workflow per `references/pm-redteam-rubric-us.md` Phase 4:

**Step 1 — Mechanical gate sweep**: Run all 14 `scripts/verify_*.py` against the structured JSON outputs. Report pass/fail per gate with the specific line/section that failed. The 14 gates:

- G1 — EPS × multiple rows multiply exactly (no rounding lies)
- G2 — Segment GM reconciles to consolidated within tolerance (±50bp industrials / ±5bp banks NIM per D24)
- G3 — SOTP monotonicity (NI ≤ Pre-Tax ≤ OP ≤ GP for industrials; NI ≤ Pre-Tax ≤ PPNR ≤ Total Revenue for banks per D24)
- G4 — Scenario probabilities sum to exactly 1.00
- G5 — Bear EPS bridge reconciles to base via line-item delta walk
- G6 — No unsourced specifics (every number tagged S1-S5 or Pending)
- G7 — Headline conditionality: if any top-3 anchor is S3 or weaker, headline must be source-conditional
- G8 — No mixed GM definitions (consolidated vs segment vs adj-ex-one-time used consistently within a row)
- G9 — What-would-reverse triggers have numerical denominators (not "deterioration in X" but "X declines >Y% over Z quarters")
- G10 — Anchor weighting impact table present (shows how anchor failure shifts target price)
- G11 — Non-GAAP figures accompanied by GAAP reconciliation (US-specific)
- G12 — SBC included in FCF or flagged explicitly excluded (US-specific)
- G13 — Barra factor exposure stated (Value/Quality/Momentum/Growth/Size/Low-Vol/Liquidity)
- G14 — Capacity / ADV / days-to-exit at 10/20/30% participation stated

**Step 2 — Rubric score**: Score the memo 1-10 across all B1-B14 bug categories from `pm-redteam-rubric-us.md`. Report the lowest-scoring band as the bottleneck. Memo passes iff overall ≥ target (default 8.5).

**Step 3 — Push-from-N-to-N+1 fixes**: For each bug category scoring below target, produce a specific actionable edit (filename, line number, before/after diff). Order by score-gain-per-effort.

**Output**: write `outputs/{TICKER}_redteam_round_{N}.md` (N = round number, increments each call) with: gate sweep table, rubric scorecard, bottleneck identification, ordered fix list. Do not modify the original memo — that is the user's call after reviewing.

This is a red-team, not a cheerleader. If the memo is mechanically broken (gates failing), say so plainly. If the memo is mechanically clean but the thesis is weak (no edge attribution, consensus reproduction, hand-wavy catalysts, S4-anchored bull thesis), say that too — those are not gate failures but they are real PM kill triggers.
