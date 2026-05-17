# NVDA v0 — Per-Bug Corruption Documentation

Narrative documentation of each single-fault bug fixture. Per-bug section format:
- The specific corruption (exact field path / before-value / after-value)
- Why this triggers gate G0N
- Why this does NOT trigger any other gate (cross-sensitivity rationale)
- Expected error message from the owning script

All 14 bug fixtures have been verified to fire only their owned gate using a baseline gate-evaluator script (run during S-C-11's build; results: 14/14 owned-gate fires only, 0/14 cross-sensitivity bleed).

---

## B01 — G1 EPS × Multiple multiplicativity

**Corruption**: 
- Path: `scenarios_inline.scenarios[id="base"].target_price`
- Before: `190.00` (= EPS 5.00 × multiple 38.0)
- After: `200.00` (now disagrees with `eps × multiple = 190.00` by >0.5%)

**Why triggers G1**: G1 verifies that for every scenario row, `EPS × multiple = target_price` within ±0.5%. The base row in B01 has 5.00 × 38.0 = 190.00 ≠ 200.00, a 5.26% delta — well above the 0.5% tolerance.

**Why NOT other gates**:
- G2 (segment GM reconcile): segment GMs unchanged, weighted avg still ≈74.88% within 50bp of consolidated 75.0%.
- G3 (SOTP monotonicity): SOTP segments unchanged.
- G4 (scenario weights): probabilities sum unchanged at 1.00.
- G5 (bear bridge sum): bridge deltas unchanged; bear/strong_bear bridges still sum to expected delta.
- G6 (source tags): MD unchanged.
- G7 (headline conditionality): JSON conditionality field unchanged at "source_conditional"; markdown headline unchanged.
- G8-G14: orthogonal sections, unchanged.

**Expected error from `verify_eps_pe.py`**:
```
gate_id: G1
status: fail
failure_reason: Scenario "base" target_price=200.00 disagrees with EPS×multiple=190.00 by 5.263% (tolerance ±0.5%)
remediation_required: scenarios_inline.scenarios[id=base].target_price OR eps/multiple
```

---

## B02 — G2 Segment GM reconciliation

**Corruption**:
- Path: `financials.ltm.segments[name="Datacenter"].gm_pct`
- Before: `76.5` (weighted GM 74.88%, delta to consolidated 12bp)
- After: `80.0` (weighted GM 78.02%, delta to consolidated 302bp — way above 50bp threshold)

**Why triggers G2**: G2 computes `Σ(segment_revenue × segment_GM) / Σ(segment_revenue)` and verifies it's within ±50bp of `gross_margin_pct`. With DC GM corrupted to 80.0%, the segment-implied consolidated GM becomes 78.02% vs reported 75.0% — 302bp delta.

**Why NOT other gates**:
- G1: scenario rows unchanged.
- G3: SOTP method's key_assumptions are decoupled from `financials.ltm.segments` — SOTP segments live in `valuation.methods[SOTP].key_assumptions` and they still satisfy monotonicity.
- G5: bear bridge JSON unchanged.
- G6/G7: source tag and headline structure unchanged.
- G8: gm_taxonomy entries unchanged.
- G9-G14: orthogonal.

**Expected error from `verify_segment_gm.py`**:
```
gate_id: G2
status: fail
failure_reason: Segment-weighted GM 78.02% diverges from consolidated GM 75.00% by 302bp (tolerance ±50bp)
remediation_required: financials.ltm.segments[].gm_pct OR financials.ltm.gross_margin_pct
```

---

## B03 — G3 SOTP monotonicity

**Corruption**:
- Path: `valuation.methods[method="SOTP"].key_assumptions.ProViz_segment.segment_ni_usd_m_fy27e`
- Before: `1100` (NI 1100 ≤ OP 1400 ≤ GP 1960 ≤ Revenue 2800 — monotonic)
- After: `2500` (NI 2500 > GP 1960 — inversion violates accounting identity)

**Why triggers G3**: G3 verifies for every SOTP segment that `NI ≤ OP ≤ GP ≤ Revenue`. The ProViz segment now has NI > GP, which is impossible by accounting identity.

**Why NOT other gates**:
- G1: scenario rows untouched.
- G2: `financials.ltm.segments` independent from valuation.methods.SOTP — segment GMs/revenue intact.
- G4-G14: orthogonal.

**Expected error from `verify_sotp_monotonicity.py`**:
```
gate_id: G3
status: fail
failure_reason: SOTP segment "ProViz" violates monotonicity: NI=$2,500M > GP=$1,960M
remediation_required: valuation.methods[SOTP].key_assumptions.ProViz_segment
```

---

## B04 — G4 Scenario weights

**Corruption**:
- Path: `scenarios_inline.scenarios[id="base"].probability`
- Before: `0.50` (sum: 0.05+0.20+0.50+0.20+0.05 = 1.00)
- After: `0.45` (sum: 0.05+0.20+0.45+0.20+0.05 = 0.95)

**Why triggers G4**: G4 verifies `Σ(probability) = 1.00 ± 0.01`. With base reduced to 0.45, sum = 0.95, delta 0.05 from 1.00 — exceeds 0.01 tolerance.

**Why NOT other gates**:
- G1: target_prices = eps × multiple still hold per scenario row.
- G2/G3/G5/G6/G7/G8/G9/G10/G11/G12/G13/G14: orthogonal sections untouched.

**Expected error from `verify_scenario_weights.py`**:
```
gate_id: G4
status: fail
failure_reason: Scenario probabilities sum to 0.95, expected 1.00 ± 0.01 (delta 0.05)
remediation_required: scenarios_inline.scenarios[].probability
```

---

## B05 — G5 Bear bridge sum

**Corruption**:
- Path: `scenarios_inline.scenarios[id="bear"].eps_bridge[label contains "Blackwell ASP haircut"].delta_eps`
- Before: `-0.30` (bear bridge total: -0.20 + -0.30 + -0.30 + -0.20 = -1.00; matches base_eps 5.00 - bear_eps 4.00)
- After: `-0.10` (bear bridge total: -0.20 + -0.30 + -0.10 + -0.20 = -0.80; mismatch vs expected -1.00)

**Why triggers G5**: G5 verifies for every non-base scenario that `Σ(bridge.delta_eps) = scenario.eps - base_eps` within rounding. Bear bridge now sums to -0.80 but expected is -1.00 (5.00 → 4.00).

**Why NOT other gates**:
- G1: bear target_price = 4.00 × 30 = 120 still verifies; the corrupted field is in the *bridge*, not in eps/multiple/target_price.
- G2/G3/G4/G6-G14: orthogonal sections unchanged.

**Expected error from `verify_bear_bridge.py`**:
```
gate_id: G5
status: fail
failure_reason: Scenario "bear" bridge deltas sum to -0.80, expected -1.00 (= scenario.eps 4.00 - base_eps 5.00) within ±0.05
remediation_required: scenarios_inline.scenarios[id=bear].eps_bridge[]
```

---

## B06 — G6 Source tag missing at first appearance

**Corruption**: Markdown layer only.
- File: `clean.md` (B06.md variant)
- Before: `"approximately $130B in FY25 revenue (S1: NVDA FY25 10-K Item 7 MD&A)"`
- After: `"approximately $130B in FY25 revenue"` (S-tag stripped at first appearance)

`clean.json` is unchanged (`B06.json == clean.json`).

**Why triggers G6**: G6 regex-scans the Markdown for specific numbers ($X B, X%, $X M, etc.) and verifies each first-appearance specific carries one of `(S1|S2|S3|S4|S5|Pending: ...)`. The `$130B` specific in §3 is now untagged at first appearance.

**Why NOT other gates**:
- G1-G5: JSON unchanged, math gates pass.
- G7: headline structure (including its citation) intact.
- G8-G14: orthogonal sections unchanged.

**Expected error from `verify_source_tags.py`**:
```
gate_id: G6
status: fail
failure_reason: Specific number "$130B" appears without S-tag citation at first appearance in clean.md §3 line ~3
remediation_required: clean.md §3 line ~3 — add (S1: NVDA FY25 10-K Item 7 MD&A) after "$130B in FY25 revenue"
```

---

## B07 — G7 Headline conditionality mismatch (cross-layer)

**Corruption**: BOTH JSON and MD layers.

JSON changes:
- `scenarios_inline.headline.conditionality`: `"source_conditional"` → `"unconditional"`
- `scenarios_inline.headline.conditional_language_pattern`: `"A_source_conditional_bias"` → `"none"`
- `scenarios_inline.headline.headline_text`: stripped of conditional language
- `source_tags_inline.headline_conditionality`: `"source_conditional"` → `"unconditional"`
- `headline.conditionality`: `"source_conditional"` → `"unconditional"`
- `recommendation.conviction_tag`: `"source_conditional"` → `"moderate_conviction"`

MD changes (clean.md):
- Headline §1 paragraph rewritten without "Source-conditional", "conditional on", "if [trigger] downgrade".
- §1 conviction-tag line changed.
- §2 HEADLINE CONDITIONALITY line changed from `source_conditional` to `unconditional`.

Top-3 anchors (A1 S1, A2 S5, A3 S3) are UNCHANGED — so the JSON inconsistently claims `unconditional` while still anchoring on an S3.

**Why triggers G7**: G7 cross-checks `headline.conditionality` against the top-3 anchors' S-levels. Rule: any top-3 anchor of S3 or weaker requires `source_conditional` headline. Here A3 is S3 but headline claims `unconditional` — G7 fail. G7 also cross-checks the Markdown headline language for one of patterns A-D against the structured field; B07 strips conditional language while top-3 still has S3.

**Why NOT other gates**:
- G1-G5: math fields unchanged, all pass.
- G6: source tags at first appearance still present (only headline *language* changed, not citation tags).
- G8-G14: orthogonal sections unchanged.

**Expected error from `verify_headline_conditionality.py`**:
```
gate_id: G7
status: fail
failure_reason: headline.conditionality="unconditional" but top-3 anchors include S3 anchor A3 (Blackwell ASP). Required: "source_conditional" with Pattern A/B/C language.
remediation_required: scenarios_inline.headline + clean.md §1 — restore Pattern A source-conditional language and conditionality="source_conditional"
```

---

## B08 — G8 GM taxonomy box missing

**Corruption**:
- Path: `gm_taxonomy.entries`
- Before: 5 entries spanning T1_consolidated, T2_segment, T3_sub_segment, T4_analyst_modeled, T5_marginal
- After: `[]` (empty array)

**Why triggers G8**: G8 verifies that `gm_taxonomy.entries` is non-empty AND contains explicit taxonomy types. Empty array fails.

**Why NOT other gates**:
- G2 (segment GM reconcile) uses `financials.ltm.segments[].gm_pct` and `financials.ltm.gross_margin_pct` — these are decoupled from `gm_taxonomy.entries`. G2 still passes.
- G1, G3-G7, G9-G14: orthogonal.

**Expected error from `verify_gm_taxonomy.py`**:
```
gate_id: G8
status: fail
failure_reason: gm_taxonomy.entries is empty; required: at least 1 entry covering T1-T5 types
remediation_required: gm_taxonomy.entries[] — populate per `references/gm-taxonomy-us.md`
```

---

## B09 — G9 What-would-reverse missing numerical denominator

**Corruption**:
- Path: `what_would_reverse[0].numerical_threshold` and `[0].unit`
- Before: `"Hyperscaler aggregate CY26 capex YoY growth <+10% confirmed by MSFT/GOOG/META/AMZN FY26Q2 prints"`, unit `"%"`
- After: `"if hyperscaler capex weakens materially"`, unit `""` (no number, no denominator)

**Why triggers G9**: G9 verifies each `what_would_reverse[]` entry has a `numerical_threshold` that contains at least one digit AND a populated `unit` field. The handwave phrase "weakens materially" contains no digit.

**Why NOT other gates**:
- G1-G8: orthogonal sections unchanged.
- G10-G14: orthogonal.

**Expected error from `verify_what_would_reverse.py`**:
```
gate_id: G9
status: fail
failure_reason: what_would_reverse[0].numerical_threshold "if hyperscaler capex weakens materially" lacks numerical denominator (no digit found)
remediation_required: what_would_reverse[0].numerical_threshold + .unit — rewrite with explicit number and denominator base per `references/what-would-reverse-us.md`
```

---

## B10 — G10 weighting_sensitivity missing

**Corruption**:
- Path: `scenarios_inline.weighting_sensitivity`
- Before: present (with base_minus_10_to_bear, base_minus_10_to_bull, strong_tail_plus_10 keys)
- After: deleted (key absent)

**Why triggers G10**: G10 verifies the `weighting_sensitivity` block exists on the scenarios JSON. Absence fails.

**Why NOT other gates**:
- G1-G9: orthogonal sections unchanged.
- G11-G14: orthogonal.

**Expected error from `verify_weighting_sensitivity.py`**:
```
gate_id: G10
status: fail
failure_reason: scenarios_inline.weighting_sensitivity block is missing; required for anchor weighting impact table per references/five-scenario-framework-us.md §5.2
remediation_required: scenarios_inline.weighting_sensitivity — populate with base±10pp shift impacts
```

---

## B11 — G11 Non-GAAP/GAAP reconciliation absent (cross-layer)

**Corruption**: BOTH JSON and MD layers.

JSON:
- `forensic_flags.non_gaap_reconciliation_present`: `true` → `false`

MD (clean.md §6.0 GAAP/non-GAAP parallel paragraph and §12 forensic line):
- Before (§6.0): `"GAAP/non-GAAP parallel: T1 non-GAAP 75.0%; T1 GAAP equivalent 74.5% per S2 FY26Q1 10-Q reconciliation table (B11 forensic discipline). Delta primarily driven by SBC + acquired intangible amortization (~50bp)."`
- After (§6.0): `"All GM references are non-GAAP. Non-GAAP EPS FY27E $5.00 is the headline base case figure."` (no GAAP counterpart shown)
- Before (§12): `"- Non-GAAP/GAAP reconciliation: present (S2: NVDA FY26Q1 10-Q Item 2 MD&A reconciliation table). Delta ~50bp on EBIT margin, ~$0.24/share on EPS."`
- After (§12): `"- Non-GAAP/GAAP reconciliation: not separately disclosed in this fixture."`

**Why triggers G11**: G11 verifies that whenever a non-GAAP number is cited in memo, an adjacent GAAP reconciliation is shown. With the parallel paragraph removed AND `non_gaap_reconciliation_present=false`, both layers consistently signal absence.

**Why NOT other gates**:
- G1-G5: math fields unchanged.
- G6: source tags at first appearance still present.
- G7: headline conditionality unchanged.
- G8: gm_taxonomy.entries intact (T1/T2 still listed).
- G9-G10: scenario block unchanged.
- G12-G14: orthogonal.

**Expected error from `verify_non_gaap.py`**:
```
gate_id: G11
status: fail
failure_reason: forensic_flags.non_gaap_reconciliation_present=false AND non-GAAP EPS $5.00 cited in clean.md §1 / §6.0 without adjacent GAAP reconciliation table
remediation_required: clean.md §6.0 — restore GAAP/non-GAAP parallel paragraph; forensic_flags.non_gaap_reconciliation_present → true
```

---

## B12 — G12 FCF SBC-addback silent

**Corruption**:
- Path: `financials.ltm.fcf_includes_sbc_addback`
- Before: `false` (SBC deducted from FCF; clean disclosure)
- After: `true` (SBC added back to FCF — dilution masked)

AND `forensic_flags.fcf_definition` remains `"OCF_minus_capex"` (which is INCONSISTENT with `fcf_includes_sbc_addback=true`, since adding back SBC would imply `OCF_minus_capex_minus_sbc` is the deducted base; an `OCF_minus_capex` definition with SBC addback flag = silently masking dilution).

**Why triggers G12**: G12 detects unflagged SBC addbacks. Logic: if `ltm.fcf_includes_sbc_addback=true`, the forensic_flags must declare `fcf_definition="OCF_minus_capex_minus_sbc"` OR carry an explicit B12-class red flag. Neither is present in B12.

**Why NOT other gates**:
- G1-G10: orthogonal.
- G11: `non_gaap_reconciliation_present` still `true`; non-GAAP reconciliation parallel paragraph in §6.0 intact.
- G13-G14: quant_overlay unchanged.

**Expected error from `verify_fcf_definition.py`**:
```
gate_id: G12
status: fail
failure_reason: financials.ltm.fcf_includes_sbc_addback=true but forensic_flags.fcf_definition="OCF_minus_capex" (inconsistent — should be "OCF_minus_capex_minus_sbc" or carry explicit B12 red flag)
remediation_required: financials.ltm.fcf_includes_sbc_addback OR forensic_flags.fcf_definition — align disclosure per references/forensic-accounting-checklist-us.md B12
```

---

## B13 — G13 Factor exposure missing required factors

**Corruption**:
- Path: `quant_overlay.factor_tags`
- Before: all 7 factors present (value, quality, momentum, growth, size, low_vol, liquidity)
- After: only 3 present (value, quality, momentum) — 4 missing (growth, size, low_vol, liquidity)

**Why triggers G13**: G13 requires all 7 Barra-style factor tags. 4 of 7 missing = G13 fail.

**Why NOT other gates**:
- G1-G12: orthogonal sections unchanged.
- G14: `quant_overlay.capacity` block still intact with all required fields including `days_to_exit_10pct_participation`.

**Expected error from `verify_quant_overlay.py`** (G13 check path):
```
gate_id: G13
status: fail
failure_reason: quant_overlay.factor_tags missing 4 of 7 required factors: growth, size, low_vol, liquidity
remediation_required: quant_overlay.factor_tags — populate all 7 Barra-style z-scores per schemas/memo.json
```

---

## B14 — G14 Capacity check missing days-to-exit

**Corruption**:
- Path: `quant_overlay.capacity.days_to_exit_10pct_participation`
- Before: `0.5` (present, days-to-exit at 10% participation)
- After: field absent (deleted from JSON)

**Why triggers G14**: G14 requires `quant_overlay.capacity` block to include `adv_30d_usd_m`, `days_to_exit_10pct_participation`, and at least one further participation tier (20pct or 30pct). Removing `days_to_exit_10pct_participation` fails the required-fields check.

**Why NOT other gates**:
- G1-G12: orthogonal.
- G13: `factor_tags` block intact, all 7 factors present.

**Expected error from `verify_quant_overlay.py`** (G14 check path):
```
gate_id: G14
status: fail
failure_reason: quant_overlay.capacity missing required field "days_to_exit_10pct_participation"
remediation_required: quant_overlay.capacity — populate days-to-exit at 10% participation against 30-day ADV per schemas/memo.json
```

---

## Cross-sensitivity validation summary

A baseline gate-evaluator was run during S-C-11 build with the following result matrix (rows = bug fixture, columns = which gates the fixture triggers; expected: exactly the diagonal):

```
           G1  G2  G3  G4  G5  G6  G7  G8  G9  G10 G11 G12 G13 G14
clean      .   .   .   .   .   .   .   .   .   .   .   .   .   .
B01        X   .   .   .   .   .   .   .   .   .   .   .   .   .   ✓ (G1 only)
B02        .   X   .   .   .   .   .   .   .   .   .   .   .   .   ✓ (G2 only)
B03        .   .   X   .   .   .   .   .   .   .   .   .   .   .   ✓ (G3 only)
B04        .   .   .   X   .   .   .   .   .   .   .   .   .   .   ✓ (G4 only)
B05        .   .   .   .   X   .   .   .   .   .   .   .   .   .   ✓ (G5 only)
B06        .   .   .   .   .   X   .   .   .   .   .   .   .   .   ✓ (G6 only — MD layer)
B07        .   .   .   .   .   .   X   .   .   .   .   .   .   .   ✓ (G7 only — both layers)
B08        .   .   .   .   .   .   .   X   .   .   .   .   .   .   ✓ (G8 only)
B09        .   .   .   .   .   .   .   .   X   .   .   .   .   .   ✓ (G9 only)
B10        .   .   .   .   .   .   .   .   .   X   .   .   .   .   ✓ (G10 only)
B11        .   .   .   .   .   .   .   .   .   .   X   .   .   .   ✓ (G11 only — both layers)
B12        .   .   .   .   .   .   .   .   .   .   .   X   .   .   ✓ (G12 only)
B13        .   .   .   .   .   .   .   .   .   .   .   .   X   .   ✓ (G13 only)
B14        .   .   .   .   .   .   .   .   .   .   .   .   .   X   ✓ (G14 only)
```

Status: clean fires no gates; each B0N fires exactly its owned gate. Single-fault isolation verified.

## Notes for verification-script authors (S-C-1 through S-D-4)

When implementing your verification script, you can use these fixtures as a unit-test contract:

```python
# pseudocode template
import subprocess

def test_verify_script(script_name, owned_bug_num):
    # 1. Should return 0 on clean
    rc = subprocess.run([script_name, "--memo-json", "clean.json", "--memo-md", "clean.md"]).returncode
    assert rc == 0, f"{script_name} failed on clean"
    
    # 2. Should return non-zero on its owned bug
    rc = subprocess.run([script_name, "--memo-json", f"bugs/B{owned_bug_num:02d}.json", "--memo-md", f"bugs/B{owned_bug_num:02d}.md"]).returncode
    assert rc != 0, f"{script_name} did not detect its owned bug B{owned_bug_num:02d}"
    
    # 3. Should return 0 on all 13 other bugs (cross-sensitivity check)
    for n in range(1, 15):
        if n == owned_bug_num:
            continue
        rc = subprocess.run([script_name, "--memo-json", f"bugs/B{n:02d}.json", "--memo-md", f"bugs/B{n:02d}.md"]).returncode
        assert rc == 0, f"{script_name} incorrectly fired on B{n:02d} (cross-sensitivity)"
```

The orchestrator's Phase C / Phase D acceptance criterion is: this 14×14 cross-sensitivity matrix produces exactly the diagonal.
