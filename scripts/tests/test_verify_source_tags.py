"""Tests for scripts/verify_source_tags.py — gate G6, bug B06.

Cross-sensitivity contract: this script must fire only on B06.md,
return 0 on clean.md and B01-B05, B07-B14.

Per the bug-script-matrix:
- B06 is the only MD-only bug (a stripped S-tag at first appearance).
- B07 and B11 modify the Markdown layer too, but in DIFFERENT ways
  (headline language rewrite and §6.0 GAAP/non-GAAP paragraph removal
  respectively). G6 must NOT trip on those — they are owned by G7 and
  G11 respectively.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_source_tags.py"
FIXTURE_ROOT = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"

OWNED_BUG = "B06"
BUG_IDS = [f"B{n:02d}" for n in range(1, 15)]  # B01 ... B14


def _fixture_md_path(fixture_id: str) -> Path:
    if fixture_id == "clean":
        return FIXTURE_ROOT / "clean.md"
    return FIXTURE_ROOT / "bugs" / f"{fixture_id}.md"


def _expected_nonzero(fixture_id: str) -> bool:
    return fixture_id == OWNED_BUG


# Parametrized over all 15 fixtures: clean + B01..B14
@pytest.mark.parametrize(
    "fixture_id",
    ["clean"] + BUG_IDS,
    ids=["clean"] + BUG_IDS,
)
def test_verify_source_tags(fixture_id: str) -> None:
    fixture_path = _fixture_md_path(fixture_id)
    assert fixture_path.is_file(), f"Missing fixture: {fixture_path}"

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(fixture_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    if _expected_nonzero(fixture_id):
        assert result.returncode != 0, (
            f"Fixture {fixture_id}: expected non-zero exit, got 0.\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        # Must emit structured G6 failure output.
        assert "gate_id: G6" in result.stdout, (
            f"B06 failure output missing 'gate_id: G6': {result.stdout!r}"
        )
        assert "status: fail" in result.stdout, (
            f"B06 failure output missing 'status: fail': {result.stdout!r}"
        )
        # Must point to the offending phrase / anchor.
        assert "$130B" in result.stdout or "revenue" in result.stdout, (
            f"B06 failure should reference the stripped revenue anchor: "
            f"{result.stdout!r}"
        )
    else:
        assert result.returncode == 0, (
            f"Fixture {fixture_id}: expected exit 0, got "
            f"{result.returncode}.\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
        assert "gate_id: G6" in result.stdout
        assert "status: pass" in result.stdout
