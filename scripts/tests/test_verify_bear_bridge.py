"""Test suite for `scripts/verify_bear_bridge.py` (gate G5, bug B05).

Invariants enforced:
1. Returns exit code 0 on `clean.json`.
2. Returns non-zero on `bugs/B05.json` (the owned bug).
3. Returns exit code 0 on each of B01-B04, B06-B14 (no cross-sensitivity).

15 fixtures total (clean + 14 bugs). pytest -q exits 0 with 15 tests passing.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "verify_bear_bridge.py"
FIXTURES = ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"
CLEAN_JSON = FIXTURES / "clean.json"
CLEAN_MD = FIXTURES / "clean.md"
BUGS_DIR = FIXTURES / "bugs"

OWNED_BUG = 5  # G5 owns B05


def _run(memo_json: Path, memo_md: Path) -> int:
    """Run the verification script and return its exit code."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--memo-json",
            str(memo_json),
            "--memo-md",
            str(memo_md),
        ],
        capture_output=True,
        text=True,
    )
    return result.returncode


def test_clean_passes() -> None:
    """Invariant 1: clean fixture returns exit 0."""
    rc = _run(CLEAN_JSON, CLEAN_MD)
    assert rc == 0, f"verify_bear_bridge.py failed on clean (rc={rc})"


def test_owned_bug_fires() -> None:
    """Invariant 2: B05 fixture returns non-zero."""
    bug_json = BUGS_DIR / f"B{OWNED_BUG:02d}.json"
    bug_md = BUGS_DIR / f"B{OWNED_BUG:02d}.md"
    rc = _run(bug_json, bug_md)
    assert rc != 0, f"verify_bear_bridge.py did not detect owned bug B{OWNED_BUG:02d} (rc={rc})"


@pytest.mark.parametrize(
    "bug_num",
    [n for n in range(1, 15) if n != OWNED_BUG],
)
def test_cross_sensitivity_silent(bug_num: int) -> None:
    """Invariant 3: all non-owned bugs (B01-B04, B06-B14) must NOT fire G5."""
    bug_json = BUGS_DIR / f"B{bug_num:02d}.json"
    bug_md = BUGS_DIR / f"B{bug_num:02d}.md"
    rc = _run(bug_json, bug_md)
    assert rc == 0, (
        f"verify_bear_bridge.py incorrectly fired on B{bug_num:02d} "
        f"(cross-sensitivity violation; rc={rc})"
    )
