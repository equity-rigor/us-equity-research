# NVDA v0 — Bug × Script Ownership Matrix

This document specifies which verification script owns which bug fixture in `bugs/B01.json…B14.json` and the test invariant each script must satisfy. Authored by S-C-11; consumed by S-C-1 through S-C-10 (Phase C, gates G1-G10) and S-D-2 through S-D-4 (Phase D, gates G11-G14).

## Ownership table

| Bug | Description | Owner script | Gate | Phase | Cross-sensitivity requirement |
|-----|-------------|--------------|------|-------|-------------------------------|
| **B01** | EPS × Multiple multiplicativity violation in base scenario (target_price=200, but eps×mult=190) | `scripts/verify_eps_pe.py` | G1 | C | All other 13 scripts (verify_segment_gm, …, verify_quant_overlay) must return 0 on B01 |
| **B02** | Segment GM weighted average diverges from consolidated GM by >50bp **on the LTM period** (Datacenter GM corrupted 76.5% → 80.0%). G2 scope is LTM/forward only — historical-period segment mismatches are informational, not gate-tripping (real 10-K disclosures routinely diverge 50-150bp on historicals due to corporate allocation, "Other / Unallocated" buckets, source-filing rounding). See `gm-taxonomy-us.md` G2-scope paragraph and `pm-redteam-rubric-us.md` B2 scope note. | `scripts/verify_segment_gm.py` | G2 | C | All other 13 scripts must return 0 on B02 |
| **B03** | SOTP monotonicity inversion (ProViz segment_NI 2500 > segment_GP 1960) | `scripts/verify_sotp_monotonicity.py` | G3 | C | All other 13 scripts must return 0 on B03 |
| **B04** | Scenario probabilities sum to 0.95 not 1.00 (base probability reduced 0.50 → 0.45) | `scripts/verify_scenario_weights.py` | G4 | C | All other 13 scripts must return 0 on B04 |
| **B05** | Bear bridge sum mismatch (Clean 1 Blackwell ASP haircut delta_eps corrupted -0.30 → -0.10; bridge total -0.80 ≠ expected -1.00) | `scripts/verify_bear_bridge.py` | G5 | C | All other 13 scripts must return 0 on B05 |
| **B06** | Source tag missing at first appearance in clean.md ("$130B in FY25 revenue" stripped of `(S1: NVDA FY25 10-K Item 7 MD&A)` tag) | `scripts/verify_source_tags.py` | G6 | C | All other 13 scripts must return 0 on B06 |
| **B07** | Headline conditionality mismatch — JSON `conditionality="unconditional"` but top-3 anchor A3 is S3; clean.md headline stripped of "Source-conditional" / "conditional on" / "if … downgrade" language | `scripts/verify_headline_conditionality.py` | G7 | C | All other 13 scripts must return 0 on B07 |
| **B08** | GM taxonomy box missing (`gm_taxonomy.entries = []`) | `scripts/verify_gm_taxonomy.py` | G8 | C | All other 13 scripts must return 0 on B08 |
| **B09** | what_would_reverse trigger 0 has handwave numerical_threshold ("if hyperscaler capex weakens materially" — no digit) | `scripts/verify_what_would_reverse.py` | G9 | C | All other 13 scripts must return 0 on B09 |
| **B10** | weighting_sensitivity block deleted from scenarios_inline | `scripts/verify_weighting_sensitivity.py` | G10 | C | All other 13 scripts must return 0 on B10 |
| **B11** | Non-GAAP/GAAP reconciliation flagged absent — `forensic_flags.non_gaap_reconciliation_present=false`; clean.md §6.0 GAAP/non-GAAP parallel paragraph removed; §12 forensic checklist line changed | `scripts/verify_non_gaap.py` | G11 | D | All other 13 scripts must return 0 on B11 |
| **B12** | FCF SBC-addback silent — `financials.ltm.fcf_includes_sbc_addback=true` while `forensic_flags.fcf_definition="OCF_minus_capex"` (declaration conflicts with addback flag; no B12 forensic red flag carried) | `scripts/verify_fcf_definition.py` | G12 | D | All other 13 scripts must return 0 on B12 |
| **B13** | Factor exposure incomplete — `quant_overlay.factor_tags` keeps only value/quality/momentum; growth, size, low_vol, liquidity (4 of 7 required factors) absent | `scripts/verify_quant_overlay.py` | G13 | D | All other 13 scripts must return 0 on B13 |
| **B14** | Capacity check absent — `quant_overlay.capacity.days_to_exit_10pct_participation` field removed | `scripts/verify_quant_overlay.py` | G14 | D | All other 13 scripts must return 0 on B14 |

## Per-script test invariant

Each verification script S-C-N (N ∈ {1..10}) and S-D-N (N ∈ {2..4}) MUST satisfy:

1. **Returns exit code 0 on `clean.json` / `clean.md`** — the clean fixture has all gates passing.
2. **Returns non-zero exit code on its owned fixture** (e.g., `verify_eps_pe.py` returns non-zero on `bugs/B01.json`).
3. **Returns exit code 0 on all 13 other bug fixtures** — no cross-sensitivity. (`verify_eps_pe.py` is silent on B02 through B14.)

This isolation is the only design that proves "S-C-3 detects B3 and only B3," giving the orchestrator a clean test matrix.

## File mapping (input layer per bug)

| Bug | clean.json | bugs/B0N.json | clean.md | bugs/B0N.md |
|-----|------------|---------------|----------|-------------|
| B01 | clean | **corrupted** | clean | clean (copy) |
| B02 | clean | **corrupted** | clean | clean (copy) |
| B03 | clean | **corrupted** | clean | clean (copy) |
| B04 | clean | **corrupted** | clean | clean (copy) |
| B05 | clean | **corrupted** | clean | clean (copy) |
| B06 | clean | clean (copy) | clean | **corrupted** |
| B07 | clean | **corrupted** | clean | **corrupted** (both layers, consistency-check) |
| B08 | clean | **corrupted** | clean | clean (copy) |
| B09 | clean | **corrupted** | clean | clean (copy) |
| B10 | clean | **corrupted** | clean | clean (copy) |
| B11 | clean | **corrupted** | clean | **corrupted** (both layers, consistency-check) |
| B12 | clean | **corrupted** | clean | clean (copy) |
| B13 | clean | **corrupted** | clean | clean (copy) |
| B14 | clean | **corrupted** | clean | clean (copy) |

JSON-only bugs: B01, B02, B03, B04, B05, B08, B09, B10, B12, B13, B14 (11 of 14).
MD-only bug: B06 (1 of 14).
Both-layer bugs: B07, B11 (2 of 14) — these test cross-layer consistency between structured JSON and rendered Markdown.

## Phase ownership

- **Phase C (S-C-1 through S-C-10)**: own B01-B10, gates G1-G10.
- **Phase D (S-D-2 through S-D-4)**: own B11-B14, gates G11-G14. (Note S-D-4 owns both G13 and G14 via a single `verify_quant_overlay.py` per file-ownership.md.)

## Verification script invocation contract

Each verification script accepts:
- `--memo-json <path>` for the structured JSON (clean.json or bugs/B0N.json)
- `--memo-md <path>` for the rendered Markdown (clean.md or bugs/B0N.md)

Both paths must be provided in every invocation; scripts can opt to read only one layer if their gate is structurally JSON-only or Markdown-only, but the calling contract is uniform.

Exit codes:
- `0` — gate passes
- non-zero — gate fails (script prints structured error matching `schemas/verification_gates.json` `evidence` block)

stdout structure when failing should include:
```
gate_id: G<N>
status: fail
failure_reason: <specific>
remediation_required: <file:section pointer>
```
