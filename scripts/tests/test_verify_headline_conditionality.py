"""
Tests for scripts/verify_headline_conditionality.py (Gate G7 / Bug B07).

Invariants (per scripts/tests/fixtures/nvda_v0/bug-script-matrix.md):
  1. Returns 0 on clean.json / clean.md.
  2. Returns non-zero on bugs/B07.json + bugs/B07.md (its owned bug).
  3. Returns 0 on bugs/B01.json … B14.json EXCEPT B07 (no cross-sensitivity).

Total fixture invocations exercised: 15 (clean + 14 bugs). pytest collects:
  - test_clean_passes
  - test_owned_bug_b07_fails
  - 13 parametrized cross-sensitivity assertions

Calling contract: positional memo_json arg + optional --memo-md flag; the
script defaults to the sibling .md when --memo-md is omitted.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_headline_conditionality.py"
FIXTURE_DIR = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"
CLEAN_JSON = FIXTURE_DIR / "clean.json"
CLEAN_MD = FIXTURE_DIR / "clean.md"
BUGS_DIR = FIXTURE_DIR / "bugs"

OWNED_BUG = "B07"


def _run(memo_json: Path, memo_md: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(memo_json), "--memo-md", str(memo_md)],
        capture_output=True,
        text=True,
    )


def test_clean_passes() -> None:
    """G7 on clean.json/clean.md must exit 0 (source_conditional matches weak top-3)."""
    result = _run(CLEAN_JSON, CLEAN_MD)
    assert result.returncode == 0, (
        f"verify_headline_conditionality.py failed on clean.json "
        f"(rc={result.returncode})\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert "gate_id: G7" in result.stdout
    assert "status: pass" in result.stdout


def test_owned_bug_b07_fails() -> None:
    """G7 must fire on owned bug B07 (both JSON and MD layers corrupted)."""
    bug_json = BUGS_DIR / f"{OWNED_BUG}.json"
    bug_md = BUGS_DIR / f"{OWNED_BUG}.md"
    result = _run(bug_json, bug_md)
    assert result.returncode != 0, (
        f"verify_headline_conditionality.py did not detect owned bug {OWNED_BUG} "
        f"(rc={result.returncode})\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert "gate_id: G7" in result.stdout
    assert "status: fail" in result.stdout


@pytest.mark.parametrize("bug_num", [n for n in range(1, 15) if n != 7])
def test_cross_sensitivity_other_bugs_pass(bug_num: int) -> None:
    """G7 must NOT fire on any non-owned bug (B01-B06, B08-B14)."""
    tag = f"B{bug_num:02d}"
    bug_json = BUGS_DIR / f"{tag}.json"
    bug_md = BUGS_DIR / f"{tag}.md"
    result = _run(bug_json, bug_md)
    assert result.returncode == 0, (
        f"verify_headline_conditionality.py incorrectly fired on {tag} "
        f"(rc={result.returncode}; cross-sensitivity violation)\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
