# Contributing

This is a personal project published as a portfolio piece. Issues are welcome; pull requests are considered but not guaranteed.

## Maintenance status

Active development, single maintainer. Responses to issues and PRs within days to weeks depending on complexity and my own bandwidth. If you need a faster response for commercial use, see the README sections on optional paid-data integration via sister plugins.

## Issues

If you find a bug or have a feature request, please open an issue using the templates in `.github/ISSUE_TEMPLATE/`. Useful issues include:

- Specific reproduction steps for verifier scripts: which gate, which memo or fixture, what failed, what you expected
- Schema validation problems against existing v0.1.x / v0.2.0 / v0.3.0 / v0.4.0 fixtures
- Methodology discussion: what the gates SHOULD verify that they don't, with a concrete example of a real-world memo defect that gets past current discipline
- Documentation gaps where a reference file or SKILL.md instruction is ambiguous enough to cause incorrect orchestrator behavior

Less useful issues (likely to be closed without action):

- "The framework should be better" without a specific defect named
- Requests to add stock recommendations or backtest results (the framework is verification infrastructure, not a backtest platform)
- Requests to remove the red-team voice or honest-framing disclaimers from documentation

## Pull requests

If you want to contribute code:

1. Open an issue first describing the change. PRs without prior issue discussion are at higher risk of being closed without merge.
2. Fork the repo, branch from `main`, make the change.
3. Match the existing code style:
   - Verifier scripts: stdlib + pydantic v2, with the `try: from pydantic import ... except ModuleNotFoundError` shim for environments without pydantic.
   - Schema changes: **additive-only with grandfathering**. Any change that breaks v0.1.x / v0.2.0 / v0.3.0 / v0.4.0 / v0.5.0 memo validation is a non-starter. New optional fields fine; new required fields require v1.0.0 with migration script.
   - Reference files (Markdown): dense prose, no excessive bulleting, red-team voice. Match the existing tone.
4. All new verifier scripts must include smoke tests covering pass / fail / n_a / grandfathered paths. See `scripts/verify_consensus_variance.py` smoke test patterns in commit history.
5. Run `pytest -q` before submitting. The v0.5.1 baseline is `266 passed, 17 skipped` — must continue passing. If your change touches `scripts/` or `schemas/` at repo root, also run `bash scripts/sync_plugin_files.sh` to refresh the plugin copies; CI fails if they drift from canonical sources. If you add a new schema_version, update `KNOWN_SCHEMA_VERSIONS` in `scripts/tests/test_schema_version_coverage.py` AND add it to every verifier's `RUNNABLE_SCHEMA_VERSIONS` set — the meta-test will fail otherwise.

## What I will NOT accept

- Schema changes that break backward compatibility with any existing memo
- Removal of the schema_version grandfathering pattern
- Verifier scripts that pass without actually verifying (presence-only when arithmetic verification is documented in the schema)
- Marketing copy, vague hedge fund references, or anything that erodes the red-team voice in the documentation
- "Cleanup" PRs that remove honest framing of what the framework does NOT do

## Code review philosophy

I treat the framework's documentation as load-bearing. A PR that changes verifier behavior without updating the corresponding gate description, schema field docstring, and SKILL.md reference will be asked to update those before merge. Same for the reverse: documentation-only PRs that don't reflect the verifier code's actual behavior will be asked to fix one side or the other.

## Composition and dependencies

This repo composes with `anthropics/claude-for-financial-services` for Excel DCF / Excel comps / polished DOCX assembly. Any change that breaks that soft-dependency contract (documented in `us-equity-research/references/tool-composition-us.md`) needs to update both sides of the contract or include a fallback for users without the upstream plugins installed.
