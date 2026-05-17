"""Tests for scripts/verify_eps_pe.py — gate G1, bug B01.

Cross-sensitivity contract: this script must fire only on B01.json,
return 0 on clean.json and B02-B14.json.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_eps_pe.py"
FIXTURE_ROOT = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"

OWNED_BUG = "B01"
BUG_IDS = [f"B{n:02d}" for n in range(1, 15)]  # B01 ... B14


def _fixture_path(fixture_id: str) -> Path:
    if fixture_id == "clean":
        return FIXTURE_ROOT / "clean.json"
    return FIXTURE_ROOT / "bugs" / f"{fixture_id}.json"


def _expected_exit(fixture_id: str) -> int:
    if fixture_id == OWNED_BUG:
        return 1  # script MUST detect its owned bug
    return 0  # clean fixture and all non-owned bug fixtures must pass


# Parametrized over all 15 fixtures: clean + B01..B14
@pytest.mark.parametrize(
    "fixture_id",
    ["clean"] + BUG_IDS,
    ids=["clean"] + BUG_IDS,
)
def test_verify_eps_pe(fixture_id: str) -> None:
    fixture_path = _fixture_path(fixture_id)
    assert fixture_path.is_file(), f"Missing fixture: {fixture_path}"

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(fixture_path)],
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
        # Must emit structured G1 failure output.
        assert "gate_id: G1" in result.stdout, (
            f"B01 failure output missing 'gate_id: G1': {result.stdout!r}"
        )
        assert "status: fail" in result.stdout, (
            f"B01 failure output missing 'status: fail': {result.stdout!r}"
        )
        assert '"base"' in result.stdout or "base" in result.stdout, (
            f"B01 failure should reference scenario 'base': {result.stdout!r}"
        )
