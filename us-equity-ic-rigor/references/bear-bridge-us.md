# Bear EPS bridge — three-layer construction (US)

## What this solves

PMs do not believe a bear EPS unless they can see, line by line, which assumption did the work. "Bear EPS $2.40 because conditions are bad" is not a bear case — it is an opinion. A bear bridge starts at consensus or base EPS, applies a series of **named, quantified adjustments**, and lands on the bear number. The reader can disagree with any single adjustment and redo the math.

The three-layer structure (**soft / clean / strong**) lets the reader see the conviction gradient. Soft = adjustments most market participants would accept. Clean = adjustments only a few participants make. Strong = adjustments unique to your bear thesis. Each layer maps to a probability weighting in the 5-scenario distribution.

The G5 verification gate (`scripts/verify_bear_bridge.py`) checks that the sum of named adjustments equals (base_eps − scenario_eps) within rounding.

## Required structure

The bear bridge is a row-form table. Every row carries a label, layer tag, EPS impact, cumulative running total, and source tag.

```
| Adjustment                                          | Layer  | EPS impact | Cumulative EPS | Source / anchor                |
|-----------------------------------------------------|--------|------------|----------------|--------------------------------|
| Base / consensus EPS (FY27E)                        | —      | —          | 4.80           | S4: Visible Alpha n=42 median  |
| Soft 1: SBC headwind (3.5% of revenue, growing)     | Soft   | -0.20      | 4.60           | S1: NVDA FY24 10-K ASC 718     |
| Soft 2: cycle-trough GM compression −200bp          | Soft   | -0.40      | 4.20           | S2: NVDA FY24Q3 10-Q trend     |
| Soft cumulative                                     |        | **-0.60**  | **4.20**       |                                |
| Clean 1: Blackwell ASP haircut -10%                 | Clean  | -0.30      | 3.90           | S3: NVDA FY24Q4 call + S5 chain |
| Clean 2: hyperscaler DC capex flat YoY              | Clean  | -0.20      | 3.70           | S5: Counterpoint capex tracker  |
| Clean 3: §174 R&D capitalization headwind (+50bp tax)| Clean | -0.10      | 3.60           | S1: NVDA FY24 10-K tax note    |
| Clean cumulative                                    |        | **-0.60**  | **3.60**       |                                |
| Strong 1: AMD MI400 share to 12% (from 8%)          | Strong | -0.40      | 3.20           | S5: hyperscaler RFP signals    |
| Strong 2: customer concentration risk (top-4 50%)   | Strong | -0.20      | 3.00           | S2: 10-K segment + S3 IR       |
| Strong 3: export control re-tightens China DC rev    | Strong | -0.40      | 2.60           | S5 + macro tail event          |
| Strong 4: SBC % rev step-up under cycle             | Strong | -0.20      | 2.40           | derived from S1 SBC trend       |
| Strong cumulative                                   |        | **-1.20**  | **2.40**       |                                |
| **Strong_bear EPS**                                 |        |            | **2.40**       |                                |
| **Mid-bear EPS (soft + clean only)**                |        |            | **3.60**       |                                |
```

Verify: 4.80 − 0.20 − 0.40 − 0.30 − 0.20 − 0.10 − 0.40 − 0.20 − 0.40 − 0.20 = 2.40 ✓
Verify: 4.80 − 0.20 − 0.40 − 0.30 − 0.20 − 0.10 = 3.60 ✓

These numbers feed directly into the 5-scenario table EPS column in `five-scenario-framework-us.md`.

## Layer definitions

### Soft layer

Adjustments that are **already in motion or empirically observed in recent reports**. Most market participants would mark to these if asked. The soft layer represents the "modal-bear" view — the bear most sell-side analysts would write.

Examples (US-specific):
- **SBC headwind growing** as a percentage of revenue (when ASC 718 expense rises faster than top-line growth)
- **Cycle-trough margin compression** for cyclicals when the cycle has clearly turned (auto OEMs in inventory glut; semi inventory correction visible in days-of-inventory)
- **Working capital build** when 1Q working-capital cycle days have visibly extended (DSO +5 days QoQ)
- **FX translation hit** when USD index has already moved (S&P 500 ~40% foreign rev exposure)
- **Volume mix shift** when channel data already shows it (Yipit, Second Measure prints)
- **Inventory write-down trail** already disclosed in recent 10-Qs

Rule: if a sell-side analyst not constructing a bear case would still mark to this, it's soft.

### Clean layer

Adjustments that are **plausibly coming based on visible inputs but have not yet shown in reported financials**. These are the conviction-adjusted bear case.

Examples (US-specific):
- **Customer concentration risk** where the customer has signaled price negotiation or insourcing but it hasn't hit price yet (Apple in-house chip migration affecting QCOM; Google in-house TPU affecting NVDA)
- **Capacity coming online** that will pressure pricing in 2-4 quarters (TSMC N3 / N2 utilization affecting margin)
- **Buyback offset gap**: if buyback dollars < SBC dollars, dilution is being masked by ASR mechanics. Build the dilution into bear share count.
- **§174 R&D amortization headwind** (TCJA 2017 — 5-year amortization of domestic R&D, 15-year foreign; was supposed to be repealed but hasn't been; raises effective tax rate by 200-400bp at the margin until rolled off)
- **Tax rate normalization**: NOL exhaustion, IRA Section 45X / 48 credit roll-off after sunset dates, expiry of CHIPS Act 48D for fabs
- **Non-GAAP to GAAP conversion gap widening**: if non-GAAP EPS grows faster than GAAP EPS, the gap is itself a bear-bridge layer (the "real" EPS is GAAP, and it's growing slower than the headline)
- **Pension contribution requirement** (ERISA-triggered mandatory contribution if PBO underfunded ratio crosses thresholds — legacy autos, airlines, industrials)
- **Restatement reserve build-up** in legal contingencies section of 10-K

Rule: a sell-side analyst not constructing a bear case would *not* make this adjustment, but if you showed a PM the logic chain, they would accept it.

### Strong layer

Adjustments unique to your bear thesis. These are the **non-consensus calls** — where the rest of the market disagrees with you.

Examples (US-specific):
- **Specific asset impairment** you forecast that management doesn't acknowledge (goodwill on a recent acquisition that's underperforming; intangibles on declining product line)
- **Demand collapse on a structural basis** (share loss to a new entrant; technology generational shift like inference TPUs vs training GPUs)
- **Tail events with non-trivial probability** (FTC Second Request blocking pending M&A; OFAC SDN listing; DOJ Section 1/2 enforcement)
- **Quality-of-earnings adjustments** that reveal hidden trouble (deferred revenue declines flagging churn for SaaS; channel-stuffing DSO patterns)
- **Customer in-house substitution** at scale (Tesla 4680 cell in-housing; Apple AirPods chip in-housing affecting CRUS)
- **8-K Item 4.02 restatement risk** based on SEC AAER pattern or PCAOB inspection deficiency at the auditor

Rule: this is the layer that justifies *your* bear vs the market's bear. If your strong layer is empty, you have a market-consensus bear, not a differentiated view.

## US-specific named adjustments catalog

Use these standard line items where applicable. Naming consistency lets PMs across firms read your bear bridge without re-interpreting.

| Adjustment label | Typical layer | Typical magnitude | Notes |
|---|---|---|---|
| SBC headwind | Soft (if visible trend) or Clean (if forecasting acceleration) | 1-5% of revenue, 10-30% of GAAP EPS | ASC 718; the most universally-applicable US bear adjustment |
| Buyback offset gap | Clean | dilution = SBC − buyback in $, /diluted shares | Triggered when buyback $ < SBC $; B12 forensic flag |
| §174 R&D amortization headwind | Clean | +200-400bp ETR for R&D-heavy names | TCJA 2017; awaiting repeal that hasn't come; affects MSFT, GOOGL, NVDA, META, CRM, etc. |
| Tax rate normalization | Clean | +100-500bp ETR | NOL exhaustion (legacy losses used up); IRA 45X / 48 / 48D credit roll-off |
| Non-GAAP→GAAP conversion gap | Clean | varies | grows over time when SBC + acquired intangible amortization escalate |
| Pension contribution (ERISA) | Clean | $100M-$1B per year | applies when PBO funded ratio < threshold; legacy industrials, airlines, autos |
| Restatement reserve | Strong | varies | when 8-K Item 4.02 pattern emerges |
| Goodwill / intangible impairment | Strong | varies | ASC 350 triggering events at segment level |
| Customer concentration price pressure | Clean | varies; depends on customer mix | applies when top-5 customers >40% of revenue and concentration is increasing |
| Tariff / Section 301 escalation | Strong (if escalation scenario) | 5-25% of COGS for affected SKUs | Section 301 China, Section 232 steel/aluminum; tracked in monitoring framework |
| Export control re-tightening | Strong | varies (NVDA: ~$10-15B China DC rev exposure at H20 SKU level) | BIS Entity List / OFAC SDN expansion |
| FX headwind | Soft (if USD already moved) or Clean (forward) | 50-300bp on revenue/EBIT | applies to multinationals; flag relative to base modeling FX |

## Mapping to scenarios

The three layers map to the 5-scenario distribution per `five-scenario-framework-us.md`:

- **base**: base EPS, none of the bridge applied → probability ~30-50%
- **bear**: base EPS − (soft + clean) layers → probability ~15-25%
- **strong_bear**: base EPS − (soft + clean + strong) layers → probability ~5-10%

Symmetric construction for the bull side: the bear bridge has a mirror — the **bull bridge** — where you start at base and *add* soft / clean / strong upward adjustments:

- **bull**: base + (soft positives + clean positives) → probability ~15-25%
- **strong_bull**: base + (soft + clean + strong positives) → probability ~5-10%

Bull-bridge named adjustments mirror the catalog above with sign reversed: GM expansion from mix, ASP step-up from new product, buyback yield re-rate, IRA tax credit acceleration, share gain from competitor stumble, etc. Symmetric construction is **mandatory** for non-bear theses; an asymmetric bridge looks like advocacy.

## How PMs challenge a bear bridge

Common PM challenges (and what to be ready for):

1. **"Where does adjustment X come from?"** — every adjustment must have a source tag. If the source is S3-S5, the adjustment is acceptable but the scenario *probability* should be lower than if all adjustments were S1-S2.
2. **"Are you double-counting?"** — soft and clean must be mutually exclusive. If "cycle-trough GM compression −200bp" (soft) already incorporates "Blackwell ASP haircut", you cannot then add "Blackwell ASP haircut -10%" (clean) without showing they hit different P&L lines.
3. **"What's the time horizon?"** — bear EPS for FY+1 vs FY+2 vs FY+3 will differ. Be explicit which year the bridge is computing. The period must match the scenario EPS_period field in `scenarios.json`.
4. **"What about offsetting positives?"** — a bear bridge that ignores known cost-side positives (raw material tailwind, FX swing in favor, IRA credits already secured) is one-sided. Either include them as negative adjustments to the cumulative bear total, or note in narrative that they're insufficient to offset.
5. **"Why is SBC in clean and not in base?"** — if SBC is a recurring cost (it is), it should already be in GAAP base EPS. The bear adjustment is the *change* in SBC trajectory, not the level. Be precise.

## NVDA worked example (FY27E base $4.80 → strong_bear $2.40)

(Same as the table at the top of this file, re-stated with explicit period and price anchor.)

```
NVDA FY27E base EPS:                                                  $4.80 (S4: Visible Alpha n=42 median)
  Soft 1: SBC growth from 3.0% → 3.5% of revenue (50bp drag)         -0.20
  Soft 2: cycle-trough GM compression -200bp (73% → 71% non-GAAP)    -0.40
                                                Soft cumulative:      $4.20
  Clean 1: Blackwell ASP haircut -10% (hyperscaler pushback)         -0.30
  Clean 2: hyperscaler DC capex flat YoY (vs base +15%)              -0.20
  Clean 3: §174 R&D capitalization headwind (+50bp ETR)              -0.10
                                                Clean cumulative:     $3.60
  Strong 1: AMD MI400 share to 12% (from 8% base)                    -0.40
  Strong 2: customer concentration tail (top-4 hyperscalers 50%)     -0.20
  Strong 3: export control re-tightens China DC rev ($10B exposure) -0.40
  Strong 4: SBC step-up under cycle pressure                         -0.20
                                                Strong cumulative:    $2.40
                                                                      
                                                bear EPS (soft+clean):  $3.60
                                                strong_bear EPS (all):  $2.40
```

Each adjustment carries an S-source tag (see catalog table above). Each is a named, defensible delta. PM can disagree with any single line, recompute, and arrive at a different bear total. That is the point of the bridge — to make the bear case auditable rather than rhetorical.

## The bear bridge box (mandatory)

Every memo with a meaningful bear case (≥10% probability on bear + strong_bear) must include the bear bridge as a standalone table in §6.x. Layer separation must be visually clear (use shading or section breaks). The G5 verification script reads the structured `eps_bridge` array in `scenarios.json` to check that named adjustments sum to (base_eps − scenario_eps) within rounding.

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| "Bear EPS $2.40, 50% lower than base" — no decomposition | unreviewable; PM cannot disagree with anything specific |
| All adjustments lumped together (no layers) | reader can't separate "obvious" from "non-consensus" |
| Strong layer empty (only soft + clean) | you have a market-consensus bear, not a differentiated view; flag conviction tag down |
| Soft and clean overlapping (double-counted) | mathematically unsound; PM red-team kills |
| Bear bridge applied to wrong year (e.g., bridge for FY+2 used in FY+1 scenario) | inconsistent time horizon; G5 fail |
| No upside cross-check (only bear bridge, no symmetric bull bridge) | one-sided framework biases probability assignment |
| Soft adjustments cited without source tags | "GM compression -200bp" with no anchor is hand-waving |
| SBC adjustment without showing the buyback offset (B12 hook) | misses whether dilution is real or masked |
| Non-GAAP to GAAP conversion not flagged when it would change the base | starting from non-GAAP base then adjusting for GAAP-only items double-counts |
| Strong layer adjustments not tied to specific identifiable events / triggers | reader has no signal for when to test conviction |

## How this file ties into the rest of the rigor batch

- The EPS deltas computed here become the per-scenario EPS values in `five-scenario-framework-us.md`.
- Layer probabilities (which adjustments to apply for bear vs strong_bear) influence scenario probability assignment.
- Bear floor sanity check via P/E P5 / EV/Sales trough / FCF yield is in `three-method-valuation-us.md`.
- GM assumptions (e.g., -200bp cycle compression) tag back to `gm-taxonomy-us.md` T4 modeled GM.
- Source tags for each adjustment follow `source-stratification-us.md`.
- Triggers that would confirm or refute the strong-layer assumptions are mapped in `what-would-reverse-us.md`.
- B11 (non-GAAP/GAAP), B12 (SBC in FCF), and other US-specific forensic hooks belong in `forensic-accounting-checklist-us.md`.
- Tail events feeding the strong layer (export control, OFAC, FTC, recession) are catalogued in `tail-risk-mapping-us.md`.
