"""Tests for scripts/verify_view_defensibility.py (Gate G20, view defensibility
+ the v0.4.0 graduated rigor scale).

First committed pytest coverage for G20. It promotes the previously uncollected
smoke harness scripts/tests/smoke_g20_graduated_rigor.py — whose filename is not
test_-prefixed, so pytest's default collection ignored it — into the collected
suite by importing its branch table and asserting every branch under pytest.
The 198-green suite did not touch G18/G19/G20 before this; that blind spot is
what let the G19 schema-version skip bug ship in v0.4.0.

Coverage:
  - All 10 smoke branches (the 6 required from
    design/sprint-3a-context.md#item-3 Deliverable 3c plus 4 red-team guards:
    the 9.0 strict-boundary, pre-0.3.0 grandfather, undeterminable-writer,
    and the additive-not-replacement cap-8.5 guard).
  - Direct guards that a v0.4.0 memo RUNS (is not grandfathered) and a
    pre-0.3.0 memo is skipped — symmetry with the G19 regression guards.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_view_defensibility.py"
SMOKE_PATH = REPO_ROOT / "scripts" / "tests" / "smoke_g20_graduated_rigor.py"


def _load_smoke():
    """Import the (uncollected) smoke harness by path so the test and the smoke
    share one branch table — they cannot drift apart."""
    spec = importlib.util.spec_from_file_location("smoke_g20_graduated_rigor", SMOKE_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


smoke = _load_smoke()
BRANCHES = smoke._branches()


def _run(memo: dict, md_text: str, tmp_path: Path) -> subprocess.CompletedProcess:
    mj = tmp_path / "memo.json"
    mj.write_text(json.dumps(memo), encoding="utf-8")
    md = tmp_path / "memo.md"
    md.write_text(md_text, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(mj), "--memo-md", str(md)],
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize(
    "bid,desc,memo,exp_exit,markers",
    BRANCHES,
    ids=[b[0] for b in BRANCHES],
)
def test_graduated_rigor_branch(bid, desc, memo, exp_exit, markers, tmp_path: Path) -> None:
    res = _run(memo, smoke.MEMO_MD, tmp_path)
    assert res.returncode == exp_exit, (
        f"[{bid}] {desc}: expected exit {exp_exit}, got {res.returncode}\n"
        f"stdout:\n{res.stdout}\nstderr:\n{res.stderr}"
    )
    for m in markers:
        assert m in res.stdout, f"[{bid}] {desc}: missing marker {m!r}\nstdout:\n{res.stdout}"


def test_v040_is_not_grandfathered(tmp_path: Path) -> None:
    """Symmetry with the G19 guard: a v0.4.0 memo RUNS G20, never skipped."""
    memo = smoke._base_memo(
        schema_version="0.4.0",
        current_score=8.7,
        author_model="claude-opus-4-8",
        attack=smoke._attack(isolated=False, attacker_model=None),
    )
    res = _run(memo, smoke.MEMO_MD, tmp_path)
    assert "status: skipped" not in res.stdout, res.stdout
    assert "grandfathered" not in res.stdout, res.stdout
    assert res.returncode == 0


def test_pre030_is_grandfathered(tmp_path: Path) -> None:
    memo = smoke._base_memo(
        schema_version="0.2.0",
        current_score=9.5,
        author_model="claude-opus-4-8",
        attack=smoke._attack(isolated=True, attacker_model="claude-sonnet-4-6"),
    )
    res = _run(memo, smoke.MEMO_MD, tmp_path)
    assert res.returncode == 0
    assert "status: skipped" in res.stdout
    assert "grandfathered_pre_v0_3" in res.stdout
