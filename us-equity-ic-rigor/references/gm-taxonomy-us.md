# GM taxonomy — five distinct gross margin concepts (US)

## The problem this solves

In a single memo about NVDA, you might see "GM 70-75%", "GM 78%", "GM 60-65%", "GM 50-55%" all appear within three pages. The PM reads this and concludes one of two things: either you're contradicting yourself, or you're sloppy. Both kill the memo.

The reality is that those numbers reference four different concepts pointing to four different cuts of the same business: consolidated GAAP, consolidated non-GAAP, Datacenter segment GM (T2), and Hopper SKU-mix sub-segment GM within Datacenter (T3). The fix is not to pick one — it's to label them rigorously. This file specifies the five distinct GM concepts you'll encounter in any US filer, the discipline for using them in a single doc, the **mandatory GM taxonomy box** (G8 gate), and the US-specific addition: **non-GAAP vs GAAP parallel discipline**.

## The 5 GM types (matches `schemas/memo.json` `gm_taxonomy_type` enum)

### Type 1: Consolidated GM (T1_consolidated)

- **Definition**: company-level total GP / total revenue, as reported on the income statement.
- **Source**: S1 (10-K) for annual; S2 (10-Q) for quarterly. For ADRs / FPIs, S1 from 20-F.
- **Use**: highest-level aggregate metric, useful for trend tracking and peer comparison at the company level.
- **Example (NVDA)**: FY24 consolidated GAAP GM = 72.7%; FY24 consolidated non-GAAP GM = 73.6%; FY25E consolidated GAAP GM range 73-75%.
- **Characteristic**: a single number. It does not tell you which segment is driving margin and which is dragging.

### Type 2: Segment GM (T2_segment)

- **Definition**: per-business-segment GP / segment revenue, as reported in segment notes.
- **Source**: S1 (10-K Note on Segments — most US filers comply with ASC 280 segment reporting); S2 (10-Q) if disclosed. Some companies disclose only revenue by segment and not GP — flag and downgrade S-level accordingly.
- **Use**: shows which segment is contributing margin and which is dragging.
- **Example (NVDA, FY24 10-K Note 17 "Segment Information")**:
  - Datacenter segment GM ≈ 75-78%
  - Gaming segment GM ≈ 60-65%
  - Professional Visualization segment GM ≈ 65-70%
  - Automotive & Embedded segment GM ≈ 55-60%
- **Critical constraint (G2 gate)**: **Σ(segment_revenue × segment_GM) / Σ(segment_revenue) must equal Type 1 consolidated GM within ±50bp**. If not, either segment data is incomplete, periods are mismatched, or you've mixed sources/cuts. Add an "Other / Unallocated" row OR fix the segment assumption.

### Type 3: Sub-segment / product-line GM (T3_sub_segment)

- **Definition**: GM of a specific product line within a segment. Companies rarely disclose formally; more often from IR commentary, sell-side product-line decomposition, or third-party industry trackers.
- **Source**: S3 (IR / earnings call), S4 (sell-side analyst decomp like Visible Alpha line items), S5 (industry tracker like Omdia, Counterpoint, IDC).
- **Use**: explains intra-segment mix shift; helps separate cyclical vs structural margin moves.
- **Example (NVDA Datacenter segment, FY24)**:
  - Hopper (H100/H200) SKU GM ≈ 78-80% (S3 inference + S5 supply-chain margin tracker)
  - Blackwell (B200/B300) GM at full ramp ≈ 75-78% (S4 sell-side modeled)
  - Networking (Spectrum-X, NVLink switches) GM ≈ 65-70%
  - DGX systems GM ≈ 55-60% (lower because of bundled hardware)
- **Critical constraint**: use for explaining mix shift; do NOT show T3 sub-segment numbers to the reader without anchoring them to the parent T2 segment. Otherwise the reader sees "GM 78%" and "GM 60%" in the same paragraph and assumes contradiction.

### Type 4: Analyst-modeled GM (T4_analyst_modeled)

- **Definition**: forward-period GM assumption that you or sell-side analysts produce in a forward model. Can sit at consolidated, segment, or sub-segment level.
- **Source**: S4 (sell-side consensus via Visible Alpha / FactSet / Bloomberg or free aggregator like Yahoo Finance) OR self-modeled (no S-tier — disclose as own assumption).
- **Use**: input parameters for EPS bridge and scenario table.
- **Example**: Our FY27E NVDA Datacenter segment GM assumption = 73% base / 76% bull / 69% bear / 65% strong_bear. Visible Alpha consensus FY27E NVDA consolidated GM = 71-74% (n=42 analysts).
- **Critical constraint**: must be explicitly tagged as **"modeled"** or **"forecast"** or **"E"** suffix on the period. Never use a forward GM in the same sentence as a historical GM without flagging. Wording: "FY24 GM was 72.7% (T1); our FY27E modeled assumption is 73% (T4)."

### Type 5: Marginal GM (T5_marginal)

- **Definition**: GM on the *incremental* revenue dollar — what GM the next unit of revenue earns. Almost always a derivation, never a reported number.
- **Source**: derivation (combine S3 IR commentary on operating leverage + S5 supply chain tracker + internal assumption). Always **S5-tagged with explicit derivation path** when used.
- **Use**: explains why consolidated GM trend moves direction-consistent with revenue mix change; sizing operating leverage.
- **Example (NVDA Blackwell at full ramp)**:
  - Blackwell marginal GM ≈ 78-82% (well above current T1 consolidated 73%)
  - Derivation path: ASP per Blackwell unit ($35-45K range, S5 supply chain) − BOM cost ($7-9K, S5 component tracker) − fab + assembly + test (~$2K) − warranty / support reserve (~$1K) → margin ~ 76-80%. Plus packaging and HBM allocation noise.
- **Critical constraint**: **always a derivation; always S5-tagged**; the derivation path must be written down. PM red-team challenges T5 margins because they're modeled, not reported.

## US-specific addition: non-GAAP vs GAAP parallel discipline

Most US companies report **GAAP GM** (as required by Reg G + Item 10(e)) and **non-GAAP GM** (excludes SBC, acquired intangible amortization, restructuring charges, etc.) **separately**. Both belong in the GM taxonomy box as distinct T1 entries, tagged "GAAP" or "non-GAAP" explicitly.

**The non-GAAP / GAAP delta on GM is itself a forensic signal** (G11 hook in `forensic-accounting-checklist-us.md`):

- Small delta (<50bp): non-GAAP adjustments are immaterial. The two metrics carry roughly the same information content.
- Medium delta (50-200bp): SBC and acquired intangibles material. Track whether the gap is growing or shrinking.
- Large delta (>200bp): non-GAAP GM is materially flattering reported economics. Bear scrutiny is warranted — what specifically is being excluded?
- **Growing delta over 3-5 years**: non-GAAP GM trending up while GAAP GM flat or down → SBC compensation is escalating faster than top-line; this is a real cost being whitewashed. Add to bear bridge clean layer.

Format in the GM taxonomy box:

| Type | Name | Value (range) | Source |
|---|---|---|---|
| T1 (GAAP) | Consolidated GAAP GM | 72.7% (FY24) | S1: NVDA FY24 10-K |
| T1 (non-GAAP) | Consolidated non-GAAP GM | 73.6% (FY24) | S1: NVDA FY24 10-K non-GAAP reconciliation table |
| GAAP-to-non-GAAP delta | | 90bp | derived; mostly SBC + acquired intangible amortization |

When citing GM in the memo, **always include the GAAP / non-GAAP qualifier** at first mention. Subsequent uses inherit the qualifier unless explicitly switched.

## The GM taxonomy box (mandatory in §6.0; G8 gate)

```
| Type        | Name                            | Value (range)        | Source                                |
|-------------|---------------------------------|----------------------|---------------------------------------|
| T1 GAAP     | Consolidated GAAP GM            | 72.7% (FY24A)        | S1: NVDA FY24 10-K Item 8 IS          |
| T1 non-GAAP | Consolidated non-GAAP GM        | 73.6% (FY24A)        | S1: NVDA FY24 10-K Reg G recon table   |
| T2          | Datacenter segment GM           | 75-78% (FY24A est)   | S1: NVDA FY24 10-K Note 17 (derived; segment GP not explicit but inferred from segment OP + opex split) |
| T2          | Gaming segment GM               | 60-65% (FY24A est)   | S1: NVDA FY24 10-K Note 17            |
| T2          | ProViz segment GM               | 65-70% (FY24A est)   | S1: NVDA FY24 10-K Note 17            |
| T3          | Hopper SKU GM (within DC)       | 78-80% (FY24 est)    | S3: NVDA FY24Q4 call + S5 supply chain |
| T3          | Blackwell GM (within DC)        | 75-78% modeled       | S4: Visible Alpha consensus + S5      |
| T4          | FY27E modeled consolidated GM   | 73% base / 76% bull / 69% bear / 65% strong_bear | self-modeled forward assumption (T4) |
| T5          | Blackwell marginal GM (full ramp)| 78-82% derived       | derivation: ASP $35-45K − BOM $7-9K − fab/assy/test $2K (S5 supply chain) |
```

Reader sees at a glance: 72.7% is T1 GAAP consolidated; 73.6% is T1 non-GAAP consolidated; 75-78% is T2 Datacenter; 78-80% is T3 Hopper SKU; 78-82% is T5 marginal. No confusion.

## Reconciliation discipline — segment GM weighted check (G2 gate)

Every memo with segment GM (T2) must include a reconciliation table demonstrating that segments tie to the consolidated number within ±50bp:

```
| Segment                  | Revenue $B | Segment GM | Segment GP $B |
|--------------------------|------------|------------|---------------|
| Datacenter               | 47.5       | 77%        | 36.6          |
| Gaming                   | 10.4       | 62%        | 6.4           |
| Professional Visualization| 1.6        | 67%        | 1.1           |
| Automotive & Embedded    | 1.1        | 57%        | 0.6           |
| **Total**                | **60.6**   |            | **44.7**      |
| Implied consolidated GM  |            |            | 44.7/60.6 = 73.8% |
| Company reported (FY24)  |            |            | 72.7% (GAAP)  |
| Difference               |            |            | 110bp — **outside ±50bp tolerance, flagged** |
```

If the difference exceeds ±50bp, one of three things is happening:

1. **Segment data is incomplete** — an unallocated bucket exists (corporate overhead, eliminations, investments). Add an "Other / Corporate / Unallocated" row that absorbs the difference, with a one-line explanation. For NVDA the unallocated is typically stock-based compensation that gets pushed into corporate-allocated opex but is partially in COGS for engineering allocated to product. This brings the 110bp gap into tolerance.
2. **Periods are mismatched** — full-year revenue paired with quarterly or H1-annualized GM for some segments. Fix by aligning fiscal periods.
3. **Sources / cuts are mixed** — e.g., you mixed an S3 IR sub-segment GM (T3) into an S1 segment GM list (T2). Fix by re-checking source levels.

If you can't reconcile within ±50bp without forcing it, **you do not understand segment economics yet**. Stop, re-read the 10-K Segment Note, identify what's missing.

The script `scripts/verify_segment_gm.py` automates this check against `outputs/<ticker>_segments.json`.

## How GM types interact in a memo (narrative sequence)

The typical narrative sequence:

1. **Open with T1** consolidated trend — reader gets aggregate context. Pair GAAP and non-GAAP.
2. **Decompose into T2** segment GM — reader sees mix.
3. **Within the key segment, explain via T3** sub-segment GM — reader sees what's driving (Hopper vs Blackwell mix in NVDA Datacenter; iPhone Pro vs base in Apple Products; AWS vs Ads in AMZN AWS+Ads).
4. **Build forward via T4** modeled assumption — reader sees your scenario inputs.
5. **Stress-test via T5** marginal GM — reader sees operating leverage / mix sensitivity.

Every sentence with a GM number must implicitly tag which type it is at first mention. If the reader has to guess, you have failed. Re-mention with the type tag if you switch types within a paragraph.

## Anti-patterns (these fail PM red-team)

| Anti-pattern | Why wrong | Fix |
|---|---|---|
| "GM 70-75%" without specifying which layer | reader can't tell if T1, T2, or T3 | "Datacenter segment GM (T2) 75-78%" |
| Mixing GAAP and non-GAAP without flagging | apples to oranges | always qualify "GAAP" or "non-GAAP" at first mention |
| Quoting T3 sub-segment GM without showing it sums consistent with T2 | partial picture, may mislead | always pair T3 with the T2 segment it sits within |
| Using T4 forward GM in same sentence as T1 historical without flagging | reader can't tell what's reported vs assumed | "FY24 GAAP GM 72.7% (T1); we model FY27E (T4) at 73%" |
| T5 marginal GM presented without derivation | unverifiable | "Blackwell marginal GM ~78-82% derived from ASP $35-45K − BOM $7-9K − fab+assy+test $2K (S5 supply chain tracker)" |
| Segment GM × revenue weighted ≠ consolidated, no explanation (G2 fail) | broken reconciliation | add "Other / Unallocated" row OR fix the assumption |
| No GM taxonomy box at all (G8 fail) | reader cannot navigate which number is which | insert §6.0 box per the template above |
| Non-GAAP GM cited in headline thesis without GAAP counterpart (G11 fail) | hiding real economics | always show both; flag the delta |

## Worked example: NVDA Round 1 GM taxonomy gap

Before fix, the memo had:
- "GM 70-75%" (intended: T1 consolidated FY25E, vague)
- "GM 78%" (intended: T2 Datacenter segment FY24, no tag)
- "GM 60-65%" (intended: T2 Gaming segment FY24, no tag)
- "Blackwell marginal GM 78-82%" (T5, but reader doesn't know it's a derivation)

PM challenge: "What's the actual consolidated GM? You're saying 70-75%, 78%, 60-65%, and 78-82% in the same memo. Are these the same metric? What's the GAAP versus non-GAAP split? And how did you get 78-82% — is that what the company reports?"

Fix: insert §6.0 GM taxonomy box (the table above), explicitly distinguish GAAP/non-GAAP at T1, tag every GM mention in the memo body with its type at first appearance, and add the derivation path for T5. Round 1 score moved 7.6 → 8.2.

A separate but adjacent fix: the segment GM × revenue weighted reconciliation came in 110bp off consolidated. We added the "Other / Unallocated" row (mostly SBC allocated to corporate but partially in COGS — ASC 718 mechanics), explained it, brought the reconciliation into ±50bp tolerance. That alone moved 8.2 → 8.5.

These two fixes — taxonomy box + segment reconciliation — are the canonical first-round pattern for any multi-segment US filer. Banks, REITs, conglomerates, multi-product tech all benefit from the same discipline.

## How this file ties into the rest of the rigor batch

- The T2 segment GM declared here is the source of truth used in `three-method-valuation-us.md` SOTP rows.
- T4 modeled GM values feed the scenario EPS bridge in `bear-bridge-us.md`.
- T1 GAAP / non-GAAP delta hooks into `forensic-accounting-checklist-us.md` (B11 / G11).
- Source tags for T3 / T5 GM follow `source-stratification-us.md` conventions.
- Verification gate G2 (segment reconciliation) and G8 (taxonomy box exists) are scored by `pm-redteam-rubric-us.md`.
- T5 marginal GM derivations cite supply chain and industry trackers per `us-data-sources.md` Tier S5.
