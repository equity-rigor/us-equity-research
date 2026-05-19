# us-equity-research / us-equity-ic-rigor — Build Log

**Purpose**: project state document for `/clear` safety mid-Phase-E. Conversation history is not load-bearing — all state is on disk. Any new orchestrator session can pick up Phase E or Phase F by reading this file + the referenced design / schema / reference files.

**Branch**: `build-us-equity-skill`. **Main branch for eventual PR**: `main`. Current HEAD at time of write: `324ad78 phase D S-D-4: verify_quant_overlay.py (G13+G14, owns B13+B14)`.

**Repo path**: `/Users/hongyi/projects/us-equity-research/`.

---

## Phase A→D commit history (one-line)

```
324ad78 phase D S-D-4: verify_quant_overlay.py (G13+G14, owns B13+B14)
86ce59c phase D S-D-2: verify_non_gaap.py (G11, owns B11)
16e70ef phase D S-D-1: quant-overlay-us.md (G13/G14 scope authority)
937960c phase D S-D-3: verify_fcf_definition.py (G12, owns B12)
43e2fd0 phase C.1: CLI contract normalization + G2 scope codification
5718961 phase C S-C-7: verify_headline_conditionality.py
d4948da phase C S-C-2: verify_segment_gm.py
5762e59 phase C S-C-6: verify_source_tags.py
315692c phase C S-C-10: verify_weighting_sensitivity.py
8c01789 phase C S-C-8: verify_gm_taxonomy.py
410c26c phase C S-C-9: verify_what_would_reverse.py
dac641b phase C S-C-3: verify_sotp_monotonicity.py
84ca010 phase C S-C-5: verify_bear_bridge.py
3b5d8d4 phase C S-C-1: verify_eps_pe.py
0e04f85 phase C S-C-4: verify_scenario_weights.py
6ffa603 phase C0: NVDA fixture set (clean + 14 single-bug)
05ecf11 phase B2.1: anchor stability fix + phase-file headroom
afb0b04 phase B2: reference + template scaffolding (24 files)
f2e61de phase B1: skill scaffolding (5 files)
3dffced phase B0: shared contracts with conformance audit
0be35bc phase A.1: composition strategy with marketplace plugins
df629c5 phase A: hypothesis tree + data spec
e551d32 scaffold: import templates and build prompt
4c428b4 import china equity skill templates as starting point
```

---

## Standing context block (DO NOT redefine; reference by ID only)

- **14 verification gates**: G1-G14 per `schemas/verification_gates.json` `gate_definitions`. G11-G14 are US-specific (non-GAAP/GAAP reconciliation, SBC-in-FCF, Barra factor exposure, capacity/ADV/days-to-exit).
- **14 bug classes**: B1-B14, catalog in `us-equity-ic-rigor/references/pm-redteam-rubric-us.md`. B11-B14 mirror G11-G14.
- **23 decisions**: D1-D23 in `design/open-decisions.md`. D22 = 4-schema decomposition. D23 = reference-folder gitignore. **If a Phase E ambiguity surfaces requiring a NEW decision, tag as "PROPOSED D24" and stop.**
- **5-band rating** per D1: Strong Buy / Buy / Hold / Sell / Strong Sell with ±10% / ±20% bands.
- **5 scenarios** per `schemas/scenarios.json`: strong_bear / bear / base / bull / strong_bull.
- **5 mandate types** per D3: long_only_large_cap / long_only_smid / long_short_hedge_fund / sector_specialty / pair_trade.
- **6 S-levels** per `schemas/source_tags.json`: S1 / S2 / S3 / S4 / S5 / Pending.
- **5 GM types**: T1_consolidated / T2_segment / T3_sub_segment / T4_analyst_modeled / T5_marginal per `us-equity-ic-rigor/references/gm-taxonomy-us.md`.
- **6 standing A0 tail events** per D12: NBER recession / Fed rate shock / sector regulatory / sanctions-export / tariff-trade / election-political (+ 2-3 idiosyncratic per name).
- **Citation regex** per D16: `\((S[1-5]|Pending):.+?\)` at first appearance.
- **Min 12 WebSearch+WebFetch calls** per memo per D9.
- **EDGAR-only default** per D5; premium hooks opt-in.
- **Markdown is the only mandatory output** per D15; Excel/DOCX optional delegation.
- **3-phase workflow preserved 1:1 from China** per D7: Phase 0 → Phase 1 (5 specialists parallel) → Phase 1.5 refresh if needed → Phase 2 (5 deepening specialists) → Phase 3 (4 valuation + final) → Verification → Final IC Memo.
- **G2 scope**: LTM/forward only; historical-period segment reconciliation is informational only (corporate allocation, "Other / Unallocated" buckets, source-filing rounding). Per `us-equity-ic-rigor/references/gm-taxonomy-us.md` G2-scope paragraph (canonical) and `us-equity-ic-rigor/references/pm-redteam-rubric-us.md` B2 entry. Codified phase C.1.
- **CLI contract for all 13 verify scripts** per phase C.1 commit `43e2fd0`: flag-form only via stdlib argparse with `--memo-json` required (or `--memo-md` required for G6); positional forms dropped; no shared helpers.

---

## File map (where state lives on disk)

### Design (read-only after each phase's commit)
- `design/us-vs-china-delta-matrix.md` — 16-section US-vs-China mapping
- `design/open-decisions.md` — D1-D23
- `design/skill-composition.md` — marketplace plugin composition strategy
- `design/file-ownership.md` — one-owner-per-file map across all phases
- `design/b0-conformance-diff.md` — schema-conformance audit vs official equity-research plugin
- `design/build-log.md` — THIS FILE; pointer to project state

### Schemas (frozen at end of B0)
- `schemas/memo.json` — umbrella schema
- `schemas/source_tags.json` — S1-S5 + Pending stratification
- `schemas/scenarios.json` — 5-scenario block
- `schemas/verification_gates.json` — 14-gate definitions

### Skill: `us-equity-research/` (multi-agent orchestrator)
- `us-equity-research/SKILL.md` — orchestrator trigger phrases + workflow
- `us-equity-research/references/`:
  - `us-data-sources.md` — S1-S5 + Tier 6 data catalog (EDGAR, FRED, agencies, alt-data)
  - `source-stratification-us.md` — S1-S5 + Pending discipline
  - `tool-composition-us.md` — marketplace plugin delegation contracts
  - `forensic-accounting-checklist-us.md` — ASC 606/842/718, non-GAAP, SBC, restatements, Form 4 (15 items)
  - `regulatory-desk-us.md` — 8 regulatory domains
  - `positioning-sentiment-us.md` — 12 positioning data classes
  - `valuation-discipline-us.md` — WACC build + D8 sector multiples + terminal value
  - `phase-1-deep-dive-us.md` — 5 specialist prompts (A1/A4/A5/A8/FS)
  - `phase-2-continuation-us.md` — 5 specialist prompts (A2/A3/A3-Peers/R/A6)
  - `phase-3-valuation-us.md` — 4 specialist prompts (A7/Mirror/Topic-Forensic/R-v2)
  - `verification-protocol-us.md` — 12-call discipline + transcript-over-press-release rule
  - `monitoring-framework-us.md` — Tier 1/2/3 triggers + cadence
  - `ic-memo-template-us.md` — deliverable HOW (rendered shape with placeholders)
  - `lp-letter-template.md` — LP variant per D4
  - `earnings-prep-template.md` — night-before checklist
  - `earnings-flash-template.md` — T+30min post-print

### Skill: `us-equity-ic-rigor/` (PM red-team layer)
- `us-equity-ic-rigor/SKILL.md` — rigor trigger phrases + 14 gates + score bands
- `us-equity-ic-rigor/references/`:
  - `five-scenario-framework-us.md` (G1/G4/G10 hooks)
  - `three-method-valuation-us.md` (G2/G3 hooks)
  - `gm-taxonomy-us.md` (G2/G8/G11 hooks; G2 scope authority)
  - `bear-bridge-us.md` (G5 hook)
  - `what-would-reverse-us.md` (G9 hook)
  - `tail-risk-mapping-us.md` (D12 A0 events)
  - `position-sizing-us.md` (D3/D6; G13/G14 feed)
  - `pm-redteam-rubric-us.md` (B1-B14 catalog + score bands)
  - `multi-audience-delivery-us.md` (D4 audience variants)
  - `quant-overlay-us.md` (G13/G14 scope authority; per D13)
- `us-equity-ic-rigor/templates/`:
  - `opinion-letter-section-checklist-us.md` (12-section WHAT)
  - `ic-debate-script-template-us.md` (verbal Q&A bank)

### Scripts (13 total; 198 pytest passing)
- `scripts/verify_eps_pe.py` (G1) — script + `scripts/tests/test_verify_eps_pe.py`
- `scripts/verify_segment_gm.py` (G2; LTM scope) — + test
- `scripts/verify_sotp_monotonicity.py` (G3) — + test
- `scripts/verify_scenario_weights.py` (G4) — + test
- `scripts/verify_bear_bridge.py` (G5) — + test
- `scripts/verify_source_tags.py` (G6; MD-primary) — + test
- `scripts/verify_headline_conditionality.py` (G7; cross-layer) — + test
- `scripts/verify_gm_taxonomy.py` (G8) — + test
- `scripts/verify_what_would_reverse.py` (G9) — + test
- `scripts/verify_weighting_sensitivity.py` (G10) — + test
- `scripts/verify_non_gaap.py` (G11; cross-layer) — + test
- `scripts/verify_fcf_definition.py` (G12) — + test
- `scripts/verify_quant_overlay.py` (G13+G14, dual-gate emission) — + test

### Fixtures
- `scripts/tests/fixtures/nvda_v0/clean.json` + `clean.md` — happy-path memo
- `scripts/tests/fixtures/nvda_v0/bugs/B01.json..B14.json` + `B01.md..B14.md` — single-fault-injected
- `scripts/tests/fixtures/nvda_v0/bug-script-matrix.md` — ownership table
- `scripts/tests/fixtures/nvda_v0/nvda_v0_bugs.md` — per-bug narrative

### Reference (gitignored)
- `reference/anthropic-official/equity-research/` — third-party plugin source (read-only, soft-dependency for delegation)
- `reference/anthropic-official/financial-analysis/` — same

### Templates (read-only)
- `templates/china-equity-research/` — China original (structural analog)
- `templates/china-equity-ic-rigor/` — China original (structural analog)

---

## Phase E plan

### Sequencing (per user dispatch)

1. **Phase E.NVDA — alone, end-to-end, iterate to ≥8.5**
   - Builder subagent runs the multi-phase workflow on NVDA
   - Web budget: target 25-40 WebSearch+WebFetch; surface to user at 50; hard cap 60
   - Outputs: `outputs/NVDA_IC_memo.md`, `outputs/NVDA_structured.json`, `outputs/NVDA_scenarios.json`, `outputs/NVDA_source_tags.json`, `outputs/NVDA_verification_gates.json`
   - Run all 14 verify scripts; all must exit 0
   - Independent PM-red-team scorer subagent reads only artifacts (no orchestrator reasoning); outputs score 6.0-9.0+ + fix-list
   - Iterate ≤3 cycles per BUILD_PROMPT; orchestrator dispatches fix subagent with fix-list
   - Commit `phase E.NVDA` once score ≥8.5

2. **Phase E.calibration — 4 in parallel after NVDA passes**
   - JPM (large bank, P/B + ROE-implied)
   - XOM (E&P, EV/EBITDAX + NAV + FCF yield)
   - MRK (large pharma, P/E + NPV pipeline)
   - DLR (mid-cap data center REIT, P/AFFO + NAV — chosen by orchestrator for cross-thesis NVDA correlation check + uncovered multiple_type)
   - Same web budget per ticker
   - Same independent scorer
   - Each iterates to ≥8.5 independently
   - Commit `phase E.JPM`, `phase E.XOM`, `phase E.MRK`, `phase E.DLR`

3. **Phase E.calibration-summary**
   - Cross-sector factor exposure baseline (B13 calibration data) — 7 Barra factors × 5 tickers; identify which factors vary most by sector, which are stable; document baseline ranges per sector
   - Capacity threshold table by mandate size (B14 calibration data) — days-to-exit at 10/20/30% participation for NVDA ($30B ADV) vs JPM (~$10B) vs XOM (~$5B) vs MRK (~$2B) vs DLR (~$500M); flag where mandate sizing breaks
   - Commit `phase E.calibration-summary`

### Independent PM-red-team scorer scope

Reads ONLY:
- `outputs/<ticker>_IC_memo.md`
- `outputs/<ticker>_structured.json`
- `outputs/<ticker>_scenarios.json`
- `outputs/<ticker>_source_tags.json`
- `outputs/<ticker>_verification_gates.json`
- `us-equity-ic-rigor/references/pm-redteam-rubric-us.md` (score bands + bug catalog)
- 14 verify_*.py exit codes (orchestrator runs scripts; reports exit codes to scorer)

Cannot read:
- Intermediate Phase 1/2/3 briefs
- Orchestrator reasoning / iteration context
- Builder subagent transcripts

Output:
- Single score 6.0-9.0+ per rubric bands
- Fix-list keyed to gate IDs (G1-G14) and bug classes (B1-B14)
- One-paragraph adjudication on each top-3 anchor's source classification

Iteration loop: orchestrator dispatches fix subagent with the fix-list, fix subagent edits outputs, rerun verify scripts, rerun scorer. ≤3 cycles.

### Web verification budget per memo

- Target: 25-40 WebSearch + WebFetch calls
- Surface to user at 50
- Hard cap: 60
- Source-priority order per `us-equity-research/references/verification-protocol-us.md`:
  1. EDGAR full-text search (`efts.sec.gov`)
  2. EDGAR company filings + XBRL company facts API
  3. FRED for R_f, ERP, sector indicators
  4. Federal Register for regulatory designations (BIS Entity List, OFAC SDN, FDA actions)
  5. Trade press (sector-specific per us-data-sources.md)
  6. Free aggregators (Yahoo Finance, StockAnalysis.com, MarketWatch) for consensus
  7. Damodaran for ERP + industry betas

Mgmt guidance MUST be verified against earnings call transcript, NOT against press release (delta matrix §11 rule).

### Forward-looking calibration items for Phase E

- **B13 calibration**: factor exposure z-scores vary materially by sector. Phase E will document baseline ranges (e.g., banks typically score high Quality + high Size + mid Value + low Momentum; mega-cap tech high Growth + high Momentum + low Value). The 7-factor schema is fixed; the EXPECTED RANGES per sector need calibration.
- **B14 calibration**: capacity thresholds depend on strategy size, not just stock-level metrics. A $500M fund and a $5B fund have very different days-to-exit constraints on the same $500M ADV stock. Phase E will document threshold tables by mandate size (long_only_large_cap typically $1-10B AUM; long_only_smid typically $200M-2B AUM; long_short_hedge_fund varies; etc.).
- **Sector-specific A0 events**: D12 enumerates 6 standing A0 events; Phase E may surface sector-specific idiosyncratic A0s (e.g., for DLR: hyperscaler bypass via in-house data centers; for JPM: CCAR stress capital build requirement; for XOM: stranded asset risk under climate transition; for MRK: Keytruda LOE). Document in `tail-risk-mapping-us.md` Phase E annex.

---

## Phase F preview (post Phase E)

- `us-equity-research/.claude-plugin/plugin.json` — manifest with marketplace metadata
- `us-equity-ic-rigor/.claude-plugin/plugin.json` — manifest with `requires` block declaring soft-dependency on `claude-for-financial-services/financial-analysis` (per D21) and `equity-research`
- `README.md` at project root — install instructions for Claude Code (`/plugin install us-equity-research@<marketplace>`) and Cowork (manual skill install path); EDGAR-only mode default; premium hooks optional
- `git status` clean
- Print full git log of all commits

---

## /clear safety contract

Any new session can resume Phase E or Phase F by:
1. Reading this file (`design/build-log.md`)
2. Reading `design/file-ownership.md` for owner table
3. Reading `design/open-decisions.md` for D1-D23
4. Reading `schemas/verification_gates.json` `gate_definitions` for G1-G14
5. Reading `us-equity-ic-rigor/references/pm-redteam-rubric-us.md` for B1-B14
6. Running `git log --oneline` to find current HEAD
7. Running `python -m pytest -q scripts/tests/` to verify 198 passing baseline

No conversation history is required. All decisions, gates, bug classes, file ownership, and CLI contracts are documented on disk.
