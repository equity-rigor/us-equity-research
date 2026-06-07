#!/usr/bin/env python3
"""Smoke harness for the v0.4.0 G20 graduated rigor scale (Sprint 3a Item 5b).

NOT a pytest module (filename is not test_*-prefixed, so pytest's default
collection ignores it; the committed suite stays at 198). Run directly:

    python3 scripts/tests/smoke_g20_graduated_rigor.py

It builds synthetic memos from the committed fixtures in
scripts/tests/fixtures/r-v2-isolation/ (weak_variance.json = S3-only,
medium_variance.json = S2), invokes scripts/verify_view_defensibility.py as a
subprocess across the 6 branches enumerated in
design/sprint-3a-context.md#item-3 Deliverable 3c plus 4 red-team guard
branches, and asserts the exit code and the structured stdout markers
(status, blocks_score_above). verify_view_defensibility.py imports no pydantic,
so this runs on a bare interpreter.

Exit 0 = all branches behaved as specified; exit 1 = at least one mismatch.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "verify_view_defensibility.py"
FIXTURES = REPO_ROOT / "scripts" / "tests" / "fixtures" / "r-v2-isolation"

WEAK = json.loads((FIXTURES / "weak_variance.json").read_text(encoding="utf-8"))
MEDIUM = json.loads((FIXTURES / "medium_variance.json").read_text(encoding="utf-8"))

WRITER = "claude-opus-4-8"
ATTACKER_DIVERSE = "claude-sonnet-4-6"

MEMO_MD = (
    "# NVDA — Buy — PT $125 (+25%)\n\n"
    "Non-consensus call: FY27 datacenter compute revenue runs above Street.\n\n"
    "## Thesis\nThe FY26Q1 10-Q segment split implies a compute exit-rate the "
    "Street's aggregated FY27 line has not yet absorbed.\n"
)


def _attack(
    *, isolated, attacker_model, outcome="rebutted", target="V_med", attack_type="base_rate_sanity"
):
    """One adjudication_trail variance_attack entry. Fields the verifier reads
    plus a schema-legal resolution (>=50 chars)."""
    entry = {
        "entry_id": "AT1",
        "type": "variance_attack",
        "phase": 3,
        "target_variance_id": target,
        "attack_type": attack_type,
        "attack_description": "R-v2 challenged the base rate of an NVDA DC compute beat of this magnitude.",
        "attack_outcome": outcome,
        "resolution": (
            "R-v2 attacked V_med on base-rate grounds; the 10-Q exit-rate and a "
            "two-year analog set rebut the attack, so the variance survives intact."
        ),
        "supporting_evidence_refs": MEDIUM["evidence_refs"],
        "attacker_independent_source_reads": 3,
    }
    if isolated is not None:
        entry["attacker_context_isolation"] = isolated
    if attacker_model is not None:
        entry["attacker_model"] = attacker_model
    return entry


def _base_memo(*, schema_version, current_score, author_model, attack, variances=None):
    memo = {
        "schema_version": schema_version,
        "current_price_usd": 100.0,
        "recommendation": {"rating": "Buy", "upside_downside_pct": 25.0},
        "consensus_variance": variances if variances is not None else [WEAK, MEDIUM],
        "top_anchors": [
            {
                "claim": "Street consensus price target (PT) median",
                "value": 110.0,
                "citation": {
                    "s_level": "S4",
                    "source_type": "FactSet consensus",
                    "ref": "FactSet NVDA PT median n=42 2026-05",
                },
            }
        ],
        "revision_velocity": {"n_analysts": 42},
        "adjudication_trail": [attack] if attack is not None else [],
    }
    md = {}
    if current_score is not None or author_model is not None:
        md = {}
        if current_score is not None:
            md["current_score"] = current_score
        if author_model is not None:
            md["author_model"] = author_model
        memo["memo_metadata"] = md
    return memo


# Each branch: (id, description, memo, expected_exit, required_markers[])
def _branches():
    surviving_noniso = _attack(isolated=False, attacker_model=None)
    surviving_iso_same = _attack(isolated=True, attacker_model=WRITER)
    surviving_iso_diverse = _attack(isolated=True, attacker_model=ATTACKER_DIVERSE)

    return [
        (
            "1_v030_pass",
            "v0.3.0 memo passing (a)+(b)+(c); graduated check N/A",
            _base_memo(
                schema_version="0.3.0",
                current_score=None,
                author_model=None,
                attack=surviving_noniso,
            ),
            0,
            ["status: pass", "graduated_rigor: n_a (v0.3.0 schema"],
        ),
        (
            "2_v040_8.7_noiso_pass",
            "v0.4.0 claim 8.7, no isolation, passes (a)+(b)+(c) -> 8.5-9.0 band",
            _base_memo(
                schema_version="0.4.0",
                current_score=8.7,
                author_model=WRITER,
                attack=surviving_noniso,
            ),
            0,
            ["status: pass", "graduated_rigor: n_a (claimed score 8.7"],
        ),
        (
            "3_v040_9.2_noiso_fail",
            "v0.4.0 claim 9.2, surviving but NON-isolated attack -> cap 9.0",
            _base_memo(
                schema_version="0.4.0",
                current_score=9.2,
                author_model=WRITER,
                attack=surviving_noniso,
            ),
            9,
            ["status: fail", "blocks_score_above: 9.0"],
        ),
        (
            "4_v040_9.2_iso_samemodel_fail",
            "v0.4.0 claim 9.2, isolated attack but attacker==writer model -> cap 9.0",
            _base_memo(
                schema_version="0.4.0",
                current_score=9.2,
                author_model=WRITER,
                attack=surviving_iso_same,
            ),
            10,
            ["status: fail", "blocks_score_above: 9.0"],
        ),
        (
            "5_v040_9.2_iso_diversemodel_pass",
            "v0.4.0 claim 9.2, isolated + model-diverse surviving attack -> pass",
            _base_memo(
                schema_version="0.4.0",
                current_score=9.2,
                author_model=WRITER,
                attack=surviving_iso_diverse,
            ),
            0,
            ["status: pass", "graduated_rigor: satisfied"],
        ),
        (
            "6_v040_9.5_all_met_pass",
            "v0.4.0 claim 9.5, all conditions met -> pass",
            _base_memo(
                schema_version="0.4.0",
                current_score=9.5,
                author_model=WRITER,
                attack=surviving_iso_diverse,
            ),
            0,
            ["status: pass", "graduated_rigor: satisfied"],
        ),
        # --- red-team guard branches (beyond the required 6) ---
        (
            "7_v040_9.0_boundary_noiso_pass",
            "GUARD: claim EXACTLY 9.0 is not > 9.0 -> graduated n_a, pass (strict inequality)",
            _base_memo(
                schema_version="0.4.0",
                current_score=9.0,
                author_model=WRITER,
                attack=surviving_noniso,
            ),
            0,
            ["status: pass", "graduated_rigor: n_a (claimed score 9.0"],
        ),
        (
            "8_pre030_grandfathered_skip",
            "GUARD: v0.2.0 memo grandfathered -> skipped",
            _base_memo(
                schema_version="0.2.0",
                current_score=9.5,
                author_model=WRITER,
                attack=surviving_iso_diverse,
            ),
            0,
            ["status: skipped", "grandfathered_pre_v0_3"],
        ),
        (
            "9_v040_9.2_iso_diverse_no_writer_fail",
            "GUARD: claim 9.2, isolated+diverse attack but writer model undeterminable -> cap 9.0",
            _base_memo(
                schema_version="0.4.0",
                current_score=9.2,
                author_model=None,
                attack=surviving_iso_diverse,
            ),
            8,
            ["status: fail", "blocks_score_above: 9.0"],
        ),
        (
            "10_v040_9.2_breaks_condition_b_cap85",
            "GUARD: claim 9.2 but only S3 (weak) variance -> (b) fails, cap 8.5 (graduated is additive, not a replacement)",
            _base_memo(
                schema_version="0.4.0",
                current_score=9.2,
                author_model=WRITER,
                attack=_attack(isolated=True, attacker_model=ATTACKER_DIVERSE, target="V_weak"),
                variances=[WEAK],
            ),
            4,
            ["status: fail", "blocks_score_above: 8.5"],
        ),
    ]


def main() -> int:
    if not SCRIPT.is_file():
        print(f"FATAL: verifier not found at {SCRIPT}")
        return 2
    tmp = Path(tempfile.mkdtemp(prefix="g20smoke-"))
    md_path = tmp / "memo.md"
    md_path.write_text(MEMO_MD, encoding="utf-8")

    rows = []
    all_ok = True
    for bid, desc, memo, exp_exit, markers in _branches():
        mj = tmp / f"{bid}.json"
        mj.write_text(json.dumps(memo), encoding="utf-8")
        res = subprocess.run(
            [sys.executable, str(SCRIPT), "--memo-json", str(mj), "--memo-md", str(md_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        exit_ok = res.returncode == exp_exit
        markers_ok = all(m in res.stdout for m in markers)
        ok = exit_ok and markers_ok
        all_ok = all_ok and ok
        rows.append((bid, ok, exp_exit, res.returncode, desc))
        if not ok:
            print(f"--- MISMATCH [{bid}] ---")
            print(f"  expected exit {exp_exit}, got {res.returncode}; markers_ok={markers_ok}")
            print(f"  required markers: {markers}")
            print("  stdout:\n" + "\n".join("    " + ln for ln in res.stdout.splitlines()))
            if res.stderr.strip():
                print("  stderr:\n" + "\n".join("    " + ln for ln in res.stderr.splitlines()))

    print("\n=== G20 v0.4.0 graduated rigor smoke ===")
    for bid, ok, exp, got, desc in rows:
        print(f"  [{'PASS' if ok else 'FAIL'}] {bid:<40} exit exp={exp} got={got}  {desc}")
    print(
        f"\n{'ALL BRANCHES OK' if all_ok else 'SMOKE FAILED'} ({sum(1 for r in rows if r[1])}/{len(rows)})"
    )
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
