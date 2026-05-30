# Sprint 3a Auto-Execution Context

This file is the self-contained briefing for any scheduled session executing Sprint 3a work. Each daily session reads this file plus `design/sprint-3a-status.json`, identifies the next pending item, executes it end-to-end, commits, updates the status file, and pushes. After 5 days of successful runs, Sprint 3a is complete and v0.4.0 ships.

## Quick orientation for the scheduled session

- **User**: Hongyi Gu (`hg2670@columbia.edu`). Quant researcher / buy-side analyst. Institutional depth, red-team voice, no hand-holding, no clarifying questions when assumptions can be stated.
- **Repo**: `/Users/hongyi/projects/us-equity-research` (origin: `https://github.com/GGHongyi/us-equity-research`, private).
- **Current state**: v0.3.0 shipped 2026-05-29 (commit `00d85b8` on `main`). Both plugins at version 0.3.0.
- **Sprint 3a goal**: Close the adversarial isolation gap — make R-v2 a structurally independent attacker within Claude-only infrastructure (no GPT/Gemini). Per the design conversation, this is the highest-severity remaining issue after v0.3.0.
- **Target version**: v0.4.0 (minor bump for additive changes, schema_version enum extension to include "0.4.0").
- **Cadence**: One Sprint 3a item per daily session. 5 items total → 5 days → ships v0.4.0.

## Required reading on first invocation (before executing any item)

In order:
1. This file in full.
2. `design/sprint-3a-status.json` — current progress.
3. `CHANGELOG.md` v0.3.0 entry — most detailed recent reconstruction.
4. `us-equity-research/SKILL.md` Manifest generation + Scope and Limitations sections (v0.3.0 additions).
5. `us-equity-ic-rigor/SKILL.md` Scope and Limitations + gates list (G18/G19/G20 documented).
6. `us-equity-research/references/pm-synthesis-adjudication-us.md` — the existing R-v2 5-point attack methodology (Sprint 2 Item 5 deliverable).
7. `schemas/memo.json` definitions/adjudication_trail_entry — schema R-v2 attacks write into.
8. `scripts/verify_view_defensibility.py` — G20 verifier, the gate Sprint 3a tightens.

## Universal constraints (apply to every session)

- **Schema changes are additive-only.** Use the schema_version enum grandfathering pattern established in v0.2.0 / v0.3.0. v0.1.x, v0.2.0, v0.3.0 memos must continue to validate clean against v0.4.0 schemas.
- **Smoke test all new verifier scripts.** Multiple branches per gate, including pass / fail / n_a / grandfathered paths. Pattern: synthetic JSON fixtures in `/tmp/`, run verifier, check exit code + structured stdout. Match the v0.3.0 smoke test patterns (see prior commits for examples).
- **Pydantic optional import shim.** New verifier scripts must use the `try: from pydantic import ... except ModuleNotFoundError: ...` shim pattern (see `verify_source_tags.py` or `verify_sotp_monotonicity.py` for examples). The user's production environment has pydantic; the CI/sandbox environment doesn't.
- **Heredoc-via-file for multi-line commit messages.** Write the commit message to `/tmp/v0.4.0-itemN-msg.txt` via `cat > /tmp/file.txt << 'EOF' ... EOF`, then `git commit -F /tmp/file.txt`. Multi-line `git commit -m "..."` paste has corrupted commits twice in this project's history. The heredoc-to-file pattern is the safe path.
- **No inline `#` comments in copy-paste shell blocks.** The user's zsh has `interactive_comments` off and treats `#` as a command. Annotate in prose around blocks, not inside them.
- **Disable git auto-pager for stat output.** If the session opens a new shell, run `git config --global pager.stat false` once. Auto-pager interrupted both v0.2.0 and v0.3.0 ships; this prevents recurrence.
- **If blocked or uncertain, STOP — do not guess.** Set `blocked: true` and `blocked_reason: "<specific question>"` in `design/sprint-3a-status.json`, commit that status update, and exit without modifying anything else. The user reviews on next observation.
- **Red-team voice in commit messages and any documentation written.** No cheerleading. State honestly what landed and what's still loose.

## Versioning and schema strategy for Sprint 3a

- `schema_version` enums in memo.json, source_tags.json, verification_gates.json, scenarios.json all extend from `["0.1.0", "0.2.0", "0.3.0"]` to `["0.1.0", "0.2.0", "0.3.0", "0.4.0"]`.
- `manifest.json` schema_version stays at `const "0.3.0"` until manifest structure itself changes (Sprint 3a may add `attacker_model` and `attacker_context_isolation` fields under `agent_provenance` — if so, bump manifest.json to "0.4.0" via enum extension matching the other schemas).
- `verification_gates.json` gate_id enum extends to include any new gate IDs added (Sprint 3a does NOT add new gate numbers; it tightens G20). The `gates` array maxItems stays at 20.
- v0.3.0 memos continue to run G20 with the v0.3.0 conditions. v0.4.0 memos run G20 with the tightened conditions (graduated rigor scale: 8.5-9.0 uses v0.3.0 G20; 9.0+ additionally requires adversarial isolation per Item 3).

## The 5 Sprint 3a items (execute in order)

### Item 1 — Isolated R-v2 subagent spawn pattern (estimated 3 sessions of agent time; 1 daily scheduled run)

**Deliverable 1a:** New reference file `us-equity-research/references/r-v2-isolated-attack-us.md` (~250 lines) documenting:

- *Subagent spawn contract.* The orchestrator at end of Phase 2 dispatches R-v2 via the Task tool with `description="R-v2 isolated adversarial attack"`. The R-v2 prompt MUST contain only: the structured consensus_variance JSON, the structured source_tags.top_anchors JSON, the 5-point attack methodology, the explicit adversarial framing and win condition, and tool access to WebSearch / WebFetch / EDGAR. The R-v2 prompt MUST NOT contain: A-Consensus's narrative output, the PM Synthesis brief, the bull-thesis narrative, the full IC memo draft.
- *5-point attack methodology* (reference the existing 5 dimensions from `pm-synthesis-adjudication-us.md`: evidence_credibility, triangulation_completeness, base_rate_sanity, catalyst_dependency, timing_arbitrage). Each dimension gets ~30 lines: what to attack, what evidence rebuts the attack, what makes the attack survive.
- *Win condition specification.* R-v2's prompt explicitly: "Your success criterion is to find at least one attack point per load-bearing variance, with documented evidence supporting the attack. A run that concludes 'the variances look reasonable' or 'no specific weaknesses identified' is FAILED. Your incentive is to find what the analyst missed."
- *Independent source re-verification requirement.* For each attack point, R-v2 must independently pull at least one source document via WebFetch on the cited URL or WebSearch for the specific evidence_ref, quote the specific passage R-v2 is using to attack, and record the WebSearch/WebFetch call in the manifest's web_search_log.
- *Bounded context window.* R-v2's prompt explicitly limits its context to ~30-50K tokens of structured inputs + tool use. This forces R-v2 to be selective about which 3-4 variances it attacks hard rather than 20 thinly.
- *Output schema.* R-v2 returns one adjudication_trail_entry per variance attacked, each with `type="variance_attack"`, `target_variance_id`, `attack_type` in the 5 canonical dimensions, `attack_description`, `attack_outcome` in {rebutted, modified, conceded}, `supporting_evidence_refs` (the source citations R-v2 pulled), and new fields `attacker_model` + `attacker_context_isolation=true`.
- *Failure modes and remediation.* If R-v2 spawn fails or returns "no attack points found" on a load-bearing variance, the orchestrator must flag the variance as `load_bearing=false` (or remove it from the load-bearing set). G15 may then fail because the memo now lacks a load-bearing variance with adequate evidence, forcing the analyst to reconsider whether the rating can be non-Hold.

**Deliverable 1b:** Update `us-equity-research/references/phase-3-valuation-us.md` (find the R-v2 section, add explicit subagent dispatch instructions referencing the new isolated-attack reference file).

**Deliverable 1c:** Update `us-equity-research/references/phase-2-continuation-us.md` A-Consensus section: add a note that R-v2 will be dispatched as an isolated subagent and will see only the structured consensus_variance entries, not the narrative reasoning. A-Consensus must make each consensus_variance entry self-contained — every evidence_ref must be retrievable by URL or full citation; no implicit references to prior PM brief content.

**Commit message after Item 1**: `"Sprint 3a Item 1: isolated R-v2 subagent spawn pattern + 5-point attack methodology documentation"`

### Item 2 — Schema augmentation for adversarial isolation tracking (~1 session)

**Deliverable 2a:** Extend `adjudication_trail_entry` in `schemas/memo.json` with three new optional fields:

- `attacker_model`: optional string. Free-form identifier of which model produced this attack entry. Examples: "claude-opus-4-6", "claude-opus-4-8", "claude-sonnet-4-6", "claude-opus-4-8-with-extended-thinking". The orchestrator sets this when it spawns the R-v2 subagent.
- `attacker_context_isolation`: optional boolean. True if R-v2 was spawned as an isolated subagent without A-Consensus reasoning trace in its context. False (or absent) means R-v2 ran in the same orchestrator session as A-Consensus.
- `attacker_independent_source_reads`: optional integer ≥ 0. Count of WebFetch/WebSearch calls R-v2 made specifically to verify or attack this variance. Useful for distinguishing thorough attacks (≥3 independent reads) from shallow ones.

**Deliverable 2b:** Update `us-equity-research/references/pm-synthesis-adjudication-us.md` to reference the new fields. Specifically, add a subsection "Adversarial isolation tracking (v0.4.0)" explaining what each field means and when each should be populated.

**Deliverable 2c:** Bump schema_version enums in `schemas/memo.json`, `schemas/source_tags.json`, `schemas/verification_gates.json`, `schemas/scenarios.json` to include `"0.4.0"`.

**Commit message after Item 2**: `"Sprint 3a Item 2: schema additions for attacker_model + attacker_context_isolation + attacker_independent_source_reads"`

### Item 3 — G20-augment verifier check for adversarial isolation (~1 session)

**Deliverable 3a:** Extend `scripts/verify_view_defensibility.py` with a new graduated rigor scale:

- For memos claiming score in (8.5, 9.0]: require the v0.3.0 G20 conditions (a)+(b)+(c) — already implemented; do not change.
- For memos claiming score above 9.0: additionally require `attacker_context_isolation == true` AND `attacker_model != writer_model` on at least one surviving variance_attack entry.

The "writer_model" comes from `memo_metadata.author_model` if present, OR from `manifest.plugin_versions.us_equity_research` matched against the model used (the manifest's writer model should be the same as A-Consensus's model, since both run in Plugin 1's orchestrator session).

For the check, "writer_model != attacker_model" succeeds if the strings differ at all (e.g., "claude-opus-4-8" vs "claude-sonnet-4-6", or "claude-opus-4-8" vs "claude-opus-4-6"). The verifier does not parse semantic version; literal string comparison.

**Failure mode:** If memo claims score > 9.0 but adversarial isolation conditions not met, fail with `blocks_score_above=9.0` (the score gets capped at 9.0, the v0.3.0 G20 ceiling). NOT 8.5 — that's the v0.3.0 G20 cap. The graduated rigor lets memos still score 8.5-9.0 with the v0.3.0 conditions; only the 9.0+ claim is rubric-discriminated.

**Deliverable 3b:** Update the schema_version branching in `verify_view_defensibility.py` — v0.3.0 memos run only the v0.3.0 conditions; v0.4.0 memos run v0.3.0 conditions AND the graduated 9.0+ check.

**Deliverable 3c:** Smoke test: 6 branches minimum.
- v0.3.0 memo passing all original conditions → pass (graduated check not applicable)
- v0.4.0 memo claiming 8.7 score, no isolation, passing v0.3.0 conditions → pass (8.5-9.0 band)
- v0.4.0 memo claiming 9.2 score, no isolation, passing v0.3.0 conditions → fail with blocks_score_above=9.0
- v0.4.0 memo claiming 9.2 score, isolation=true, same model → fail with blocks_score_above=9.0 (model diversity required)
- v0.4.0 memo claiming 9.2 score, isolation=true, different model → pass
- v0.4.0 memo claiming 9.5 score, all conditions met → pass

**Commit message after Item 3**: `"Sprint 3a Item 3: G20 graduated rigor scale for 9.0+ claims (adversarial isolation + model diversity)"`

### Item 4 — Plugin 1 orchestrator wiring documentation (~1 session)

**Deliverable 4a:** Update Plugin 1 `us-equity-research/SKILL.md` Phase 3 section with explicit R-v2 subagent dispatch instructions. Specify:

- The Task tool invocation: `description="R-v2 isolated adversarial attack"`, prompt construction from `r-v2-isolated-attack-us.md` template, no `subagent_type` (uses default general-purpose).
- The prompt must populate the variables: `{ticker}`, `{consensus_variance_json}`, `{source_tags_top_anchors_json}`, `{attacker_model_choice}` (the orchestrator declares which model the subagent uses; default "claude-sonnet-4-6" for cross-size diversity vs Opus-running orchestrator).
- The expected output schema: array of adjudication_trail_entry objects, parsed by the orchestrator and appended to memo's adjudication_trail.
- The failure path: if R-v2 returns zero attack points on any load-bearing variance, the orchestrator flags the variance as `load_bearing=false` and re-runs G15 (which may then fail — this is the design's enforcement that the analyst must defend the variance).

**Deliverable 4b:** Update Plugin 1 SKILL.md reference-files list to include `r-v2-isolated-attack-us.md` with a one-line description.

**Deliverable 4c:** Add a paragraph to Plugin 1 SKILL.md "Common Failure Modes" section: "R-v2 spawn fails or returns weak attacks — if R-v2 cannot find specific attack points on a declared variance, the structural enforcement is to demote the variance, not to soften R-v2's requirements. A variance that no isolated red team can find weakness in is, by construction, defensible. A variance that cannot be attacked by any specific dimension is, by construction, decorative or unfalsifiable — both bad."

**Commit message after Item 4**: `"Sprint 3a Item 4: Plugin 1 orchestrator wiring for isolated R-v2 subagent dispatch"`

### Item 5 — Smoke test the full pipeline + Sprint 3a wrap (~1 session)

**Deliverable 5a:** Build a synthetic test fixture in `scripts/tests/fixtures/r-v2-isolation/`:
- `weak_variance.json`: a `consensus_variance` entry with sizing_impact_pp=4.0, evidence_refs=[{s_level: "S3"}], i.e., load-bearing but with only S3 evidence (G15 passes, G20 v0.3.0 fails).
- `medium_variance.json`: sizing_impact_pp=4.0, evidence_refs=[{s_level: "S2"}], passes G20 v0.3.0.
- `expected_attack_dimensions.json`: for each variance, list the expected canonical attack types that should fire on it (a manual annotation of what a good R-v2 should find).

**Deliverable 5b:** Smoke test the v0.4.0 G20 verifier against the fixtures + various synthetic adjudication_trail configurations. Verify the graduated rigor scale fires correctly across the 6 branches enumerated in Item 3 Deliverable 3c.

**Deliverable 5c:** Sprint 3a wrap commit:
- Bump both `plugin.json` files: `0.3.0 → 0.4.0`.
- Update `CHANGELOG.md` with v0.4.0 entry documenting Sprint 3a deliverables.
- Update `README.md`: gate count description unchanged (still 20 gates), but graduated rigor scale documented; version badge `0.3.0 → 0.4.0`.
- Update `design/sprint-3a-status.json` with all items marked complete, `next_session_scheduled_for: null`, and the scheduled task self-deletes itself via `mcp__scheduled-tasks__update_scheduled_task` setting `enabled: false`.
- Run pytest. If 198 passing, proceed. If regression, fix or block.
- Tag `v0.4.0`, push origin main, push origin --tags.

**Commit message after Item 5**: `"v0.4.0 Sprint 3a: R-v2 adversarial isolation + graduated rigor scale"` (full message; use heredoc-via-file pattern).

## Per-session execution pattern

Every scheduled run follows this exact sequence:

1. `cd /Users/hongyi/projects/us-equity-research`.
2. Read this file (`design/sprint-3a-context.md`).
3. Read `design/sprint-3a-status.json`.
4. If `blocked == true`: log "Sprint 3a is blocked: <reason>" and exit. Do not modify the repo.
5. If all 5 items show `status == "completed"`: log "Sprint 3a complete; disabling scheduled task" and disable the scheduled task. Exit.
6. Identify the next item with `status == "pending"`. Set its `status = "in_progress"`, `started_at = <ISO 8601>`. Save status file. Commit just this status update with message `"Sprint 3a Item N: in progress"`. Push.
7. Execute the item per the spec above. Read referenced files. Write deliverables. Smoke test verifier scripts. Update schemas / SKILL.md / templates as specified.
8. After deliverables are complete: stage all changes, write commit message to `/tmp/v0.4.0-itemN-msg.txt` via heredoc, commit with `-F`, push to origin main.
9. Update `design/sprint-3a-status.json`: set the item's `status = "completed"`, `completed_at = <ISO 8601>`, `commit_sha = <head commit sha>`. Save. Commit the status update with message `"Sprint 3a Item N: completed"`. Push.
10. Log completion and exit.

If at any step (especially step 7) the session encounters something genuinely ambiguous that requires user judgment (e.g., a design choice not specified in the spec), the session should: set `blocked = true`, `blocked_reason = "<specific question>"`, commit the status update, push, and exit. The user reviews on next observation and either updates the status to unblock or modifies the relevant Item spec.

## Sanity check before each ship (Items 2, 3, 5)

- All JSON schemas parse: `python3 -c "import json; [json.load(open(f'schemas/{f}')) for f in ['memo.json','source_tags.json','scenarios.json','verification_gates.json','manifest.json']]"`
- All verifier scripts AST-parse.
- Gate ID consistency: enum in verification_gates.json == gate_definitions catalog keys.
- pytest: 198 passing.

## Cross-references

- `CHANGELOG.md` v0.3.0 entry — pattern for v0.4.0 entry structure.
- `us-equity-research/references/pm-synthesis-adjudication-us.md` — existing 5-point attack methodology.
- `us-equity-research/references/consensus-variance-us.md` — what variances are.
- `scripts/verify_view_defensibility.py` — what to extend in Item 3.
- `scripts/verify_provenance_manifest.py` — pattern for schema_version-gated verifier behavior.
- v0.2.0 / v0.3.0 commits for the smoke-test patterns to mirror.

---

**This file is the contract.** A scheduled session that follows this file end-to-end will produce v0.4.0 in 5 daily runs. A session that deviates without setting `blocked: true` is in violation of the contract and the next user observation should treat the deviation as a bug.
