"""Tests for scripts/verify_sotp_monotonicity.py (Gate G3, Bug B03).

Invariants enforced:
  1. clean.json   -> exit 0
  2. bugs/B03.json -> non-zero (owned bug fires)
  3. bugs/B{01..14 except 03}.json -> exit 0 (no cross-sensitivity)

Total: 15 fixture parameterizations; pytest -q must pass.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_sotp_monotonicity.py"
FIXTURE_DIR = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"
CLEAN = FIXTURE_DIR / "clean.json"
BUGS_DIR = FIXTURE_DIR / "bugs"

OWNED_BUG = 3  # G3 owns B03


def _run(memo_json: Path) -> int:
    """Run the verification script and return its exit code."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(memo_json)],
        capture_output=True,
        text=True,
    )
    return proc.returncode


def test_clean_passes() -> None:
    """Invariant 1: clean.json -> exit 0."""
    assert CLEAN.exists(), f"clean fixture missing: {CLEAN}"
    rc = _run(CLEAN)
    assert rc == 0, f"verify_sotp_monotonicity.py failed on clean.json (rc={rc})"


def test_owned_bug_fails() -> None:
    """Invariant 2: bugs/B03.json -> non-zero (owned bug fires)."""
    b03 = BUGS_DIR / f"B{OWNED_BUG:02d}.json"
    assert b03.exists(), f"B03 fixture missing: {b03}"
    rc = _run(b03)
    assert rc != 0, "verify_sotp_monotonicity.py did not detect owned bug B03"


@pytest.mark.parametrize(
    "bug_num",
    [n for n in range(1, 15) if n != OWNED_BUG],
)
def test_other_bugs_do_not_trigger(bug_num: int) -> None:
    """Invariant 3: all non-B03 bug fixtures -> exit 0 (no cross-sensitivity)."""
    bug_path = BUGS_DIR / f"B{bug_num:02d}.json"
    assert bug_path.exists(), f"fixture missing: {bug_path}"
    rc = _run(bug_path)
    assert rc == 0, (
        f"verify_sotp_monotonicity.py incorrectly fired on B{bug_num:02d} (cross-sensitivity)"
    )


def test_flag_form_supported() -> None:
    """Uniform calling contract: --memo-json flag form must also work."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(CLEAN)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"flag form failed on clean.json: {proc.stderr}"


# --- v0.4.0 strict-mode routing (regression guard for the G19-class bug) ---
# The strict segment-shape check was gated on `schema_version == "0.3.0"`, so a
# v0.4.0 memo silently reverted to the lenient pre-0.3.0 path. An incomplete
# segment (only Revenue + GP) is excluded under strict (=> no complete segments
# => fail) but accepted under lenient (>=2 fields => monotonic pass). Routing is
# therefore observable from the exit code alone.

_INCOMPLETE_SEGMENT_MEMO = {
    "valuation": {
        "methods": [
            {
                "method": "SOTP",
                "key_assumptions": {
                    "SegA": {"SegA_revenue": 100.0, "SegA_segment_gp": 60.0},
                },
            }
        ]
    },
}


@pytest.mark.parametrize(
    "schema_version,expected_rc",
    [
        ("0.2.0", 0),  # legacy: lenient -> pass
        ("0.3.0", 1),  # strict -> fail (incomplete segment)
        ("0.4.0", 1),  # the fix: v0.4.0 must run strict, not legacy
    ],
)
def test_strict_mode_routes_v040(tmp_path: Path, schema_version: str, expected_rc: int) -> None:
    memo = dict(_INCOMPLETE_SEGMENT_MEMO, schema_version=schema_version)
    mj = tmp_path / "memo.json"
    mj.write_text(json.dumps(memo), encoding="utf-8")
    rc = _run(mj)
    assert rc == expected_rc, (
        f"G3 schema_version={schema_version}: expected exit {expected_rc}, got {rc} "
        f"(v0.4.0 must route to strict, not the lenient pre-0.3.0 path)"
    )
