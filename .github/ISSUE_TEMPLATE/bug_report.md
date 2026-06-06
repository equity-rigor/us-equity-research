---
name: Bug report
about: Report a problem with a verifier, schema, or orchestration step
title: '[Bug] '
labels: bug
assignees: ''
---

## What gate or component?

(e.g., G6 / `verify_source_tags.py`, or "the orchestrator skill at Phase 2 dispatch", or "schemas/memo.json adjudication_trail validation")

## Schema version of the memo or fixture

(0.1.0 / 0.2.0 / 0.3.0 / 0.4.0)

## Repro steps

1.
2.
3.

## What you expected

## What you actually got

(Paste the full structured stdout from the verifier, including `gate_id`, `status`, `failure_reason`. Or paste the Python traceback if the verifier crashed.)

## Minimal reproduction

If reproducible against a specific memo or fixture, link or paste the relevant structured JSON (or a minimal reproduction). Redact any sensitive information first.

## Environment

- OS:
- Python version: `python3 --version`
- pydantic version (if applicable): `python3 -c "import pydantic; print(pydantic.__version__)"`
- Are you running from the published plugin install or from a git clone?

## Additional context

Anything else that might help diagnose the issue.
