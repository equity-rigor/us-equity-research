---
description: Build a buy-side IC memo on a US-listed ticker — runs Phase 0 (delegated to us-equity-research) → Phases 1-3 (S1-S5 source stratification, 5-scenario probabilistic framework, three-method valuation reconcile, GM taxonomy T1-T5, bear EPS bridge) → enforces all 20 verification gates (G1-G20) → produces institutional-grade Markdown memo + consolidated structured JSON + provenance manifest
argument-hint: "[ticker] [optional: thesis direction long/short/pair]"
allowed-tools:
  - Read
  - Write(outputs/**)
  - Edit(outputs/**)
  - WebSearch
  - WebFetch(domain:data.sec.gov)
  - WebFetch(domain:www.sec.gov)
  - WebFetch(domain:efts.sec.gov)
  - WebFetch(domain:fred.stlouisfed.org)
  - WebFetch(domain:api.fred.stlouisfed.org)
  - WebFetch(domain:www.bls.gov)
  - WebFetch(domain:www.bea.gov)
  - WebFetch(domain:www.eia.gov)
  - WebFetch(domain:home.treasury.gov)
  - WebFetch(domain:www.federalreserve.gov)
  - WebFetch(domain:www.fdic.gov)
  - WebFetch(domain:www.occ.gov)
  - WebFetch(domain:www.ftc.gov)
  - WebFetch(domain:www.justice.gov)
  - WebFetch(domain:ofac.treasury.gov)
  - WebFetch(domain:www.bis.doc.gov)
  - WebFetch(domain:finance.yahoo.com)
  - WebFetch(domain:query1.finance.yahoo.com)
  - WebFetch(domain:stockanalysis.com)
  - WebFetch(domain:www.wsj.com)
  - WebFetch(domain:www.bloomberg.com)
  - WebFetch(domain:www.reuters.com)
  - WebFetch(domain:www.ft.com)
  - WebFetch(domain:seekingalpha.com)
  - WebFetch(domain:www.fool.com)
  - WebFetch(domain:web.archive.org)
  - Bash(mkdir -p outputs)
  - Bash(mkdir -p outputs/*)
  - Bash(cat outputs/*)
  - Bash(cat outputs/**)
  - Bash(ls outputs/)
  - Bash(ls outputs/*)
  - Bash(python3 -m json.tool *)
  - Bash(python3 scripts/verify_*)
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/verify_*)
  - Bash(python3 scripts/write_manifest.py *)
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest.py *)
  - Task
---

Load the `us-equity-ic-rigor` skill and begin the IC memo build pipeline on the ticker provided.

If a ticker is provided as the first argument, use it. Otherwise ask the user which name and what thesis direction (long, short, or pair-trade structure).

Workflow per `SKILL.md` Phases 0-3:

**Phase 0** — delegate to `us-equity-research` (run `/us-equity-research:research {TICKER}` first if those outputs don't already exist in `outputs/`). Phase 0 produces raw research; do not skip.

**Phase 1** — source stratification gate. Every specific number must be classified S1 (audited 10-K/20-F), S2 (unaudited filing: 10-Q/8-K/DEF 14A/S-1/13D/13F/Form 4/6-K), S3 (earnings call transcript / mgmt guidance / Investor Day), S4 (sell-side consensus median + dispersion — not mean), S5 (alt-data/expert network with provider + methodology + sample + freshness), or Pending (do NOT promote to headline anchor). G7 hard rule: if any of the top-3 anchors is S3 or weaker, headline must be source-conditional.

**Phase 2** — five-scenario probabilistic framework (strong_bear / bear / base / bull / strong_bull). Probabilities must sum to 1.00 (G4 enforces). Bear bridge must reconcile to base via line-item delta walk (G5).

**Phase 3** — three-method valuation reconcile: DCF + Comps + multi-multiple bear floor + SOTP (per D8 sector branching — P/E mature, EV/EBITDA leveraged, EV/ARR + Rule of 40 SaaS, P/B + ROE banks, P/AFFO + NAV REITs, NPV pipeline biotech, P/AUM asset managers). EPS × multiple rows must multiply exactly (G1). Segment GM must reconcile to consolidated within tolerance per `gm-taxonomy-us.md` (G2 — ±50bp industrials, ±5bp banks NIM per D24). SOTP NI ≤ Pre-Tax ≤ PPNR ≤ Total Revenue (G3 monotonicity). Mandatory quant overlay per D13 — Barra factor exposure (Value/Quality/Momentum/Growth/Size/Low-Vol/Liquidity) per G13, capacity/days-to-exit at 10/20/30% ADV per G14. v0.2.0+ also requires consensus variance disclosure (G15), bank discipline if sector=Banks (G16), and revision velocity (G17). v0.3.0+ requires quant cross-doc consistency (G18), provenance manifest (G19), and view defensibility (G20) for any score claim above 8.5.

**Output (v0.5.0+ consolidated convention)**: at the end of Phase 3, write these files to `outputs/`:

- `{TICKER}_IC_memo.md` — institutional Markdown memo, English-only per D4
- `{TICKER}_structured.json` — consolidated structured representation containing `memo_metadata`, `recommendation`, `source_tags`, `scenarios`, `consensus_variance`, `quant_overlay`, `gm_taxonomy`, `bear_eps_bridge`, `what_would_reverse`, `position_sizing`, and any other domain-specific blocks (banks, biotech, REITs). All sub-objects live inline in this single JSON file rather than in separate sidecar files.
- `{TICKER}_manifest.json` — provenance manifest written by `${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest.py` containing run_id, phase_timing, agent_provenance (≥15 agents per D9), web_search_log (≥12 entries per D9), verification_calls_count, output file SHA-256 hashes, attacker_model + isolation flag for R-v2.

(The prior v0.4.x convention of separate `_source_tags.json` and `_scenarios.json` sidecar files is grandfathered for backward compatibility; v0.5.0+ memos use the consolidated structure.)

After the Markdown + structured JSON + manifest are written, run all 20 verification gate scripts (`${CLAUDE_PLUGIN_ROOT}/scripts/verify_*.py`) against the structured JSON. Write the gate-run audit trail to `outputs/{TICKER}_verification_gates.json` conforming to `${CLAUDE_PLUGIN_ROOT}/schemas/verification_gates.json`. Report pass/fail per gate. If any gate fails, fix and re-run before declaring the memo done.

If a verifier script cannot be reached (file not found, permission denied, import error), DO NOT degrade to LLM-analytical gate evaluation. STOP, report the error to the user with the exact command and exact error message, and follow the SKILL.md anti-degradation preamble protocol.

Then prompt the user: "Run /us-equity-ic-rigor:red-team {TICKER} to score this memo against the PM rubric?"

Optional artifact delegation (per D21) — if `claude-for-financial-services/equity-research` is installed, offer to dispatch `equity-research:initiating-coverage` Task 5 for a polished 30-50pg DOCX; if `claude-for-financial-services/financial-analysis` is installed, offer `financial-analysis:dcf-model` for Excel DCF and `financial-analysis:comps-analysis` for Excel comps.
