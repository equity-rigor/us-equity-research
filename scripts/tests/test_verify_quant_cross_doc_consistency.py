"""Tests for scripts/verify_quant_cross_doc_consistency.py (Gate G18).

G18 was the last of the three v0.3.0 audit-closing gates with no committed
coverage (G19/G20 gained tests with the v0.4.0 hotfixes; G18 had none). It
catches the disease where the Markdown narrative quotes a Barra factor z-score
that diverges (> ±0.2) from the structured quant_overlay.factor_tags block — the
exact NVDA "Momentum +1.8 here / +2.3 there" inconsistency it was built for.

Self-contained synthetic fixtures (stdlib-only verifier; no nvda_v0 bug fixtures
needed). Covers: n_a, no-reference pass, in-tolerance pass, divergence fail,
absent-factor fail, and code-block exclusion.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_quant_cross_doc_consistency.py"


def _run(memo_json: Path, memo_md: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(memo_json), "--memo-md", str(memo_md)],
        capture_output=True, text=True,
    )


def _write(tmp_path: Path, memo_obj: dict, md_text: str) -> tuple[Path, Path]:
    mj = tmp_path / "memo.json"
    mj.write_text(json.dumps(memo_obj), encoding="utf-8")
    md = tmp_path / "memo.md"
    md.write_text(md_text, encoding="utf-8")
    return mj, md


def test_na_when_factor_tags_absent(tmp_path: Path) -> None:
    mj, md = _write(tmp_path, {"ticker": "NVDA"}, "Momentum +2.3 in the narrative.\n")
    res = _run(mj, md)
    assert res.returncode == 0
    assert "status: n_a" in res.stdout


def test_pass_when_no_markdown_references(tmp_path: Path) -> None:
    memo = {"quant_overlay": {"factor_tags": {"momentum": 1.5, "value": -1.0}}}
    mj, md = _write(tmp_path, memo, "## Thesis\nNo factor numbers quoted here.\n")
    res = _run(mj, md)
    assert res.returncode == 0
    assert "status: pass" in res.stdout


def test_pass_within_tolerance(tmp_path: Path) -> None:
    memo = {"quant_overlay": {"factor_tags": {"momentum": 1.5}}}
    mj, md = _write(tmp_path, memo, "Momentum +1.6 (rounded) is constructive.\n")
    res = _run(mj, md)
    assert res.returncode == 0, res.stdout
    assert "status: pass" in res.stdout


def test_fail_on_divergence(tmp_path: Path) -> None:
    # The owned disease: narrative +2.3 vs structured +1.8 -> delta 0.5 > 0.2.
    memo = {"quant_overlay": {"factor_tags": {"momentum": 1.8}}}
    mj, md = _write(tmp_path, memo, "We flag Momentum +2.3 as crowded.\n")
    res = _run(mj, md)
    assert res.returncode == 1, res.stdout
    assert "status: fail" in res.stdout
    assert "momentum" in res.stdout.lower()


def test_fail_when_markdown_factor_absent_from_structured(tmp_path: Path) -> None:
    memo = {"quant_overlay": {"factor_tags": {"value": -1.0}}}
    mj, md = _write(tmp_path, memo, "Growth +2.0 is top-decile.\n")
    res = _run(mj, md)
    assert res.returncode == 1, res.stdout
    assert "status: fail" in res.stdout


def test_code_block_values_excluded(tmp_path: Path) -> None:
    # A divergent value inside a fenced code block must NOT trip the gate.
    memo = {"quant_overlay": {"factor_tags": {"momentum": 1.5}}}
    md_text = (
        "## Thesis\nNarrative quotes no factor numbers.\n\n"
        "```\nMomentum +9.9   # illustrative code sample, not a claim\n```\n"
    )
    mj, md = _write(tmp_path, memo, md_text)
    res = _run(mj, md)
    assert res.returncode == 0, res.stdout
    assert "status: pass" in res.stdout
