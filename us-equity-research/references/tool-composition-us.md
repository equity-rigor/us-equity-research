# Tool Composition — Delegation Contracts to Marketplace Plugins

This file documents the **delegation contracts** between the `us-equity-research` orchestrator and three skills from the `claude-for-financial-services` marketplace:

- `financial-analysis:dcf-model` — Excel DCF construction
- `financial-analysis:comps-analysis` — Excel comps construction
- `equity-research:initiating-coverage` Task 5 — polished DOCX assembly

Companion files: `design/skill-composition.md` (full inventory + composition choice per skill), `design/b0-conformance-diff.md` (schema-conformance audit). Per D23, the official plugin source lives under `reference/anthropic-official/` (gitignored).

---

## 1. Composition stance

Per **D21** (soft-dependency composition), `us-equity-research` owns the **analytical content** — the Markdown IC memo and the structured JSON conforming to `schemas/memo.json` — and delegates the construction of Excel artifacts (DCF, comps) and the polished DOCX initiation report to the existing marketplace plugins **only when the user requests them**. Per **D15**, Markdown is the default and only mandatory output; Excel/DOCX are conditional outputs. If the dependency plugins are not installed, the orchestrator still runs end-to-end and produces the full Markdown + JSON deliverable; it surfaces a one-line note explaining how to enable Excel/DOCX. The Markdown memo + structured JSON are the **single source of truth**: any derived artifact must round-trip from JSON so that a number changed during PM red-team propagates uniformly on rebuild.

---

## 2. Soft-dependency detection

At runtime, the orchestrator checks whether the Skill tool surfaces these names:

- `financial-analysis:dcf-model`
- `financial-analysis:comps-analysis`
- `financial-analysis:3-statement-model` (optional, for full 3-statement workbook)
- `financial-analysis:audit-xls` (optional, QC gate on any Excel we produce)
- `equity-research:initiating-coverage`

Detection rule: if the user requests an Excel or DOCX output AND the corresponding skill name is not in the available-skills list, the orchestrator emits exactly one note before producing Markdown-only:

> "Excel DCF / Excel comps / polished DOCX outputs require installing `financial-analysis@claude-for-financial-services` and `equity-research@claude-for-financial-services`. Producing Markdown + JSON only."

If the user never asks for Excel/DOCX, no detection check is needed and no note is emitted. This is the **EDGAR-only portability principle** (per BUILD_PROMPT and D5): the plugin works standalone.

---

## 3. Delegation contract A — Excel DCF via `financial-analysis:dcf-model`

### When to delegate

User language trigger: "build the DCF Excel", "I need a DCF model", "open in Excel", "give me the Excel", "use dcf-model", "DCF workbook". Default off; opt-in only.

### Input contract — JSON paths from `schemas/memo.json` to dcf-model inputs

| dcf-model input | Source field in memo.json |
|---|---|
| Current stock price | `current_price_usd` |
| Shares outstanding (diluted, M) | `financials.ltm.diluted_shares_m` |
| Net debt ($M) | `financials.ltm.net_debt_usd_m` |
| Historical revenue ($M, 3-5y) | `financials.historical[].revenue_usd_m` |
| Historical EBIT margin (%) | `financials.historical[].ebit_margin_pct` |
| Historical D&A % rev | derive from `financials.historical[].depreciation_amortization_usd_m / revenue_usd_m` |
| Historical CapEx % rev | derive from `financials.historical[].capex_usd_m / revenue_usd_m` |
| Tax rate (%) | `valuation.dcf_components.wacc_components.tax_rate_pct` |
| Risk-free rate (%) | `valuation.dcf_components.wacc_components.risk_free_rate_pct` |
| Beta | `valuation.dcf_components.wacc_components.beta` |
| Equity risk premium (%) | `valuation.dcf_components.wacc_components.equity_risk_premium_pct` |
| Pre-tax cost of debt (%) | `valuation.dcf_components.wacc_components.pre_tax_cost_of_debt_pct` |
| Equity weight (%) | `valuation.dcf_components.wacc_components.equity_weight_pct` |
| Debt weight (%) | `valuation.dcf_components.wacc_components.debt_weight_pct` |
| Terminal growth rate (%) | `valuation.dcf_components.terminal_growth_pct` |
| Terminal method | `valuation.dcf_components.terminal_method` (default `perpetuity_growth`) |
| Explicit forecast years | `valuation.dcf_components.explicit_forecast_years` (3-10) |
| WACC sensitivity range | `valuation.dcf_components.sensitivity_wacc_range_pct` (5 values) |
| Terminal-g sensitivity range | `valuation.dcf_components.sensitivity_terminal_g_range_pct` (5 values) |

### 5→3 scenario collapse (encoded in `delegation_outputs.scenarios_3case_for_dcf_plugin`)

`financial-analysis:dcf-model` operates on **3 cases** (Bear/Base/Bull). We maintain **5 scenarios** internally (strong_bear, bear, base, bull, strong_bull) per `schemas/scenarios.json` for proper P10/P90 calibration and tail-vs-ordinary distinction. The collapse rule is **probability-weighted averaging** within each side:

Let `P(s)` denote the scenario probability per `scenarios.json` (probabilities sum to 1.00 per G4). For year N and metric M in {revenue_growth_pct, ebit_margin_pct}:

```
bear_M_yN  = (P(strong_bear) * sb_M_yN + P(bear) * b_M_yN) / (P(strong_bear) + P(bear))
base_M_yN  = base_M_yN                                                                    (passthrough)
bull_M_yN  = (P(bull) * bl_M_yN + P(strong_bull) * sbl_M_yN) / (P(bull) + P(strong_bull))
```

Worked example (year 1 revenue growth, NVDA-style probabilities):
- P(strong_bear)=0.05, P(bear)=0.20, P(base)=0.45, P(bull)=0.25, P(strong_bull)=0.05
- strong_bear y1_rev_growth = -10%, bear y1 = +5%
- bear_rev_growth_y1 = (0.05 × −10 + 0.20 × 5) / (0.05 + 0.20) = (−0.5 + 1.0) / 0.25 = 0.5 / 0.25 = **+2.0%**

The resulting block is written into `memo.json` `delegation_outputs.scenarios_3case_for_dcf_plugin` with arrays of length = `explicit_forecast_years`:

```
{
  "bear_case_revenue_growth_pcts":  [y1, y2, y3, y4, y5],
  "bear_case_ebit_margin_pcts":     [y1, y2, y3, y4, y5],
  "base_case_revenue_growth_pcts":  [y1, y2, y3, y4, y5],
  "base_case_ebit_margin_pcts":     [y1, y2, y3, y4, y5],
  "bull_case_revenue_growth_pcts":  [y1, y2, y3, y4, y5],
  "bull_case_ebit_margin_pcts":     [y1, y2, y3, y4, y5]
}
```

These map 1:1 to dcf-model's three scenario assumption blocks (per dcf-model SKILL.md §"Section 3: DCF Scenario Assumptions"), populated via the case-selector cell (1=Bear, 2=Base, 3=Bull) and consolidation column with INDEX formulas. The dcf-model Bear-case block consumes `bear_case_revenue_growth_pcts` and `bear_case_ebit_margin_pcts` horizontally across FY1–FY5; same pattern for Base and Bull.

### Sensitivity tables

dcf-model produces **three sensitivity tables at the bottom of the DCF sheet**, each 5×5 with the model's actual base case at the center cell:

1. WACC vs Terminal Growth — axes from `sensitivity_wacc_range_pct` × `sensitivity_terminal_g_range_pct`
2. Revenue Growth vs EBIT Margin — axes derived from the bear/base/bull collapse (typically ±2pp around base for revenue growth, ±2pp around base for EBIT margin)
3. Beta vs Risk-Free Rate — axes derived from `wacc_components.beta ± 0.2` and `risk_free_rate_pct ± 50bp`

If the orchestrator does not specify axes for tables 2 and 3, dcf-model constructs symmetric axes around the base case per its standard rule (`[base - 2*step, base - step, base, base + step, base + 2*step]`).

### Cell comments — source citations

Every hardcoded input written to the Excel must have a cell comment in the format `"Source: [System/Document], [Date], [Reference], [URL if applicable]"` (per dcf-model SKILL.md). The orchestrator passes citation strings from `source_tags_ref` JSON. Format:

- For S1/S2 anchors: `"Source: 10-K FY2024 Note 4, accessed 2025-03-15, https://www.sec.gov/..."`
- For S3 transcripts: `"Source: NVDA FY24Q4 earnings call, 2025-02-26"`
- For S4 consensus: `"Source: Visible Alpha consensus, n=42, range $X-$Y, median $Z"`
- For S5 third-party: `"Source: Damodaran implied ERP, 2025-01"`

### Output expected

`outputs/<ticker>_DCF.xlsx` — two sheets (DCF + WACC), zero formula errors after `recalc.py`, sensitivity tables fully populated with formulas.

### Error handling

If dcf-model fails (formula errors that don't resolve after re-run, recalc timeout, missing input):
1. Surface the error message to the user
2. Continue with remaining delegations (do not abort the run)
3. Fall back to **Markdown-only DCF narrative** drawn from `valuation.methods[method=DCF]` + `valuation.dcf_components`; emit a one-line note that the Excel build failed

The Markdown DCF narrative is ALWAYS produced regardless of Excel build success/failure. It is the source of truth.

---

## 4. Delegation contract B — Excel Comps via `financial-analysis:comps-analysis`

### When to delegate

User language trigger: "build the comps Excel", "I need a comp table", "compare to peers in Excel", "use comps-analysis", "peer comp workbook". Default off; opt-in only.

### Input contract — JSON paths from `schemas/memo.json` to comps-analysis inputs

| comps-analysis input | Source field in memo.json |
|---|---|
| Peer list (5-10 names) | `company_qualitative.competitive_landscape.peers[]` |
| Peer ticker | `company_qualitative.competitive_landscape.peers[].ticker` |
| Peer market cap | `company_qualitative.competitive_landscape.peers[].market_cap_usd_b` |
| Peer market share | `company_qualitative.competitive_landscape.peers[].market_share_pct` |
| Peer revenue growth | `company_qualitative.competitive_landscape.peers[].revenue_growth_pct` |
| Peer EBITDA margin | `company_qualitative.competitive_landscape.peers[].ebitda_margin_pct` |
| Subject revenue (LTM) | `financials.ltm.revenue_usd_m` |
| Subject gross profit | `financials.ltm.gross_profit_usd_m` |
| Subject gross margin | `financials.ltm.gross_margin_pct` |
| Subject EBITDA | `financials.ltm.ebitda_usd_m` |
| Subject EBITDA margin | `financials.ltm.ebitda_margin_pct` |
| Subject market cap | `market_cap_usd_b` |
| Subject enterprise value | `enterprise_value_usd_b` |

For each peer ticker, the orchestrator must supply (or instruct comps-analysis to fetch via its own MCP/data sources) the same LTM financial fields: Revenue, Revenue growth %, Gross profit, Gross margin %, EBITDA, EBITDA margin %, Market Cap, Enterprise Value, EV/Revenue, EV/EBITDA, P/E.

### Operating metrics block (comps-analysis §Section 2 core columns)

The 7 core columns: Company, Revenue (LTM), Revenue Growth (YoY), Gross Profit, Gross Margin, EBITDA, EBITDA Margin.

### Valuation metrics block (comps-analysis §Section 3 core columns)

The 6 core valuation columns: Company, Market Cap, Enterprise Value, EV/Revenue, EV/EBITDA, P/E Ratio.

### Statistics block

comps-analysis auto-computes Maximum / 75th Percentile / Median / 25th Percentile / Minimum for every comparable metric using `=MAX`, `=QUARTILE(range,3)`, `=MEDIAN`, `=QUARTILE(range,1)`, `=MIN`. The orchestrator does not supply these; it relies on the formula.

### Output expected

`outputs/<ticker>_Comps.xlsx` — single workbook, formulas-not-hardcodes for every ratio and statistic, blue font for hardcoded inputs, cell comments with citations on each hardcoded peer datapoint.

### Error handling

Same fallback as contract A. If comps-analysis fails, surface error and continue; the comps narrative in `valuation.methods[method=Trading_comps]` is the source of truth.

---

## 5. Delegation contract C — Polished DOCX via `equity-research:initiating-coverage`

This is the most complex delegation. `initiating-coverage` is a strict 5-task pipeline (per its SKILL.md — "one task at a time, never chain"). Two orchestration modes are supported.

### When to delegate

User language trigger: "build the DOCX report", "I need a polished initiation report", "client-facing version", "full sell-side-style report", "initiation deck", "investment banking format". Default off; opt-in only.

### Mode 1 — Task-5-only (recommended default)

The orchestrator pre-produces the four input artifacts Task 5 expects and dispatches `equity-research:initiating-coverage` directly to Task 5. This bypasses Tasks 1-4, which we do not need because our pipeline has already produced richer equivalents.

**Input artifacts** (paths recorded in `memo.json` `delegation_outputs`):

| Task 5 expected input | Our deliverable | Source in memo.json |
|---|---|---|
| `<Company>_Research_Document_<Date>.md` | Rendered 6-8K word qualitative narrative | `company_qualitative.description` + `.history` + `.products` + `.customers_gtm` + `.industry` + `.competitive_landscape` + `management[]` + `risks[]` + `tail_risks[]` |
| `<Company>_Financial_Model_<Date>.xlsx` | Excel with 6 tabs (Revenue Model, IS, CF, BS, Scenarios, DCF Inputs) | Produced via contract A (DCF) + contract B (comps) merged, or via `financial-analysis:3-statement-model` chained delegation |
| `<Company>_Valuation_Analysis_<Date>.md` | 4-6 page valuation narrative w/ price target + recommendation | `valuation.methods[]` + `valuation.dcf_components` + `valuation.reconciliation_narrative` + `recommendation` + `catalysts[]` |
| `<Company>_Charts_<Date>.zip` | 25-35 PNG/JPG @ 300 DPI | Generated from memo.json data per §6 chart-list mapping below |

**Word-count discipline for the rendered Research Document.md**: minimum 6,000 words, target 7,000-8,000 (per Task 1 spec). Sections must include all Task 1 subsections — Company overview, history, products, customers/GTM, industry overview, TAM (with current/projected/CAGR), competitive landscape (5-10 peers), management bios (300-400 words each, 3-4 execs from our `management[]` array — take top 4 by relevance), risk assessment (8-12 risks). The orchestrator's rendering layer maps our 7-category risk taxonomy down to Task 1's 4 categories (company / industry / financial / macroeconomic) — `regulatory`, `geopolitical`, `esg` collapse into the closest of {industry_market, macroeconomic} based on context.

**Valuation Analysis.md discipline**: 4-6 pages, must include DCF summary + comps summary + precedent transactions (if any) + price target derivation with weighting per method + recommendation (one of OUTPERFORM / BUY / HOLD / MARKET PERFORM / UNDERPERFORM / SELL — see §8 label translations) + 3-5 catalysts.

### Mode 2 — Sequential dispatch through Tasks 1-5

When the user explicitly requests "use the full initiating-coverage pipeline" or "run all 5 tasks": orchestrator dispatches one Skill invocation per task in order, providing prerequisites from prior tasks as required by the skill's internal verification. This mode is more expensive (5 Skill invocations) and lets `initiating-coverage` own its outputs entirely. Default behavior is Mode 1; Mode 2 is opt-in.

### Output expected

`outputs/<ticker>_Initiation_Report_<Date>.docx` — 30-50 pages, 10,000-15,000 words, 25-35 embedded charts, 12-20 tables. Times New Roman, clickable hyperlinks for citations, INITIATING COVERAGE Page 1 format.

### Error handling

Same fallback: surface error, continue, Markdown memo remains source of truth. If `equity-research:initiating-coverage` is unavailable, our Markdown memo + structured JSON are the deliverable.

---

## 6. Chart list (B0 backfill)

Task 4 of `initiating-coverage` requires 25-35 specific charts at 300 DPI. Mapping each chart to its data source in `memo.json` so the orchestrator can render them from our structured data.

### 4 mandatory charts (Task 5 spec requires all 4)

| ID | Description | Data source in memo.json |
|---|---|---|
| chart_03 | Revenue by product (stacked area) | `financials.revenue_by_product[]` |
| chart_04 | Revenue by geography (stacked bar) | `financials.revenue_by_geography[]` |
| chart_28 | DCF sensitivity (2-way heatmap) | `valuation.dcf_components.sensitivity_wacc_range_pct` × `sensitivity_terminal_g_range_pct` |
| chart_32 | Valuation football field (horizontal bars) | `valuation.methods[].price_range_low_usd` / `.price_range_high_usd` + `valuation.football_field_range_low_usd` / `.football_field_range_high_usd` |

### 21 other required charts (total 25 required)

| ID | Description | Data source in memo.json |
|---|---|---|
| chart_01 | Stock price performance, 12-24mo | External (Yahoo Finance / market data MCP); current price from `current_price_usd` |
| chart_02 | Revenue growth trajectory | `financials.historical[].revenue_usd_m` + `.projected[].revenue_usd_m` |
| chart_05 | Company overview / timeline | `company_qualitative.history` |
| chart_06 | Key milestones timeline | `company_qualitative.history` (milestones extracted) |
| chart_07 | Organizational structure | `management[]` |
| chart_08 | Product portfolio overview | `company_qualitative.products[]` |
| chart_09 | Customer segmentation | `company_qualitative.customers_gtm` |
| chart_10 | Gross margin evolution | `financials.historical[].gross_margin_pct` + `.projected[].gross_margin_pct` |
| chart_11 | EBITDA margin progression | `financials.historical[].ebitda_margin_pct` + `.projected[].ebitda_margin_pct` |
| chart_12 | Free cash flow trend | `financials.historical[].fcf_usd_m` + `.projected[].fcf_usd_m` |
| chart_13 | Operating metrics dashboard | Multi-source — `financials.*` selected KPIs |
| chart_14 | Scenario comparison (Bull/Base/Bear) | `scenarios_ref` → `scenarios.json` per-scenario revenue / EPS / price |
| chart_15 | Market size evolution (TAM) | `company_qualitative.industry.tam` |
| chart_16 | Competitive positioning matrix | `company_qualitative.competitive_landscape.peers[]` plotted by 2 metrics (e.g., growth × margin) |
| chart_17 | Market share breakdown | `company_qualitative.competitive_landscape.peers[].market_share_pct` |
| chart_18 | Competitive benchmarking | `company_qualitative.competitive_landscape.peers[]` multi-metric bar chart |
| chart_29 | DCF valuation waterfall (EV components) | `valuation.dcf_components` — PV of explicit FCFs, PV of terminal, EV, − Net Debt, Equity Value |
| chart_30 | Trading comps scatter (e.g., EV/EBITDA vs growth) | `company_qualitative.competitive_landscape.peers[]` + valuation block |
| chart_31 | Peer multiples comparison | derived from comps Excel (contract B) |
| chart_33 | Price target scenarios | `scenarios_ref` per-scenario price + `recommendation.price_target_range_low_usd` / `.price_target_range_high_usd` |
| chart_34 | Historical valuation multiples | External (Yahoo Finance / Bloomberg); plotted against `valuation.methods[]` current multiples |

### 10 optional charts (for 26-35 range)

| ID | Description | Data source in memo.json |
|---|---|---|
| chart_19 | Customer acquisition trends | `company_qualitative.customers_gtm` (qualitative) or sector-specific |
| chart_20 | Unit economics evolution | sector-specific; SaaS LTV/CAC if applicable |
| chart_21 | Product roadmap timeline | `company_qualitative.products[]` |
| chart_22 | Geographic expansion map | `financials.revenue_by_geography[]` |
| chart_23 | R&D investment trends | derived from `financials.*` (R&D as % rev if disclosed) |
| chart_24 | Sales & marketing efficiency | derived from `financials.*` (S&M as % rev) |
| chart_25 | Working capital trends | derived from `financials.*` |
| chart_26 | Debt maturity schedule | `forensic_flags.asc_842_lease_pv_usd_m` + balance sheet items |
| chart_27 | Ownership structure | `positioning_sentiment.top_holders_13f[]` |
| chart_35 | Analyst price target distribution | `positioning_sentiment.sell_side_distribution.pt_low_usd` / `.pt_median_usd` / `.pt_high_usd` |

The orchestrator's chart-rendering layer reads the canonical Task 4 reference at `reference/anthropic-official/equity-research/skills/initiating-coverage/references/task4-chart-generation.md` for chart styling (300 DPI, file naming `chart_##_description.png`, color palette).

---

## 7. Prose quality checklist (B0 backfill)

`initiating-coverage` carries a ~130-line prose quality checklist embedded in `references/task5-report-assembly.md` covering LENGTH / PAGE 1 FORMAT / SECTION WORD COUNTS / CITATIONS / PROFESSIONAL VOICE / NUMBER CONSISTENCY / etc. We deliberately **do not replicate this in `schemas/verification_gates.json`** — those 14 gates are **buy-side rigor gates** (EPS×PE multiplicativity, segment GM reconciliation, source stratification, scenario weighting, bear bridge, what-would-reverse, headline conditionality, GAAP/non-GAAP discipline, FCF definition, quant overlay, capacity) — not formatting QC.

When the orchestrator delegates to Task 5 (Mode 1 or Mode 2), the formatting QC pass is **owned by `equity-research:initiating-coverage` Step 7**. The orchestrator surfaces this delegation explicitly to the user:

> "Formatting QC delegated to initiating-coverage Step 7 checklist (length, page 1 format, section word counts, citation discipline, professional voice). Buy-side rigor QC owned by us-equity-ic-rigor 14 verification gates."

**Reference path** (read-only, gitignored per D23): `reference/anthropic-official/equity-research/skills/initiating-coverage/references/task5-report-assembly.md`.

---

## 8. Label translations

`equity-research:initiating-coverage` Task 5's PAGE 1 format uses sell-side labels. Our 5-band rating (per **D1**) is buy-side. The rendering layer maps:

| Our rating (memo.json `recommendation.rating`) | Sell-side label (Task 5 DOCX) |
|---|---|
| Strong Buy | OUTPERFORM |
| Buy | BUY (or OUTPERFORM if sell-side-format requested) |
| Hold | HOLD (or MARKET PERFORM) |
| Sell | UNDERPERFORM |
| Strong Sell | UNDERWEIGHT / SELL |

Mapping is renderer-side only; the JSON always stores our 5-band label. If the user requests "use sell-side labels throughout", the orchestrator passes the mapped label to Task 5; otherwise the buy-side label survives.

Conviction tag (`recommendation.conviction_tag`) is not part of the standard Task 5 PAGE 1 format and is ignored by the DOCX renderer; it survives in the Markdown memo.

---

## 9. Failure modes & fallback

For each delegated artifact, if production fails (recalc error, missing input, skill unavailable, version mismatch):

1. **Surface the error message** to the user with the artifact name and the failure reason
2. **Continue with remaining delegations** — one failure does not abort the run
3. **Fall back to Markdown-only** for that artifact:
   - Failed Excel DCF → keep `valuation.methods[method=DCF]` narrative in the Markdown memo
   - Failed Excel comps → keep `valuation.methods[method=Trading_comps]` narrative + peer table in the Markdown memo
   - Failed DOCX → the full Markdown IC memo remains the deliverable

**Invariant**: the Markdown IC memo (`outputs/<ticker>_IC_memo.md`) and the structured JSON (`outputs/<ticker>_structured.json` conforming to `schemas/memo.json`) are ALWAYS produced regardless of delegation success or failure. They are the single source of truth. All derived artifacts round-trip from the JSON.

---

## 10. Versioning

Marketplace plugin versions can drift; our delegation contract is tested against:

- `equity-research@claude-for-financial-services` version **0.1.0** (tested)
- `financial-analysis@claude-for-financial-services` version **0.1.0** (tested)

If the user has a newer version installed and the input contract has changed upstream, delegation may break silently (e.g., Task 5 expects a new file naming pattern). Mitigation per D23 + Phase F packaging:

- Phase F `plugin.json` `requires` block declares the tested-against version
- If a version mismatch is detected at runtime, the orchestrator emits a one-line warning:

> "Delegation contract tested against `equity-research@0.1.0` / `financial-analysis@0.1.0`. Installed version is `X.Y.Z`. Excel/DOCX outputs may behave unexpectedly; fall back to Markdown if issues observed."

Version-drift surveillance is a Phase F concern; the version-pin clause is the mechanism.

---

## Cross-references

- **D1** — 5-band rating taxonomy (drives §8 label translations)
- **D15** — Markdown is default output (drives §1 composition stance and §9 fallback invariant)
- **D21** — Soft-dependency composition (origin of this file)
- **D23** — `reference/anthropic-official/` gitignored; read-only for subagents (governs §7 reference path)
- `design/skill-composition.md` — full inventory + composition choice per marketplace skill
- `design/b0-conformance-diff.md` — schema-conformance audit and backfill assignments (§6 chart list, §7 prose checklist, 5→3 scenario collapse)
- `schemas/memo.json` `delegation_outputs` block — runtime structured payload encoding the 5→3 collapse and intermediate artifact paths
- `schemas/scenarios.json` — 5-scenario probabilistic framework being collapsed to 3 cases in §3
