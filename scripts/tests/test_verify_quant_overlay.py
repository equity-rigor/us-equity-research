"""
Tests for scripts/verify_quant_overlay.py (Gates G13 + G14 / Bugs B13 + B14).

Per the dual-gate emission requirement in S-D-4's brief, a single script
invocation produces TWO independent gate_check objects (G13, G14) in the
stdout JSON, and the exit code encodes their per-gate status:

  0 — both gates pass
  1 — G13 fails, G14 passes      (B13 fixture)
  2 — G13 passes, G14 fails      (B14 fixture)
  3 — both gates fail            (not exercised by any single-fault fixture)

Tests assert NOT just the exit code but also the per-gate status parsed from
stdout JSON, which is what makes the "G13-only fail ≠ G14-only fail ≠ both-fail"
isolation automatic across the existing 15 fixtures.

Invariants verified:
  1. clean.json → exit 0, G13=pass, G14=pass
  2. bugs/B13.json → exit 1, G13=fail, G14=pass  (G13-only fail)
  3. bugs/B14.json → exit 2, G13=pass, G14=fail  (G14-only fail)
  4. bugs/B01.json…B12.json → exit 0, G13=pass, G14=pass (no cross-sensitivity)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_quant_overlay.py"
FIXTURE_DIR = REPO_ROOT / "scripts" / "tests" / "fixtures" / "nvda_v0"
CLEAN_JSON = FIXTURE_DIR / "clean.json"
CLEAN_MD = FIXTURE_DIR / "clean.md"
BUGS_DIR = FIXTURE_DIR / "bugs"


def _run(memo_json: Path, memo_md: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
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


def _gate_status(stdout: str, gate_id: str) -> str:
    """Parse the structured JSON stdout and return the per-gate status."""
    parsed = json.loads(stdout)
    for gate in parsed["gates"]:
        if gate["gate_id"] == gate_id:
            return gate["status"]
    raise AssertionError(f"gate {gate_id} not present in stdout JSON")


def _resolve_fixture(fixture_name: str) -> tuple[Path, Path]:
    """Map a fixture key (clean | B0N) to its (json, md) pair on disk."""
    if fixture_name == "clean":
        return CLEAN_JSON, CLEAN_MD
    return BUGS_DIR / f"{fixture_name}.json", BUGS_DIR / f"{fixture_name}.md"


# Parametrize across all 15 fixtures. Each row asserts THREE things via the
# per-gate status pulled from stdout JSON:
#   - the dual-gate exit code (0 / 1 / 2 / 3)
#   - the G13 status
#   - the G14 status
# This is what makes B13 ≠ B14 ≠ both-fail isolation automatic.
FIXTURE_MATRIX = [
    ("clean", 0, "pass", "pass"),
    ("B01", 0, "pass", "pass"),
    ("B02", 0, "pass", "pass"),
    ("B03", 0, "pass", "pass"),
    ("B04", 0, "pass", "pass"),
    ("B05", 0, "pass", "pass"),
    ("B06", 0, "pass", "pass"),
    ("B07", 0, "pass", "pass"),
    ("B08", 0, "pass", "pass"),
    ("B09", 0, "pass", "pass"),
    ("B10", 0, "pass", "pass"),
    ("B11", 0, "pass", "pass"),
    ("B12", 0, "pass", "pass"),
    ("B13", 1, "fail", "pass"),  # G13-only fail
    ("B14", 2, "pass", "fail"),  # G14-only fail
]


@pytest.mark.parametrize("fixture_name, expected_exit, expected_g13, expected_g14", FIXTURE_MATRIX)
def test_fixture(
    fixture_name: str,
    expected_exit: int,
    expected_g13: str,
    expected_g14: str,
) -> None:
    memo_json, memo_md = _resolve_fixture(fixture_name)
    result = _run(memo_json, memo_md)

    assert result.returncode == expected_exit, (
        f"{fixture_name}: exit code mismatch "
        f"(got {result.returncode}, expected {expected_exit})\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    g13_status = _gate_status(result.stdout, "G13")
    g14_status = _gate_status(result.stdout, "G14")

    assert g13_status == expected_g13, (
        f"{fixture_name}: G13 status mismatch (got {g13_status}, "
        f"expected {expected_g13})\nstdout: {result.stdout}"
    )
    assert g14_status == expected_g14, (
        f"{fixture_name}: G14 status mismatch (got {g14_status}, "
        f"expected {expected_g14})\nstdout: {result.stdout}"
    )


def test_dual_gate_output_shape() -> None:
    """Smoke-check the structured JSON contract on the clean fixture."""
    result = _run(CLEAN_JSON, CLEAN_MD)
    assert result.returncode == 0
    parsed = json.loads(result.stdout)
    assert set(parsed.keys()) >= {"gates", "overall_pass", "blocks_score_above"}
    assert len(parsed["gates"]) == 2
    gate_ids = [g["gate_id"] for g in parsed["gates"]]
    assert gate_ids == ["G13", "G14"]
    assert parsed["overall_pass"] is True
    assert parsed["blocks_score_above"] == 10.0


def test_isolation_invariant_distinct_exit_codes() -> None:
    """B13-only fail (exit 1) and B14-only fail (exit 2) must be distinct
    from the both-pass case (exit 0). This is the cross-fixture invariant
    that gives the orchestrator clean signal on which gate broke."""
    clean = _run(CLEAN_JSON, CLEAN_MD)
    b13_json, b13_md = _resolve_fixture("B13")
    b14_json, b14_md = _resolve_fixture("B14")
    b13 = _run(b13_json, b13_md)
    b14 = _run(b14_json, b14_md)
    exits = {clean.returncode, b13.returncode, b14.returncode}
    assert exits == {0, 1, 2}, (
        f"Exit codes for {{clean, B13, B14}} must be distinct {{0, 1, 2}}; got {exits}"
    )
