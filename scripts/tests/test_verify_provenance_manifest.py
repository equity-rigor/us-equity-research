"""Tests for scripts/verify_provenance_manifest.py (Gate G19, provenance manifest).

First committed coverage for G19. Before this, G18/G19/G20 — the three v0.3.0
audit-closing gates — had zero collected pytest coverage; only the older math /
structural gates were tested. That gap is exactly why the v0.4.0 ship silently
disabled G19: the gate read the literal `schema_version != "0.3.0"`, so every
v0.4.0 memo took the grandfather/skip branch and ran neither the manifest
requirement nor the on-disk sha256 integrity check. The Sprint 3b fix widens the
gate to RUNNABLE_SCHEMA_VERSIONS = {0.3.0, 0.4.0}.

Invariants pinned here:
  1. The fix: a v0.4.0 memo RUNS G19, never 'skipped' — hand_authored -> pass
     (cap 7.5); missing manifest -> fail (exit 1). (regression guard)
  2. Full happy path with a real on-disk hash-matching manifest -> pass, for
     both 0.3.0 and 0.4.0 memos.
  3. The integrity check actually fires on v0.4.0: tampering an output file
     after the manifest is written -> fail with a hash mismatch (exit 11).
  4. Genuine pre-0.3.0 memos (0.1.0 / 0.2.0) are still grandfathered (skipped).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_provenance_manifest.py"

# 15 agent ids = the v0.3.0 agent_provenance floor (Phase 1: 5, Phase 2: 6,
# Phase 3: 4) per schemas/manifest.json agent_provenance.minItems.
AGENT_IDS = [
    "A1", "A4", "A5", "A8", "FS",
    "A2", "A3", "A3-Peers", "R", "A6", "A-Consensus",
    "A7", "Mirror", "Topic-Forensic", "R-v2",
]
TS = "2026-05-31T00:00:00+00:00"


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _run(memo_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memo-json", str(memo_path)],
        capture_output=True,
        text=True,
    )


def _write_memo(tmp_path: Path, schema_version: str, **metadata) -> Path:
    memo = {
        "schema_version": schema_version,
        "ticker": "NVDA",
        "memo_metadata": metadata,
    }
    p = tmp_path / "memo.json"
    p.write_text(json.dumps(memo), encoding="utf-8")
    return p


def _build_full_run(tmp_path: Path, schema_version: str) -> tuple[Path, list[Path], Path]:
    """A memo + a complete, hash-consistent manifest + its referenced outputs.

    G19 does not validate the manifest against schemas/manifest.json; it checks
    presence of required top-level fields, manifest_version == '0.3.0', ticker
    match, the count floors (>=12 web searches, >=12 verification calls, >=15
    agents), and that each declared output's sha256 matches the bytes on disk.
    The manifest stays manifest_version '0.3.0' even for a 0.4.0 memo because the
    manifest schema is unchanged in v0.4.0 (see scripts/write_manifest.py).
    """
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    files: list[Path] = []
    for name, content in [
        ("NVDA_IC_memo.md", "# NVDA IC memo\nBody.\n"),
        ("NVDA_structured.json", '{"ticker": "NVDA"}'),
        ("NVDA_source_tags.json", '{"top_anchors": []}'),
        ("NVDA_scenarios.json", '{"scenarios": []}'),
    ]:
        f = outputs / name
        f.write_text(content, encoding="utf-8")
        files.append(f)

    manifest = {
        "manifest_version": "0.3.0",
        "ticker": "NVDA",
        "run_id": str(uuid.uuid4()),
        "created_at": TS,
        "plugin_versions": {
            "us_equity_research": "0.4.0",
            "us_equity_ic_rigor": "0.4.0",
        },
        "phase_timing": {
            k: {"start": TS, "end": TS}
            for k in ("phase_0", "phase_1", "phase_2", "phase_3", "verification")
        },
        "agent_provenance": [
            {"agent_id": a, "phase": 1, "status": "skipped"} for a in AGENT_IDS
        ],
        "web_search_log": [
            {"tool": "WebSearch", "query_or_url": f"q{i}", "timestamp": TS}
            for i in range(12)
        ],
        "verification_calls_count": 12,
        "outputs_produced": [
            {"path": str(f), "sha256": _sha256(f), "file_type": "workpaper_md"}
            for f in files
        ],
    }
    man_path = outputs / "NVDA_manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    memo = {
        "schema_version": schema_version,
        "ticker": "NVDA",
        "memo_metadata": {"manifest_ref": str(man_path)},
    }
    memo_path = tmp_path / "memo.json"
    memo_path.write_text(json.dumps(memo), encoding="utf-8")
    return memo_path, files, man_path


# --- the fix: v0.4.0 is no longer grandfathered out -----------------------

def test_v040_hand_authored_runs_not_skipped(tmp_path: Path) -> None:
    """Regression guard: a v0.4.0 hand_authored memo RUNS G19 (pass, cap 7.5),
    it is not silently skipped as it was before the Sprint 3b fix."""
    memo_path = _write_memo(tmp_path, "0.4.0", hand_authored=True)
    res = _run(memo_path)
    assert "status: skipped" not in res.stdout, res.stdout
    assert "mode: hand_authored" in res.stdout
    assert "blocks_score_above: 7.5" in res.stdout
    assert res.returncode == 0


def test_v040_missing_manifest_fails_not_skipped(tmp_path: Path) -> None:
    """Regression guard: a v0.4.0 memo with neither a manifest nor the
    hand_authored flag FAILS — provenance is now enforced, not skipped."""
    memo_path = _write_memo(tmp_path, "0.4.0")
    res = _run(memo_path)
    assert "status: skipped" not in res.stdout, res.stdout
    assert res.returncode == 1
    assert "manifest_ref is absent" in res.stdout


@pytest.mark.parametrize("schema_version", ["0.3.0", "0.4.0"])
def test_runnable_versions_full_happy_path(tmp_path: Path, schema_version: str) -> None:
    """Both runnable schema versions pass against a complete, hash-consistent
    manifest. Pins that the fix did not break the 0.3.0 path."""
    memo_path, _files, _man = _build_full_run(tmp_path, schema_version)
    res = _run(memo_path)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "status: pass" in res.stdout


def test_v040_hash_tamper_detected(tmp_path: Path) -> None:
    """The on-disk integrity check actually runs on a v0.4.0 memo: editing an
    output file after the manifest is written is caught as a hash mismatch."""
    memo_path, files, _man = _build_full_run(tmp_path, "0.4.0")
    files[0].write_text("# NVDA IC memo TAMPERED\n", encoding="utf-8")
    res = _run(memo_path)
    assert res.returncode == 11, res.stdout
    assert "actual on-disk sha256" in res.stdout


# --- genuine pre-0.3.0 memos remain grandfathered -------------------------

@pytest.mark.parametrize("schema_version", ["0.1.0", "0.2.0"])
def test_pre_v030_grandfathered_skip(tmp_path: Path, schema_version: str) -> None:
    memo_path = _write_memo(tmp_path, schema_version)
    res = _run(memo_path)
    assert res.returncode == 0
    assert "status: skipped" in res.stdout
    assert "grandfathered_pre_v0_3" in res.stdout
