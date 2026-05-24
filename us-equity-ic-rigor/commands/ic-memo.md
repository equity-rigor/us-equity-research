---
description: Build a buy-side IC memo on a US-listed ticker — runs Phase 0 (delegated to us-equity-research) → Phases 1-3 (S1-S5 source stratification, 5-scenario probabilistic framework, three-method valuation reconcile, GM taxonomy T1-T5, bear EPS bridge) → enforces all 14 verification gates (G1-G14) → produces institutional-grade Markdown memo + structured JSON
argument-hint: "[ticker] [optional: thesis direction long/short/pair]"
---

Load the `us-equity-ic-rigor` skill and begin the IC memo build pipeline on the ticker provided.

If a ticker is provided as the first argument, use it. Otherwise ask the user which name and what thesis direction (long, short, or pair-trade structure).

Workflow per `SKILL.md` Phases 0-3:

**Phase 0** — delegate to `us-equity-research` (run `/us-equity-research:research {TICKER}` first if those outputs don't already exist in `outputs/`). Phase 0 produces raw research; do not skip.

**Phase 1** — source stratification gate. Every specific number must be classified S1 (audited 10-K/20-F), S2 (unaudited filing: 10-Q/8-K/DEF 14A/S-1/13D/13F/Form 4/6-K), S3 (earnings call transcript / mgmt guidance / Investor Day), S4 (sell-side consensus median + dispersion — not mean), S5 (alt-data/expert network with provider + methodology + sample + freshness), or Pending (do NOT promote to headline anchor). G7 hard rule: if any of the top-3 anchors is S3 or weaker, headline must be source-conditional.

**Phase 2** — five-scenario probabilistic framework (strong_bear / bear / base / bull / strong_bull). Probabilities must sum to 1.00 (G4 enforces). Bear bridge must reconcile to base via line-item delta walk (G5).

**Phase 3** — three-method valuation reconcile: DCF + Comps + multi-multiple bear floor + SOTP (per D8 sector branching — P/E mature, EV/EBITDA leveraged, EV/ARR + Rule of 40 SaaS, P/B + ROE banks, P/AFFO + NAV REITs, NPV pipeline biotech, P/AUM asset managers). EPS × multiple rows must multiply exactly (G1). Segment GM must reconcile to consolidated within tolerance per `gm-taxonomy-us.md` (G2 — ±50bp industrials, ±5bp banks NIM per D24). SOTP NI ≤ Pre-Tax ≤ PPNR ≤ Total Revenue (G3 monotonicity). Mandatory quant overlay per D13 — Barra factor exposure (Value/Quality/Momentum/Growth/Size/Low-Vol/Liquidity) per G13, capacity/days-to-exit at 10/20/30% ADV per G14.

**Output**: `outputs/{TICKER}_IC_memo.md` (institutional Markdown, English-only per D4) + `outputs/{TICKER}_structured.json` + `outputs/{TICKER}_scenarios.json` + `outputs/{TICKER}_source_tags.json` + `outputs/{TICKER}_verification_gates.json`.

After Phase 3 completes, run all 14 verification gates (`scripts/verify_*.py`) and report pass/fail per gate. If any gate fails, fix and re-run before declaring the memo done. Then prompt the user: "Run /us-equity-ic-rigor:red-team {TICKER} to score this memo against the PM rubric?" Optional artifact delegation (per D21) — if `claude-for-financial-services/equity-research` is installed, offer to dispatch `equity-research:initiating-coverage` Task 5 for a polished 30-50pg DOCX; if `claude-for-financial-services/financial-analysis` is installed, offer `financial-analysis:dcf-model` for Excel DCF and `financial-analysis:comps-analysis` for Excel comps.
