# File Ownership — Phase B → F

Per BUILD_PROMPT §"Memory and Isolation Discipline" point 5: every file in this project has exactly one **owner** (a subagent or phase) responsible for writing it. Multiple subagents may read any file; only the owner writes. This is the contract that lets parallel subagents dispatch without trampling each other's work.

The two collision modes this prevents:
1. **Concurrent writes** — two parallel agents writing the same file race and one loses.
2. **Stale-base writes** — agent A reads the file at T=0, agent B writes at T=5, agent A writes at T=10 with stale base, B's work is silently lost.

A second-class invariant: every Phase ends with a **clean working tree**. If a Phase B1 subagent fails halfway, the orchestrator MUST revert or stage its partial work explicitly; never leave a half-written file for the next phase to inherit.

## Cross-phase contract files (owned by orchestrator, never modified by subagents)

These are the contracts subagents read but never write:

| File | Owner | Phase | Purpose |
|---|---|---|---|
| `schemas/memo.json` | Orchestrator (Phase B0) | B0 | Umbrella schema for full structured memo. |
| `schemas/source_tags.json` | Orchestrator (Phase B0) | B0 | S1-S5 + Pending stratification schema. |
| `schemas/scenarios.json` | Orchestrator (Phase B0) | B0 | 5-scenario probabilistic framework schema. |
| `schemas/verification_gates.json` | Orchestrator (Phase B0) | B0 | 14 verification gates schema (10 inherited + 4 US-specific). |
| `design/file-ownership.md` | Orchestrator (Phase B0) | B0 | This file. |
| `design/us-vs-china-delta-matrix.md` | Orchestrator (Phase A) | A | Read-only after Phase A commits. |
| `design/open-decisions.md` | Orchestrator (Phase A, A.1) | A | Read-only after Phase A.1 commits. D22, D23 ratification happens here. |
| `design/skill-composition.md` | Orchestrator (Phase A.1) | A.1 | Read-only after A.1 commits. |
| `design/b0-conformance-diff.md` | Orchestrator (Phase B0) | B0 | Diff between our schemas and the official `equity-research:initiating-coverage` implicit contract. |

**Rule for orchestrator:** schemas frozen at end of B0. Any change post-B0 must be a deliberate B0.X commit with backward-compat note. Subagents that try to write to `schemas/*` MUST fail.

## Phase B1 — Skill scaffolding (parallel subagent dispatch)

Phase B1 dispatches subagents in parallel to write the skill structure. Each subagent owns specific files and reads only the shared contracts.

### Subagent S-B1-1: us-equity-research SKILL.md author
- Owner of: `us-equity-research/SKILL.md`
- Reads: `schemas/*`, `templates/china-equity-research/SKILL.md` (for structure), `design/us-vs-china-delta-matrix.md`, `design/open-decisions.md`
- Output: SKILL.md with trigger phrases per D18, 3-phase workflow, mode flag (EDGAR-only vs premium-hooks per D5)
- Does NOT write: anything outside its own SKILL.md

### Subagent S-B1-2: us-equity-ic-rigor SKILL.md author
- Owner of: `us-equity-ic-rigor/SKILL.md`
- Reads: `schemas/*`, `templates/china-equity-ic-rigor/SKILL.md`, `design/us-vs-china-delta-matrix.md`
- Output: PM red-team layer SKILL.md, triggers per D18 second block, 14 verification gates listed, score rubric reference
- Does NOT write: anything outside its own SKILL.md

### Subagent S-B1-3: us-data-sources author
- Owner of: `us-equity-research/references/us-data-sources.md`
- Reads: `schemas/source_tags.json`, `design/us-vs-china-delta-matrix.md` §1
- Output: Per-S-tier data source catalog with URLs (EDGAR full-text, FRED, Federal Register, etc.), free vs premium tiering per D5
- Does NOT write: anything outside this file

### Subagent S-B1-4: source-stratification-us author
- Owner of: `us-equity-research/references/source-stratification-us.md`
- Reads: `schemas/source_tags.json`, `templates/china-equity-ic-rigor/references/source-stratification.md`, `design/us-vs-china-delta-matrix.md` §2
- Output: S1-S5 taxonomy ported to US (10-K/10-Q/8-K/transcripts/consensus/alt-data), conditional headline patterns, US-localized examples
- Does NOT write: anything outside this file

### Subagent S-B1-5: tool-composition-us author (NEW from A.1)
- Owner of: `us-equity-research/references/tool-composition-us.md`
- Reads: `schemas/memo.json`, `reference/anthropic-official/equity-research/skills/initiating-coverage/SKILL.md`, `reference/anthropic-official/financial-analysis/skills/dcf-model/SKILL.md`, `reference/anthropic-official/financial-analysis/skills/comps-analysis/SKILL.md`, `design/skill-composition.md`
- Output: JSON-contract documentation for delegating Excel DCF, Excel comps, polished DOCX to the marketplace plugins; 5→3 scenario mapping; fallback behavior
- Does NOT write: anything outside this file

**Dispatch discipline:** all 5 subagents fire in parallel with the same shared context (schemas + Phase A docs + China templates). Each gets a "synthesis brief" telling it (a) what it owns, (b) what it must NOT touch, (c) which other subagents are working simultaneously. Orchestrator does NOT re-dispatch any subagent that already owns a file in this list — that's a collision.

## Phase B2 — Phase-specific reference files (parallel)

After B1 completes and is committed, B2 dispatches more parallel subagents for the per-phase analytical references. Same one-owner discipline.

### Subagent S-B2-1: forensic-accounting-checklist-us author
- Owner of: `us-equity-research/references/forensic-accounting-checklist-us.md`
- Reads: schemas, china forensic template, delta §6
- Output: ASC 606/842/718, non-GAAP/GAAP discipline, SBC/FCF treatment, restatement triggers, Form 4 patterns, ~80-120 lines

### Subagent S-B2-2: regulatory-desk-us author
- Owner of: `us-equity-research/references/regulatory-desk-us.md`
- Reads: schemas, delta §3
- Output: FTC/DOJ/State AGs/EU CMA, BIS/OFAC/CFIUS, sector regulators, tariffs, securities enforcement, ~80-120 lines

### Subagent S-B2-3: positioning-sentiment-us author
- Owner of: `us-equity-research/references/positioning-sentiment-us.md`
- Reads: schemas, delta §7
- Output: 13F + Form 4 + short interest + options + ETF flows + index inclusion + activist filings, ~80-120 lines

### Subagent S-B2-4: valuation-discipline-us author
- Owner of: `us-equity-research/references/valuation-discipline-us.md`
- Reads: schemas, delta §5, china three-method-valuation reference
- Output: Sector-specific multiple branching per D8 table, WACC discipline, terminal value rules

### Subagent S-B2-5: phase-references (china-style port)
- Owner of: `us-equity-research/references/phase-1-deep-dive-us.md`, `phase-2-continuation-us.md`, `phase-3-valuation-us.md`, `verification-protocol-us.md`, `monitoring-framework-us.md`
- Reads: schemas, china phase templates
- Output: Phase prompts for subagents, mostly 1:1 ports with US-specific WebSearch examples
- (Internal-batch: this one owner writes all 5 files because they share template structure and need consistent voice; subagent dispatches NOT parallelized further inside this batch)

### Subagent S-B2-6: ic-rigor references (china-style port)
- Owner of: `us-equity-ic-rigor/references/five-scenario-framework-us.md`, `three-method-valuation-us.md`, `gm-taxonomy-us.md`, `bear-bridge-us.md`, `what-would-reverse-us.md`, `tail-risk-mapping-us.md`, `position-sizing-us.md`, `pm-redteam-rubric-us.md`, `multi-audience-delivery-us.md`
- Reads: schemas, china ic-rigor references
- Output: 1:1 ports of china rigor references, US-specific examples, B11-B14 bug additions to rubric

### Subagent S-B2-7: templates (output structures)
- Owner of: `us-equity-ic-rigor/templates/opinion-letter-section-checklist-us.md`, `ic-debate-script-template-us.md`, `lp-letter-template.md` (D4), `earnings-prep-template.md`, `earnings-flash-template.md`
- Reads: schemas/memo.json, china templates, delta §8
- Output: 12-section institutional memo template; English-only per D4

**Phase B2 dispatch parallelism:** Subagents B2-1 through B2-7 can run in parallel because they own disjoint file sets. Orchestrator reviews each commit before declaring B2 complete.

## Phase C — Verification scripts (parallel)

### Subagent S-C-1 through S-C-10: one script per gate
- Owner of: `scripts/verify_eps_pe.py`, `verify_segment_gm.py`, `verify_sotp_monotonicity.py`, `verify_scenario_weights.py`, `verify_bear_bridge.py`, `verify_source_tags.py`, `verify_headline_conditionality.py`, `verify_gm_taxonomy.py`, `verify_what_would_reverse.py`, `verify_weighting_sensitivity.py`
- Reads: `schemas/verification_gates.json`, the relevant input JSON schema
- Output: One Python script per gate G1-G10. Exit 0 on pass, non-zero on fail. Prints structured output conforming to `verification_gates.json` `evidence` object.

### Subagent S-C-11: example JSON fixtures
- Owner of: `scripts/example_nvda_scenarios.json`, `example_nvda_segments.json`, `example_nvda_source_tags.json`, `example_nvda_memo.json`
- Reads: schemas
- Output: Example JSONs for testing each verification script

## Phase D — Quant overlay (parallel)

### Subagent S-D-1: quant-overlay-us reference
- Owner of: `us-equity-ic-rigor/references/quant-overlay-us.md`
- Reads: schemas, delta §13
- Output: Factor exposure, capacity, edge decay, correlation placeholder, stress overlay discipline

### Subagent S-D-2 through S-D-4: G11-G14 verification scripts
- Owner of: `scripts/verify_non_gaap.py` (G11), `verify_fcf_definition.py` (G12), `verify_quant_overlay.py` (G13+G14)
- Reads: schemas/verification_gates.json + relevant JSON inputs
- Output: One script per gate; combined verify_quant_overlay covers G13+G14 since both probe the same `quant_overlay` JSON block

## Phase E — NVDA self-test

Phase E runs the full pipeline on NVDA and produces:
- Owner: Orchestrator (single agent, not parallelized)
- Outputs: `outputs/NVDA_IC_memo.md`, `outputs/NVDA_scenarios.json`, `outputs/NVDA_source_tags.json`, `outputs/NVDA_segments.json`, `outputs/NVDA_verification_gates.json`, `outputs/NVDA_structured.json`, `outputs/NVDA_Research_Document_<date>.md` (delegation input), `outputs/NVDA_Valuation_Analysis_<date>.md` (delegation input)
- Verification: All 14 gates exit 0; PM red-team rubric ≥ 8.5

## Phase F — Plugin packaging

### Subagent S-F-1: plugin manifest authors
- Owner of: `us-equity-research/.claude-plugin/plugin.json`, `us-equity-ic-rigor/.claude-plugin/plugin.json`
- Reads: SKILL.md files for descriptions
- Output: Manifest with `requires` block declaring soft-dependency on `claude-for-financial-services/financial-analysis` (D21)

### Subagent S-F-2: README author
- Owner of: `README.md` at project root
- Output: Single README documenting both install paths (Claude Code via `/plugin install`, Cowork via .plugin upload); EDGAR-only mode default; premium hooks optional

## Output file conventions (consumed across phases)

These files are written at runtime by the skill operating on a ticker, not by build subagents:

| Pattern | Written by | When |
|---|---|---|
| `outputs/<ticker>_IC_memo.md` | us-equity-research orchestrator | Each invocation |
| `outputs/<ticker>_structured.json` | us-equity-research orchestrator | Each invocation; conforms to schemas/memo.json |
| `outputs/<ticker>_scenarios.json` | Phase 3 valuation specialist | Each invocation; conforms to schemas/scenarios.json |
| `outputs/<ticker>_source_tags.json` | Phase 1.5 source-stratification gate | Each invocation; conforms to schemas/source_tags.json |
| `outputs/<ticker>_verification_gates.json` | Phase 4 verification phase | Each invocation; conforms to schemas/verification_gates.json |
| `outputs/<ticker>_Research_Document_<date>.md` | Phase 1 (optional, only if user requests DOCX delegation) | Conditional |
| `outputs/<ticker>_Valuation_Analysis_<date>.md` | Phase 3 (optional, only if user requests DOCX delegation) | Conditional |
| `outputs/<ticker>_DCF.xlsx` | financial-analysis:dcf-model (delegated) | Conditional |
| `outputs/<ticker>_Comps.xlsx` | financial-analysis:comps-analysis (delegated) | Conditional |
| `outputs/<ticker>_Initiation_Report_<date>.docx` | equity-research:initiating-coverage Task 5 (delegated) | Conditional |

## Concurrency rules summary

1. **Schemas frozen at B0.** Any post-B0 schema change requires a deliberate B0.X commit.
2. **One owner per file.** No exceptions.
3. **Parallel subagent dispatch within a phase only.** Cross-phase dependencies serialize.
4. **Each phase ends with clean working tree.** Orchestrator commits or reverts; never leaves half-state.
5. **Subagents read shared contracts; orchestrator alone writes them.**
6. **Reference plugin files (`reference/anthropic-official/`) are READ-ONLY** for all subagents. Gitignored per D23.
7. **Cowork driving Phase B0 from outside Claude Code is permitted** but Claude Code should be paused while Cowork is writing to avoid the collision we hit during this phase. Once B0 commits, hand back to Claude Code.

## Open-decision linkages

- D17 ratifies orchestrator-only schema ownership (this file enforces it).
- D21 introduces `tool-composition-us.md` (S-B1-5 owner).
- D22 ratifies the three sub-schemas as Phase B0 deliverables, plus this umbrella `memo.json`.
- D23 ratifies `.gitignore` of `reference/anthropic-official/`.
