# Changelog

All notable changes to this project will be documented in this file. Format
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) +
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-05-29

### Sprint 1 of post-v0.1.x improvement roadmap

This release closes the three highest-leverage gaps identified in the
internal red-team audit of Plugin 1 (`us-equity-research`):

1. **Where is consensus wrong?** Plugin 1 had explicit S1-S5 source
   stratification that correctly downweighted sell-side as S4, but no
   structured place to declare a specific non-consensus view. Memos with
   non-Hold ratings could be assembled without ever stating where the
   analyst disagreed with FactSet median EPS.
2. **Banks.** The original FS forensic agent handled tech, pharma, energy,
   and REITs adequately but collapsed on depositories — no AOCI bridge,
   no CET1 walk, no NIM/deposit-beta discipline, no stress capital
   context. Banks are ~17% of S&P 500 market cap and the original
   treatment was gestural.
3. **Earnings revision velocity.** Tracked only as passive
   "PT revision trend"; not a first-class fundamental-with-quant-overlay
   signal as it is at any real L/S desk.

### Added — three new verification gates

- **G15 — Consensus variance** (`scripts/verify_consensus_variance.py`).
  Memos with non-Hold ratings must declare ≥1 load-bearing entry in
  `source_tags.consensus_variance` block (type ∈ {revenue, margin,
  multiple, scenario_weight, timing}; `sizing_impact_pp` ≥ 2.0; ≥1
  evidence_ref at S1-S3). Hold ratings, memos with headline self-labeled
  "consensus-anchored", and names with n_analysts < 5 → n_a. Cap at 7.0
  on fail. Full discipline in new file `us-equity-research/references/
  consensus-variance-us.md` (~390 lines).
- **G16 — Bank discipline** (`scripts/verify_bank_metrics.py`). For
  sector ∈ {Financials/Banks, Diversified Banks, Regional Banks,
  Investment Banking & Brokerage, Insurance, BDC}, `source_tags.
  bank_metrics` block must contain (a) AOCI bridge (AFS book/fair value,
  AOCI mark, HTM unrealized loss, MTM TBVPS), (b) CET1 walk (period-
  over-period bridge), (c) NIM trajectory (5y + deposit beta), (d)
  stress capital (SCB + capital return capacity + CCAR/DFAST trough,
  trough optional for Category IV / <$100B). Non-bank sectors → n_a.
  Cap at 7.0 on fail. Inline augmentation to `phase-1-deep-dive-us.md`
  §FS-Banks Augmentation (~210 lines).
- **G17 — Revision velocity** (`scripts/verify_revision_velocity.py`).
  Memos with n_analysts ≥ 5 must populate `source_tags.revision_velocity`
  block with `fy1_eps_revision_3m_pct` + `breadth_3m` (in [-1.0, 1.0]) +
  `g17_status="disclosed"`. Optional but recommended: 1m/6m windows, FY2
  revision, PT revision, pre-print drift, peer median comparison. Thin
  coverage → n_a. Cap at 7.5 on fail. Added as ~80-line subsection
  under A6 in `phase-2-continuation-us.md`.

### Added — new Phase 2 specialist

- **A-Consensus** (~165 lines added to `phase-2-continuation-us.md`).
  Phase 2 now dispatches **six** agents in parallel (was five). A-Consensus
  pulls the FactSet / Visible Alpha / Bloomberg EE consensus snapshot,
  identifies material disagreements per the variance taxonomy, sizes each
  variance, and either declares it (with S1-S3 evidence) or recommends
  "consensus-anchored" headline labeling. The agent that forces the memo
  to claim edge specifically or admit absence honestly.

### Added — IC memo template sections

- New top-level section **CONSENSUS VARIANCE & REVISION VELOCITY**
  between INVESTMENT THESIS and VALUATION FRAMEWORK in
  `ic-memo-template-us.md`. Includes consensus snapshot table, declared
  variances block, revision velocity snapshot, fallback labeling for
  consensus-anchored memos.
- New subsection **Bank-specific metrics** (conditional, gated by sector)
  under KEY FINANCIAL DATA in `ic-memo-template-us.md`. Six sub-tables:
  AOCI bridge, CET1 walk, SCB/capital return, NIM/deposit beta, CECL/CRE
  concentration, bank category + regulatory currency.

### Changed — schemas (additive-only, backwards-compatible)

- `schemas/source_tags.json` — `schema_version` const "0.1.0" → enum
  `["0.1.0", "0.2.0"]` for grandfathering. Added three optional top-
  level blocks: `consensus_variance` (array of variance objects),
  `revision_velocity` (object), `bank_metrics` (object). Each block has
  its full sub-schema.
- `schemas/verification_gates.json` — gate_id enum extended G14 → G17.
  `gates` array `minItems`/`maxItems` relaxed from 14 to 14-17 range
  (exact count enforced by verifier per schema_version). `gate_definitions`
  reference catalog adds G15/G16/G17 const descriptions.
- `schemas/memo.json` — `schema_version` const "0.1.0" → enum
  `["0.1.0", "0.2.0"]`. No required field changes.
- `schemas/scenarios.json` — unchanged.

### Backwards compatibility

v0.1.x memos with `schema_version="0.1.0"` validate clean against v0.2.0
schemas and are exempt from G15-G17 (gates skipped with
`status: skipped, reason: grandfathered_v0_1`). The five Phase E
calibration memos (NVDA / JPM / MRK / XOM / DLR) remain in the
`outputs/` directory and pass under v0.2.0 schemas without modification.

### Operational changes

- Phase 2 now dispatches six agents (was five). Total elapsed time
  largely unchanged because A-Consensus is dispatched in parallel.
- Phase 0 sector capture is now load-bearing for G16 enforcement —
  incorrect sector classification (e.g., a bank misclassified as
  "Financials/Diversified") cascades into wrong gate activation. New
  cross-check against NASDAQ Symbol Directory or 10-K cover page Item 1
  recommended in SKILL.md.
- Both plugin.json files: `version` "0.1.0" → "0.2.0".

### Validation gate for v0.2.0 (must complete before tagging)

Re-run JPM end-to-end with v0.2.0. Required outcomes:
(a) FS-Banks Augmentation produces visible AOCI bridge and CET1 walk
(b) G16 passes only because of that content
(c) A-Consensus identifies ≥1 EPS or multiple variance with S1-S3 evidence
(d) G15 passes
(e) Revision velocity numbers appear in the memo
If any of (a)-(e) fails, the new content is decorative and Sprint 1 is
incomplete. **Status as of file commit: JPM re-run pending — requires
live agent dispatch.**

### Files added

- `us-equity-research/references/consensus-variance-us.md` (~390 lines)
- `scripts/verify_consensus_variance.py` (~190 lines)
- `scripts/verify_bank_metrics.py` (~230 lines)
- `scripts/verify_revision_velocity.py` (~190 lines)

### Files modified

- `us-equity-research/SKILL.md` (Phase 2 table 5→6 agents, reference list,
  Phase 0 sector load-bearing, gate count 14→17)
- `us-equity-research/references/phase-1-deep-dive-us.md` (FS-Banks
  Augmentation inline section)
- `us-equity-research/references/phase-2-continuation-us.md` (A-Consensus
  H2 section + A6 revision velocity subsection + PM Synthesis items 7b/8b)
- `us-equity-research/references/ic-memo-template-us.md` (Consensus
  Variance section + Bank Metrics subsection)
- `us-equity-ic-rigor/SKILL.md` (gate count, gates list G15-G17, bug
  catalog B15-B17, scripts list, description)
- `schemas/source_tags.json`, `schemas/verification_gates.json`,
  `schemas/memo.json` (additive-only changes)
- `us-equity-research/.claude-plugin/plugin.json`,
  `us-equity-ic-rigor/.claude-plugin/plugin.json` (version bump)
- `README.md` (gate count, brief Sprint 1 mention)

### Deferred to Sprint 2 (v0.3.0) and beyond

Per the prioritization in the design discussion:
- v0.3.0: biotech rNPV per asset, special-situations template, PM
  synthesis adjudication codification, "$50K pre-IC research" mechanism
- v0.4.0+ or deferred: cyclicals-at-inflection methodology, small-cap
  thin-disclosure adaptation
- Sister plugins (not Plugin 1 / 2 extensions): alt-data integration,
  real Barra/Axioma factor feed, non-US/ADR substance, crowding-cost
  modeling
- Out of scope for plugin work: forensic-flag historical backtest
  (separate research project requiring CRSP/Compustat universe)

## [0.1.1] — 2026-05-24

### Added — slash command surface

Both plugins now expose deterministic slash-command entry points alongside
the existing auto-discovered skill triggers. Same underlying pipelines,
explicit invocation:

- `us-equity-research/commands/research.md` — `/us-equity-research:research [ticker]`
  runs Phase 0 fundamental research and stops. Does not chain into IC
  memo construction unless the user's request implies it.
- `us-equity-ic-rigor/commands/ic-memo.md` — `/us-equity-ic-rigor:ic-memo
  [ticker]` chains Phase 0 → Phases 1-3 → enforces all 14 verification
  gates → produces full IC memo + 4 structured JSON artifacts.
- `us-equity-ic-rigor/commands/red-team.md` — `/us-equity-ic-rigor:red-team
  [ticker] [target-score]` runs Phase 4 only; assumes IC memo outputs
  exist; produces gate sweep + rubric score + ordered push-from-N-to-N+1
  fix list. Default target 8.5 per D20.

### Rationale

Auto-discovery via SKILL.md description matching works but is probabilistic
— the loader scores prompt similarity against every available skill's
description and can miss when the prompt phrasing is unusual. Slash
commands give a deterministic entry point for daily research routines
where invocation reliability matters more than natural language fit.

The set is deliberately minimal (3 commands, not 9) — each maps to a
distinct phase boundary. Anthropic's `claude-for-financial-services/
equity-research` ships 9 commands; that surface is already available
when that plugin is installed, so duplicating it adds menu noise without
adding capability.

### Non-breaking

No schema changes. No SKILL.md changes. No verify_*.py changes. Auto-
discovery triggers still work exactly as in 0.1.0. The 198 pytest tests
still pass — slash commands are scaffolding files, not executable code.

## [0.1.0] — 2026-05-20

### Added — initial release

Two plugins released as one project:

- `us-equity-research` — multi-agent orchestrator for buy-side fundamental
  research on US equities. Phase 0 setup → Phase 1 (5 parallel specialists)
  → Phase 2 (5 deepening specialists) → Phase 3 (4 valuation specialists)
  → verification → institutional IC memo. EDGAR-only default; premium
  hooks opt-in.
- `us-equity-ic-rigor` — PM red-team layer. 14 verification gates G1-G14
  (10 inherited from China A-share precedent + 4 US-specific: non-GAAP
  reconciliation, SBC-in-FCF, Barra factor exposure, capacity / ADV /
  days-to-exit). 5-scenario probabilistic framework. 5-band rating per
  D1. Score-band PM rubric (6.0-9.0+).

### Design decisions ratified

24 decisions (D1-D24) documented in `design/open-decisions.md`. Notable:

- D5: EDGAR-only default mode for portability
- D13: quant overlay mandatory in every institutional memo
- D15: Markdown-only mandatory output
- D17 / D22: 4-schema decomposition frozen at end of Phase B0
- D21: soft-dependency composition with claude-for-financial-services
- D24: banks GM-taxonomy + SOTP adaptation (NIM / efficiency-ratio T1-T5;
  PPNR / Pre-Tax SOTP columns)

### Phase E calibration set

5 institutional IC memos produced end-to-end and PM-red-team scored:

- NVDA (mega-cap tech, P/E primary): scored 8.9 after 1 iteration cycle
- JPM (banks, P/B + ROE-implied): scored 8.7
- XOM (integrated E&P, EV/EBITDAX + NAV): scored 9.0
- MRK (large-cap pharma, P/E + NPV pipeline): scored 9.0
- DLR (mid-cap data center REIT, P/AFFO + NAV): scored 9.0

All 5 cleared D20 ≥8.5. Cross-thesis correlation: NVDA-DLR ~0.55-0.65
(shared hyperscaler-capex anchor). See
`design/phase-e-calibration-summary.md` for B13 factor profile baseline
+ B14 capacity threshold tables.

### Test surface

13 verification scripts + 198 pytest tests passing (15 per gate × 14
gates against the single-fault-injected NVDA fixture matrix; +1 calling-
contract test for G3).

### Known follow-ups (post-v0.1.0)

- REIT codification (D25-candidate): DLR memo handled REIT field-
  mapping inline; pending future REIT memo (AMT / PLD / EQIX / etc.) to
  trigger formal codification.
- Strategy-size-aware G14 thresholds: current G14 checks presence
  of `adv_30d_usd_m` + `days_to_exit_10pct_participation`; does not
  yet parameterize mandate-specific thresholds.
- Polish fix-list: ~60 min of polish across the 5 Phase E memos
  documented in calibration summary.
