"""
Test-gate for the v0.7.0 judgment-layer schema change (Gates G21-G23).

Asserts that the schema makes G21-G23 first-class and that the change is
mirrored across the canonical schema and both plugin copies, and that the
three verifier scripts ship in scripts/ and both plugin scripts/ dirs.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_COPIES = [
    REPO_ROOT / "schemas" / "verification_gates.json",
    REPO_ROOT / "us-equity-ic-rigor" / "schemas" / "verification_gates.json",
    REPO_ROOT / "us-equity-research" / "schemas" / "verification_gates.json",
]
NEW_GATES = ("G21", "G22", "G23")
NEW_SCRIPTS = (
    "verify_fair_value_reconciliation.py",
    "verify_revision_attribution.py",
    "verify_source_tier_public.py",
)
SCRIPT_DIRS = [
    REPO_ROOT / "scripts",
    REPO_ROOT / "us-equity-ic-rigor" / "scripts",
    REPO_ROOT / "us-equity-research" / "scripts",
]


@pytest.mark.parametrize("schema_path", SCHEMA_COPIES, ids=lambda p: str(p.parent.parent.name))
def test_schema_declares_judgment_gates(schema_path: Path):
    d = json.loads(schema_path.read_text())
    enum = d["definitions"]["gate_id"]["enum"]
    gate_defs = d["properties"]["gate_definitions"]["properties"]
    for g in NEW_GATES:
        assert g in enum, f"{g} missing from gate_id enum in {schema_path}"
        assert g in gate_defs, f"{g} missing from gate_definitions in {schema_path}"
        assert "const" in gate_defs[g], f"{g} gate_definitions entry must carry a const description"


@pytest.mark.parametrize("schema_path", SCHEMA_COPIES, ids=lambda p: str(p.parent.parent.name))
def test_judgment_layer_gates_property(schema_path: Path):
    d = json.loads(schema_path.read_text())
    jlg = d["properties"].get("judgment_layer_gates")
    assert jlg is not None, "judgment_layer_gates property missing"
    assert jlg["type"] == "array"
    assert jlg["items"] == {"$ref": "#/definitions/gate_check"}
    # mechanical `gates` array must remain the count-capped (<=20) contract
    assert d["properties"]["gates"]["maxItems"] == 20


def test_all_schema_copies_identical():
    blobs = {p.read_text() for p in SCHEMA_COPIES}
    assert len(blobs) == 1, "verification_gates.json out of sync across plugin copies — run the schema sync"


@pytest.mark.parametrize("script", NEW_SCRIPTS)
def test_new_scripts_present_in_all_dirs(script: str):
    for d in SCRIPT_DIRS:
        assert (d / script).is_file(), f"{script} missing from {d} — run the script sync"
