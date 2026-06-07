"""Tests for scripts/verify_non_gaap.py — gate G11, bug B11.

Invariants (per scripts/tests/fixtures/nvda_v0/bug-script-matrix.md):
  1. Returns 0 on clean.json + clean.md.
  2. Returns non-zero on bugs/B11.json + bugs/B11.md (its owned bug — both
     layers corrupted: JSON `forensic_flags.non_gaap_reconciliation_present`
     flipped to false; MD §6.0 parallel paragraph removed and §12 forensic
     line changed).
  3. Returns 0 on bugs/B01..B14 EXCEPT B11 (no cross-sensitivity, including
     B12 which corrupts a sibling forensic_flags field but leaves the G11
     `non_gaap_reconciliation_present` flag intact).

Parametrized over all 15 fixtures: clean + B01..B14. pytest -q exits 0 with
15 passing tests.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_non_gaap.py"
FIXTURE_ROOT = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"

OWNED_BUG = "B11"
BUG_IDS = [f"B{n:02d}" for n in range(1, 15)]  # B01 ... B14


def _fixture_paths(fixture_id: str) -> tuple[Path, Path]:
    """Return (json_path, md_path) for the named fixture."""
    if fixture_id == "clean":
        return FIXTURE_ROOT / "clean.json", FIXTURE_ROOT / "clean.md"
    return (
        FIXTURE_ROOT / "bugs" / f"{fixture_id}.json",
        FIXTURE_ROOT / "bugs" / f"{fixture_id}.md",
    )


def _expected_nonzero(fixture_id: str) -> bool:
    return fixture_id == OWNED_BUG


@pytest.mark.parametrize(
    "fixture_id",
    ["clean"] + BUG_IDS,
    ids=["clean"] + BUG_IDS,
)
def test_verify_non_gaap(fixture_id: str) -> None:
    json_path, md_path = _fixture_paths(fixture_id)
    assert json_path.is_file(), f"Missing JSON fixture: {json_path}"
    assert md_path.is_file(), f"Missing MD fixture: {md_path}"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--memo-json",
            str(json_path),
            "--memo-md",
            str(md_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if _expected_nonzero(fixture_id):
        assert result.returncode != 0, (
            f"Fixture {fixture_id}: expected non-zero exit (owned bug B11), "
            f"got {result.returncode}.\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        assert "gate_id: G11" in result.stdout, (
            f"B11 failure output missing 'gate_id: G11': {result.stdout!r}"
        )
        assert "status: fail" in result.stdout, (
            f"B11 failure output missing 'status: fail': {result.stdout!r}"
        )
        # Failure should reference the structured flag.
        assert (
            "non_gaap_reconciliation_present" in result.stdout
            or "reconciliation" in result.stdout.lower()
        ), f"B11 failure should reference reconciliation absence: {result.stdout!r}"
    else:
        assert result.returncode == 0, (
            f"Fixture {fixture_id}: expected exit 0 (cross-sensitivity), "
            f"got {result.returncode}.\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        assert "gate_id: G11" in result.stdout
        assert "status: pass" in result.stdout
