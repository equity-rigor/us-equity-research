"""
Tests for scripts/verify_source_tier_public.py (Gate G23, v0.7.0 judgment layer).

Invariants:
  1. n_a (exit 0) when no source_tags supplied (self-gating).
  2. pass when all citations resolve to public sources.
  3. fail on an entitlement marker in a citation ref (client-only broker note).
  4. fail on an explicit access_tier='restricted' / public_access=false flag.
  5. pass when public sell-side SIGNAL (aggregated consensus PT) is cited.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_source_tier_public.py"


def _run(tags, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    p = tmp_path / "tags.json"
    p.write_text(json.dumps(tags))
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--source-tags-json", str(p)],
        capture_output=True, text=True,
    )


def test_no_tags_is_na(tmp_path):
    r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
    assert r.returncode == 0 and "status: n_a" in r.stdout


def test_public_citations_pass(tmp_path):
    tags = {"all_citations": [
        {"s_level": "S1", "source_type": "10-K", "ref": "MU FY2025 10-K (SEC EDGAR)"},
        {"s_level": "S4", "source_type": "FactSet consensus", "ref": "Consensus PT median $829 (44 analysts)"},
        {"s_level": "S1", "source_type": "FRED", "ref": "FRED DGS10 10-yr UST 4.55%"},
    ]}
    r = _run(tags, tmp_path)
    assert r.returncode == 0 and "status: pass" in r.stdout


def test_public_sellside_signal_passes(tmp_path):
    tags = {"all_citations": [
        {"s_level": "S4", "source_type": "Other", "ref": "Publicly reported avg analyst PT and rating distribution (aggregator)"},
    ]}
    r = _run(tags, tmp_path)
    assert r.returncode == 0 and "status: pass" in r.stdout


def test_entitlement_marker_fails(tmp_path):
    tags = {"all_citations": [
        {"s_level": "S1", "source_type": "10-K", "ref": "MU FY2025 10-K"},
        {"s_level": "S4", "source_type": "Other", "ref": "Example broker research note, client-only, do not redistribute"},
    ]}
    r = _run(tags, tmp_path)
    assert r.returncode != 0 and "status: fail" in r.stdout


def test_access_tier_restricted_fails(tmp_path):
    tags = {"all_citations": [
        {"s_level": "S4", "source_type": "Other", "ref": "broker estimate", "access_tier": "restricted"},
    ]}
    r = _run(tags, tmp_path)
    assert r.returncode != 0 and "status: fail" in r.stdout


def test_top_anchor_citation_checked(tmp_path):
    tags = {"all_citations": [], "top_anchors": [
        {"anchor_id": "A1", "citation": {"s_level": "S4", "source_type": "Other",
                                         "ref": "Example sell-side desk, proprietary research, subscriber-only"}},
    ]}
    r = _run(tags, tmp_path)
    assert r.returncode != 0 and "status: fail" in r.stdout
