"""
Tests for scripts/verify_fcf_definition.py (Gate G12 / Bug B12).

Invariants:
  1. Returns 0 on clean.json.
  2. Returns non-zero on bugs/B12.json (its owned bug).
  3. Returns 0 on bugs/B01.json … B14.json EXCEPT B12 (no cross-sensitivity).

Cross-sensitivity invariant means there are 15 fixture checks total:
  clean → 0
  B01..B14 → 0 except B12 → non-zero.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_fcf_definition.py"
FIXTURE_DIR = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"
CLEAN_JSON = FIXTURE_DIR / "clean.json"
CLEAN_MD = FIXTURE_DIR / "clean.md"
BUGS_DIR = FIXTURE_DIR / "bugs"

OWNED_BUG = "B12"


def _run(memo_json: Path, memo_md: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(memo_json), "--memo-md", str(memo_md)],
        capture_output=True,
        text=True,
    )


def test_clean_passes() -> None:
    """G12 on clean.json must exit 0."""
    result = _run(CLEAN_JSON, CLEAN_MD)
    assert result.returncode == 0, (
        f"verify_fcf_definition.py failed on clean.json (rc={result.returncode})\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert "gate_id: G12" in result.stdout
    assert "status: pass" in result.stdout


def test_owned_bug_b12_fails() -> None:
    """G12 must fire on its owned bug B12 (fcf_definition vs addback flag conflict)."""
    bug_json = BUGS_DIR / f"{OWNED_BUG}.json"
    bug_md = BUGS_DIR / f"{OWNED_BUG}.md"
    result = _run(bug_json, bug_md)
    assert result.returncode != 0, (
        f"verify_fcf_definition.py did not detect owned bug {OWNED_BUG} "
        f"(rc={result.returncode})\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    # G12 evidence body present
    assert "gate_id: G12" in result.stdout
    assert "status: fail" in result.stdout


@pytest.mark.parametrize("bug_num", [n for n in range(1, 15) if n != 12])
def test_cross_sensitivity_other_bugs_pass(bug_num: int) -> None:
    """G12 must NOT fire on any non-owned bug (B01-B11, B13-B14)."""
    tag = f"B{bug_num:02d}"
    bug_json = BUGS_DIR / f"{tag}.json"
    bug_md = BUGS_DIR / f"{tag}.md"
    result = _run(bug_json, bug_md)
    assert result.returncode == 0, (
        f"verify_fcf_definition.py incorrectly fired on {tag} "
        f"(rc={result.returncode}; cross-sensitivity violation)\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
