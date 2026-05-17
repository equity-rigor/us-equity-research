# Five-scenario probabilistic framework (US)

## Why five (not three, not seven)

Three scenarios (bear / base / bull) under-resolve real PM disagreement: the gap between a "tail-bear" (Fed-cycle pivot fails, hyperscaler capex inflects negative) and an "ordinary-bear" (one-quarter ASP haircut) is precisely the disagreement most analysts and PMs argue about. Two scenarios collapse those distinctions. Seven scenarios over-resolve: once you assign <10% probability mass to each tail, the difference between 5% and 8% is noise, and the table becomes too wide for IC.

Five scenarios — **strong_bear / bear / base / bull / strong_bull** (matches `schemas/scenarios.json` enum exactly) — cleanly separates "this is the modal world" from "this is what a tail looks like" on each side. Probabilities typically distribute roughly 5-20-50-20-5 for a high-conviction view; 10-25-30-25-10 for a low-conviction view; and 5-15-30-30-20 (or its mirror) for an asymmetric thesis.

## Required structure

Every memo's §5 (valuation core) contains a 5-scenario table with these columns. Column names match `schemas/scenarios.json` field names so the verification scripts can parse the table directly.

| Column | Required | Notes |
|---|---|---|
| Scenario | yes | `strong_bear` / `bear` / `base` / `bull` / `strong_bull` |
| Probability | yes | sum to 1.00 (allow ±0.01 rounding display); G4 gate |
| Narrative one-liner | yes | the world this scenario describes, single sentence |
| EPS (FY+1 or FY+2) | yes | period must be consistent across all 5 rows |
| Multiple | yes | the multiple you are applying in this scenario |
| Multiple_type | yes | per D8 sector default — `P/E`, `EV/EBITDA`, `EV/Sales`, `EV/ARR`, `P/B`, `P/AFFO`, `NPV_pipeline`, `SOTP`, etc. See `valuation-discipline-us.md`. |
| Target_price | yes | = EPS × multiple (P/E case) — **must actually multiply within ±0.5%**; G1 gate |
| Expected_return | yes | (target_price − current_price) / current_price |
| Anchors | yes | anchor IDs (from `source_tags.json`) driving this scenario |
| Strongest_anchor_S_level | yes | the highest-quality S-level among this scenario's anchors |

The most-failed gate in red-team practice is **G1: target_price column not actually = EPS × multiple**. PMs verify with a calculator; the script `scripts/verify_eps_pe.py` automates this check across all five rows.

## Probability assignment discipline

Probabilities must reflect three constraints:

1. **Anchor strength in each scenario**: a scenario whose narrative depends on S3-S5 anchors should carry less probability mass than one whose narrative is consistent with S1-S2 trajectories. If `strong_bull` requires an unverified rumor (Pending) or a single S5 alt-data print, `strong_bull` probability ≤10%.
2. **Path dependence**: `strong_bull` and `strong_bear` should be reachable only through specific identifiable paths (not just "things go really well"). If you cannot describe the precise sequence of events that produces `strong_bull` within 12 months, `strong_bull` probability is too high.
3. **Symmetry check**: |P(strong_bull) − P(strong_bear)| should reflect actual setup asymmetry. Symmetric tails for an asymmetric situation (e.g., heavily-shorted, single-customer-concentrated name) is lazy.

Common probability mistakes:

- **Anchoring on consensus**: "sell-side 70% Buy → bull +20pp probability" is wrong if your underlying anchors don't support consensus.
- **Tail inflation for narrative drama**: `strong_bull` / `strong_bear` over 15% each on a non-binary stock is rare; usually one tail dominates.
- **Linear-ladder default (10/20/40/20/10)**: this is the lazy distribution. The actual distribution should be informed by *which* anchors you have, not by aesthetic symmetry.

## EPS path discipline per scenario

Each scenario's EPS must be derivable from the bear bridge (or its bull-symmetric equivalent — see `bear-bridge-us.md`). The reader must be able to:

1. Start from base EPS
2. See which adjustments are applied (named, line-by-line)
3. Land on the scenario EPS

If you cannot show this bridge, the scenario EPS is hand-waving. The G5 gate verifies that Σ(named adjustments) = (base_eps − scenario_eps) within rounding. PMs catch this as: "where does NVDA strong_bear EPS $3.20 come from?" and the right answer is "base $4.80 − DC revenue miss −$0.80 − Blackwell ASP compression −$0.40 − share loss to AMD MI400 −$0.30 − SBC headwind −$0.10 = $3.20 (mix of S3 mgmt commentary + S5 hyperscaler capex tracker)".

## Multiple discipline per scenario

Each scenario's multiple must be:

1. **Justified by historical range**: cite the 5- or 10-year band (P5 / P25 / median / P75 / P95) for that multiple type. Use YCharts, Macrotrends, or Bloomberg HMI as data source.
2. **Reflective of scenario growth/quality profile**: `bull` / `strong_bull` multiple > `base` only if growth, ROIC, or capital intensity differs in that scenario; otherwise applying a higher multiple to a higher EPS is double-counting.
3. **Bound by peer comp at sector level**: within ±20-30% of sector peer median for that scenario's growth profile.
4. **Multiple_type consistent with sector default (D8)**: P/E for mature equities; EV/EBITDA for high-leverage industrial; EV/Sales or EV/ARR for high-growth pre-profit; P/B for banks/insurers; P/AFFO for REITs; NPV pipeline for pre-revenue biotech. See `valuation-discipline-us.md` for the full table. Where you deviate from sector default (e.g., using P/E on an early-stage SaaS), justify in narrative.

Common multiple-discipline mistakes:

- **Same multiple in all scenarios**: under-resolves. The multiple *should* differ across scenarios because risk premium and growth differ.
- **Higher multiple × higher EPS in bull without justification**: only valid if quality / cycle position genuinely differs; otherwise double-counting.
- **Floor multiple = 0.5× current without historical analog**: in a true `strong_bear`, multiple compression is real, but cite the trough year (e.g., NVDA P/E 25x at FY23 trough vs current ~45x).

## Scenario narrative ↔ anchor consistency

Each scenario row's "anchors" column must list the specific anchor IDs (from `source_tags.json`) driving it. The narrative must be consistent with those anchors. Example (NVDA `base` scenario row):

| Scenario | Probability | Narrative | FY27E EPS | P/E | Target | Return | Anchors | S-level |
|---|---|---|---|---|---|---|---|---|
| base | 50% | DC capex grows mid-teens; Blackwell ramp on schedule; AMD MI400 stays ≤10% share | 4.80 | 35 | 168.00 | +0.6% | A1 (S3), A2 (S2), A3 (S5) | mixed S3/S5 → conditional |

The reader can trace: anchors A1 (NVDA Q4 call DC guide) + A2 (10-Q segment split) + A3 (Omdia hyperscaler capex tracker) → narrative → EPS path → P/E band → target. If any link breaks (e.g. base EPS $4.80 doesn't follow from those anchors), the scenario is incoherent and PM red-team will flag it.

## Anchor weighting impact table (mandatory adjacent table; G10 gate)

Immediately after the 5-scenario table, include the **anchor weighting impact table**. This is the table PMs use to attack the scenario distribution and is required for IC defense.

```
| Probability shift                     | Headline median return |
|---------------------------------------|-----------------------|
| Base case (as published)              | +0.6%                 |
| Base −10pp → bear +10pp               | −2.8%                 |
| Base −10pp → bull +10pp               | +4.0%                 |
| Strong_bear +10pp at base expense     | −5.6%                 |
| Strong_bull +10pp at base expense     | +6.5%                 |
```

Reason: PMs ask "what's the variance of your headline if your probabilities are slightly wrong?" Having this in the doc preempts the question. The script `scripts/verify_weighting_sensitivity.py` checks that the `weighting_sensitivity` block in `scenarios.json` has been populated.

## Aggregating to headline

```
headline_median_return = Σ (P_scenario × return_scenario)
headline_range_P10_P90 = [P10, P90] of the discrete distribution
```

With 5 discrete scenarios, P10 / P90 will usually land on a scenario boundary. Standard practice: cite [worst-case return, best-case return] of scenarios within the 10-90 mass; call out tails (strong_bear, strong_bull) separately rather than diluting the headline range with low-probability mass.

## Scenario probabilities → conviction tag (D6 calibration)

Map the probability distribution to a conviction tag for the headline. Aligned with the `scenarios.json` conviction_tag enum and the D6 multiplier ranges (0.10× to 0.50× of base position):

| Distribution shape | Conviction tag | Position-sizing multiplier |
|---|---|---|
| >50% on bull+strong_bull side; tails balanced | `high_bull` | 0.50× |
| 35-50% on bull side | `moderate_bull` | 0.30-0.40× |
| Mass split roughly 30-30-30 across base/bull/bear cluster | `neutral` | 0.15-0.25× |
| 35-50% on bear side | `moderate_bear` | 0.30-0.40× |
| >50% on bear+strong_bear side | `high_bear` | 0.50× |
| Any top-3 anchor is S3 or weaker | `source_conditional` | 0.10-0.20× regardless of distribution |
| Tail (strong_bear OR strong_bull) >15% | flag in conviction note ("note tail risk") | apply ×0.5 further multiplier on top of base |

The conviction tag flows into the default_action (`hold_long`, `add_long`, `trim_long`, `initiate_short`, etc.) per `schemas/scenarios.json` headline block. Position-sizing math is in `position-sizing-us.md`.

## NVDA worked example (running through all 14 gates in Phase E)

```
Current price (as of 2026-05-15):  $167.00
FY27E period anchor:                CY26 calendar year, NVDA fiscal FY27E

| Scenario     | Prob | Narrative one-liner                                                                    | FY27E EPS | P/E  | Target  | Return  | Anchors          | Strongest S |
|--------------|------|----------------------------------------------------------------------------------------|-----------|------|---------|---------|------------------|-------------|
| strong_bull  | 5%   | Hyperscaler capex +30% YoY; Blackwell ASP +30%; sovereign AI clusters add 5pts share   | $6.40     | 45.0 | $288.00 | +72.5%  | A1, A4 (both S3) | S3          |
| bull         | 20%  | DC capex +20% YoY; Blackwell ASP +20%; MI400 stays <10% share through CY26             | $5.60     | 40.0 | $224.00 | +34.1%  | A1, A2 (S2/S3)   | S2          |
| base         | 50%  | DC capex +15% YoY; Blackwell on schedule; MI400 share 8-10%; Hopper EOL absorbed       | $4.80     | 35.0 | $168.00 | +0.6%   | A1, A2, A3       | S2          |
| bear         | 20%  | DC capex flat YoY; Blackwell ASP haircut -10%; MI400 share 12%; SBC drag widens        | $3.60     | 28.0 | $100.80 | -39.6%  | A1, A3, A5       | S3          |
| strong_bear  | 5%   | DC capex -10% YoY; MI400 share 15%; export-control re-tightens China DC revenue        | $2.40     | 22.0 | $52.80  | -68.4%  | A3, A5, A6 (S5)  | S5          |
|                                                                       Probability-weighted median return: +1.7%                            |
```

- **G1 (multiplicativity)**: every row verifies — 6.40×45.0 = 288.00 ✓, 5.60×40.0 = 224.00 ✓, 4.80×35.0 = 168.00 ✓, 3.60×28.0 = 100.80 ✓, 2.40×22.0 = 52.80 ✓.
- **G4 (probability sum)**: 0.05 + 0.20 + 0.50 + 0.20 + 0.05 = 1.00 ✓.
- **G10 (weighting impact)**: required adjacent table — populate `scenarios.json.weighting_sensitivity`.
- **Conviction tag**: 0.50 on base + 0.20 on bull = 70% non-bear cluster mass, but top-3 anchors mix S2/S3/S5 → `source_conditional` rather than `moderate_bull`. Headline rating defaults to **Hold** (median +1.7% within ±10% band per D1) with `source_conditional` conviction; default_action = `hold_long`.

## Anti-patterns (these fail PM red-team)

| Anti-pattern | Why wrong | Fix |
|---|---|---|
| target_price not = EPS × multiple in row | G1 fail; PM catches with calculator | re-multiply each row mechanically |
| Probabilities sum to 0.95 or 1.05 | G4 fail; arithmetic carelessness | reweight; round to 5pp steps if needed |
| Same multiple in all 5 scenarios | under-resolves; multiple should reflect risk premium differential | bear multiple = historical P25; strong_bear = historical P5; base = median; bull = P75 |
| Strong_bull narrative requires post-cutoff Pending anchor | high tail mass with low source quality is incoherent | either cap strong_bull at 5-7% or downgrade headline to source_conditional |
| Linear ladder probability (10-20-40-20-10) regardless of underlying | shows you defaulted | distribution must reflect anchor strength and path dependence |
| Bear scenario has higher P/E than base (without quality differential) | double-counting — applying both lower EPS and lower multiple is the discipline; applying lower EPS at *higher* multiple is incoherent | re-derive scenario multiple from historical analog |
| No weighting sensitivity table | G10 fail | add ±10pp shift impact table |
| EPS period inconsistent across rows (FY+1 in one row, FY+2 in another) | scenarios not comparable | freeze on FY+2 for cyclical / capacity-heavy names; freeze on FY+1 for stable growth |

## How this file ties into the rest of the rigor batch

- Scenario EPS values are constructed via `bear-bridge-us.md` (soft / clean / strong layers).
- Scenario multiples are bounded by sector-default discipline in `valuation-discipline-us.md`.
- Three-method reconciliation (EPS × multiple vs SOTP vs multi-multiple bear floor) is in `three-method-valuation-us.md`.
- GM assumptions used in deriving scenario EPS must be tagged per `gm-taxonomy-us.md`.
- What-would-reverse triggers per scenario are in `what-would-reverse-us.md`.
- Conviction tag → position sizing math is in `position-sizing-us.md`.
- PM red-team scoring of the scenario block is in `pm-redteam-rubric-us.md`.
- Source-stratification and conditional-headline language patterns are in `source-stratification-us.md`.
