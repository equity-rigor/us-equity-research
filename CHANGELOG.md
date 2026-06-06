# Changelog

All notable changes to this project will be documented in this file. Format
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) +
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] — 2026-06-06

### Sprint 4 — Privacy, UX, CI, regression coverage

A second v0.5.x release the same day as v0.5.0, bundling Sprint 4 hygiene
items that were not strictly blocking but are credibility-critical before
HN promotion: maintainer-email scrub, plugin-level permission defaults,
real CI workflows, Python packaging manifest, and a schema-version
regression meta-test that already caught two real silent-skip bugs in G19
and G20 the moment it ran.

### Fixed — Schema-version silent-skip bugs in G19 and G20

The new `scripts/tests/test_schema_version_coverage.py` meta-test immediately
caught that `verify_provenance_manifest.py` (G19) and `verify_view_defensibility.py`
(G20) both had `RUNNABLE_SCHEMA_VERSIONS = {"0.3.0", "0.4.0"}` and would
silently skip on the new v0.5.0 schema. This is the exact bug class that
required Sprint 3a's G20 fix and Sprint 3b's G19 fix — recurrence demonstrates
why the meta-test was needed. Also fixed `verify_view_defensibility.py` line
401: `if schema_version == "0.4.0":` was a literal-equality check on the
graduated rigor scale that would have excluded v0.5.0 memos. Replaced with
membership against `GRADUATED_RIGOR_SCHEMA_VERSIONS = {"0.4.0", "0.5.0"}`.

### Changed — Maintainer email scrubbed from all repo files (privacy)

Replaced `hg2670@columbia.edu` everywhere with the GitHub no-reply pattern
`equity-rigor@users.noreply.github.com`. Affected files: both plugin.json,
marketplace.json, four design docs. Author name "Hongyi Gu" remains in
LICENSE and README copyright lines (legally accurate authorship attribution
for an MIT-licensed work).

The SEC User-Agent reference in `us-equity-research/references/us-data-sources.md`
was updated to explicitly forbid the orchestrator from hardcoding the
maintainer email in EDGAR User-Agent headers. Going forward, Phase 0 setup
should prompt for the user's preferred contact email or default to a
framework-identifier form. This prevents the MU-run pattern where the
maintainer's email was sent to SEC across user requests.

### Added — Plugin-level permission auto-approve (UX)

New `.claude/settings.json` at repo root with a `permissions.allow` array
that auto-approves the safe, repetitive commands the framework makes during
a normal memo run: SEC EDGAR fetches (URL-pattern gated), framework verifier
scripts, read-only filesystem ops, read-only git ops, EDGAR/FRED WebFetch
domains, WebSearch. Eliminates roughly 30-50 permission prompts per memo run
for users who clone the repo. Marketplace-install users need to copy the
snippet into their own `~/.claude/settings.json`; the README documents this.

Conservative by design: anything not on the allowlist still prompts. Curl
is URL-pattern gated, not blanket-allowed. Write operations (`git add`,
`git commit`, `git push`, `rm`) all stay in the `ask` list. Sensitive paths
(`.env`, `~/.ssh`, `~/.aws`, `~/.kube`, `~/.git-credentials`) are explicitly
denied.

### Added — Real CI workflows

- `.github/workflows/pytest.yml` — runs `pytest -q` on Python 3.11 and 3.12,
  validates all schemas as JSON, validates marketplace.json and both
  plugin.json files, runs `bash scripts/sync_plugin_files.sh --check` to
  catch plugin/repo-root drift.
- `.github/workflows/lint.yml` — runs `ruff check scripts/` and `ruff format
  --check scripts/` on Python 3.12.

The README's static "tests passing" badge is no longer a marketing claim
backed by no visible workflow — actual CI gates every push to main.

### Added — Schema-version regression meta-test (Sprint 4 Item 5)

`scripts/tests/test_schema_version_coverage.py` (23 new tests) walks every
`scripts/verify_*.py` and:

- Asserts no bare literal equality check like `if schema_version != "X.Y.Z":`
  in executable code (the silent-skip bug pattern). Docstring matches are
  excluded via AST-based docstring-range detection.
- For verifiers that define `RUNNABLE_SCHEMA_VERSIONS`, asserts the latest
  known schema version is in the set. If you add v0.6.0 to memo.json's
  enum but forget to add it to a verifier's RUNNABLE_SCHEMA_VERSIONS, the
  meta-test fails.
- Asserts `KNOWN_SCHEMA_VERSIONS` in the test matches the enum in
  `schemas/memo.json` — catches drift between the test and the schema.

The meta-test paid for itself the moment it ran by catching G19 and G20 as
described above.

### Added — Python packaging manifest

`pyproject.toml` declares the project (`us-equity-research-verifiers`, v0.5.1,
Python 3.11+, pydantic >= 2), the dev extras (`pytest`, `ruff`), the testpaths
pointing at `scripts/tests/`, and the ruff lint/format configuration. Allows
`pip install -e .[dev]` from a clone for a reproducible dev environment.
The pytest `addopts` explicitly excludes `scripts/tests/smoke_g20_graduated_rigor.py`
from collection so the committed `pytest -q` count stays auditable.

### Migration — v0.5.0 → v0.5.1

No memo content migration required. No schema changes. Users on v0.5.0 should
`/plugin update equity-rigor/us-equity-research` to receive the bug fixes
(G19/G20 RUNNABLE_SCHEMA_VERSIONS) and the scrubbed maintainer email. Users
who cloned the repo get the new permission auto-approve defaults
automatically the next time they run `claude` from the repo directory.

### Test baseline

- v0.5.0: 284 passed (270 prior + 14 plugin-file-sync).
- v0.5.1: **266 passed, 17 skipped** (added 23 schema-version meta-tests;
  some sub-tests intentionally skip for verifiers without RUNNABLE_SCHEMA_VERSIONS
  pattern, which is correct behavior — pre-version-gating verifiers like
  G1-G10 don't need the check).

## [0.5.0] — 2026-06-06

### Sprint 4 — Verifier reachability fix + consolidated output convention

Two related fixes that surfaced together from the end-to-end MU run on
2026-06-06. Both close gaps the v0.4.0 framework was advertising but not
actually delivering for users who install via the marketplace and run from
outside the cloned repo.

### Fixed — CRITICAL: Verifier scripts now reachable from plugin install (Item 8)

Prior versions (v0.1.0 through v0.4.0) distributed only the plugin directories
via the marketplace; the repo-root `scripts/` and `schemas/` directories were
NOT copied into `~/.claude/plugins/<plugin>/<version>/`. When users invoked
the framework from any directory outside the cloned repo, the agent could not
reach `scripts/verify_*.py` and silently degraded to LLM-graded "analytical"
gate evaluation. This silently nullified the framework's 20-gate verification
claim for typical install flows.

**Fix:** Each plugin directory now bundles its own `scripts/` and `schemas/`
subdirectories, synced from the canonical repo-root sources via
`scripts/sync_plugin_files.sh`. CI fails if the sync is stale (see
`scripts/tests/test_plugin_file_sync.py`). SKILL.md and command files now use
explicit `${CLAUDE_PLUGIN_ROOT}/scripts/verify_*.py` paths. Both SKILL.md
files have a new anti-degradation preamble at the top that forbids silent
fallback to analytical evaluation.

**Operator-explicit override path:** If a user is in a sandboxed environment
where Python scripts genuinely cannot be reached, they can authorize an
analytical-only run by stating "I understand the verifiers won't run; proceed
analytically anyway." The agent must then set
`memo_metadata.gates_evaluated_analytically: true` in the structured JSON,
include a visible disclaimer in the IC memo header, set every gate's
`evaluation_method` to `analytical_llm` in verification_gates.json, and cap
the rubric score at 7.5. This makes degradation loud, not silent.

**Discovery:** Found during MU end-to-end run 2026-06-06. The MU run's
manifest documented the degradation directly: "Manifest hand-assembled
because plugin scripts/write_manifest.py + schemas/ are absent in working
dir." Honest disclosure of the degradation by the orchestrator is what
surfaced the bug; the framework's own provenance discipline caught its own
packaging defect.

### Changed — Consolidated structured.json output convention (Item 9)

The v0.4.x convention required Phase 3 to write five separate JSON files
per memo (`<TICKER>_structured.json`, `_source_tags.json`, `_scenarios.json`,
`_verification_gates.json`, `_manifest.json`). The MU run naturally
consolidated `source_tags` and `scenarios` as nested sub-objects inside
`structured.json` rather than splitting them — and the result was easier to
read, easier to verify, and equally machine-parseable.

**New v0.5.0+ convention:** four files per memo, not five:

- `<TICKER>_IC_memo.md` — human-readable memo (unchanged)
- `<TICKER>_structured.json` — consolidated machine-readable representation
  containing memo_metadata + recommendation + source_tags + scenarios +
  consensus_variance + quant_overlay + bear_eps_bridge + what_would_reverse +
  position_sizing + adjudication_trail (all inline; no sidecars)
- `<TICKER>_verification_gates.json` — verifier audit trail (Phase 4 output)
- `<TICKER>_manifest.json` — provenance manifest (G19 input)

Plus optional `<TICKER>_redteam_round_N.md` for each PM red-team iteration.

**Backward compatibility:** v0.1.x through v0.4.x memos using the five-file
split convention remain valid. Verifier scripts continue to accept separate
`--source-tags-json` and `--scenarios-json` arguments for grandfathered runs.
Future verifier behavior reads sub-objects from the consolidated structured
JSON first, falling back to separate files if not found.

### Added — v0.5.0 schema additions

- `schemas/memo.json` schema_version enum extended to include "0.5.0".
- `schemas/memo.json` adds `memo_metadata.gates_evaluated_analytically`
  boolean field (default false) for the operator-explicit override path.
- `schemas/verification_gates.json` schema_version enum extended to include
  "0.5.0".
- `schemas/verification_gates.json` adds per-gate `evaluation_method` enum
  field (`programmatic_script` | `analytical_llm` | `manual_review`).
  Required for v0.5.0+ memos; missing field on pre-v0.5.0 memos is
  grandfathered as `programmatic_script` (the assumed default).

All changes are strictly additive. Existing v0.1.0-v0.4.0 memos validate
clean against the v0.5.0 schemas without modification.

### Added — sync infrastructure

- `scripts/sync_plugin_files.sh` — maintains plugin copies of repo-root
  scripts and schemas. `bash scripts/sync_plugin_files.sh` applies the sync;
  `--check` mode reports drift and exits 1 (used by CI).
- `scripts/tests/test_plugin_file_sync.py` — pytest module verifying
  SHA-256 match of plugin copies against repo-root sources. Fails CI if any
  plugin script or schema drifts from canonical source. 7 test functions
  covering source dirs exist, plugin dirs exist, plugin scripts/ exists,
  plugin schemas/ exists, script content match, schema content match, no
  orphan files.
- `design/sprint-4-item-8-verifier-reachability.md` — design doc explaining
  root cause, alternatives considered, and chosen approach.
- `design/sprint-4-item-8-skill-preamble.md` — the SKILL.md preamble text +
  insertion points + companion edits documentation.

### Migration — v0.4.0 → v0.5.0

Users on v0.4.0 should run `/plugin update equity-rigor/us-equity-research`
to receive the bundled scripts/schemas and the updated SKILL.md preambles.
No memo content migration required; all v0.4.0 outputs validate clean against
v0.5.0 schemas.

If you wrote a v0.4.0 memo with self-graded gates because the verifier
scripts weren't reachable (the MU run pattern), set
`memo_metadata.gates_evaluated_analytically: true` and add the disclaimer
manually before re-validating. The v0.5.0 verifiers respect the field; an
honest pre-existing analytical run does not need to be redone, only labeled.

## [0.4.0] — 2026-05-30

### Sprint 3a — R-v2 adversarial isolation + graduated rigor scale

v0.3.0's G20 closed the "rubric grades structure, not view" finding by
requiring a surviving R-v2 `variance_attack` for any score above 8.5. But
v0.3.0's R-v2 ran inside the orchestrator session — the A-Consensus reasoning
trace, the PM brief, and the bull narrative all sat in its context. That is
the writer arguing with itself, and a model is a weak adversary against its
own prior. Sprint 3a makes R-v2 a structurally independent attacker within
Claude-only infrastructure (no GPT/Gemini) and discriminates the top of the
rubric on whether that independence was actually exercised.

### Added — isolated R-v2 subagent spawn pattern (Item 1)

New reference `us-equity-research/references/r-v2-isolated-attack-us.md`. The
orchestrator dispatches R-v2 via the Task tool at end of Phase 2 with a
prompt containing ONLY the structured `consensus_variance` JSON, the
`source_tags.top_anchors` JSON, the 5-point attack methodology, the
adversarial framing + win condition, and tool access (WebSearch / WebFetch /
EDGAR). It MUST NOT contain A-Consensus's narrative, the PM brief, the bull
thesis, or the memo draft. The win condition is explicit: a run that
concludes "the variances look reasonable" is FAILED; the incentive is to find
what the analyst missed, with an independent source re-read per attack point.
A bounded ~30-50K-token context forces R-v2 to attack 3-4 variances hard
rather than 20 thinly. `phase-3-valuation-us.md` and
`phase-2-continuation-us.md` are wired for the isolated dispatch plus the
A-Consensus self-containment requirement (every `evidence_ref` retrievable by
URL or full citation; no implicit references to prior-brief content).

### Added — adversarial isolation tracking fields (Item 2)

`schemas/memo.json` `adjudication_trail_entry` gains three optional fields on
`variance_attack` entries: `attacker_model` (free-form model id, e.g.
"claude-sonnet-4-6"), `attacker_context_isolation` (bool — true if R-v2 ran
isolated without the A-Consensus trace), and `attacker_independent_source_reads`
(int ≥ 0 — independent WebFetch/WebSearch reads for this variance,
distinguishing ≥3-read thorough attacks from shallow ones). Additive-only:
none are required, so v0.1.x / v0.2.0 / v0.3.0 memos and field-less v0.4.0
`variance_attack` entries validate clean. `schema_version` enums in
memo / source_tags / scenarios / verification_gates extended to include
"0.4.0"; document-level metadata `schema_version` bumped to 0.4.0 in memo.json
only (the sole schema that gained its own fields).

### Added — G20 graduated rigor scale (Item 3)

`scripts/verify_view_defensibility.py` keeps the v0.3.0 conditions
(a)+(b)+(c) as the 8.5–9.0 gate and adds a graduated tier: a memo that
*claims* `memo_metadata.current_score` strictly above 9.0 must additionally
show ≥1 surviving `variance_attack` on a load-bearing variance with
`attacker_context_isolation == true` AND `attacker_model != writer_model`
(`memo_metadata.author_model`; literal string inequality, no semver parse).
Missing isolation, missing model diversity, or an undeterminable writer model
each cap the claim at 9.0 — NOT 8.5; the 8.5–9.0 band stays earned by the
v0.3.0 conditions. Fixed a latent bug in passing: the prior schema_version
branch would have silently skipped G20 on every v0.4.0 memo. The runnable set
is now {0.3.0, 0.4.0}; distinct exit codes 8 / 9 / 10 attribute
undeterminable-writer / no-isolated-attack / attacker-shares-writer-model.

### Added — Plugin 1 orchestrator wiring + isolation fixtures (Items 4, 5)

`us-equity-research/SKILL.md` Phase 3 now specifies the R-v2 Task dispatch
(`description="R-v2 isolated adversarial attack"`, no `subagent_type`, default
attacker model "claude-sonnet-4-6" for cross-size diversity vs the Opus
orchestrator), the expected `adjudication_trail` output, and the spawn-failure
enforcement loop: if R-v2 finds zero attack points on a load-bearing variance,
the orchestrator demotes it (`load_bearing=false`) and re-runs G15 — a
variance no isolated red team can dent is defensible; one that cannot be
attacked on any specific dimension is decorative. New fixtures in
`scripts/tests/fixtures/r-v2-isolation/` (weak = S3-only, fails G20(b);
medium = S2, passes G20(b); `expected_attack_dimensions.json` answer key) and
`scripts/tests/smoke_g20_graduated_rigor.py` — 10 branches: the 6 required
(Item 3 Deliverable 3c) plus 9.0-boundary / pre-0.3.0 grandfather /
undeterminable-writer / additive-cap (a 9.0+ claim failing condition (b) still
caps at 8.5) guards.

### Test surface

198 pytest tests still passing — unchanged. Sprint 3a added no `test_*`
modules; the G20 graduated rigor is covered by the standalone smoke harness
`scripts/tests/smoke_g20_graduated_rigor.py`, run directly and deliberately
not collected by pytest (filename is not `test_`-prefixed) so the committed
count stays at 198. `verification_gates.json` gate_id enum unchanged at
G1–G20 (Sprint 3a tightened G20, added no gate numbers; `gates` maxItems 20).

### Honest framing — what landed vs what is still loose

- The 9.0+ tier trusts SELF-REPORTED `attacker_*` fields. A memo can assert
  `attacker_context_isolation=true` and a diverse `attacker_model` without the
  orchestrator having actually spawned an isolated subagent. True isolation
  provenance — subagent id, bounded-context trace, and the attacker's
  independent web reads logged to the manifest and cross-checked against
  `web_search_log` — is unbuilt. The gate raises the cost of faking a 9.0+; it
  does not make one impossible. Candidate for a later sprint.
- Narrative prose in the SKILL.md files still carries stale gate-count
  phrasing in places ("17 gates", "14 gates") predating the G18–G20 additions.
  The machine-checked artifact (`verification_gates.json`) is correctly
  G1–G20. Cosmetic documentation debt, flagged not swept, to avoid prose churn
  in a wrap session.

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
