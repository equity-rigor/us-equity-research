# Session Handoff — v0.2.0 → v0.3.0 (Sprint 2)

**Purpose of this file.** This is the context-handoff document for a new Cowork session continuing work on the `us-equity-research` / `us-equity-ic-rigor` plugin system. The prior session shipped v0.2.0 (Sprint 1) on 2026-05-29. This file is the dense, opinionated brief the new session must read on startup to be productive without re-deriving design decisions. It encodes user preferences, project architecture, what was just shipped, Sprint 2 marching orders, explicit hard-NOs, and honest limitations of what's been built.

The file is self-contained — the new session can read only this document and have enough context to act productively. Subsequent files to read for depth are listed at the end.

---

## 1. Quick orientation

- **User**: Hongyi Gu (`hg2670@columbia.edu`). Quant researcher / buy-side analyst. Treat as institutional, no hand-holding. Reference voice: red team, not cheerleader.
- **Repo**: `https://github.com/equity-rigor/us-equity-research` (private). Local path on user's Mac: `/Users/hongyi/projects/us-equity-research`. Local path under Cowork workspace mount: depends on the session's mount mapping — confirm with `pwd` after `cd` into the workspace folder.
- **Current state**: tagged `v0.2.0` on `main` at commit `7e82cc9`. Both plugin.json files at `0.2.0`. Origin synced. 198 pytest tests passing, no regression on G1-G14. v0.2.0 Sprint 1 is code-complete; JPM live re-run validation is pending (see §11).
- **Tag history**: `v0.1.0` (initial release), `v0.1.1` (slash command surface), `v0.2.0` (Sprint 1).
- **Architecture in one sentence**: two-plugin system where Plugin 1 (`us-equity-research`) is the multi-agent research orchestrator producing analysis content, Plugin 2 (`us-equity-ic-rigor`) is the PM red-team layer producing verification gates and rubric scores.

## 2. User preferences (binding throughout the session)

These are already in the user's account preferences but stated here for clarity:

- Treat the user as a quant researcher / buy-side analyst. Institutional depth, no hand-holding.
- For any research task, produce: hypothesis, data spec, implementation, backtest plan, destruction analysis (edge decay, capacity, kill criteria), deployment runbook.
- Don't ask permission to go deep — assume yes.
- Don't ask clarifying questions when assumptions can be stated and proceeded from. State the assumption, proceed, let user push back.
- Default to long-form when the task is research; concise for everything else.
- Be a red team, not a cheerleader. If something is hollow, say so. If something is genuinely sharp, say so. No hedging.
- The user runs commands in a zsh shell where `#` is NOT treated as a comment by default (`interactive_comments` is off). **Never include `#` comments inline in copy-paste shell blocks.** The user has been bitten by this twice. If you need to annotate commands, do it in prose around the block, not inside it.
- The user uses heredocs with `<< 'EOF'` for multi-line commit messages — that pattern is the safe way to deliver multi-line text into commands. Multi-line `-m "..."` paste has corrupted commits in this session previously.

## 3. Architecture: the two-plugin boundary

The single most important architectural principle, encoded throughout v0.2.0:

> **Plugin 1 produces analysis. Plugin 2 enforces rigor on analysis. Sister plugins handle externally-gated capabilities (paid feeds, alt-data subscriptions, factor model licenses).**

Concretely:

- A new specialist agent (analytical work) goes in Plugin 1.
- A new verification gate (validation of analytical work) goes in Plugin 2.
- Anything that requires a Bloomberg / Barra / Yipit / GLG subscription to function goes in a sister plugin so users without the subscription aren't pretending they have edge they don't.

**Schema policy: additive-only with grandfathering.**

- All schema changes are additive (new optional fields, never modifications to existing required fields).
- `schema_version` fields are encoded as `enum: ["0.1.0", "0.2.0"]` rather than `const`, so v0.1.x memos validate clean under v0.2.0 schemas.
- New gates introduced in a minor version are skipped on memos declaring older schema_version (grandfather rule).
- This pattern must be preserved through v0.3.0 and beyond. A breaking change is v1.0.0 with a migration script — do not introduce one casually.

**Plugin 1 ↔ Plugin 2 versioning.**

- The two plugins ship together. Same version number, same git tag.
- A new gate declared in Plugin 1's reference files must have a matching `verify_*.py` in Plugin 2 before the tag.
- If Plugin 2 lags Plugin 1, gates are nominally enforced in documentation but not in code — that's worse than not declaring them.

## 4. The 17 verification gates (current state as of v0.2.0)

Located in `schemas/verification_gates.json` (canonical definitions) and `us-equity-ic-rigor/SKILL.md` §"Verification gates" (human-readable). Each gate has a Python script at `scripts/verify_*.py` that exits 0 on pass, non-zero on fail.

| Gate | Category | What it checks | Script |
|---|---|---|---|
| G1 | math | EPS × multiple = target price (±0.5%) per scenario | `verify_eps_pe.py` |
| G2 | consistency | Σ(segment_rev × segment_GM)/Σ(segment_rev) within ±50bp of consolidated GM | `verify_segment_gm.py` |
| G3 | math | SOTP monotonicity: NI ≤ OP ≤ GP ≤ Rev per segment | `verify_sotp_monotonicity.py` |
| G4 | math | Scenario probabilities sum to 1.00 ±0.01 | `verify_scenario_weights.py` |
| G5 | math | Bear/bull EPS bridge reconciles to base | `verify_bear_bridge.py` |
| G6 | source | Source tag at first use of every specific number | `verify_source_tags.py` |
| G7 | source | Headline conditionality matches top-3 anchor S-levels | `verify_headline_conditionality.py` |
| G8 | structure | GM taxonomy (T1-T5) defined + each GM mention tagged | `verify_gm_taxonomy.py` |
| G9 | structure | What-would-reverse triggers have numerical denominators | `verify_what_would_reverse.py` |
| G10 | structure | Anchor weighting impact table exists | `verify_weighting_sensitivity.py` |
| G11 | source (US, B11) | Non-GAAP/GAAP reconciliation present | `verify_non_gaap.py` |
| G12 | source (US, B12) | FCF definition declares SBC treatment | `verify_fcf_definition.py` |
| G13 | quant_overlay (US, B13) | Barra factor tags in §11 quant overlay | `verify_quant_overlay.py` |
| G14 | quant_overlay (US, B14) | Capacity / ADV / days-to-exit stated | `verify_quant_overlay.py` |
| **G15** | source/structure (v0.2.0) | Consensus variance declared OR "consensus-anchored" headline label | `verify_consensus_variance.py` |
| **G16** | structure (v0.2.0) | Bank discipline: AOCI + CET1 + NIM + stress capital (when sector=Banks) | `verify_bank_metrics.py` |
| **G17** | source (v0.2.0) | Revision velocity: 3m FY1 EPS revision + breadth (when n_analysts ≥ 5) | `verify_revision_velocity.py` |

**Score caps on failure.** Default: blocks_score_above = 8.0. Critical math gates G1 / G3 cap at 7.0. G15 caps at 7.0 (consensus variance is a core institutional discipline). G16 caps at 7.0 (banks failure is structural). G17 caps at 7.5 (signal value, not load-bearing math).

## 5. v0.2.0 Sprint 1 — what just shipped (do NOT re-suggest these)

**Plugin 1 additions:**

1. **A-Consensus specialist** as 6th Phase 2 agent. Forces structured identification of where the analyst disagrees with FactSet / Visible Alpha / Bloomberg EE consensus. Lives in `us-equity-research/references/phase-2-continuation-us.md` (new H2 section after A6). Full discipline file at `us-equity-research/references/consensus-variance-us.md` (~390 lines of dense prose covering variance taxonomy, evidence-required matrix, sizing rule, anti-patterns, calibration).
2. **FS-Banks Augmentation** under the FS forensic specialist in Phase 1. Inline addition to `phase-1-deep-dive-us.md` (sector-conditional, triggers when sector ∈ {Financials/Banks, Insurance, BDC, Broker-Dealer}). Covers AOCI bridge, CET1 walk + ORWA, NIM/deposit beta, CECL/CRE, OCI roll-through, CCAR/DFAST/SCB, Category I-IV tiering, Basel III Endgame timing.
3. **Earnings revision velocity** under A6 channel pulse. New ~80-line subsection covering 1m/3m/6m FY1 EPS revision direction + magnitude + breadth + peer comparison + pre-print drift. Cross-referenced with crowding score from positioning sentiment.
4. **IC memo template sections.** New top-level "CONSENSUS VARIANCE & REVISION VELOCITY" section between INVESTMENT THESIS and VALUATION FRAMEWORK in `ic-memo-template-us.md`. Conditional bank metrics subsection under KEY FINANCIAL DATA.

**Plugin 2 additions:**

1. **G15 — consensus variance**. Memos with non-Hold ratings must declare ≥1 load-bearing variance (sizing_impact_pp ≥ 2.0, ≥1 evidence_ref at S1-S3) OR self-label "consensus-anchored" in headline. Verifier: `scripts/verify_consensus_variance.py`.
2. **G16 — bank discipline**. Banks-sector memos must contain AOCI bridge + CET1 walk + NIM trajectory + stress capital context. Verifier: `scripts/verify_bank_metrics.py`.
3. **G17 — revision velocity**. Memos with n_analysts ≥ 5 must disclose 3-month FY1 EPS revision + breadth. Verifier: `scripts/verify_revision_velocity.py`.

**Schema additions:**

- `schemas/source_tags.json`: added optional top-level blocks `consensus_variance` (array), `revision_velocity` (object), `bank_metrics` (object). Each with full sub-schema. `schema_version` const → enum for grandfathering.
- `schemas/verification_gates.json`: `gate_id` enum extended G1-G14 → G1-G17. `gates` array `minItems`/`maxItems` relaxed from 14 to 14-17 range. `gate_definitions` reference catalog adds G15/G16/G17 const descriptions.
- `schemas/memo.json`: `schema_version` const → enum. No required field changes.

**Diff stats:** 16 files changed, +1724 / −44 lines on the v0.2.0 commit.

## 6. Sprint 2 plan (v0.3.0) — execution-ready spec

Continue the v0.2.0 pattern: Plugin 1 content + Plugin 2 gates + schema additions, all grandfather-compatible.

### Item 4 — Biotech rNPV per asset

**Hypothesis.** Pharma is ~12% of S&P 500 market cap. MRK template (large-cap pharma) gets you to multiples + IRA overhang discipline but does not cover mid-cap biotech where rNPV-per-asset is the dominant valuation methodology. Adding biotech rNPV discipline unlocks proper coverage of mid-cap pipelines (SRPT, BMRN, INCY, EXEL, etc.).

**Spec.**

- New reference file `us-equity-research/references/biotech-rnpv-us.md` (~250 lines):
  - Phase 1/2/3 POS tables from Pharmagellan / Stewart 2013 or BIO database (Phase 1: 15-25%, Phase 2: 12-18%, Phase 3: 10-15%, Approved: 8-12% discount rates)
  - Peak sales triangulation: top-down (market × penetration × pricing) vs bottom-up (KOL surveys, GLG/Tegus expert call data) vs analog drug benchmarks
  - Ex-US-vs-US revenue split conventions
  - Royalty stack accounting for partnered assets
  - Regulatory-pathway optionality: Breakthrough Designation, Fast Track, Accelerated Approval impact on rNPV discount and timeline
  - Patent cliff modeling (LOE timing, biosimilar entry, generic erosion curves)
  - Anti-patterns: applying P/E to a pre-revenue biotech (rejected), straight-line revenue ramp without competitive erosion (rejected)
- Sector-conditional dispatch in Phase 1 FS agent (similar pattern to bank discipline in v0.2.0). When `sector_gics` matches biotech/pharma sub-industries with material clinical pipeline.
- Schema additions to `source_tags.json`: optional `biotech_pipeline` block with per-asset POS, peak sales, NPV, discount rate fields.
- Plugin 2 gate **G18**: biotech-sector memos must declare rNPV-per-asset OR explicitly use multiples-based approach with justification. Verifier: `scripts/verify_biotech_rnpv.py`. Cap at 7.5 on fail.
- New section in `ic-memo-template-us.md` under VALUATION FRAMEWORK (conditional, when sector=biotech).

**Validation tickers for Sprint 2.** Existing self-test set has MRK (large pharma) only. Add: SRPT (mid-cap gene therapy with active pipeline), BMRN (mid-cap rare disease with diverse pipeline). Re-run MRK to confirm the new rNPV section is conditional (large-cap pharma can use multiples + IRA discipline as before; rNPV section is for pipeline-driven names).

**Destruction analysis.** POS tables from Pharmagellan are calibrated to historical FDA approval rates; subject to recalibration as therapeutic area mix shifts (oncology rates lower than rare disease post-Accelerated Approval rule changes). Mark as "currency-sensitive" in the reference file with quarterly refresh discipline.

### Item 5 — Special situations template

**Hypothesis.** Spin-offs, post-bankruptcy emergence, busted IPOs, SPACs/de-SPACs all carry their own analytical patterns that the steady-state SOTP discussion does not handle. Adding the template unlocks coverage of a high-alpha sub-universe.

**Spec.**

- New reference file `us-equity-research/references/special-situations-us.md` (~400 lines):
  - **Spin-offs**: Form 10 disclosure conventions, when-issued vs regular-way trading, RemainCo vs SpinCo tracking, index reweight forced selling, capital structure pre-spin vs post-spin, dis-synergy modeling
  - **Post-bankruptcy emergence**: Plan of Reorganization economics, NOL preservation under §382, equitization recoveries, fresh-start accounting, ATB (Allowed Trade Claim) basis vs current equity value, GUC settlement waterfall
  - **SPACs and de-SPACs**: S-4 disclosure mechanics, sponsor promote economics (typically 20%), warrant overhang, PIPE structure, lock-up expiration calendar (the dominant price driver for first 12mo post-merger), redemption rates
  - **Busted IPOs**: lock-up expiry calendar, secondary overhang from insiders + VCs, bake-off period (90-180 days post-lockup), sell-side coverage initiation timing
  - **Going-private rumors**: LBO arithmetic at current rates, take-private valuation precedents, anti-trust review timing for strategic acquirers, ROFR / drag-along structure in shareholder agreements
- New top-level field in `source_tags.json`: optional `situation_type` enum ∈ {spinoff, post_bankruptcy, spac, de_spac, busted_ipo, going_private_rumor, none}.
- Plugin 2 gate **G19**: when `situation_type` is set (non-none), memo must use situation-specific valuation framework, not generic SOTP. Verifier: `scripts/verify_special_situations.py`.
- New section in `ic-memo-template-us.md` (conditional, when situation_type non-none).

**Validation tickers.** Recent spin: KVUE (J&J spinoff 2023, established history of post-spin behavior). Recent SPAC/de-SPAC: many candidates from 2022-2024 vintage; pick one with available 12-18 month post-merger price history. Recent post-bankruptcy: emergent equities from 2023-2025.

### Item 6 — PM synthesis adjudication codification

**Hypothesis.** PM synthesis (the brief that ends each Phase) currently treats specialist conflict adjudication as a black box. Codifying the weighting principles when Industry / Forensic / Positioning / Regulatory conflict moves judgment from tribal knowledge to documented method.

**Spec.**

- New reference file `us-equity-research/references/pm-synthesis-adjudication-us.md` (~200 lines):
  - Weighting principles in priority order: Forensic (always dominates structural) → Regulatory (dominates if material) → Industry (base-case anchor) → Positioning (technical overlay) → Channel (timing)
  - Specific adjudication heuristics with named denominators: "if FS surfaces material weakness AND A1 is bullish on cycle, FS dominates and rating ceiling is Hold until weakness is remediated"
  - "If A5 surfaces pending Entity List addition AND A1 says structural tailwind, A5 dominates pending Federal Register confirmation"
  - "If A8 (positioning) flags crowded-long AND A6 revision velocity flags revision-down, the conjunction overrides bullish A1 narrative for technical-side underweighting"
  - Adjudication trail documentation: each agent conflict resolved gets one paragraph in the brief (which agents, what claim, how resolved, what evidence drove it)
- Schema additions: optional `adjudication_trail` array in `memo.json`, each entry capturing conflicting_agents, claim_in_dispute, resolution, supporting_evidence_refs.
- No new gate — this is judgment codification, not validation. The discipline is enforced by the writer, not by a script. If a future Sprint shows the discipline isn't followed, add G20.

**No validation ticker requirement.** Re-run NVDA / JPM and inspect whether the PM synthesis briefs now contain adjudication trails. Qualitative judgment call.

### Item 7 — "$50K pre-IC research" mechanism

**Hypothesis.** Between Phase 2 synthesis and Phase 3 dispatch, the [Topic]-Forensic agent slot in Phase 3 is currently filled by "pick something interesting from Phase 2 findings." This is too vague. Forcing a structured "if I could pay $50K for one piece of primary research right now, what would it be?" question converts the slot to "pick the highest-marginal-cost-of-being-wrong question."

**Spec.**

- ~80 lines added to `phase-3-valuation-us.md`: new section after Phase 2 → Phase 3 hand-off. The analyst writes a single specific research request (expert call with named role at named company, FOIA filing on specific regulatory matter, channel check with specific customer set, primary document retrieval from specific docket). Output is one paragraph identifying the question, the cost-of-being-wrong if not answered, and the operational mechanism (GLG / Tegus / FOIA / etc.).
- The answer drives the [Topic]-Forensic agent specification. Without the $50K question answered, [Topic]-Forensic is dispatched with the question as its target rather than with a generic "pick something" prompt.
- No new gate. Workflow change only. If Sprint 3+ shows the discipline isn't being followed, add G21.

### Sprint 2 cross-cutting decisions

- **Versioning**: v0.3.0 minor bump for both plugins.
- **Schema**: add `"0.3.0"` to the `schema_version` enums (do not remove `"0.2.0"` or `"0.1.0"` — additive).
- **Gates added**: G18 biotech_rnpv, G19 special_situations. (G20+ deferred.)
- **Test ticker expansion**: add SRPT, BMRN for biotech validation; one named SPAC/spin for special situations validation.
- **Sprint 2 validation gate (before tagging v0.3.0)**: re-run MRK end-to-end to confirm rNPV section is correctly conditional (large-cap with multiples passes; pipeline-heavy mid-cap uses rNPV). Re-run a recent SPAC/spin to validate G19. Re-run NVDA to validate adjudication trail in PM synthesis brief. If any fails, Sprint 2 incomplete.
- **Backlog items NOT in Sprint 2**: cyclicals-at-inflection methodology (v0.4.0+), small-cap thin-disclosure adaptation (v0.4.0+).

## 7. Hard NOs — do not build these in Plugin 1 or 2

Stating these explicitly so they survive scope-creep pressure:

1. **Alt-data integration** (Placer.ai, Yipit, Earnest Analytics, Second Measure, M Science). Requires paid subscriptions. Goes in a sister plugin `us-equity-altdata-supplement` that fails closed when subscriptions absent. Building it into Plugin 1 produces fake edge — a checklist that says "compute Placer foot-traffic delta" without actual Placer access is worse than silence.

2. **Real Barra / Axioma factor feed**. Requires paid feed. Sister plugin pattern same as above. Plugin 1's "Barra factor tags on -3 to +3 z-score with brief justification" is *intentionally* a structured guess discipline, not a real factor model. Do not pretend otherwise.

3. **Crowding-cost modeling**. Requires factor history + book-context. Sister plugin or separate research project.

4. **Forensic flag historical backtest**. Requires CRSP/Compustat universe, point-in-time data construction, forward-return computation. This is a 2-3 month research project, not a plugin enhancement. Out of scope for plugin work entirely. If user wants empirical validation of the forensic flags ("SBC > 20% + buyback < SBC + diluted share count growing" → underperformance), that's a separate project.

5. **Non-US / ADR / China VIE deep substance**. Low base-rate for a US-focused plugin. Right move: sister plugin `non-us-equity-research` or use the existing `china-equity-research` skill that's already in the user's skill tree. Adding a thin ADR section to Plugin 1 creates false capability impression.

6. **A "find me alpha" agent**. The discipline is to gate edge claims, not to generate them. Avoid suggesting any feature framed as "Claude finds non-consensus opportunities." See §10.

## 8. Backlog (open items, not Sprint 2)

These are real follow-ups but explicitly *not* Sprint 2 work. File or mention only when relevant.

1. **JPM live re-run validation (v0.2.0 follow-up)**. The CHANGELOG entry for v0.2.0 explicitly notes "JPM re-run validation pending — requires live agent dispatch." This is the only test that proves G15 / G16 / G17 actually fire on real content rather than synthetic fixtures. **Highest-priority backlog item**. Run `/us-equity-ic-rigor:ic-memo JPM` in a Claude Code session, inspect whether bank discipline content appears and gates fire as designed.

2. **v0.1.x memo data drift (Sprint 1 discovery)**. Schema validation against `memo.json` surfaced five field-level divergences in the existing self-test memos: NVDA `what_would_reverse[].direction` uses `reverse_base_to_bear` which is not in the enum; JPM `gm_taxonomy.reconciliation_consolidated_vs_implied_bp` is `null` where schema requires number; MRK `tail_risks` items have shape mismatch; XOM `headline.default_action` uses `'hold'` which should be `'hold_long'` or `'hold_short'`; DLR `valuation.methods` items have shape mismatch. These pre-date v0.2.0. Either fix the five memos (~30 min) or relax the schema to accept the divergent shapes (drops gate coverage — risky). File as GitHub issue.

3. **B15-B17 rubric documentation in Plugin 2**. `us-equity-ic-rigor/references/pm-redteam-rubric-us.md` still details only B1-B14. Plugin 2 SKILL.md mentions B15-B17 and the gates exist, but the rubric reference file does not carry the remediation discipline for the new bug classes. Sprint 2 or Sprint 3 follow-up.

4. **Test fixture coverage for G15/G16/G17**. v0.1.x had a 15-fixture-per-gate cross-sensitivity matrix proving each verifier fires only on its own bug class. The three new gates have smoke-test coverage only (7 smoke tests, all passing). Building the matching matrix is ~3-5 sessions of fixture authoring. Required before claiming production readiness on G15-G17 against arbitrary memos.

5. **Public visibility decision**. Repo is currently `--private`. Decision deferred until: (a) user decides on compliance posture vis-à-vis any employer outside-business-activity rules, (b) memos in `outputs/` are relocated to `examples/` with disclaimer + LICENSE file added. See discussion in earlier session transcripts.

6. **Default branch rename done** (v0.1.x → v0.2.0 transition): was `build-us-equity-skill`, now `main`. v0.1.x tag history was on the feature branch but reachable via tag.

## 9. Files to read on first invocation (in this order)

For the new session to be productive, read these in order before suggesting any changes:

1. **This file** (`design/session-handoff-v0_2_to_v0_3.md`) — you're already doing this.
2. `CHANGELOG.md` — the v0.2.0 entry has the most detailed Sprint 1 reconstruction.
3. `README.md` — for the user-facing description of the system.
4. `us-equity-research/SKILL.md` — Plugin 1 orchestration spine, 262 lines + v0.2.0 augmentations.
5. `us-equity-ic-rigor/SKILL.md` — Plugin 2 PM red-team layer, 224 lines + v0.2.0 augmentations.
6. `us-equity-research/references/consensus-variance-us.md` — the canonical example of v0.2.0's discipline-style reference file. Read this to understand the writing standard for new reference files in Sprint 2.
7. `design/open-decisions.md` — D1-D24 design decisions register. The decisions that informed v0.1.x architecture are still binding.
8. `schemas/source_tags.json` — the canonical schema with v0.2.0 additions (consensus_variance, revision_velocity, bank_metrics blocks).
9. `schemas/verification_gates.json` — the 17-gate definitions catalog.
10. `scripts/verify_consensus_variance.py` — the canonical example of a v0.2.0 verifier script. Read to understand the pattern (pydantic v2, structured stdout, n_a branching, exit codes) before writing new verifiers in Sprint 2.

For Sprint 2 specifically, also read the reference files closest to the Sprint 2 work:

11. `us-equity-research/references/phase-1-deep-dive-us.md` — for the FS-Banks Augmentation pattern (the model for biotech rNPV sector-conditional dispatch in Sprint 2 Item 4).
12. `us-equity-research/references/phase-2-continuation-us.md` — for the A-Consensus specialist pattern (the model for any new Phase 2 specialist in future sprints).
13. `us-equity-research/references/valuation-discipline-us.md` — for the existing biotech multiples / NPV stub that Sprint 2 Item 4 expands on.
14. `us-equity-research/references/phase-3-valuation-us.md` — for the [Topic]-Forensic slot that Sprint 2 Item 7 ("$50K pre-IC") restructures.

## 10. Honest limitations (red team voice on what's been built)

Stating these so the new session doesn't overstate what v0.2.0 accomplished. The user asked the question explicitly at the end of the previous session: "have we addressed the consensus-driven issue?" The honest answer is **structurally yes, substantively partially, alpha-wise no**.

- **The discipline doesn't generate edge — it disciplines the claim of edge.** G15 is a quality gate, not an alpha gate. It catches the most common LLM and junior-analyst failure mode (decorative variance language without numerical content) and forces explicit "consensus-anchored" labeling when no real variance exists. Memos that pass G15 are not automatically alpha-generating; they are at minimum non-fraudulent in their edge claims.
- **The 2.0pp sizing threshold for G15 is arbitrary.** No empirical calibration; chosen on principle. If running across a coverage list shows variances cluster at 2.0-2.5pp, that's anchoring to the threshold (degenerate behavior) and the threshold needs recalibration.
- **The "honest base rate" calibration (1-2 variances for 30-50% of names) is an estimate, not a measured frequency.** Until A-Consensus runs across a real coverage list of 10+ names, we don't know whether the escape hatch is being used at the right rate.
- **A-Consensus declares in Phase 2; R-v2 attacks in Phase 3.** One-phase lag between variance declaration and adversarial pressure. Worth tracking how often R-v2 kills a Phase 2-declared variance; if frequent, Phase 2 gate is too permissive.
- **S1-S3 evidence ≠ non-consensus interpretation.** The discipline catches "Street hasn't pulled this primary source" cleanly. It's weaker on "Street pulled the same source but interpreted differently." Arguing about interpretation quality is harder to gate mechanically.
- **No backtest validates G11-G17 predictive value.** The whole construction is theoretically motivated. We do not know whether names triggering G12 (SBC excluded from FCF without flag), G15 (declared load-bearing variance), or G16 (bank discipline gap) actually correlate with forward return underperformance. Until the forensic-flag historical backtest runs, the framework is *defensible* but not *validated*.
- **Plugin 1 still has the gaps the audit named that are NOT in Sprint 1 / Sprint 2.** Cyclicals-at-inflection methodology, small-cap thin-disclosure adaptation, non-US/ADR substance, real alt-data integration. These are explicitly deferred or out-of-scope; they remain real gaps.

For external positioning (interviews, LP pitches, portfolio reviews): the accurate framing is "we built a structured discipline that prevents consensus-anchored memos from masquerading as non-consensus views, and forces explicit edge claims to carry S1-S3 evidence and sized scenario impact." The inaccurate framing would be "v0.2.0 helps Claude find non-consensus opportunities." It does not. It just doesn't let Claude pretend otherwise.

## 11. First-action recommendation for the new session

When the user invokes the new Cowork session with a starter prompt pointing here:

1. **Confirm orientation**. Read this file fully + the files in §9 lines 1-10. Then report back to the user in ≤200 words: what is the system, what just shipped, what's the immediate next item per the user's direction.
2. **Wait for user direction.** The user may want any of:
   - JPM live re-run (highest-priority backlog item — validates v0.2.0 works on real content)
   - Sprint 2 execution starting with Item 4 (biotech rNPV)
   - Sprint 2 execution starting with Item 5 (special situations) or Item 6 (PM synthesis) or Item 7 ($50K pre-IC)
   - v0.1.x memo data drift cleanup (Sprint 1 follow-up)
   - Something not on the backlog (user discretion)
3. **Do not start Sprint 2 work without explicit direction.** The Sprint 2 spec is execution-ready but the order of items within Sprint 2 is a user decision. State the four items + their dependencies, recommend Item 4 (biotech rNPV) as the natural first because it has the cleanest pattern match with v0.2.0's bank-discipline addition, and wait for confirmation.
4. **If the user says "begin Sprint 2," do not redesign Sprint 2.** The spec in §6 above is the contract. State assumptions, proceed.
5. **If the user pushes back on any Sprint 2 design choice**, that's a redesign request — treat as new work, not as continuing Sprint 2. Update this handoff document or create a new design note.

## 12. Operational notes carried forward

- **The user runs `pytest -q` for regression validation**. v0.2.0 passes with 198 tests. Run before any tag.
- **Schema validation requires a `RefResolver` with `store` keyed by `$id` URL** (not bare filenames). Do not give the user a validation command without proper resolver setup. The naked `jsonschema.validate(data, schema)` against `memo.json` will fail with "Unresolvable" errors because of cross-file `$ref`s.
- **Commit messages with multi-line content must use `git commit -F /tmp/<msg-file>.txt`** with the message written via heredoc (`cat > /tmp/<file> << 'EOF' ... EOF`). Multi-line `-m "..."` paste has corrupted commits twice in this project's history. Trust the user when they say a paste is going wrong — the zsh shell behavior on this user's machine has well-documented quirks.
- **Git tags attach to current HEAD.** If a commit fails (e.g., due to `.git/index.lock`), do NOT run `git tag` before fixing the commit, or the tag will attach to the prior HEAD and push to origin with the wrong reference. Recovery requires `git tag -d <tag>` locally and `git push origin :refs/tags/<tag>` to delete the misplaced remote tag.

---

## Starter prompt for the new Cowork session

Paste this at the start of the new session:

> I'm continuing work on the us-equity-research / us-equity-ic-rigor plugin system at /Users/hongyi/projects/us-equity-research (also at https://github.com/equity-rigor/us-equity-research private). v0.2.0 just shipped on 2026-05-29. Before doing anything else, read `design/session-handoff-v0_2_to_v0_3.md` in the workspace folder — it contains my preferences, the project architecture, what was just shipped (Sprint 1), the Sprint 2 plan, explicit hard-NOs, and honest limitations of what's been built. After reading the handoff file plus the files it points you to in §9 lines 1-10, report back in ≤200 words: what is the system, what just shipped, what's the immediate next item per the priority recommendation. Then wait for my direction before starting any execution work.

---

**End of handoff document.** Last updated 2026-05-29 by the v0.2.0 ship session. Next update: end of Sprint 2 / v0.3.0 ship.
