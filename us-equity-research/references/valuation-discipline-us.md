# US Valuation Discipline — Build Side

This file is the **BUILD discipline** for US equity valuation: which primary multiple per sector, how to construct the WACC, how to handle terminal value, how to read historical multiple bands, and how to assemble comps. The **RECONCILE discipline** — how DCF / Comps / SOTP / multi-multiple-bear audit each other (and the hard rule that they are NEVER averaged) — lives in `three-method-valuation-us.md`.

Convention: USD reporting per D11. ADR native currency in appendix only. All citations follow the source-tag regex defined in D16 (see `source-stratification-us.md`).

---

## 1. WACC build

WACC is the discount rate for any unlevered DCF and the implied cost of equity in the levered case. Build it from observable inputs; do not pluck a number.

### Risk-free rate (R_f)

- **Source**: 10Y US Treasury yield. Primary feed: **FRED series `DGS10`** (`fred.stlouisfed.org/series/DGS10`).
- **Discipline**: verify the rate **on the memo date**, not at session start, not from training-data memory. The 10Y moves 5-15bp/day; a stale R_f propagates into a stale WACC and a stale price target.
- **Cite as**: `(S5: FRED DGS10, [YYYY-MM-DD], [value]%)`.
- **For ADRs / foreign-issuer US-listed**: still use 10Y UST if the cash flow is in USD; if you discount native-currency cash flows, use the appropriate sovereign 10Y.

### Equity risk premium (ERP)

- **Source**: Damodaran implied US ERP, monthly update at `pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/implprem.html`.
- **Typical range**: 4.5-6.0% over the last decade.
- **Discipline**: implied ERP (back-solved from S&P 500 prices and consensus dividends/buybacks) is preferred over historical ERP. Historical ERP (6-7%) overstates forward expectations when starting valuations are above mid-cycle.
- **Cite as**: `(S5: Damodaran implied ERP, [YYYY-MM], [value]%)`.

### Beta

Choose one of four bases. State the basis explicitly:

| Basis | When to use | Pros | Cons |
|---|---|---|---|
| **5y_monthly_vs_SP500** | Standard for liquid large-cap names | Most precedented; smooths noise | Slow to reflect business-model shift |
| **2y_daily_vs_SP500** | Higher-frequency reads; recent regime change | More current | Higher sample noise |
| **industry_unlevered** | Newly public, no/short history; private comparable; segment-level | Captures business-model risk irrespective of capital structure | Requires re-lever step |
| **adjusted_bloomberg** | Thin-trade or estimation-noisy names | Shrinks toward 1.0; reduces estimation error | Mechanical shrinkage may bias |

- **Adjusted beta formula** (Bloomberg convention): `adj_β = 0.67 × raw_β + 0.33 × 1.0`.
- **Re-lever formula** (when using industry unlevered): `β_levered = β_unlevered × (1 + (1 − t) × D/E)`.
- **Damodaran industry betas**: `pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html` (US, monthly update).
- **Cyclicals**: do NOT freeze beta across cycle. Cyclical names see real beta variation (e.g., autos β = 1.1 mid-cycle but observed-rolling 1.6 during a recession). Use longer windows AND state the cycle position.

### Cost of equity (CAPM)

```
R_e = R_f + β × ERP
```

- For high-tail-risk names (biotech pre-revenue, distressed turnarounds, micro-cap), add a **size premium** or a **specific risk premium** of 100-300bp (Duff & Phelps / Kroll size premia, or judgment).
- For ADRs in less-stable home jurisdictions, add a **country risk premium** (Damodaran country ERP table).

### Cost of debt (R_d)

- **Investment-grade (BBB-/Baa3 or higher)**: use the relevant rating's yield curve. Primary feed: **FRED `BAMLC0A0CM`** (ICE BofA US Corporate Index OAS) plus the corresponding Treasury yield.
- **High-yield (BB+/Ba1 or lower)**: **FRED `BAMLH0A0HYM2`** (HY OAS).
- **For specific issuers**: pull recent bond YTW from MarketAxess / FINRA TRACE / FRED BFAA / Bloomberg. If the company has no public debt, use a comparable-rated peer or industry median.
- **After-tax**: `R_d_after_tax = R_d_pre_tax × (1 − ETR)`. Use effective tax rate from filings, not statutory.

### Capital structure weights

- **At MARKET VALUE, not book.**
  - `E (market) = current_share_price × diluted_shares`
  - `D (market) = book debt if trading near par, else market value of debt; capitalized operating leases (ASC 842 PV) included`
- `equity_weight = E / (E + D)`, `debt_weight = D / (E + D)`. Weights sum to 1.00.
- **Net cash position**: when cash > debt, debt_weight is signed negative or set to zero with a note; WACC effectively approaches cost of equity. State the convention explicitly.
- **No-debt company**: `WACC = R_e`.

### WACC formula

```
WACC = (E / (E + D)) × R_e + (D / (E + D)) × R_d × (1 − t)
```

### Typical WACC bands (sanity check)

| Profile | Typical WACC |
|---|---|
| Large stable (utility, staples, mature industrial) | 7-9% |
| Standard mid-cap growth | 9-12% |
| High-growth tech / SaaS / biotech | 12-15% |
| Distressed / high-tail-risk | 15-20% |
| Pre-revenue biotech (use risk-adjusted DCF per asset instead) | 10-12% for the DCF; probability-of-success multiplies cash flows separately |

If your computed WACC is outside these bands, audit the inputs before publishing.

### Anti-patterns

- Frozen WACC across cycle for cyclicals
- WACC computed at book-value weights
- After-tax cost of debt using statutory rate when ETR diverges materially
- Beta from a one-year window during a regime break
- ERP from "historical average" without disclosing whether 1928-base or post-WWII base

---

## 2. Sector-default multiple table (per D8)

Every sector gets a primary multiple and a secondary. Applying the wrong multiple is the single biggest valuation error in cross-sector coverage.

| Sector | Primary | Secondary | Why primary fits / what breaks if wrong |
|---|---|---|---|
| Mature industrial / consumer / staples | P/E, EV/EBITDA | EV/Sales, P/B | Stable margins and capital intensity → earnings-based metrics work. EV/Sales discards margin reality. |
| Banks (commercial) | P/B, P/E | P/PPNR, ROTCE-implied | Balance sheet IS the business. Capital structure is the product, not financing. **P/E alone ignores leverage and capital adequacy.** Target P/B = (ROE − g) / (COE − g). CCAR / DFAST stress drives capital return discipline. |
| Insurance | P/B, P/E | ROE-implied P/B | Float economics + combined ratio drive earnings; book value is the cushion against loss reserves. |
| REITs | P/AFFO, NAV | Implied cap rate | GAAP earnings depressed by D&A on real estate. **AFFO** (FFO − maintenance capex − straight-line rent) is the cash metric. NAV = property-by-property cap rate × NOI. **P/E on a REIT is meaningless.** |
| SaaS / software | EV/ARR, Rule of 40 | EV/Sales, FCF yield | Pre-profit growth phase; ARR + NRR are the business. Rule of 40 = revenue growth % + FCF margin %; ≥40 is healthy, <30 is concerning. **P/E breaks for pre-profit names.** |
| Biotech (pre-revenue) | NPV pipeline | (no multiple) | No earnings; revenue lumpy. **rNPV** per asset = Σ(probability_of_success_adjusted_peak_sales × discount). LOE / patent-cliff modeled explicitly. |
| E&P (oil/gas) | EV/EBITDAX, NAV | FCF yield | EBITDAX adds back exploration expense (industry convention). NAV = PV-10 of proved reserves + risked probables. **EV/EBITDA without the X distorts comparability** between exploration-active and pure-PDP names. |
| Autos | EV/EBITDA, P/E | EV/Sales | Heavy operating leverage on volume. Through-cycle margin matters more than spot. R&D + capex normalize at OE/A factory level. |
| Airlines | EV/EBITDAR | P/E (cyclical) | Aircraft leases dominate cost structure; **rent-adjusted** EBITDA is the comparable metric across owned vs leased fleets. Pre-ASC 842 carriers benefit visibility-adjustment. |
| Asset managers | P/AUM, P/E | EV/EBITDA | AUM × fee rate = revenue; operating leverage is high but fee compression risk caps multiples. Mix shift (active vs passive vs alts) matters more than headline AUM. |
| Semis (cyclical) | P/E, EV/EBITDA | Mid-cycle normalized | Spot P/E misleads at trough (P/E artificially high on collapsed E) and peak (P/E artificially low). **Mid-cycle normalized earnings** anchor through-cycle. |
| Tech (mega-cap) | P/E, EV/FCF | EV/Sales | Profitable mega-caps with capex moats. **EV/FCF** captures real cash generation after capitalized R&D variants. |
| MedDev | EV/EBITDA, P/E | EV/Sales | Stable margins, pipeline-driven growth. Discount future product approvals separately if material. |
| Defense | P/E, EV/EBITDA | FCF yield | Government contract cycle (multi-year backlog) gives visibility; FCF yield checks working-capital strain from progress payments. |

**Anti-patterns**:
- Applying P/E to a bank — ignores capital structure, capital adequacy, and the fact that earnings are produced by the balance sheet you're trying to value
- Applying P/AFFO to non-REITs — meaningless (no analog construction)
- EV/Sales for a profitable mature business — discards the margin reality you should be defending
- P/E for a pre-revenue biotech — ill-defined, growth-rate sensitive past usefulness
- Spot P/E for a cyclical at trough — produces an apparently "expensive" stock that is actually mid-cycle cheap

---

## 3. Terminal value and method

### Perpetuity growth (Gordon)

```
TV = FCF_{T+1} / (WACC − g)
```

- **g (terminal growth)**: 2.0-2.5%. Aligned to US long-run nominal GDP (real GDP ~1.5-2% + Fed inflation target 2%). Above 3% is hard to defend in steady state.
- **Constraint**: `g < WACC` strictly. If g ≥ WACC, terminal value is infinite or negative — model is broken. Most often a symptom of either ERP set too low or g set too high.

### Exit multiple sanity check

Always cross-check Gordon TV against an exit-multiple TV:

```
TV = terminal_year_EBITDA × terminal_EV/EBITDA  (or P/E × earnings)
```

- **Terminal multiple**: long-run sector average (15-25y), NOT spot, NOT forward.
- Convergence check: implied EV/EBITDA from Gordon TV (= TV / terminal_year_EBITDA) should be within ±20% of the long-run sector mean. If not, one of the two TV methods is mispriced.
- **Anti-pattern**: terminal multiple > forward multiple with no rationale. Forward multiple incorporates near-term growth; terminal multiple should be at or below it because growth fades.

### TV as % of total EV

| TV / EV | Read |
|---|---|
| <40% | Model may be too conservative on terminal; check whether explicit forecast captures the steady-state |
| 50-70% | Healthy range |
| >75% | Model is over-reliant on terminal value; small changes in g produce big changes in price target |

Disclose TV / EV in the valuation appendix.

### Mid-year convention

- **Discount periods** for explicit FCFs: 0.5, 1.5, 2.5, ... (FCFs assumed to arrive on average mid-year, not end-of-year).
- **Terminal value discount**: use period (N − 0.5) for end of last explicit year if applying TV as of that point; or period N if TV is computed off year N+1 FCF and discounted from end of N.
- State which convention you use; differences are 4-5% of NPV.

---

## 4. Forecast horizon by company type

| Type | Explicit | Fade | Terminal |
|---|---|---|---|
| Mature stable (staples, utility) | 3-5y | none | perpetuity at g = 2.0-2.5% |
| Standard | 5y | none | perpetuity |
| High-growth (SaaS, growth tech) | 3y explicit | 7y fade to terminal margin/growth | perpetuity at g = 2.5% |
| Cyclical (autos, semis, materials, airlines) | 10y normalized | n/a | through-cycle steady-state; multi-cycle averaged |
| Biotech pre-revenue | Per-asset NPV through patent expiry (typically 10-15y) | LOE handled explicitly | no perpetuity — value decays to zero post-LOE absent pipeline |

**Cyclicals discipline**: use mid-cycle revenue and mid-cycle margin assumptions, not current-year run-rate. Specify the cycle phase (trough, mid, peak) and how the explicit forecast traverses it.

---

## 5. Multiple bands and historical context

A scenario's multiple must have a historical anchor. "Bear P/E = 15" is unanchored; "Bear P/E = 15 = NVDA 5y P5" is anchored.

### Pulling percentile bands

Sources:
- **YCharts** (premium): historical P/E, EV/EBITDA, P/B, P/AFFO, P/S percentiles with chart-rebase
- **Macrotrends** (free): `macrotrends.net/stocks/charts/<ticker>/<company>/pe-ratio` etc., trailing series
- **Bloomberg HMI** (premium): full multiple history with custom percentile bands
- **stockanalysis.com** (free): summary statistics
- **simplywall.st** (freemium): bands with peer context

### Required percentiles

For each chosen multiple, report:

```
P5 / P25 / median / P75 / P95
```

over a 5y window (default) or 10y (for cyclicals to capture cycle).

### Citation example

`(S5: NVDA 5y P/E P5/P25/median/P75/P95 = 28 / 35 / 45 / 58 / 72; YCharts pull [date])`

### Scenario-specific multiple assignment

| Scenario | Typical multiple band |
|---|---|
| Strong bear (A0 tail) | < P5 (de-rating beyond historical floor) |
| Bear | P5 to P25 |
| Base | P25 to P50 (or P50 to P75 if structural improvement is the base) |
| Bull | P50 to P75 |
| Strong bull | P75 to P95 |

When applying a multiple **above P95** or **below P5**, the memo must explain what structural change justifies stepping outside historical bands. "Just because" is not an answer.

### Anti-patterns

- Multiple band without source date (stale by definition)
- Same multiple across all five scenarios (defeats the purpose)
- Cycle-spanning percentile on a 2-year window
- Comparing today's P/E to "long-run average" without specifying base period

---

## 6. Comps construction

### Peer selection

- **Default**: same GICS sub-industry (Level 4). Pull the list directly from S&P GICS or your vendor.
- **Curated**: 5-10 hand-picked peers when GICS is too broad (e.g., NVDA's GICS includes hardware that aren't truly comparable; curated set might be: AMD, AVGO, ASML, AMAT, INTC, MRVL).
- **Cross-listed comparators**: for multinationals, include ADR or foreign-listed peers if economic exposure overlaps (e.g., BHP vs RIO vs VALE).
- **Exclusion criteria** (state explicitly): distressed names, names in active M&A, names with one-time accounting events.

### Required columns

Operating:
- LTM revenue, NTM revenue growth %, gross margin %, EBITDA margin %, FCF margin %, ROIC %

Valuation:
- EV / NTM EBITDA, EV / NTM Sales, P / NTM EPS, P / NTM AFFO (REITs), EV / ARR (SaaS), P / B (financials)

Statistics row:
- min / 25th / **median** / 75th / max — median is the anchor, not mean (means are skewed by outliers)

### Construction discipline

- **Same fiscal calendar**: align peers to comparable LTM or NTM periods. Mixing FY-end variants distorts comparability.
- **Same accounting basis**: GAAP vs non-GAAP must be flagged. If using non-GAAP EBITDA across peers, disclose which adjustments each peer makes.
- **Same currency**: USD-translate non-USD peers; disclose FX rate and date.
- **Exclude negatives**: a peer with negative EBITDA produces a meaningless multiple — exclude with a note, not the math.

### Free vs premium pathway

- **Premium**: Visible Alpha for granular consensus + line-item peer comps; Capital IQ Pro / FactSet for one-click peer multiples.
- **Free / EDGAR-only**: build manually from XBRL company facts (`data.sec.gov/api/xbrl/companyfacts/CIK*.json`), Yahoo Finance, stockanalysis.com. Delegate Excel artifact production to `financial-analysis:comps-analysis` if available (see `tool-composition-us.md`).

---

## 7. Precedent M&A

Useful for mature, M&A-active sectors (industrial roll-ups, consumer brands, midstream energy, regional banks); less useful for high-growth tech (rare strategic M&A at acquirer scale) or pre-revenue biotech (deal structure varies wildly with milestone-based contingents).

### Sources

- **Premium**: Capital IQ M&A module, SDC Platinum (LSEG), Mergermarket, PitchBook
- **Free**: SEC 8-K Item 1.01 (entry into material agreement) + 8-K Item 2.01 (completion); company press releases; trade press archives

### Rule of thumb

- **Control premium**: 25-35% over LTM unaffected trading levels (1-day, 1-week, 30-day VWAP)
- **Strategic vs financial**: strategic acquirers typically pay 5-10pts higher premium than financial sponsors due to synergy capture
- **Synergy disclosure**: in 8-K or merger proxy (DEFM14A) — extract run-rate cost synergy guidance and use as upside scenario

### When NOT to apply

- Pre-revenue or pre-profit names (no precedent EBITDA multiple)
- Sectors where M&A is regulated out (e.g., post-Hart-Scott-Rodino blocking precedent)
- Mega-cap names where no peer is large enough to acquire

---

## 8. LTM vs NTM vs forward

| Metric | Definition | When primary |
|---|---|---|
| **LTM (last 12 months)** | Trailing 4 quarters from latest 10-Q or 10-K | Backward-looking sanity; comparability when forwards are unreliable |
| **NTM (next 12 months)** | Rolling 12 months forward from memo date | **Default for valuation** in stable/growth names |
| **FY+1 / FY+2** | Specific fiscal year end (e.g., FY26E) | Useful when fiscal years differ across peers; explicit horizon |
| **Mid-cycle normalized** | Average through cycle (typically 7-10y) | **Default for cyclicals** — NTM is misleading at trough or peak |

**Discipline**: state explicitly which basis you use. "EV/EBITDA 12x" without basis is ambiguous; "EV / NTM EBITDA 12x (as of 2026-05-16)" or "EV / FY27E EBITDA 12x" is unambiguous.

---

## 9. Currency

Default reporting: **USD** per D11.

- ADR / foreign-issuer with native reporting currency (yen, EUR, GBP, etc.): native disclosure in appendix only. Translate to USD using the FX rate as of the memo date (cite FRED `DEXJPUS`, `DEXUSEU`, `DEXUSUK` etc.).
- **FX translation impact attribution**: for multinationals with material non-USD revenue (S&P 500 average is ~40%), disclose FX impact on YoY growth in the financials section. A 5% USD move can flip a name's growth rate.
- **Hedged vs unhedged**: if the company hedges, disclose hedge ratio and tenor; if not, mark FX as an unmitigated A0 tail.

---

## 10. Free cash flow definition (G12 hook)

Free cash flow is **not** a defined GAAP measure; every issuer defines it slightly differently. The G12 verification gate exists because "FCF" can be artificially inflated by definitional games.

### Required disclosure in the memo

State the FCF definition explicitly. Options:

| Definition | Formula | Notes |
|---|---|---|
| Standard | OCF − capex | Default; most defensible |
| SBC-deducted | OCF − capex − SBC | Conservative; matches buyback-adjusted real return |
| EBITDA-derived | EBITDA − capex − Δ WC − cash taxes | Bypasses GAAP working capital noise but misses non-cash items |
| Non-standard | Issuer-specific | Disclose every adjustment; treat with skepticism |

### B12 forensic flag

- If SBC is added back into FCF without a buyback offset adequate to fully neutralize dilution (`buyback_$ / SBC_$ ≥ 1.0`), the reported FCF overstates shareholder return.
- Track `buyback_offsets_sbc_ratio` in the memo financials section per `schemas/memo.json`.

---

## 11. Concrete examples

### NVDA (semis, high-growth tech)
- Primary: P/E with EV/Sales secondary. NOT mid-cycle normalized despite GICS being semis — the AI-accelerator pivot has detached NVDA from the cyclical-semis through-cycle math.
- 5y P/E bands required (P5/P25/median/P75/P95); apply scenario-specific multiple.
- High-growth fade DCF: 3y explicit + 7y fade to terminal growth 2.5%, terminal margin to long-run software.
- Capacity overlay (ADV-permitted position size) per quant overlay — large ADV permits larger position.

### JPM (commercial bank)
- Primary: P/B (target P/B = ROE / COE under steady-state) + P/E secondary. **NOT P/AFFO** (not a REIT). **NOT EV/EBITDA** (depository's earnings come from balance sheet).
- ROTCE > 15% sustains premium P/B; ROTCE 10-12% supports P/B 1.2-1.5x.
- CCAR / DFAST stress drives capital-return discipline (buyback + dividend capacity).

### SPG (REIT)
- Primary: P/AFFO with NAV secondary. **NOT P/E** (GAAP earnings depressed by real-estate D&A). **NOT EV/EBITDA without rent-adjustment**.
- AFFO = FFO − maintenance capex − straight-line rent adjustments. NAV = property-level cap rate applied to NOI by property class.
- Implied cap rate cross-check vs private-market transactions in same geography/class.

### DDOG (SaaS)
- Primary: EV / ARR with Rule of 40 anchor. **NOT P/E** (pre-meaningful-profit at scale phase). **NOT EV/EBITDA** (margin still scaling).
- NRR > 120% is healthy; <110% is concerning. CAC payback < 18mo is best-in-class.
- 3y explicit + 7y fade to terminal SaaS margin (30%+ FCF margin steady state).

### XOM (E&P / integrated)
- Primary: EV / EBITDAX with NAV secondary (PV-10 of reserves). **NOT EV/EBITDA without X** (distorts vs exploration-active peers).
- FCF yield as bear floor — capex discipline and dividend coverage are the bear story.
- Commodity price deck disclosed (Brent / WTI / Henry Hub) by scenario.

### MRK (large pharma)
- Primary: P/E on current franchise + NPV pipeline. NOT pure DCF (LOE on Keytruda dominates; pipeline replacement is binary and risk-adjusted).
- Per-asset rNPV including probability of approval, peak sales estimate, LOE date.
- Patent cliff scenarios as A0 tails.

---

## 12. Cross-references

- **Reconciliation discipline** (how DCF / Comps / SOTP / multi-multiple-bear cross-check, NEVER average): `three-method-valuation-us.md`
- **Scenario framework** (how 5 scenarios drive multiple selection): `five-scenario-framework-us.md`
- **GM taxonomy** (segment GM consistency check feeds SOTP audit): `gm-taxonomy-us.md`
- **Source stratification** (citation discipline for every multiple cited): `source-stratification-us.md`
- **Data sources** (FRED, Damodaran, YCharts URLs): `us-data-sources.md`
- **Tool composition** (delegate Excel DCF / Excel comps when premium plugins present): `tool-composition-us.md`
- **Forensic accounting** (non-GAAP/GAAP gap, SBC, FCF definition): `forensic-accounting-checklist-us.md`
- **Quant overlay** (ADV capacity constrains position from valuation conclusion): `quant-overlay-us.md`
- **Schema fields** (`dcf_components`, `valuation_method`): `schemas/memo.json`
