# Phase B0 Conformance Diff — Our Schemas vs. Official `equity-research` Plugin

The premise of D21's soft-dependency composition is that we delegate Excel/DOCX artifact construction to `claude-for-financial-services/equity-research:initiating-coverage` (Task 5 for DOCX) and `financial-analysis:dcf-model` / `comps-analysis` (for Excel artifacts). Before B0 commits the shared contracts, this document audits where we **conform** to their implicit contracts vs. where we **deliberately diverge** for buy-side rigor. This diff is the human-review gate per the user's stated requirement: "B0 must produce a printed diff against the official schemas before B1 starts using them."

## Headline finding

**The official `initiating-coverage` plugin has no formal JSON schema.** Its contract is at the file-format layer (Markdown + Excel + DOCX), not the schema layer. Task 5 (DOCX assembly) consumes:

1. `<Company>_Research_Document_<Date>.md` — 6-8K word qualitative narrative (Task 1 output)
2. `<Company>_Financial_Model_<Date>.xlsx` — 6-tab Excel with Bull/Base/Bear scenarios (Task 2 + Task 3 outputs)
3. `<Company>_Valuation_Analysis_<Date>.md` — 4-6 page valuation narrative with price target + recommendation (Task 3 output)
4. `<Company>_Charts_<Date>.zip` — 25-35 PNG/JPG charts at 300 DPI (Task 4 output)

There is no `memo.json` analog on their side. Their DOCX output structure is rigid (30-50pg, INITIATING COVERAGE format, 10-15K words) but the **input** is prose + Excel, not structured data.

**Implication:** we are NOT constrained to conform our `schemas/memo.json` to anything on their side. There's no schema collision because they have no schema. Our delegation contract is:
- Render our structured JSON → intermediate `.md` files matching their expected sections + an Excel model populated via `financial-analysis:dcf-model`
- Hand those to Task 5

This is documented as Phase B1 file: `us-equity-research/references/tool-composition-us.md`.

## Conformance table — per-element

| Element | Our schema | Official plugin | Conformance status | Notes |
|---|---|---|---|---|
| **Rating taxonomy** | 5-band (Strong Buy / Buy / Hold / Sell / Strong Sell) | 5-band (BUY / OUTPERFORM / HOLD / UNDERPERFORM / SELL) or simpler 3-band (BUY/HOLD/SELL) per Page 1 spec | **Deliberate divergence (label-level)** | Both are 5-band conceptually; their labels (Outperform/Underperform) are sell-side; ours (Strong Buy/Sell) are buy-side. Mapping is trivial: Outperform↔Buy, Underperform↔Sell. Per D1. |
| **Scenarios** | 5 (strong_bear/bear/base/bull/strong_bull) with probabilities sum to 1.00 | 3 (Bull/Base/Bear) with stated probability percentages | **Deliberate divergence (superset)** | 5 captures tail-vs-ordinary on each side. For delegation to `dcf-model` (which expects 3 cases), we collapse: Bear = strong_bear + bear (probability-weighted); Base = base; Bull = bull + strong_bull. Mapping documented in `memo.json/delegation_outputs/scenarios_3case_for_dcf_plugin`. |
| **Source citations** | S1-S5 + Pending stratification with inline first-use tags `(S2: NVDA FY24Q3 10-Q Note 4)` | URLs in appendix as clickable hyperlinks, no S-level | **Deliberate divergence (superset)** | Their citations are reader-navigation aids. Ours are rigor gates — anchor strength determines headline conditionality. Both can coexist: our S1-S5 tags appear inline in the rendered .md; the appendix URLs are derived from our `citation.url` field. |
| **Valuation methods** | Required ≥2: DCF + Comps; optional Precedent / SOTP / Multi-multiple bear | Required: DCF + Comps; Precedent transactions "if applicable" | **Conform on minimum + extend** | Our minimum matches theirs. SOTP and multi-multiple bear are buy-side additions for three-method reconcile discipline (per china-equity-ic-rigor port). Not required by their Task 5 — we just produce richer valuation block. |
| **DCF inputs** | WACC components (Rf, beta, ERP, cost of debt, tax rate, weights), terminal growth, explicit forecast years, sensitivity grid 5×5 | WACC components in CAPM form, terminal growth 2.0-3.0% default, 5-year explicit forecast, three sensitivity tables (WACC×TermGrowth, Rev×Margin, Beta×Rf) | **Conform** | Direct compatibility with `financial-analysis:dcf-model`. Our schema fields map 1:1 to their Excel inputs. |
| **Price target derivation** | Weighted-average across methods with weight_pct fields | Weighted-average across methods (DCF 50% / Comps 40% / Precedent 10% example) | **Conform** | Direct match. |
| **Football field** | football_field_range_low_usd / football_field_range_high_usd | "Football field" horizontal bar chart per method | **Conform** | We provide the range; they render the chart in DOCX. |
| **Catalysts** | 3-8 catalysts with date, type, expected_impact_pct, what_would_reverse | 3-5 catalysts with timeframes per Task 3 spec | **Conform on minimum + extend** | We may have more catalysts; their Task 5 picks top 3-5 for the recommendation block. The `what_would_reverse` and `anchor_ref` fields are buy-side additions, ignored by their renderer. |
| **Risk factors** | 8-15 with category enum (company_specific / industry_market / financial / macroeconomic / regulatory / geopolitical / esg), severity, mitigants | 8-12 in 4 categories (company / industry / financial / macroeconomic), 50-100 word each | **Conform on count + extend categories** | Our categories include `regulatory` / `geopolitical` / `esg` as separate (they fold these into `industry`). Mapping for delegation: collapse to 4 categories when rendering Task 1 risk section. |
| **Investment thesis pillars** | 3-5 with title, key_statistic, narrative ≥200 words, anchor_refs, timeline | 3-5 pillars, each 200-300 words, lead with key statistic | **Conform** | Direct mapping. |
| **Management bios** | 3-6 bios with name, title, tenure_years, bio ≥300 words, compensation, ownership | 3-4 bios at 300-400 words each | **Conform on bio length** | We allow 6 max; their template stops at 4. Take top 4 by relevance for delegation. |
| **Financial periods** | historical (3-5y) + LTM + projected (5+y) with full GAAP/non-GAAP split | 3-5y historical + 5y projected (no explicit LTM, no GAAP/non-GAAP split required) | **Superset** | Our non-GAAP/GAAP split feeds G11 verification. Their Task 2 doesn't require it; we provide both. |
| **Segments** | Per-period segment array with name, revenue, GM, gm_taxonomy_type (T1-T5), source | Revenue by product (20-30 rows) + Revenue by geography (15-20 rows) in Revenue Model tab | **Different cuts** | Theirs is product × geography; ours is reporting-segment × GM-taxonomy. Both can coexist. For delegation, render our segment data into their product/geography breakdown. |
| **Industry/TAM** | tam.current_tam_usd_b + projected_tam_usd_b + cagr_pct + source | TAM 500-700 words with sizing + segmentation | **Conform** | Direct mapping. |
| **Competitive landscape** | 5-10 peers with name, ticker, market_cap, market_share, differentiator, growth, margin + positioning_narrative | 5-10 competitors with market positioning + competitive advantages | **Conform** | Direct mapping. |
| **GM taxonomy** | 5-type box (T1 consolidated / T2 segment / T3 sub-segment / T4 modeled / T5 marginal) + reconciliation check | None | **Net-new (buy-side)** | Buy-side rigor addition. Not in their schema; ignored by their renderer. Drives G2 and G8 gates. |
| **Bear/bull EPS bridge** | Per-scenario eps_bridge array with named adjustments + soft/clean/strong layer | None — they don't bridge scenarios explicitly | **Net-new (buy-side)** | Drives G5 gate. |
| **Source-conditional headline** | conditionality enum (unconditional / source_conditional / range_only) + pattern enum (A/B/C/D) + headline_text | Their "Investment Update" headline is unconditional by default | **Net-new (buy-side)** | Drives G7 gate. Cannot be expressed in their schema; rendered inline in the headline text we provide. |
| **What-would-reverse triggers** | array with numerical_threshold + observable_via | None | **Net-new (buy-side)** | Drives G9 gate. |
| **Tail risks (A0 events)** | 5-12 events with probability_shift across scenarios + downside_impact | None — risk factors handle this | **Net-new (buy-side)** | Different concept: A0 events are probability-mass-shifters, distinct from idiosyncratic risk factors. |
| **Forensic flags** | ASC 606 red flags, ASC 842 lease PV, ASC 718 SBC %, non-GAAP/GAAP delta, FCF definition, goodwill, auditor, restatement, Form 4 net, going-concern, VIE, pension | None — partially folded into Risk Factors | **Net-new (buy-side)** | Drives G11, G12 gates. |
| **Positioning sentiment** | 13F clusters, short interest, options skew, ETF passive %, sell-side distribution, activist 13D, Form 4 pattern, index inclusion | None — they're sell-side, positioning is the audience, not the data | **Net-new (buy-side)** | Buy-side delta. |
| **Regulatory status** | Open antitrust matters, export control (BIS/OFAC/CFIUS), sector regulator open matters, tariff exposure, tax policy exposures | Partially via Risk Factors | **Net-new (buy-side, structured)** | They allow these in prose. We require structured fields. |
| **Position sizing by mandate** | 5 mandate types (long-only LC, long-only SMID, L/S HF, sector specialty, pair-trade) with active_weight_bps and conviction_adjusted_pct_nav | None — recommendation is "BUY $X target" with no sizing | **Net-new (buy-side)** | Per D3. Critical for institutional use. |
| **Quant overlay** | Barra factor tags, capacity (ADV + days-to-exit), edge decay, correlation placeholder, stress overlay | None | **Net-new (buy-side)** | Per D13. Drives G13, G14 gates. This is the key differentiator from sell-side initiation reports. |
| **Verification gates** | 14 gates with pass/fail status + evidence + remediation | None — they have a 130-line Step 7 quality checklist as prose | **Net-new (buy-side, structured)** | Their quality checklist is human-readable; ours is machine-checkable. Drives Phase C verification scripts. |
| **Audience variants** | enum (institutional_full / ic_preread / ic_debate_script / lp_letter / earnings_prep / earnings_flash / kill_memo) | One variant (institutional DOCX initiation report) | **Net-new (buy-side, multi-audience)** | Per D4. Bilingual variants dropped; LP letter added; retail dropped. |

## Three lists per the user's earlier ask

### (1) Where we conform to Anthropic's shape for interop

- 5-band rating (label translation is trivial)
- Required valuation methods: DCF + Comps minimum
- DCF inputs: CAPM-style WACC, terminal growth 2-3%, 5y forecast, 5×5 sensitivity tables
- Weighted-average price target across methods
- Risk factors count: 8-12
- Investment thesis pillars: 3-5
- Management bios: 3-4 (we cap at 6; delegation takes top 4)
- 3-5y historical + 5y projected financials
- Revenue by product (20-30 rows) + Revenue by geography (15-20 rows) — we produce both during delegation rendering
- Catalysts: 3-5 in recommendation block

### (2) Where we deliberately diverge because the official plugin is too shallow

- **5-scenario probabilistic framework** (vs their 3-case). Mapped to 3-case at delegation boundary; preserved 5 internally for proper P10/P90 calibration and tail-vs-ordinary distinction.
- **S1-S5 source stratification with inline first-use tags** (vs their appendix URLs). Their citation discipline is presentation; ours is rigor.
- **Source-conditional headline language** when anchors are S3 or weaker (vs their unconditional headline). Critical for not over-claiming on weak data.
- **GM taxonomy + segment reconciliation gate** (vs no concept). Catches the GM-definitions-mixing bug.
- **Bear/bull EPS bridge with named adjustments + soft/clean/strong layers** (vs no concept). Forces showing the work behind scenario EPS.
- **What-would-reverse with numerical denominators** (vs no falsification framework). The IC-defensibility test.
- **A0 tail catalog with probability-mass shifters** (vs no concept). Lets PM see how tails reshape distribution.
- **Position sizing by 5 mandate types** (vs no sizing). Decouples rating from sizing.
- **Quant overlay (Barra factors + capacity + edge decay)** (vs no concept). Buy-side institutional table-stakes.
- **14 machine-checkable verification gates** (vs their prose quality checklist). Bugs that kill memos in IC are mechanical; ours catches them programmatically.
- **Multi-audience derivatives** (institutional / IC preread / IC debate / LP letter / earnings prep / earnings flash / kill memo) (vs single DOCX initiation report). Different audiences need different shapes.

### (3) Where the official plugin reveals a gap in our Phase A that we should backfill before B1 freezes

- **Charts.zip with 25-35 PNGs at 300 DPI** — the official Task 4 produces 25-35 specific charts (revenue by product, revenue by geography, DCF sensitivity heatmap, valuation football field, etc.). Our Phase A delta matrix does not enumerate which charts our orchestrator must produce. **Backfill to do in B1:** add a chart-list to `tool-composition-us.md` listing the 4 mandatory + 25 required chart names so the orchestrator knows what to render when delegating to Task 4.
- **Revenue by product (20-30 rows) and Revenue by geography (15-20 rows) in Excel form** — required by Task 2 of `initiating-coverage`. Our Phase A doesn't specify these breakdown widths. **Backfill:** add to `financials.revenue_by_product` and `financials.revenue_by_geography` discipline in `phase-1-deep-dive-us.md`.
- **Quality checklist as prose** — their Step 7 has a 130-line human-readable checklist (LENGTH / PAGE 1 FORMAT / SECTION WORD COUNTS / CITATIONS / etc.). Our 14 verification gates cover the rigor side but miss the formatting side. **Decision (to be ratified):** keep formatting checks out of `verification_gates.json` (they're not buy-side rigor gates) but reference their checklist as the formatting QC for any delegated DOCX. Add to `tool-composition-us.md`.
- **Investor Day presentations as an S3 source type** — their template implicitly leans on Investor Day decks. Our `us_source_type` enum has "Investor day deck" — good, no backfill needed.
- **Customer concentration % and net retention rate** — their template's "Customer Economics" section asks for LTV/CAC, net retention, churn. Our `financial_period` doesn't carry these explicitly. **Decision:** add `customer_metrics` sub-object to `financial_period` in a B0.1 amendment, OR leave to the qualitative `company_qualitative.customers_gtm` field. Recommend the latter for B0 to keep schemas tight; revisit in B2.

## Decisions ratified in this audit

1. **No changes to schemas/memo.json or sub-schemas required** to enable delegation. The intermediate rendering layer (B1: `tool-composition-us.md`) handles the format adaptation.
2. **5→3 scenario collapse** is the only structural translation needed. Encoded in `memo.json/delegation_outputs/scenarios_3case_for_dcf_plugin`.
3. **Label translations** (Strong Buy ↔ Outperform; etc.) are renderer-side concerns, not schema concerns.
4. **Our schemas are a strict superset** of the implicit input contract. Subsets render cleanly to their format; supersets are ignored.
5. **The three gaps to backfill** (chart list, revenue breakdown widths, prose quality checklist) are documented and assigned to B1 (`tool-composition-us.md`) and B2 (`phase-1-deep-dive-us.md`).

## Risks identified

- **Their plugin evolves.** If `initiating-coverage` changes its Task 5 input shape, our delegation contract breaks silently. **Mitigation:** Phase F packaging includes a version-pin clause in our `plugin.json` `requires` block declaring tested-against version.
- **Their plugin's Task 1 / Task 4 are very prescriptive** (6-8K words, 25-35 charts at 300 DPI). If our orchestrator can't render at that fidelity, delegation produces low-quality DOCX. **Mitigation:** make delegation strictly opt-in via user request; fallback to Markdown-only.
- **Their scenarios use percentages with no probability normalization check.** Their 3-case is Bull/Base/Bear with stated %s but no enforcement that probabilities sum to 100. Our G4 gate catches this; theirs doesn't. Not a blocker but worth noting if a user uses their plugin standalone.

## Final B0 status

Schemas frozen. File ownership documented. Conformance audit complete. Backfill items assigned to B1/B2.

**Phase B0 is ready to commit.**
