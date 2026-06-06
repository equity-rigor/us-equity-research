# Sprint 4 Item 8 — SKILL.md anti-degradation preamble

This block is to be inserted at the top of **both** `us-equity-research/SKILL.md` and `us-equity-ic-rigor/SKILL.md`, immediately after the closing `---` of the YAML frontmatter (so the first thing the agent reads after the frontmatter is this critical path-resolution and anti-degradation directive).

## The preamble (insert verbatim, no edits)

```markdown
## CRITICAL: Verifier Script Path Resolution

This plugin bundles its verifier scripts at `${CLAUDE_PLUGIN_ROOT}/scripts/` and JSON schemas at `${CLAUDE_PLUGIN_ROOT}/schemas/`. All `scripts/verify_*.py` and `scripts/write_manifest.py` references in this SKILL resolve to that location.

### Execution requirements (non-negotiable)

**1. Use the explicit plugin-root path for every script invocation.**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/verify_eps_pe.py --memo-json outputs/<TICKER>_structured.json
python ${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest.py --ticker <TICKER> --outputs-dir outputs/
```

If `${CLAUDE_PLUGIN_ROOT}` is not set in the current Claude Code version, the plugin is installed at `~/.claude/plugins/<plugin-name>/<version>/` (e.g., `~/.claude/plugins/us-equity-research/0.4.1/`). Use that absolute path as a fallback.

**2. NEVER fall back to "evaluate gates analytically."**

If you cannot reach a verifier script for any reason (file not found, permission denied, Python import error, missing pydantic dependency, etc.), STOP execution of the current phase. Report the error to the user with:

- The exact command attempted
- The exact error message returned
- A request to either (a) clone the repo at `https://github.com/equity-rigor/us-equity-research` and run Claude Code from that directory, OR (b) manually copy the missing scripts to the plugin install location

Do NOT proceed to produce a memo with gate statuses you judged yourself. Self-graded gates are not gates. They are LLM opinions about LLM output.

**3. The verifier scripts are this framework's distinguishing feature.**

A memo produced without programmatic verification has no claim to the "20-gate verification" rigor advertised in the README, plugin description, or technical documentation. Self-graded gates produce a memo of the same quality as a careful prompt template — useful, but not what was promised to the user. Honest practice requires either running the scripts or honestly disclosing that they were not run.

**4. Operator-explicit override (the only allowed degradation path).**

If the user explicitly says some variant of "I understand the verifiers won't run; proceed analytically anyway," THEN you may produce the memo with analytically-judged gate statuses. In that case you MUST:

- Set `memo_metadata.gates_evaluated_analytically: true` in `<TICKER>_structured.json`
- Include this disclaimer in the IC memo header section: *"Gate statuses in this memo were evaluated analytically by the language model; the programmatic verifier scripts at `scripts/verify_*.py` did not execute for this output. Gate compliance therefore reflects LLM self-assessment against the rubric description, not Python script exit codes. The memo is otherwise structurally complete."*
- Set every gate's `evaluation_method` field to `"analytical_llm"` instead of `"programmatic_script"`
- Cap the rubric score at 7.5 regardless of mechanical compliance (analytical gates cannot support score >7.5)

The override exists for users who genuinely cannot install the scripts (sandboxed environments, network-restricted hosts, etc.). It is not a shortcut to skip verification on a normal install. If the user has not explicitly invoked the override, the failure-to-execute is itself the bug to report — do not work around it silently.

### Why this preamble exists

A v0.4.0 end-to-end run on MU on 2026-06-06 produced an output where the manifest was hand-assembled by the LLM and all 20 gate statuses were self-judged because the verifier scripts were not reachable from the user's working directory. The framework's most distinctive feature — programmatic verification — was nullified silently and the resulting memo was indistinguishable in appearance from a properly-verified one. The provenance manifest disclosed the degradation honestly, but only because the LLM happened to write the disclosure paragraph. There was no structural mechanism preventing the degradation from being silent. This preamble is that structural mechanism.
```

## Where exactly to insert it

For `us-equity-research/SKILL.md`:

```markdown
---
name: us-equity-research
description: Conduct institutional buy-side fundamental research...
license: MIT
---

[INSERT THE PREAMBLE BLOCK HERE]

[Existing SKILL.md content continues from here]
```

For `us-equity-ic-rigor/SKILL.md`:

```markdown
---
name: us-equity-ic-rigor
description: Layer PM-grade IC-deliverable rigor on top of us-equity-research...
license: MIT
---

[INSERT THE PREAMBLE BLOCK HERE]

[Existing SKILL.md content continues from here]
```

## Companion edits to existing script-reference lines

Plugin 2 `SKILL.md` has explicit script references in lines 136-156 (gate definitions) and 247-263 (script reference list). Find/replace pattern:

| Before | After |
|---|---|
| `Script: \`scripts/verify_eps_pe.py\`` | `Script: \`${CLAUDE_PLUGIN_ROOT}/scripts/verify_eps_pe.py\`` |
| (same pattern for all 20 scripts) | (same pattern) |

Plugin 1 `SKILL.md` line 264:

| Before | After |
|---|---|
| `python scripts/write_manifest.py \` | `python ${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest.py \` |

A scripted find/replace will handle the bulk of these. Pseudo-command:

```bash
sed -i.bak \
  -e 's|`scripts/verify_|`${CLAUDE_PLUGIN_ROOT}/scripts/verify_|g' \
  -e 's|`scripts/write_manifest|`${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest|g' \
  -e 's|python scripts/|python ${CLAUDE_PLUGIN_ROOT}/scripts/|g' \
  us-equity-research/SKILL.md us-equity-ic-rigor/SKILL.md
```

Verify diff manually before committing — the sed pattern is aggressive enough that it could hit edge cases in prose. Recommend running `git diff` after sed and reverting anything that wasn't actually a script reference.

## Companion edits to command files

`us-equity-research/commands/research.md`, `us-equity-ic-rigor/commands/ic-memo.md`, and `us-equity-ic-rigor/commands/red-team.md` likely have similar script references. Run the same sed pattern on those.

## Validation

After applying preamble + path updates:

1. Grep both SKILL.md files for bare `scripts/` references — there should be none outside the preamble's `${CLAUDE_PLUGIN_ROOT}/scripts/` form:
   ```bash
   grep -n "scripts/" us-equity-research/SKILL.md us-equity-ic-rigor/SKILL.md | grep -v CLAUDE_PLUGIN_ROOT
   ```
   Expected output: only matches inside the preamble's documentation prose (no executable references).

2. Run pytest:
   ```bash
   pytest -q scripts/tests/test_plugin_file_sync.py
   ```
   Expected: all tests pass (after `bash scripts/sync_plugin_files.sh` has populated the plugin copies).

3. Manual smoke test from a clean directory (requires fresh Claude Code session — see `design/sprint-4-item-8-verifier-reachability.md` migration checklist step 14).
