# Changelog

All notable changes to this project will be documented in this file. Format
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) +
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] — 2026-05-29

### Sprint 2 — Rigor hardening (closing the systemic audit findings)

This release closes the four highest-severity findings from the cross-plugin
systemic audit that ran after v0.2.0. Where Sprint 1 (v0.2.0) added new
analytical content (A-Consensus, bank discipline, revision velocity),
Sprint 2 (v0.3.0) tightens the verification stack itself — making the
gates do what they claim to do.

### Added — three new verification gates (G18 / G19 / G20)

- **G18 — Quant overlay cross-document consistency** (`scripts/verify_quant_cross_doc_consistency.py`).
  Within a single memo, the structured `quant_overlay.factor_tags` block in
  `memo.json` must match any Markdown narrative reference to the same Barra
  factor within ±0.2 tolerance. Catches authors who quote z-scores in prose
  that diverge from structured block — common LLM failure mode where the
  prose is regenerated without re-reading structured data. Pre-v0.3.0 Plugin 2
  reference files had NVDA Momentum at +1.8 in `quant-overlay-us.md` but +2.3
  in `position-sizing-us.md`; G18 catches the same disease at memo runtime.
  Cap at 7.5 on fail. n_a if no Markdown factor references found.
- **G19 — Plugin 1 to Plugin 2 provenance manifest** (`scripts/verify_provenance_manifest.py`).
  Closes the audit finding that the Plugin 1 → Plugin 2 handoff was pure
  filename convention with no provenance enforcement (a hand-authored memo
  could pass all 17 gates without Plugin 1 ever being invoked). Plugin 1
  now writes `outputs/<ticker>_manifest.json` at end of Phase 3 containing
  run_id (UUID), agent_provenance (≥15 entries with SHA-256 hashes per
  workpaper), web_search_log (≥12 entries with response hashes), phase_timing,
  and `outputs_produced` with SHA-256 hashes per file. G19 verifies the
  manifest exists, has all required fields, and that declared file hashes
  **match actual on-disk hashes** (catches lazy hand-authoring + post-hoc
  editing). Hand-authored escape hatch: set `memo_metadata.hand_authored=true`,
  G19 passes with WARNING + rubric capped at 7.5. Cap at 7.5 on fail.
- **G20 — View defensibility** (`scripts/verify_view_defensibility.py`).
  Closes the audit's highest-severity finding: the rubric was grading
  structural completeness, not view quality. A consensus-hugging memo with
  perfect mechanical execution scored 9.0+ under v0.2.0. G20 requires three
  conjunctive conditions for any rubric score above 8.5:
  - (a) Headline `recommendation.upside_downside_pct` differs from S4
    consensus PT-implied return by at least 8 absolute percentage points
  - (b) At least one load-bearing `consensus_variance` has at least one
    `evidence_ref` at S1 or S2 (G15 accepted S1-S3; G20 tightens to require
    primary-source evidence on the strongest claim)
  - (c) `adjudication_trail` contains at least one entry with
    `type='variance_attack'`, `target_variance_id` pointing to a
    load-bearing variance, `attack_type` in the 5 canonical dimensions
    (evidence_credibility / triangulation_completeness / base_rate_sanity /
    catalyst_dependency / timing_arbitrage), and `attack_outcome` in
    {rebutted, modified}
  Caps at 8.5 on fail (NOT 7.0 — G20 is rubric-discriminating, not
  memo-killing). n_a for Hold ratings, consensus-anchored headlines, thin
  coverage.

### Added — Scope and limitations sections in both SKILL.md files

Both `us-equity-research/SKILL.md` and `us-equity-ic-rigor/SKILL.md` now
carry explicit "Scope and limitations" sections that name the use cases
the framework is category-wrong for (pure event-driven trades, pure
technical/momentum/mean-reversion, pair-trade-on-flow, activist/proxy-fight,
pre-IPO/private market, bond/credit). The Plugin 2 section additionally
distinguishes what the rubric CAN tell you (math consistency, source-tag
discipline, definitional rigor) from what it CANNOT (whether the analyst
correctly identified the load-bearing assumption, whether the declared
variance is defensible, whether Barra z-scores are derived from a
calibrated factor model). Prevents the single largest category of misuse
by making the scoping explicit before invocation.

### Added — Plugin 1 manifest generation workflow

Plugin 1 SKILL.md now carries an end-of-Phase-3 step instructing the
orchestrator to maintain a `outputs/<ticker>_manifest_seed.json` during
the run (logging WebSearch/WebFetch calls with response hashes, phase
timing, verification_calls_count, orchestrator_notes) and to run
`scripts/write_manifest.py --ticker <T> --outputs-dir outputs/ --seed
outputs/<T>_manifest_seed.json` at end of Phase 3. The manifest writer
walks the workpapers directory, computes SHA-256 over each output file,
assembles `agent_provenance`, and emits a manifest conforming to
`schemas/manifest.json`. Without the seed, the script emits warnings and
writes a placeholder manifest that fails G19 (intentional degraded path).

### Added — quant overlay honest demote

`us-equity-ic-rigor/references/quant-overlay-us.md` now opens with an
"Honest framing" section explicitly stating: factor tags are directional
estimates, not regression outputs from a calibrated factor model;
conviction multipliers are decreed institutional rules of thumb, not
backtest-calibrated; do not size positions in a real book against these
numbers without an overlay from a calibrated feed. Reconciled the NVDA
example values between `quant-overlay-us.md` (canonical) and
`position-sizing-us.md` (was divergent on five of seven factors).

### Added — PM synthesis adjudication trail discipline

New reference file `us-equity-research/references/pm-synthesis-adjudication-us.md`
(89 lines, 7 sections) codifies what was previously tribal knowledge: the
weighting principles when specialists conflict (Forensic dominates
structural; Regulatory dominates if material; Industry is base-case anchor;
Positioning is technical overlay; Channel is timing), worked adjudication
patterns A-E, the R-v2 5-point attack methodology (evidence credibility,
triangulation completeness, base-rate sanity, catalyst dependency, timing
arbitrage), and the adjudication_trail schema. G20 consumes this discipline.

### Changed — verifier script rigor (closing audit Issue #3)

Three sub-fixes tightening the existing G3 / G6 / G15 / G16 / G17 verifiers:

- **G6 expansion**: `scripts/verify_source_tags.py` regex coverage grew from
  1 pattern (~5% of stated scope) to 6 patterns covering full G6 enumeration:
  revenue, gross margin, share/customer concentration, capacity (MW/GW/bpd/
  units), ADV, beta. Per-category failure attribution with category
  breakdown in additional findings. **Strict mode is opt-in via
  schema_version="0.3.0"** to preserve backwards compatibility with the
  NVDA v0 fixture matrix — pre-v0.3.0 memos (and memos invoked without
  --memo-json) run the original revenue-only pattern. v0.3.0 memos that
  pass the JSON via the orchestrator's uniform calling contract get the
  full 6-pattern coverage. Same grandfather pattern used by G3 / G15 / G16 /
  G17 / G18 / G19 / G20.
- **G15 derived-value recomputation**: `verify_consensus_variance.py` now
  recomputes `sizing_impact_pp = magnitude_pct × probability_right_pct ×
  scenario_sensitivity_pct / 10000` when the three optional inputs are
  populated and fails on ±0.1pp drift. Catches authors who write internally
  inconsistent variance math.
- **G16 derived-value recomputation**: `verify_bank_metrics.py` now
  recomputes `required_cet1_pct = 4.5 + 2.5 (CCB) + scb_pct +
  gsib_surcharge_pct` and fails on ±0.05% drift. Works for Cat I (with
  gsib_surcharge_pct) and Cat II-IV (gsib defaults 0).
- **G17 derived-value recomputation**: `verify_revision_velocity.py` now
  recomputes `breadth_3m = (up_revisions_3m - down_revisions_3m) /
  n_analysts` when optional `up_revisions_3m` and `down_revisions_3m`
  fields are populated; fails on ±0.02 drift. Backward-compatible when
  fields absent.
- **G3 SOTP strict enforcement**: `verify_sotp_monotonicity.py` v0.3.0
  fails on incomplete segment shape (previously silently returned n_a
  on segments missing GP or OP levels). Recognizes both industrial chain
  (Revenue/GP/OP/NI) and D24 banks chain (PPNR/Pre-Tax/NI). Pre-v0.3.0
  memos grandfathered via schema_version check.

### Added — new schemas

- `schemas/manifest.json` (new 5th schema, ~190 lines). Defines the
  Plugin 1 provenance manifest structure: run_id, plugin_versions,
  phase_timing, agent_provenance (≥15 entries with workpaper hashes),
  web_search_log (≥12 entries with response hashes), verification_calls_count,
  outputs_produced (with file hashes). Required `schema_version` const "0.3.0".

### Changed — existing schemas (additive only, grandfather-compatible)

- `schemas/memo.json` — schema_version enum now includes "0.3.0". Added
  optional top-level `adjudication_trail` (array of variance_attack /
  specialist_conflict entries with two-type discriminator and conditional
  required fields via `allOf` `if/then`). Added new definition
  `adjudication_trail_entry` with 5-dimension attack_type enum and
  3-outcome attack_outcome enum. Added new definition `sotp_segment` with
  `oneOf` constraint documenting industrial and banks chains. Added
  optional `memo_metadata.manifest_ref` and `memo_metadata.hand_authored`.
- `schemas/source_tags.json` — schema_version enum now includes "0.3.0".
  Added optional `revision_velocity.up_revisions_3m` and `down_revisions_3m`
  for G17 breadth recomputation.
- `schemas/verification_gates.json` — schema_version "0.3.0". gate_id
  enum extended G14 → G20. `gates` array minItems/maxItems range relaxed
  from 14-17 to 14-20. `gate_definitions` reference catalog adds G18 /
  G19 / G20 const descriptions.
- `schemas/scenarios.json` — schema_version enum now includes "0.3.0"
  (no field changes; bump for consistency).

### Backwards compatibility

v0.1.x and v0.2.0 memos validate clean against v0.3.0 schemas. Gates added
in each version are grandfathered:
- v0.1.x memos (schema_version="0.1.0"): G15-G20 skipped, logged as
  `skipped: grandfathered_v0_1`.
- v0.2.0 memos (schema_version="0.2.0"): G18-G20 skipped, logged as
  `skipped: grandfathered_v0_2`.
- v0.3.0 memos run the full 20-gate set.

The five Phase E calibration memos (NVDA / JPM / MRK / XOM / DLR) remain
in the `outputs/` directory unchanged and continue to validate as
`schema_version="0.1.0"`.

### Files added

- `us-equity-research/references/pm-synthesis-adjudication-us.md` (89 lines)
- `schemas/manifest.json` (~190 lines)
- `scripts/verify_quant_cross_doc_consistency.py` (~180 lines)
- `scripts/verify_provenance_manifest.py` (~210 lines)
- `scripts/verify_view_defensibility.py` (~210 lines)
- `scripts/write_manifest.py` (~165 lines)

### Files modified

- `us-equity-research/SKILL.md` (Scope and Limitations section; Manifest
  generation section; reference list updated for pm-synthesis-adjudication-us.md)
- `us-equity-ic-rigor/SKILL.md` (Scope and Limitations section with what
  rubric CAN/CANNOT tell; gates list extended G17 → G20; scripts catalog
  updated)
- `us-equity-ic-rigor/references/quant-overlay-us.md` (Honest framing
  disclaimer)
- `us-equity-ic-rigor/references/position-sizing-us.md` (NVDA examples
  reconciled to canonical set; G18 cross-reference)
- `us-equity-research/references/ic-memo-template-us.md` (Appendix D
  relabeled with honest framing paragraph and G18 cross-reference)
- `scripts/verify_source_tags.py` (G6 expansion: 1 pattern → 6)
- `scripts/verify_consensus_variance.py` (G15 sizing_impact_pp recompute)
- `scripts/verify_bank_metrics.py` (G16 required_cet1_pct recompute)
- `scripts/verify_revision_velocity.py` (G17 breadth_3m recompute)
- `scripts/verify_sotp_monotonicity.py` (G3 strict shape enforcement +
  banks D24 mapping recognition)
- `schemas/memo.json`, `schemas/source_tags.json`,
  `schemas/verification_gates.json`, `schemas/scenarios.json`
  (additive-only changes; schema_version enum extensions)
- `us-equity-research/.claude-plugin/plugin.json`,
  `us-equity-ic-rigor/.claude-plugin/plugin.json` (version 0.2.0 → 0.3.0)
- `README.md` (gate count 17 → 20; v0.3.0 description)

### Deferred to Sprint 3 (v0.4.0) and beyond

Per the planning discussion, Sprint 3 returns to the coverage expansion
work originally scoped for Sprint 2:
- Biotech rNPV per asset (new reference file, schema biotech_pipeline
  block, G21, validation on SRPT / BMRN)
- Special situations template (spin / SPAC / post-bk / busted IPO /
  going-private; new reference file, schema situation_type enum, G22)
- Pre-IC primary research mechanism (reframed AUM-agnostically per user
  direction — no $50K specificity)
- B15-B20 rubric documentation in pm-redteam-rubric-us.md (gate
  remediation discipline; deferred from v0.2.0 / v0.3.0)
- G15-G20 fixture matrix (15 fixtures per gate, cross-sensitivity validation)
- v0.1.x memo data drift cleanup (NVDA direction enum, JPM gm_taxonomy
  reconciliation null, MRK tail_risks shape, XOM default_action enum,
  DLR valuation methods shape)

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
