"""Tests for scripts/verify_gm_taxonomy.py — gate G8, bug B08.

Cross-sensitivity contract: this script must fire only on B08.json,
return 0 on clean.json and B01-B07, B09-B14.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_gm_taxonomy.py"
FIXTURE_ROOT = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"

OWNED_BUG = "B08"
BUG_IDS = [f"B{n:02d}" for n in range(1, 15)]  # B01 ... B14


def _fixture_path(fixture_id: str) -> Path:
    if fixture_id == "clean":
        return FIXTURE_ROOT / "clean.json"
    return FIXTURE_ROOT / "bugs" / f"{fixture_id}.json"


def _expected_nonzero(fixture_id: str) -> bool:
    return fixture_id == OWNED_BUG


# Parametrized over all 15 fixtures: clean + B01..B14
@pytest.mark.parametrize(
    "fixture_id",
    ["clean"] + BUG_IDS,
    ids=["clean"] + BUG_IDS,
)
def test_verify_gm_taxonomy(fixture_id: str) -> None:
    fixture_path = _fixture_path(fixture_id)
    assert fixture_path.is_file(), f"Missing fixture: {fixture_path}"

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(fixture_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    if _expected_nonzero(fixture_id):
        assert result.returncode != 0, (
            f"Fixture {fixture_id}: expected non-zero exit, got 0.\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        # Must emit structured G8 failure output.
        assert "gate_id: G8" in result.stdout, (
            f"B08 failure output missing 'gate_id: G8': {result.stdout!r}"
        )
        assert "status: fail" in result.stdout, (
            f"B08 failure output missing 'status: fail': {result.stdout!r}"
        )
        assert "empty" in result.stdout.lower() or "entries" in result.stdout.lower(), (
            f"B08 failure should reference empty entries: {result.stdout!r}"
        )
    else:
        assert result.returncode == 0, (
            f"Fixture {fixture_id}: expected exit 0, got {result.returncode}.\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
