"""Tests for scripts/verify_what_would_reverse.py — gate G9, bug B09.

Cross-sensitivity contract: this script must fire only on B09.json,
return 0 on clean.json and B01-B08, B10-B14.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_what_would_reverse.py"
FIXTURE_ROOT = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"

OWNED_BUG = "B09"
BUG_IDS = [f"B{n:02d}" for n in range(1, 15)]  # B01 ... B14


def _fixture_path(fixture_id: str) -> Path:
    if fixture_id == "clean":
        return FIXTURE_ROOT / "clean.json"
    return FIXTURE_ROOT / "bugs" / f"{fixture_id}.json"


def _expected_exit(fixture_id: str) -> int:
    if fixture_id == OWNED_BUG:
        return 1  # script MUST detect its owned bug
    return 0  # clean fixture and all non-owned bug fixtures must pass


@pytest.mark.parametrize(
    "fixture_id",
    ["clean"] + BUG_IDS,
    ids=["clean"] + BUG_IDS,
)
def test_verify_what_would_reverse(fixture_id: str) -> None:
    fixture_path = _fixture_path(fixture_id)
    assert fixture_path.is_file(), f"Missing fixture: {fixture_path}"

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(fixture_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    expected = _expected_exit(fixture_id)
    assert result.returncode == expected, (
        f"Fixture {fixture_id}: expected exit {expected}, got {result.returncode}.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    if fixture_id == OWNED_BUG:
        # Must emit structured G9 failure output.
        assert "gate_id: G9" in result.stdout, (
            f"B09 failure output missing 'gate_id: G9': {result.stdout!r}"
        )
        assert "status: fail" in result.stdout, (
            f"B09 failure output missing 'status: fail': {result.stdout!r}"
        )
        assert "what_would_reverse[0]" in result.stdout, (
            f"B09 failure should reference what_would_reverse[0]: {result.stdout!r}"
        )
