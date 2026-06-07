#!/usr/bin/env python3
"""
test_plugin_file_sync.py — Verify plugin script/schema copies match repo-root sources.

Sprint 4 Item 8 fix: scripts/ and schemas/ live canonically at the repo root,
and are mirrored into each plugin directory via scripts/sync_plugin_files.sh.
The mirror is required for the plugin install to ship verifier scripts; without
it, users who run the framework outside the cloned repo cannot reach the
verifier scripts and the gates silently degrade to LLM-analytical evaluation.

This test fails CI if the plugin copies drift from the canonical sources.

Run: pytest -q scripts/tests/test_plugin_file_sync.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

# Resolve repo root from this test file's location.
REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_SCRIPTS = REPO_ROOT / "scripts"
SOURCE_SCHEMAS = REPO_ROOT / "schemas"
PLUGIN_1 = REPO_ROOT / "us-equity-research"
PLUGIN_2 = REPO_ROOT / "us-equity-ic-rigor"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _list_source_files(source_dir: Path, ext: str) -> list[Path]:
    return sorted(p for p in source_dir.glob(f"*{ext}") if p.is_file())


@pytest.fixture(scope="module")
def source_scripts() -> list[Path]:
    return _list_source_files(SOURCE_SCRIPTS, ".py")


@pytest.fixture(scope="module")
def source_schemas() -> list[Path]:
    return _list_source_files(SOURCE_SCHEMAS, ".json")


def test_source_directories_exist():
    """Sanity: the canonical source directories exist."""
    assert SOURCE_SCRIPTS.is_dir(), f"Missing {SOURCE_SCRIPTS}"
    assert SOURCE_SCHEMAS.is_dir(), f"Missing {SOURCE_SCHEMAS}"


def test_plugin_directories_exist():
    """Sanity: both plugin directories exist."""
    assert PLUGIN_1.is_dir(), f"Missing {PLUGIN_1}"
    assert PLUGIN_2.is_dir(), f"Missing {PLUGIN_2}"


@pytest.mark.parametrize("plugin_dir", [PLUGIN_1, PLUGIN_2])
def test_plugin_has_scripts_directory(plugin_dir: Path):
    """Each plugin must have a scripts/ subdirectory."""
    assert (plugin_dir / "scripts").is_dir(), (
        f"Plugin {plugin_dir.name} missing scripts/ directory. "
        f"Run: bash scripts/sync_plugin_files.sh"
    )


@pytest.mark.parametrize("plugin_dir", [PLUGIN_1, PLUGIN_2])
def test_plugin_has_schemas_directory(plugin_dir: Path):
    """Each plugin must have a schemas/ subdirectory."""
    assert (plugin_dir / "schemas").is_dir(), (
        f"Plugin {plugin_dir.name} missing schemas/ directory. "
        f"Run: bash scripts/sync_plugin_files.sh"
    )


@pytest.mark.parametrize("plugin_dir", [PLUGIN_1, PLUGIN_2])
def test_plugin_scripts_match_source(plugin_dir: Path, source_scripts: list[Path]):
    """Every repo-root script file must be present and hash-identical in each plugin."""
    plugin_scripts_dir = plugin_dir / "scripts"
    drift: list[str] = []
    missing: list[str] = []
    for src in source_scripts:
        dst = plugin_scripts_dir / src.name
        if not dst.is_file():
            missing.append(f"  MISSING: {dst.relative_to(REPO_ROOT)}")
            continue
        if _sha256(src) != _sha256(dst):
            drift.append(
                f"  DRIFT: {dst.relative_to(REPO_ROOT)} differs from {src.relative_to(REPO_ROOT)}"
            )
    issues = missing + drift
    assert not issues, (
        f"Plugin {plugin_dir.name} script copies out of sync with repo root:\n"
        + "\n".join(issues)
        + "\n\nRun: bash scripts/sync_plugin_files.sh"
    )


@pytest.mark.parametrize("plugin_dir", [PLUGIN_1, PLUGIN_2])
def test_plugin_schemas_match_source(plugin_dir: Path, source_schemas: list[Path]):
    """Every repo-root schema file must be present and hash-identical in each plugin."""
    plugin_schemas_dir = plugin_dir / "schemas"
    drift: list[str] = []
    missing: list[str] = []
    for src in source_schemas:
        dst = plugin_schemas_dir / src.name
        if not dst.is_file():
            missing.append(f"  MISSING: {dst.relative_to(REPO_ROOT)}")
            continue
        if _sha256(src) != _sha256(dst):
            drift.append(
                f"  DRIFT: {dst.relative_to(REPO_ROOT)} differs from {src.relative_to(REPO_ROOT)}"
            )
    issues = missing + drift
    assert not issues, (
        f"Plugin {plugin_dir.name} schema copies out of sync with repo root:\n"
        + "\n".join(issues)
        + "\n\nRun: bash scripts/sync_plugin_files.sh"
    )


@pytest.mark.parametrize("plugin_dir", [PLUGIN_1, PLUGIN_2])
def test_no_orphan_scripts_in_plugin(plugin_dir: Path, source_scripts: list[Path]):
    """Plugin scripts/ must not contain files that don't exist at repo root.

    This catches the case where a script was deleted from repo-root but
    a stale copy remains in a plugin directory.
    """
    plugin_scripts_dir = plugin_dir / "scripts"
    if not plugin_scripts_dir.is_dir():
        pytest.skip("plugin scripts/ directory missing — covered by earlier test")
    source_names = {p.name for p in source_scripts}
    orphans = [f.name for f in plugin_scripts_dir.glob("*.py") if f.name not in source_names]
    assert not orphans, (
        f"Plugin {plugin_dir.name} has script files not in repo-root scripts/: "
        f"{orphans}. Delete them or restore them to the canonical source."
    )


@pytest.mark.parametrize("plugin_dir", [PLUGIN_1, PLUGIN_2])
def test_no_orphan_schemas_in_plugin(plugin_dir: Path, source_schemas: list[Path]):
    """Plugin schemas/ must not contain files that don't exist at repo root."""
    plugin_schemas_dir = plugin_dir / "schemas"
    if not plugin_schemas_dir.is_dir():
        pytest.skip("plugin schemas/ directory missing — covered by earlier test")
    source_names = {p.name for p in source_schemas}
    orphans = [f.name for f in plugin_schemas_dir.glob("*.json") if f.name not in source_names]
    assert not orphans, (
        f"Plugin {plugin_dir.name} has schema files not in repo-root schemas/: "
        f"{orphans}. Delete them or restore them to the canonical source."
    )
