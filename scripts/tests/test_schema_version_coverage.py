#!/usr/bin/env python3
"""
test_schema_version_coverage.py — Schema-version regression meta-test.

Sprint 4 Item 5: catches the recurring "silent schema-version skip" bug class
that has appeared multiple times in the CHANGELOG (G19 Sprint 3b fix, G20
Sprint 3a fix, G3/G6 strict-mode widening). The pattern: a verifier script
gates on a literal schema_version equality check like:

    if schema_version != "0.3.0":
        return SKIPPED

When the schema enum is widened to add v0.4.0, v0.5.0, etc., the verifier
silently skips on the new version because the literal check still says "0.3.0".
The memo's gate appears to pass (because skipped != failed) but the verifier
never actually ran. This is the exact bug that nullified G19 on v0.4.0 memos
until Sprint 3b caught it.

This meta-test asserts that every verifier script in scripts/verify_*.py uses
either:
  (a) Membership against a RUNNABLE_SCHEMA_VERSIONS set/frozenset, OR
  (b) A documented intentional skip with a comment explaining why a specific
      schema_version is excluded.

It fails CI if a verifier uses a bare literal `schema_version != "X.Y.Z"` or
`schema_version == "X.Y.Z"` check without the membership pattern, because that
pattern is what causes silent skips when the enum widens.

This test does NOT validate that the actual behavior is correct (a separate
per-verifier test does that). It validates only the structural pattern that
prevents the silent-skip bug class. A verifier can still have wrong logic;
this test catches the specific class of "I forgot to update the literal".
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Canonical schema versions across the framework's history. This list MUST
# stay in sync with the enum in schemas/memo.json's schema_version field. If
# you add a new version to the schema, add it here too.
KNOWN_SCHEMA_VERSIONS = {"0.1.0", "0.2.0", "0.3.0", "0.4.0", "0.5.0"}


def _list_verifier_scripts() -> list[Path]:
    return sorted(SCRIPTS_DIR.glob("verify_*.py"))


def _docstring_line_ranges(source: str) -> list[tuple[int, int]]:
    """Return list of (start_line, end_line) for module-level and function-level docstrings.

    Uses AST to find string-literal expressions that act as docstrings
    (the first statement of a module, class, or function body). Returns
    ranges where literal-equality patterns appearing inside should be
    treated as documentation, not as executable code.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    ranges: list[tuple[int, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", [])
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                ds = body[0]
                start = ds.lineno
                end = getattr(ds, "end_lineno", start)
                ranges.append((start, end))
    return ranges


def test_at_least_one_verifier_exists():
    scripts = _list_verifier_scripts()
    assert len(scripts) >= 14, (
        f"Expected at least 14 verifier scripts (G1-G14 baseline); found {len(scripts)}"
    )


@pytest.mark.parametrize("script_path", _list_verifier_scripts(), ids=lambda p: p.name)
def test_no_literal_schema_version_equality_skip(script_path: Path):
    """Each verifier must use membership pattern, not bare literal version equality.

    The forbidden pattern looks like:
      if schema_version != "0.3.0":
          return SKIPPED

    The allowed patterns are:
      RUNNABLE_SCHEMA_VERSIONS = {"0.3.0", "0.4.0", "0.5.0"}
      if schema_version not in RUNNABLE_SCHEMA_VERSIONS:
          return SKIPPED

    OR a documented intentional check with a comment like
    `# INTENTIONAL: this gate is grandfathered v0.1.x only` adjacent to the
    literal check.
    """
    source = script_path.read_text(encoding="utf-8")

    # Find lines with schema_version literal-equality checks
    # Pattern: schema_version != "X.Y.Z"  or  schema_version == "X.Y.Z"
    suspicious_patterns = [
        r'schema_version\s*!=\s*[\'"]\d+\.\d+\.\d+[\'"]',
        r'schema_version\s*==\s*[\'"]\d+\.\d+\.\d+[\'"]',
    ]

    # Determine which line ranges are inside docstrings (where literal
    # equality patterns appear as documentation, not as code that runs).
    docstring_ranges = _docstring_line_ranges(source)

    issues: list[str] = []
    for line_num, line in enumerate(source.splitlines(), start=1):
        # Skip lines inside docstrings.
        if any(start <= line_num <= end for start, end in docstring_ranges):
            continue
        # Skip lines that are pure comments.
        if line.strip().startswith("#"):
            continue
        # Skip lines where the schema_version pattern appears inside a
        # backtick-quoted markdown reference (`schema_version == "X"`).
        backtick_pos = line.find("`")
        for pattern in suspicious_patterns:
            match = re.search(pattern, line)
            if match:
                # If a backtick appears BEFORE the match, this is markdown prose.
                if 0 <= backtick_pos < match.start():
                    continue
                # Check INTENTIONAL marker
                prev_line = source.splitlines()[line_num - 2] if line_num >= 2 else ""
                if (
                    "INTENTIONAL" not in line
                    and "INTENTIONAL" not in prev_line
                    and "grandfathered" not in line.lower()
                ):
                    issues.append(f"  line {line_num}: {line.strip()}")

    if issues:
        pytest.fail(
            f"{script_path.name} uses literal schema_version equality check "
            f"instead of RUNNABLE_SCHEMA_VERSIONS membership pattern. This is "
            f"the silent-skip bug class that caused G19 to silently skip on "
            f"v0.4.0 memos (CHANGELOG Sprint 3b). Either:\n"
            f"  (a) Convert to a membership check against RUNNABLE_SCHEMA_VERSIONS, OR\n"
            f"  (b) Add an `# INTENTIONAL: <reason>` comment on or above the "
            f"line if the literal check is genuinely intentional.\n\n"
            f"Findings:\n" + "\n".join(issues)
        )


@pytest.mark.parametrize("script_path", _list_verifier_scripts(), ids=lambda p: p.name)
def test_runnable_schema_versions_includes_latest(script_path: Path):
    """If a verifier defines RUNNABLE_SCHEMA_VERSIONS, the latest known version
    must be in it (modulo intentional grandfathering documented inline).

    This catches the case where a maintainer adds v0.5.0 to the schema enum
    but forgets to add it to a verifier's RUNNABLE_SCHEMA_VERSIONS set.
    """
    source = script_path.read_text(encoding="utf-8")

    # Look for: RUNNABLE_SCHEMA_VERSIONS = {...}  or  RUNNABLE_SCHEMA_VERSIONS: ... = {...}
    match = re.search(
        r"RUNNABLE_SCHEMA_VERSIONS\s*(?::\s*[^=]+)?\s*=\s*([\{\[][^}\]]+[\}\]])",
        source,
    )
    if not match:
        pytest.skip(
            f"{script_path.name} does not define RUNNABLE_SCHEMA_VERSIONS — "
            f"either grandfathered design or uses a different pattern. Skipped."
        )

    # Parse the set/list literal
    try:
        runnable = ast.literal_eval(match.group(1))
    except (ValueError, SyntaxError):
        pytest.skip(f"Could not parse RUNNABLE_SCHEMA_VERSIONS literal in {script_path.name}")

    if isinstance(runnable, (list, tuple)):
        runnable = set(runnable)

    # The latest known version (0.5.0) should be in the runnable set unless
    # the file has an INTENTIONAL comment justifying exclusion.
    latest = max(KNOWN_SCHEMA_VERSIONS)
    if latest not in runnable:
        if "INTENTIONAL" not in source:
            pytest.fail(
                f"{script_path.name} defines RUNNABLE_SCHEMA_VERSIONS = {runnable} "
                f"but does not include the latest known schema version '{latest}'. "
                f"This is the silent-skip bug pattern. Either:\n"
                f"  (a) Add '{latest}' to RUNNABLE_SCHEMA_VERSIONS, OR\n"
                f"  (b) Add an `# INTENTIONAL` comment in the file explaining "
                f"why this verifier is grandfathered to an earlier version subset.\n\n"
                f"Found: {runnable}\n"
                f"Latest known: '{latest}' (from KNOWN_SCHEMA_VERSIONS in this test)"
            )


def test_known_schema_versions_matches_memo_schema():
    """KNOWN_SCHEMA_VERSIONS in this test must match the enum in memo.json.

    If you add a new schema version, update both this test's KNOWN_SCHEMA_VERSIONS
    AND schemas/memo.json's schema_version enum. This test fails if they drift.
    """
    import json

    memo_schema_path = REPO_ROOT / "schemas" / "memo.json"
    with memo_schema_path.open() as f:
        schema = json.load(f)

    enum_versions = set(schema["properties"]["schema_version"]["enum"])

    missing_from_test = enum_versions - KNOWN_SCHEMA_VERSIONS
    missing_from_schema = KNOWN_SCHEMA_VERSIONS - enum_versions

    assert not missing_from_test and not missing_from_schema, (
        f"KNOWN_SCHEMA_VERSIONS in this test and memo.json schema_version enum "
        f"have drifted.\n"
        f"  Missing from this test (in schema but not test): {missing_from_test}\n"
        f"  Missing from schema (in test but not schema): {missing_from_schema}\n"
        f"Update both to match."
    )
