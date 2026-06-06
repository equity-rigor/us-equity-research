# Sprint 4 Item 8 — Verifier-reachability fix

**Status:** Draft for review · **Author:** us-equity-research maintainer · **Target version:** v0.4.1 (or v0.5.0 if bundled with Item 9)

## Problem

The MU run on 2026-06-06 surfaced a critical packaging defect. The framework's plugin install via `/plugin marketplace add equity-rigor/us-equity-research` installs only the two plugin directories (`us-equity-research/` and `us-equity-ic-rigor/`) into `~/.claude/plugins/<plugin>/<version>/`. The repository-root `scripts/` directory (20 verifier scripts) and `schemas/` directory (5 schema files) are NOT copied during install. They live only in the cloned repo.

When the user runs `claude` from a directory outside the cloned repo (e.g., `~/Desktop`), the agent has no reachable path to `scripts/verify_*.py` or `scripts/write_manifest.py`. SKILL.md currently says things like `Script: scripts/verify_eps_pe.py` as a bare relative path. The agent looks in cwd, doesn't find it, and gracefully degrades to "evaluate this gate analytically against the rubric." The MU manifest documents this directly:

> Manifest hand-assembled because plugin scripts/write_manifest.py + schemas/ are absent in working dir.

And the MU red-team round 1:

> The plugin's scripts/verify_*.py are not present in this build, and the memo was authored via the base us-equity-research workflow ... Gates were therefore evaluated **analytically** against the memo + JSON, not by script execution.

This nullifies the framework's most distinctive feature. The 20 verification gates are not actually verifying anything for users who install from the marketplace. The LLM grades its own work against the rubric description and reports the grades as if Python scripts had run.

## Root cause

The repository layout was designed for in-repo development (`pytest -q` runs verifier scripts against test fixtures from repo root). When the same layout was packaged for marketplace distribution, only the plugin subdirectories shipped. The scripts were not bundled. SKILL.md continued to reference them as if they lived at cwd.

## Design

### Option chosen: bundle scripts and schemas inside each plugin directory

After reviewing Anthropic's skill-packaging conventions (the official `pptx`, `pdf`, and `docx` skills all bundle `scripts/` directories inside their skill root), the cleanest fix is to mirror that pattern. Each plugin self-contains everything it needs to execute its skill, including verifier scripts and schemas.

The repo root keeps `scripts/` and `schemas/` as the canonical source of truth for development, testing (`pytest -q`), and CI. A sync script copies these into each plugin directory. CI fails if the copies drift from the canonical sources.

### Final directory structure

```
us-equity-research/                         (repo root, canonical sources)
├── scripts/                                ← SOURCE OF TRUTH
│   ├── verify_*.py (20 files)
│   └── write_manifest.py
├── schemas/                                ← SOURCE OF TRUTH
│   ├── memo.json
│   ├── scenarios.json
│   ├── source_tags.json
│   ├── verification_gates.json
│   └── manifest.json
├── us-equity-research/                     Plugin 1 directory
│   ├── .claude-plugin/plugin.json
│   ├── SKILL.md
│   ├── commands/research.md
│   ├── references/
│   ├── scripts/                            ← NEW: SYNCED COPY
│   │   ├── verify_source_tags.py
│   │   ├── verify_consensus_variance.py
│   │   ├── verify_bank_metrics.py
│   │   ├── verify_revision_velocity.py
│   │   └── write_manifest.py
│   └── schemas/                            ← NEW: SYNCED COPY (all 5)
└── us-equity-ic-rigor/                     Plugin 2 directory
    ├── .claude-plugin/plugin.json
    ├── SKILL.md
    ├── commands/{ic-memo,red-team}.md
    ├── references/
    ├── templates/
    ├── scripts/                            ← NEW: SYNCED COPY (all 20 verifier scripts)
    └── schemas/                            ← NEW: SYNCED COPY (all 5)
```

### Script-to-plugin assignment

| Script | Plugin 1 (orchestrator) | Plugin 2 (rigor) |
|---|---|---|
| `write_manifest.py` | ✓ (writes manifest at end of Phase 3) | — |
| `verify_source_tags.py` (G6) | ✓ (Phase 0-3 sourcing discipline) | ✓ (rerun in red-team) |
| `verify_consensus_variance.py` (G15) | ✓ (Phase 2 A-Consensus produces, Phase 1 validates) | ✓ |
| `verify_bank_metrics.py` (G16) | ✓ (Phase 1 FS-Banks Augmentation) | ✓ |
| `verify_revision_velocity.py` (G17) | ✓ (Phase 2 A6 produces) | ✓ |
| `verify_eps_pe.py` (G1) | — | ✓ |
| `verify_segment_gm.py` (G2) | — | ✓ |
| `verify_sotp_monotonicity.py` (G3) | — | ✓ |
| `verify_scenario_weights.py` (G4) | — | ✓ |
| `verify_bear_bridge.py` (G5) | — | ✓ |
| `verify_headline_conditionality.py` (G7) | — | ✓ |
| `verify_gm_taxonomy.py` (G8) | — | ✓ |
| `verify_what_would_reverse.py` (G9) | — | ✓ |
| `verify_weighting_sensitivity.py` (G10) | — | ✓ |
| `verify_non_gaap.py` (G11) | — | ✓ |
| `verify_fcf_definition.py` (G12) | — | ✓ |
| `verify_quant_overlay.py` (G13/G14) | — | ✓ |
| `verify_quant_cross_doc_consistency.py` (G18) | — | ✓ |
| `verify_provenance_manifest.py` (G19) | — | ✓ |
| `verify_view_defensibility.py` (G20) | — | ✓ |

Plugin 1 gets 5 scripts (4 sourcing/discipline + manifest writer). Plugin 2 gets all 20 verifier scripts (it's the rigor layer; it runs the full gate suite). Schemas are duplicated in both because both plugins reference them.

Alternative considered: bundle the FULL `scripts/` directory in both plugins. Simpler sync (just `cp -r`), no per-script classification, no risk of forgetting a new verifier. Marginal storage cost (<100KB). Rejected only because Plugin 1 doesn't conceptually need the rigor verifiers — but on reflection, simplicity matters more than logical purity. **Recommend revisiting and going with "full copy in both"** unless there's a strong reason to keep them separate.

### Path resolution in SKILL.md

Per Anthropic's skill conventions (confirmed by inspecting the bundled `pptx`, `pdf`, `docx` skills), SKILL.md can reference scripts via bare relative paths like `scripts/verify_eps_pe.py` and the agent resolves them relative to the skill's installed directory. The pptx SKILL.md uses exactly this pattern:

```markdown
python scripts/thumbnail.py presentation.pptx
```

So the SKILL.md path updates are minimal — most existing paths already use the right form. However, the MU run showed the agent CAN fall back to analytical evaluation when scripts aren't found, without escalating the error to the user. We need an explicit **anti-degradation preamble** in both SKILL.md files that prevents this fallback.

### SKILL.md preamble to insert

Insert this block at the top of both `us-equity-research/SKILL.md` and `us-equity-ic-rigor/SKILL.md`, immediately after the YAML frontmatter:

```markdown
## CRITICAL: Verifier Script Path Resolution

This plugin bundles its verifier scripts at `${CLAUDE_PLUGIN_ROOT}/scripts/` and JSON schemas at `${CLAUDE_PLUGIN_ROOT}/schemas/`. All `scripts/verify_*.py` references in this SKILL resolve to that location.

**Execution requirements:**

1. Always invoke verifier scripts with the explicit prefix `python ${CLAUDE_PLUGIN_ROOT}/scripts/<script_name>.py [args]`, OR change directory first with `cd ${CLAUDE_PLUGIN_ROOT} && python scripts/<script_name>.py [args]`.

2. If `${CLAUDE_PLUGIN_ROOT}` is not set in your environment (older Claude Code versions), the plugin is installed at `~/.claude/plugins/<plugin-name>/<version>/` — use that absolute path.

3. **NEVER fall back to "evaluate gates analytically."** If you cannot reach a verifier script (file not found, permission denied, Python import error, etc.), STOP execution of that phase, report the error to the user with the exact command attempted and the exact error message, and ask them to either (a) clone the repo at https://github.com/equity-rigor/us-equity-research and run Claude Code from that directory, OR (b) manually copy the missing scripts to the plugin install location. Do NOT produce a memo with gate statuses you judged yourself rather than ran programmatically.

4. The verifier scripts are the framework's distinguishing feature. A memo produced without running them has no claim to the "20-gate verification" rigor the framework advertises. Self-graded gates produce a memo of the same quality as a careful prompt template — useful, but not what was promised.

5. If the user explicitly says "I understand the verifiers won't run; proceed analytically anyway," THEN you may produce the memo with analytically-judged gate statuses, but you MUST set `memo_metadata.gates_evaluated_analytically: true` in `<TICKER>_structured.json` and include a clear disclaimer in the IC memo header: "Gates evaluated analytically by the LLM; programmatic verifier scripts did not run for this output."
```

The 5th paragraph is the escape hatch — it allows continuation when the user accepts the degradation, but forces the degradation to be visible in the output metadata and the memo itself. This prevents silent quality degradation while preserving usability when scripts genuinely can't be reached.

## Sync mechanism

A shell script at `scripts/sync_plugin_files.sh` copies repo-root sources to plugin directories. Run it before any `git commit` that touches `scripts/` or `schemas/`. CI fails if the plugin copies are stale.

See `scripts/sync_plugin_files.sh` (separately written) for the implementation.

## CI integration

Add a step to `.github/workflows/pytest.yml` (the workflow added in Sprint 4 Item 2):

```yaml
- name: Verify plugin file sync
  run: |
    bash scripts/sync_plugin_files.sh --check
    if [ $? -ne 0 ]; then
      echo "Plugin script/schema copies are out of sync with repo-root sources."
      echo "Run: bash scripts/sync_plugin_files.sh"
      exit 1
    fi
```

The `--check` flag runs the sync logic in dry-run mode; if anything would change, exit non-zero.

## Migration checklist

In order:

1. [ ] Write `scripts/sync_plugin_files.sh` with `--check` mode
2. [ ] Run `bash scripts/sync_plugin_files.sh` to populate `us-equity-research/scripts/`, `us-equity-research/schemas/`, `us-equity-ic-rigor/scripts/`, `us-equity-ic-rigor/schemas/`
3. [ ] Add `.gitkeep` files in newly-created directories if they're empty in the source-of-truth (none are, but defensive)
4. [ ] Insert the SKILL.md preamble (above) at top of both plugins' SKILL.md, immediately after YAML frontmatter
5. [ ] Update Plugin 1's SKILL.md line 264 from `python scripts/write_manifest.py` to `python ${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest.py`
6. [ ] Update Plugin 2's SKILL.md gate-definition section (lines 136-155) to use `${CLAUDE_PLUGIN_ROOT}/scripts/verify_*.py` everywhere
7. [ ] Update Plugin 2's SKILL.md command reference list (lines 247-263) to use `${CLAUDE_PLUGIN_ROOT}/scripts/verify_*.py`
8. [ ] Update Plugin 1's `commands/research.md` if it references any scripts
9. [ ] Update Plugin 2's `commands/ic-memo.md` and `commands/red-team.md` script references
10. [ ] Bump both `plugin.json` versions to 0.4.1
11. [ ] Bump `marketplace.json` version to 0.4.1
12. [ ] Add CHANGELOG entry (template below)
13. [ ] Add CI step to `.github/workflows/pytest.yml` for sync check
14. [ ] Smoke-test from a clean clone: `claude` in a fresh directory, install plugins, run `/us-equity-research:research AAPL` (a quick sector different from MU), verify scripts actually execute
15. [ ] If smoke test passes: tag v0.4.1, push, update README badge

## Test plan

**Unit test:** `scripts/tests/test_sync_plugin_files.sh` — create temp dir, populate with repo-root layout, run sync, assert all expected files present in plugin directories with matching content.

**Integration test:** add a `pytest` test that walks both `us-equity-research/scripts/` and `us-equity-ic-rigor/scripts/` and asserts each file's SHA-256 matches its counterpart in repo-root `scripts/`. Same for schemas. Run on every CI invocation.

**End-to-end smoke test:** documented manual procedure in CHANGELOG that maintainer runs before each release. Install plugin from clean state, run a memo on a small ticker, verify scripts were invoked (check for the verifier's stdout signature in the agent's tool call log).

## CHANGELOG entry template

```markdown
## [0.4.1] - 2026-06-DD

### Fixed

- **CRITICAL: Verifier scripts now reachable from plugin install (Sprint 4 Item 8).** Prior versions distributed only the plugin directories via the marketplace; the repo-root `scripts/` and `schemas/` were NOT copied into `~/.claude/plugins/<plugin>/<version>/`. When users invoked the framework from any directory outside the cloned repo, the agent could not reach `scripts/verify_*.py` and silently degraded to LLM-graded "analytical" gate evaluation. This silently nullified the framework's 20-gate verification claim for typical install flows.

  **Fix:** Each plugin directory now bundles its own `scripts/` and `schemas/` subdirectories, synced from the canonical repo-root sources via `scripts/sync_plugin_files.sh`. CI fails if the sync is stale. SKILL.md now uses explicit `${CLAUDE_PLUGIN_ROOT}/scripts/...` paths. An anti-degradation preamble in both SKILL.md files prevents silent fallback to analytical evaluation.

  **Migration:** Users on v0.4.0 should `/plugin update equity-rigor/us-equity-research` to receive the bundled scripts. No memo schema changes; all v0.4.0 outputs validate clean against v0.4.1 schemas.

  **Discovery:** Found during MU end-to-end run 2026-06-06. The MU run's manifest documented the degradation directly: "Manifest hand-assembled because plugin scripts/write_manifest.py + schemas/ are absent in working dir." Honest disclosure of the degradation is what surfaced the bug; the framework's own provenance discipline caught its own packaging defect.

### Added

- `scripts/sync_plugin_files.sh` — maintains plugin copies of repo-root scripts/schemas
- CI step in `.github/workflows/pytest.yml` to verify sync
- `scripts/tests/test_plugin_file_sync.py` — pytest module verifying SHA-256 match of plugin copies against repo-root sources
- SKILL.md anti-degradation preamble in both plugins
```

## Open questions for the maintainer

1. **Bundle the full scripts/ or just the per-plugin subset?** Recommend full copy in both for simplicity. Storage cost is trivial; eliminates classification bugs.
2. **`${CLAUDE_PLUGIN_ROOT}` vs bare relative paths?** Bare paths work per Anthropic's pptx skill pattern, but the MU run showed the agent can fail to resolve them silently. The explicit `${CLAUDE_PLUGIN_ROOT}/scripts/...` form is more robust. Recommend explicit.
3. **What to do about v0.4.0 users who installed before the fix?** They keep working in degraded mode (gates evaluated analytically) until they `/plugin update`. The v0.4.1 release notes should make the update prominent.
4. **Should Item 9 (5-file output convention) ship in same release?** Probably yes — they're related and both surfaced from the same MU run. Bundle as v0.4.1 or escalate to v0.5.0.

## Expected impact

After this fix:
- A user running `claude` from any directory who installs both plugins via `/plugin install` will have the verifier scripts reachable at `${CLAUDE_PLUGIN_ROOT}/scripts/`.
- SKILL.md instructions resolve to actual Python script invocations, not analytical LLM judgments.
- Gate statuses in `<TICKER>_verification_gates.json` will be the output of `scripts/verify_*.py` exit codes plus structured stdout, not LLM self-assessment.
- The provenance manifest will be written by `scripts/write_manifest.py` with actual SHA-256 hashes of the on-disk output files, not by the LLM following the schema.
- Memos produced will have a legitimate claim to the "programmatic verification" that the README advertises.

The deep-research report's most damaging critique — that the modern framework is described as if validated but the public examples don't exercise it — is partially answered by Sprint 4 Item 3 (fresh v0.5.0 flagship example) and structurally answered by this fix: even before the flagship example ships, any new run by any user will actually invoke the verifier scripts.

This is the highest-credibility-impact single change in the Sprint 4 plan. It addresses the framework's most fundamental gap between marketing and operational reality.
