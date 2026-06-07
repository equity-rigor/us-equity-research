#!/usr/bin/env python3
"""
test_write_manifest.py — Direct tests for scripts/write_manifest.py.

Sprint 4 Item 4 final closure. Tests the manifest-writer that Plugin 1's
orchestrator calls at end of Phase 3 to produce outputs/{TICKER}_manifest.json.

Covered behavior:
  - Basic manifest written with required top-level fields
  - SHA-256 hashes computed correctly over output file contents
  - Workpapers detected from outputs/workpapers/{TICKER}_*.md
  - Manifest validates against schemas/manifest.json
  - Seed file (when present) is merged into the manifest
  - Missing outputs dir raises an error / non-zero exit
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "write_manifest.py"


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _setup_outputs_dir(tmp_path: Path, ticker: str = "TEST") -> Path:
    """Create a realistic outputs/ directory layout for the manifest writer to walk."""
    outputs = tmp_path / "outputs"
    outputs.mkdir()

    # Main deliverables
    (outputs / f"{ticker}_IC_memo.md").write_text(
        "# IC Memo\n\nSubstantive content here that exceeds 500 bytes " + "A" * 600,
        encoding="utf-8",
    )
    (outputs / f"{ticker}_structured.json").write_text(
        json.dumps({"schema_version": "0.5.0", "ticker": ticker}),
        encoding="utf-8",
    )

    # Workpapers — one per specialist, simulating the orchestrator output
    workpapers = outputs / "workpapers"
    workpapers.mkdir()
    for agent in [
        "A1_industry",
        "A4_capacity",
        "A5_regulatory",
        "A8_positioning",
        "FS_forensic",
        "A2_continuation",
        "A3_pipeline",
        "A6_channel",
        "A_Consensus",
        "A7_valuation",
        "R_redteam_v1",
        "R_v2_isolated",
    ]:
        wp = workpapers / f"{ticker}_{agent}.md"
        wp.write_text(
            f"# {agent} workpaper\n\nSubstantive findings " + "X" * 600,
            encoding="utf-8",
        )

    return outputs


def _write_seed(outputs_dir: Path, ticker: str, **overrides) -> Path:
    """Write a manifest seed file as the orchestrator would during the run."""
    seed = {
        "run_id": "test-run-uuid-1234",
        "plugin_versions": {
            "us_equity_research": "0.5.0",
            "us_equity_ic_rigor": "0.5.0",
        },
        "phase_timing": {
            "phase_0": {"started_at": "2026-06-06T00:00:00Z", "elapsed_s": 30},
            "phase_1": {"started_at": "2026-06-06T00:00:30Z", "elapsed_s": 600},
            "phase_2": {"started_at": "2026-06-06T00:10:30Z", "elapsed_s": 720},
            "phase_3": {"started_at": "2026-06-06T00:22:30Z", "elapsed_s": 600},
        },
        "web_search_log": [
            {"url": f"https://data.sec.gov/{i}", "fetched_at": "2026-06-06T00:00:00Z"}
            for i in range(15)
        ],
        "verification_calls_count": 15,
        "orchestrator_notes": "test fixture",
    }
    seed.update(overrides)
    seed_path = outputs_dir / f"{ticker}_manifest_seed.json"
    seed_path.write_text(json.dumps(seed), encoding="utf-8")
    return seed_path


def _run(
    ticker: str,
    outputs_dir: Path,
    seed_path: Path | None = None,
    extra_args: list[str] | None = None,
) -> subprocess.CompletedProcess:
    cmd = [
        sys.executable,
        str(SCRIPT),
        "--ticker",
        ticker,
        "--outputs-dir",
        str(outputs_dir),
    ]
    if seed_path is not None:
        cmd.extend(["--seed", str(seed_path)])
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(cmd, capture_output=True, text=True)


# -----------------------------------------------------------------------------
# Basic / pass cases
# -----------------------------------------------------------------------------


def test_writer_creates_manifest_file(tmp_path: Path):
    ticker = "TEST"
    outputs = _setup_outputs_dir(tmp_path, ticker)
    seed = _write_seed(outputs, ticker)
    proc = _run(ticker, outputs, seed)
    assert proc.returncode == 0, f"writer failed: {proc.stdout}\n{proc.stderr}"
    manifest_path = outputs / f"{ticker}_manifest.json"
    assert manifest_path.is_file(), "manifest file was not created"


def test_manifest_has_required_top_level_fields(tmp_path: Path):
    ticker = "TEST"
    outputs = _setup_outputs_dir(tmp_path, ticker)
    seed = _write_seed(outputs, ticker)
    _run(ticker, outputs, seed)
    manifest = json.loads((outputs / f"{ticker}_manifest.json").read_text())

    required = {
        "manifest_version",
        "ticker",
        "run_id",
        "created_at",
        "plugin_versions",
        "phase_timing",
        "agent_provenance",
        "web_search_log",
        "verification_calls_count",
        "outputs_produced",
    }
    missing = required - set(manifest.keys())
    assert not missing, f"manifest missing required fields: {missing}"


def test_manifest_ticker_matches_argument(tmp_path: Path):
    ticker = "MYCO"
    outputs = _setup_outputs_dir(tmp_path, ticker)
    seed = _write_seed(outputs, ticker)
    _run(ticker, outputs, seed)
    manifest = json.loads((outputs / f"{ticker}_manifest.json").read_text())
    assert manifest["ticker"] == ticker


def test_manifest_carries_seed_run_id(tmp_path: Path):
    ticker = "TEST"
    outputs = _setup_outputs_dir(tmp_path, ticker)
    seed = _write_seed(outputs, ticker, run_id="custom-run-id-9999")
    _run(ticker, outputs, seed)
    manifest = json.loads((outputs / f"{ticker}_manifest.json").read_text())
    assert manifest["run_id"] == "custom-run-id-9999"


# -----------------------------------------------------------------------------
# Hash integrity
# -----------------------------------------------------------------------------


def test_sha256_hash_matches_actual_file_content(tmp_path: Path):
    ticker = "TEST"
    outputs = _setup_outputs_dir(tmp_path, ticker)
    seed = _write_seed(outputs, ticker)
    _run(ticker, outputs, seed)
    manifest = json.loads((outputs / f"{ticker}_manifest.json").read_text())

    outputs_produced = manifest.get("outputs_produced", [])
    assert outputs_produced, "outputs_produced should not be empty"

    for entry in outputs_produced:
        path_str = entry.get("path")
        declared_hash = entry.get("sha256")
        assert path_str and declared_hash, f"entry malformed: {entry}"
        # Resolve path relative to outputs dir or absolute
        on_disk = Path(path_str)
        if not on_disk.is_absolute():
            # The path field is "outputs/<file>" relative to the project working dir.
            # In test, that resolves to the tmp_path/outputs/<file>.
            on_disk = outputs / Path(path_str).name
        if on_disk.is_file():
            actual_hash = _sha256(on_disk.read_bytes())
            assert actual_hash == declared_hash, (
                f"hash mismatch for {path_str}: declared={declared_hash} actual={actual_hash}"
            )


# -----------------------------------------------------------------------------
# Agent provenance detection
# -----------------------------------------------------------------------------


def test_agent_provenance_detected_from_workpapers(tmp_path: Path):
    ticker = "TEST"
    outputs = _setup_outputs_dir(tmp_path, ticker)
    seed = _write_seed(outputs, ticker)
    _run(ticker, outputs, seed)
    manifest = json.loads((outputs / f"{ticker}_manifest.json").read_text())

    provenance = manifest.get("agent_provenance", [])
    # _setup created 12 workpapers; provenance should have at least 12 entries
    # (the writer may add the orchestrator/synthesis entries on top).
    assert len(provenance) >= 12, (
        f"expected ≥12 agent entries from 12 workpapers, got {len(provenance)}: "
        f"{[e.get('id') if isinstance(e, dict) else e for e in provenance]}"
    )


def test_manifest_validates_against_schema(tmp_path: Path):
    ticker = "TEST"
    outputs = _setup_outputs_dir(tmp_path, ticker)
    seed = _write_seed(outputs, ticker)
    _run(ticker, outputs, seed)
    manifest = json.loads((outputs / f"{ticker}_manifest.json").read_text())

    schema = json.loads((REPO_ROOT / "schemas" / "manifest.json").read_text())
    required_fields = set(schema.get("required", []))
    missing = required_fields - set(manifest.keys())
    assert not missing, f"manifest fails schema 'required' check: {missing}"


# -----------------------------------------------------------------------------
# Degraded path — missing seed
# -----------------------------------------------------------------------------


def test_missing_seed_writes_manifest_with_placeholders(tmp_path: Path):
    """The writer's documented degraded path: if seed is missing, write a
    manifest with placeholder fields and emit a WARNING to stderr."""
    ticker = "TEST"
    outputs = _setup_outputs_dir(tmp_path, ticker)
    proc = _run(ticker, outputs, seed_path=None)
    # Documented behavior: exit 0 with WARNING on stderr.
    assert proc.returncode == 0, f"writer should not hard-fail on missing seed: {proc.stderr}"
    manifest_path = outputs / f"{ticker}_manifest.json"
    assert manifest_path.is_file(), "manifest should still be written"
    # Some signal that the run was degraded — either WARNING in stderr or
    # placeholder/incomplete fields in the manifest itself.
    has_warning_stderr = "warn" in proc.stderr.lower() or "placeholder" in proc.stderr.lower()
    manifest = json.loads(manifest_path.read_text())
    has_placeholder_marker = (
        manifest.get("run_id", "").startswith("placeholder")
        or manifest.get("orchestrator_notes", "") != ""
    )
    assert has_warning_stderr or has_placeholder_marker, (
        f"degraded path should signal incompleteness; stderr={proc.stderr!r} "
        f"manifest run_id={manifest.get('run_id')!r}"
    )


# -----------------------------------------------------------------------------
# Error path — missing outputs dir
# -----------------------------------------------------------------------------


def test_missing_outputs_dir_raises_error(tmp_path: Path):
    ticker = "TEST"
    bogus_outputs = tmp_path / "does_not_exist"
    proc = _run(ticker, bogus_outputs, seed_path=None)
    assert proc.returncode != 0, "writer should fail when outputs dir missing"
