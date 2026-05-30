---
name: us-equity-ic-rigor
description: Layer PM-grade IC-deliverable rigor on top of us-equity-research for institutional buy-side workflows on US-listed equities (NYSE/Nasdaq/AMEX/OTC tickers, plus ADRs via 20-F/6-K). Use whenever the user wants an IC memo, IC pre-read, IC debate script, LP letter, earnings prep, earnings flash, or kill memo, OR is iterating an existing memo through PM red-team review cycles ("score this memo", "PM red-team this", "find what is broken", "round N", "round N review", "push from 8.x to 9.x", "push from 8.5 to 9.0"). Also use when the user references the S1-S5 source stratification, five-scenario probabilistic framework (strong_bear/bear/base/bull/strong_bull), three-method reconcile (DCF / Comps / multi-multiple bear / SOTP), GM taxonomy (T1 consolidated / T2 segment / T3 sub-segment / T4 modeled / T5 marginal), bear EPS bridge, what-would-reverse triggers with numerical denominators, A0 tail mapping, anchor sensitivity, Barra factor exposure (Value/Quality/Momentum/Growth/Size/Low-Vol/Liquidity), capacity / days-to-exit at 10-20-30% ADV participation, position sizing across five mandate types (long-only LC, long-only SMID, L/S HF, sector specialty, pair-trade), or any of the 17 verification gates G1-G17 (G15-G17 added in v0.2.0: consensus variance / bank discipline / revision velocity). Also use when the user references multi-audience derivatives ("IC pre-read", "IC debate script", "LP letter", "kill memo", "earnings prep", "earnings flash"). Triggers on PM-style pushback language during a critique session: "the math doesn't add up", "where does X come from", "this is hand-wavy", "you can't make that claim without an S1", "Pending should not be a headline anchor", "the bridge doesn't reconcile", "your segment GM doesn't tie", "non-GAAP without GAAP", "FCF without SBC". Enforces the 14 verification gates that catch the bugs real PMs flag — EPS times multiple rows that do not multiply (G1), segment GM that does not reconcile (G2), SOTP where NI exceeds GP (G3), scenario probabilities that do not sum to 1.00 (G4), bear bridges that do not reconcile to base (G5), unsourced specifics (G6), unconditional headlines on S3-or-weaker anchors (G7), mixed GM definitions (G8), what-would-reverse triggers without numerical denominators (G9), missing anchor weighting impact table (G10), non-GAAP without GAAP reconciliation (G11), SBC excluded from FCF without flag (G12), missing Barra factor exposure (G13), missing capacity / ADV / days-to-exit (G14). English-only output; retail and bilingual variants intentionally dropped per D4.
---

# US Equity IC-Rigor

This skill is the **PM red-team layer** on top of `us-equity-research`. Use the base skill to do the underlying multi-agent research (Phase 0 below); use this one to harden the deliverable to the standard a buy-side PM will sign off on.

The core insight encoded here: an institutional-grade IC memo survives PM challenge not because it has a strong view, but because **every specific number is sourced (S1-S5), every transformation reconciles (segment GM ties to consolidated, bear bridge ties to base, EPS × multiple ties to target price), every headline acknowledges what it's contingent on (source-conditionality when anchors are S3 or weaker), every "what would reverse it" trigger has a numerical denominator (per G9), and every position recommendation discloses its factor exposure (per G13) and capacity profile (per G14)**. The bugs that kill a memo in IC are almost always mechanical — math doesn't multiply, definitions don't match, anchors aren't verified, non-GAAP doesn't reconcile to GAAP, FCF silently excludes SBC — not directional.

This skill imports the IC-rigor pattern from `china-equity-ic-rigor` and ports it to US conventions: SEC EDGAR primary disclosure (10-K/10-Q/8-K/DEF 14A/20-F/Form 4/13D/13F), USD reporting, 5-band rating (Strong Buy / Buy / Hold / Sell / Strong Sell with ±10/±20% bands per D1), Damodaran ERP and 10Y UST risk-free, sector-branched valuation multiples (P/E mature, EV/EBITDA leveraged, EV/ARR + Rule of 40 SaaS, P/B + ROE banks, P/AFFO + NAV REITs, NPV pipeline biotech, P/AUM asset managers — see D8). Four US-specific verification gates G11-G14 are added on top of the inherited G1-G10. Quant overlay (Barra factor tags, capacity, edge decay, correlation placeholder, stress overlay) is **mandatory in every institutional memo** per D13.

## When to use this skill

Trigger when ANY of the following appear, even in passing:

- US ticker (NYSE/Nasdaq/AMEX/OTC, 1-5 uppercase chars, optional .B for share class) + "IC memo", "investment memo", "opinion letter", "PM red-team", "score this"
- Score-band language: "round N review", "push from 8.x to 9.x", "what would push this from 8.5 to 9.0", "score this memo"
- Framework refs: "S1-S5", "five-scenario", "three-method reconcile", "GM taxonomy", "bear bridge", "what-would-reverse", "A0 tail", "anchor sensitivity", "Barra factor exposure", "capacity / days-to-exit"
- Headline-language requests: "median expected return", "P10/P90 range", "scenario-weighted [low, high]", "conviction tag", "default action", "source-conditional headline"
- Multi-audience derivatives: "IC pre-read", "IC debate script", "LP letter", "earnings prep", "earnings flash", "kill memo"
- The user is critiquing a memo and the language sounds like a PM: "the math doesn't add up", "where does this number come from", "this is hand-wavy", "you can't make that claim without an S1", "Pending should not be a headline anchor", "non-GAAP without GAAP", "FCF without SBC", "factor exposure?", "what's the ADV?"
- The user is asking for a falsification test: "what would reverse this", "what's the kill trigger", "what breaks the thesis"

If the request is for *initial fundamental research* on a US name (no opinion-letter framing yet), use `us-equity-research` directly. Add this skill once the memo construction or red-team phase begins.

## Scope and Limitations (what the 17 gates actually verify, and what they don't)

The 17 verification gates plus the 6.0-9.0+ rubric in `pm-redteam-rubric-us.md` enforce **mechanical correctness and structural completeness**. A 9.0-scored memo from this skill means: the math reconciles, every specific number is sourced, every claim has an evidence chain, every scenario has a named anchor, and every "what would reverse" trigger has a numerical denominator. **A 9.0 does not mean the view is right.** The gates and rubric grade institutional aesthetic and mechanical defensibility, not predictive value.

**What the rubric CAN tell you:**

- The memo's math is internally consistent (G1, G2, G3, G4, G5).
- Every specific number is sourced and the sources are stratified at the correct S-level (G6, G7).
- Definitional discipline holds — GM taxonomy is explicit (G8), non-GAAP reconciles to GAAP (G11), FCF discloses SBC treatment (G12).
- The scenario weighting is mathematically valid and the headline conditionality matches the anchor strength (G4, G7, G10).
- The position sizing is internally consistent across mandates and includes the quant overlay required disclosures (G13, G14).
- The memo declared a specific non-consensus variance OR honestly self-labeled "consensus-anchored" (G15, added v0.2.0).
- For banks specifically, the AOCI bridge, CET1 walk, NIM trajectory, and stress capital context are present (G16, v0.2.0).
- Earnings revision velocity is disclosed when coverage is non-thin (G17, v0.2.0).

**What the rubric CANNOT tell you (despite what the score might suggest):**

- Whether the analyst correctly identified the load-bearing assumption. A memo can pass G5 (bear bridge reconciles) while its bear case is built on the wrong sources of downside.
- Whether the declared consensus variance is *defensible*. G15 verifies that a variance is *declared* with structurally adequate evidence; it does not test whether the evidence is interpreted correctly or whether Street has read the same source and reached a different conclusion via legitimate disagreement rather than oversight. **G20 (v0.3.0) tightens this** by requiring the variance to differ from consensus by a configurable threshold AND requiring R-v2 to attempt structured attack — but G20 still cannot verify "the analyst is right." It verifies "the analyst's claim survived attack."
- Whether the scenario probabilities reflect a realistic prior given disclosed positioning. The framework prescribes how strong_bear / strong_bull map to anchor strength, but it does not test whether the assigned probabilities match the implied dispersion in Street PTs or the implied distribution in options skew. A memo can pass G4 (probabilities sum to 1.00) with any internally-consistent distribution that the analyst chooses.
- Whether the Barra factor tags, edge decay fields, conviction multipliers, or correlation overlay are computed against a real factor model. **They are not.** The quant overlay produces directional estimates the analyst asserts, not regression outputs. **G18 (v0.3.0) tightens this** by checking cross-document consistency (same name must carry same Barra z-scores across scenarios / position-sizing / quant-overlay docs) — but G18 still cannot verify "the z-scores are right." For real factor exposure, use a sister plugin with calibrated factor feed (not built as of v0.3.0).
- Whether the memo was actually produced by Plugin 1's orchestrated multi-agent workflow or hand-authored to satisfy the schemas. **G19 (v0.3.0) closes this** by requiring a provenance manifest written by Plugin 1; memos without the manifest pass with `--hand-authored` flag set and score capped at 7.5.

**What the gates STRUCTURALLY cannot tell you (category limits):**

- Whether the alpha lives in timing / flow / positioning rather than fundamentals. The gates check fundamental discipline; they do not manufacture the data needed for positioning edge. See the Scope and Limitations section in `us-equity-research/SKILL.md` for the list of use cases where this skill is category-wrong.
- Whether the memo's view is predictive of forward returns. There is no backtest of the 20 gates against historical names. The forensic flags (G11, G12) and consensus discipline (G15) are *theoretically motivated*, not *empirically validated*. The framework is defensible but unproven.

**Honest framing for external positioning.** When pitching this skill to a buy-side audience, the accurate claim is: "we built a verification layer that catches the mechanical and definitional defects that destroy IC memos — math that doesn't multiply, segment GM that doesn't reconcile, non-GAAP without GAAP, FCF without SBC, headlines unconditional on weak anchors, ratings unconditional on consensus variance, banks-sector memos missing AOCI bridge. A memo that passes these gates is non-fraudulent in its claims. It is not automatically alpha-generating." Anything stronger — "the framework finds non-consensus opportunities," "the gates predict alpha," "9.0 means defensible" — is overclaim.

## Workflow

The work proceeds in six phases (0 through 5). Phases 0-3 produce the institutional version. Phase 4 hardens it through the PM red-team loop. Phase 5 derives audience variants. Phases can interleave when the user explicitly directs it ("build the institutional and IC pre-read in parallel"). Per D7, the underlying research phase structure is preserved 1:1 from China — parallel specialization is the architectural value.

### Phase 0 — Foundational research (delegate to us-equity-research)

Use the sister skill `us-equity-research` to produce: industry context, SEC-filed financials (10-K / 10-Q / 8-K / DEF 14A / 20-F as relevant), regulatory desk read (FTC / DOJ / state AGs / EU CMA / BIS / OFAC / CFIUS / sector regulators per D12), positioning desk (13F clusters, Form 4 net, short interest, options skew, ETF passive %, sell-side distribution, activist 13D), forensic accounting (ASC 606 / 842 / 718, non-GAAP/GAAP delta, SBC treatment, goodwill, auditor history, restatement history), and a sector-appropriate baseline valuation per D8. Web-verify any post-cutoff claims with EDGAR full-text search + WebSearch; mgmt guidance verified against the **earnings call transcript** (S3 authoritative), not the press release. Phase 0 minimum: 12 WebSearch+WebFetch calls per D9, run in EDGAR-only mode by default per D5 (premium hooks for Visible Alpha / Capital IQ / AlphaSense / Bloomberg gated behind explicit user opt-in).

The output of Phase 0 is raw material — not yet shaped into the IC framework.

### Phase 1 — Source stratification gate

Before writing any specific number into the memo, classify it on the **S1-S5 + Pending** scale and decide whether the gate lets it through. See `references/source-stratification-us.md` for the full taxonomy, decision rules, and the conditional headline language patterns (A / B / C / D). The short version:

- **S1** = audited 10-K / 20-F (PCAOB-registered auditor, SOX 404(b) ICFR opinion, ASC-compliant) → use freely
- **S2** = unaudited public filing: 10-Q, 8-K (note Item 4.02 restatement is high-info; Item 8.01 other is junk-prone), DEF 14A, S-1/S-3/S-4, 13D/13G/13F, Form 4, 6-K → use freely with citation
- **S3** = earnings call transcript, mgmt guidance (Reg FD § 17 CFR 243 same-day broad distribution), Investor Day deck, IR commentary → use with "per management" framing; verify against the call, not the press release
- **S4** = Visible Alpha / FactSet / Bloomberg / Refinitiv IBES consensus, sell-side notes; or free-aggregator fallback (Yahoo Finance, StockAnalysis.com, WSJ Markets). Use **median + dispersion**, not mean. US sell-side coverage is denser than China — typical large-cap has 20-40 analysts
- **S5** = Gartner / IDC / IHS Markit (S&P Global) / Counterpoint / Omdia / NielsenIQ / Circana / Yipit / Second Measure / Placer.ai / SimilarWeb / expert networks (GLG, Tegus, AlphaSights, Third Bridge). Always disclose provider, methodology, sample, freshness
- **Pending** = unverified rumor, unsourced specifics, post-cutoff claims you couldn't verify within the current run → DO NOT promote to a headline anchor; if it must appear, mark `(Pending — not used as anchor)`

The hard rule per G7: **if any of the top-3 anchors is S3 or weaker, the headline must be source-conditional**. `headline_conditionality` in `schemas/source_tags.json` is computed from top-3 anchor strength and is enforced programmatically by `scripts/verify_headline_conditionality.py`. Conditional language patterns translate from China naturally — see references for English equivalents.

Citation format at first use (per D16, English-localized): `(S1: NVDA 2024 10-K Item 7)`, `(S2: NVDA FY24Q3 10-Q Note 4)`, `(S3: NVDA FY24Q4 earnings call 2025-02-26, ~22min mark)`, `(S4: Visible Alpha NVDA DC rev FY26E, n=42, median $X, range $Y–$Z)` or `(S4: Yahoo Finance consensus EPS $X)`, `(S5: Gartner DC GPU forecast 2026/03)`, `(Pending — not used as anchor)`.

### Phase 2 — Build the analytical pillars

Five pillars, each with its own discipline document. Construct them in parallel when possible; they cross-check each other.

- **5-scenario probabilistic framework** — strong_bear / bear / base / bull / strong_bull, probabilities sum to 1.00 ±0.01 (G4), each scenario has its own EPS path AND its own multiple AND its own narrative bridge AND its own driving anchors AND its strongest-anchor S-level. Multiple type is sector-branched (P/E mature, EV/EBITDA leveraged, EV/ARR SaaS, P/B banks, P/AFFO REITs, NPV biotech, EV/EBITDAX E&P, EV/EBITDAR airlines, P/AUM asset managers). See `references/five-scenario-framework-us.md` and `schemas/scenarios.json`.
- **Three-method valuation reconcile** — DCF + Comps minimum (matches official `equity-research:initiating-coverage` for delegation interop); optional SOTP + multi-multiple bear (P/B for banks, EV/EBITDA for mature industrial, EV/Sales for high-growth, EV/FCF for capex-heavy mature, FCF yield as bear floor). These are **cross-checks, not three independent fair values to average**. SOTP exists to test segment-level internal consistency, not to price the stock. Multi-multiple bear is the floor check. DCF is the cash-flow rigor anchor. WACC discipline: Rf from 10Y UST (FRED `DGS10`), ERP from Damodaran implied US, beta basis declared (`5y_monthly_vs_SP500` or industry unlevered), cost of debt as after-tax. Terminal growth 2.0-2.5% (US nominal GDP-aligned). 5×5 sensitivity tables for WACC × terminal-g, revenue × margin, beta × Rf. See `references/three-method-valuation-us.md`.
- **GM taxonomy discipline** — five distinct GM concepts (T1 consolidated / T2 segment / T3 sub-segment / T4 analyst-modeled / T5 marginal) and mixing them is the #1 cause of red-team rejection. The taxonomy box must appear somewhere in the memo (G8) and segment-weighted GM must tie to consolidated within ±50bp (G2). In US filings, add **non-GAAP GM parallel discipline**: track GAAP GM and non-GAAP GM (excluding SBC, amortization of acquired intangibles, restructuring) as separate T1 entries when both are cited. See `references/gm-taxonomy-us.md`.
- **Bear EPS bridge** — three-layer construction (soft / clean / strong adjustments) so the reader can see exactly which assumption is doing the work. Named adjustments must sum to (base_eps − bear_eps) within rounding (G5). US-specific named adjustments include "SBC headwind +$X", "Buyback offset −Y%", "Section 174 R&D amortization headwind", "Tax rate normalization +Zbp", "Non-GAAP-to-GAAP conversion". Symmetric construction for bull. See `references/bear-bridge-us.md`.
- **What-would-reverse triggers** — every directional view (bear, bull, neutral) must have a falsification trigger with a numerical denominator (G9): not "if margins recover" but "if Q4 datacenter revenue > $40B and consolidated non-GAAP GM > 75% for two consecutive quarters". Each trigger names the specific observable (10-Q Note, next earnings call, consensus refresh, FRED series, Form 4 cluster, FDA decision letter, etc.). See `references/what-would-reverse-us.md`.

### Phase 3 — Construct headline + valuation

Output the institutional version of the IC memo. The 12-section template lives in `templates/opinion-letter-section-checklist-us.md` (authored in Phase B2). All deliverables are Markdown per D15 (docx is delegated optionally per D21; see Output discipline below). The non-negotiables:

- **Headline contains**: 12-month median expected return, P10/P90 scenario-weighted range, 5-band rating (Strong Buy / Buy / Hold / Sell / Strong Sell per D1), conviction tag (high / moderate / low / source-conditional / reactive), default action (initiate_long / add_long / hold_long / trim_long / exit_long / initiate_short / add_short / hold_short / cover_short / no_action / spread_long_short), and the **source-conditionality flag** if any top-3 anchor is S3 or weaker (G7).
- **Anchor weighting impact table (G10)**: show how the headline median return shifts if the strongest scenario's probability moves ±10pp toward bear or bull. This is what gets challenged in IC; have it in the doc, not in your head.
- **A0 tail risk mapping**: per D12, six standing A0 events (NBER recession, Fed rate shock ±200bp, sector regulatory action via FDA/FCC/FERC/NHTSA/EPA/FAA/CFPB/FTC/DOJ, sanctions/export control via BIS/OFAC/CFIUS, tariff/trade war via Section 301/232, election/political transition) plus 2-3 idiosyncratic A0s specific to the name (e.g. for NVDA: hyperscaler capex cycle inflection, MI400 share gain, customer concentration risk; for JPM: NII normalization, CCAR stress; for MRK: Keytruda LOE; for REITs: occupancy / cap-rate gapping). For each A0 show probability shift across the 5 scenarios and worst-case EPS / multiple / price impact. See `references/tail-risk-mapping-us.md`.
- **Volatility math + position sizing**: σ → weekly / monthly / quarterly 1σ and 2σ envelopes; Sharpe and Kelly translated to a **conviction-adjusted position size** with multiplier in the 0.10× to 0.50× range per D6 (S1-S2 multi-cycle = 0.50×; mixed S1-S3 recent = 0.25-0.35×; S3-S5 dominant or source-conditional = 0.10-0.20×; heavy tail exposure halves further). Sized across **5 mandate types** per D3: long-only large-cap (vs S&P 500), long-only SMID (vs Russell 3000 / 1000 / 2000), L/S hedge fund (gross/net exposure, single-name caps), sector specialty (vs sector ETF or custom basket), and pair-trade (long ticker / short ticker, structure: dollar-neutral / beta-neutral / value-neutral / ratio). Rating is decoupled from sizing — "Buy" with "hold_long" default action is valid (already at target weight). See `references/position-sizing-us.md`.
- **Quant overlay (mandatory per D13)** — Barra-style factor tags (Value / Quality / Momentum / Growth / Size / Low-Vol / Liquidity, each on −2 to +2 z-score), capacity analysis (30-day ADV in USD millions; days-to-exit at 10% / 20% / 30% participation; max position constrained by ADV as % NAV), edge decay (thesis half-life, time-to-priced-in, refresh cadence, primary decay driver), correlation overlay (placeholder per D14 — book file path declared, live wiring deferred), stress overlay (Fed funds +200bp, oil −20%, USD +5%, recession dummy — stock % impact for each). The full discipline lives in `references/quant-overlay-us.md` (Phase D file). Verified by G13 (factor tags present) and G14 (capacity present).

### Phase 4 — PM red-team review loop

This is the iteration that takes a memo from "looks good" to actually defensible. Run the 17 verification gates programmatically (scripts in `scripts/` — v0.1.x grandfathered to 14), then score on the rubric in `references/pm-redteam-rubric-us.md`. The gate verification is non-negotiable: a memo cannot claim score >8.0 with any gate failing; critical math gates G1 (EPS × multiple multiplicativity) and G3 (SOTP monotonicity) cap at 7.0 when they fail, as do G15 (consensus variance) and G16 (bank discipline). The Phase E success criterion per D20 is score ≥ 8.5 with all applicable gates exit 0 against the structured JSON.

Score-band fix lookup (preserved from China rubric, extended with US bug classes B11-B14):

- **6.0-7.5 — mechanical bugs**: run the 14 verification scripts. Most failures here are G1 (EPS × multiple does not multiply), G2 (segment GM does not reconcile), G3 (SOTP NI exceeds GP), G4 (probabilities do not sum to 1), G5 (bear bridge does not reconcile), G6 (specifics not source-tagged), G11 (non-GAAP cited without GAAP reconciliation), G12 (FCF cited without SBC treatment disclosed). Fix the math / source / reconciliation, re-run gates, re-score. Memos in this band almost always have at least one of the critical-math gates failing — the fix is mechanical, not narrative.
- **7.5-8.5 — narrative coherence**: directional view holds but anchor weighting is off, GM taxonomy mixes types (G8), the layered bear bridge has unlabeled or implicit assumptions, or denominators are loose (G9 borderline). Common at this band: scenario narratives inconsistent with their anchors (e.g. base case cites Visible Alpha consensus but the narrative imagines hyperscaler capex growth above the consensus implied path), two pillars contradicting each other (e.g. three-method reconcile yields $X but DCF alone yields $1.4X with no narrative explaining the gap), headline median return out of sync with the probability-weighted table arithmetic.
- **8.5-9.0 — IC-grade hardness**: the memo is defensible but not airtight. Look for the issues PMs catch in IC: A0 catalog completeness (all 6 standing + 2-3 idiosyncratic, with probability shifts across the 5 scenarios), three-method reconcile narrative (not just three numbers; the *why they agree or disagree* story — e.g. "DCF says $X because of the explicit FCF path; comps say $0.9X because the peer set is mid-cycle and we are near peak; SOTP says $1.05X because segment Z is mispriced standalone"), source-conditional language matching anchor strength (G7) — every weak anchor reflected in the headline qualifier, position sizing math shown across all 5 mandate types with conviction adjustment explicit, specific action articulated (not "we like this name" but "initiate at 60bp active vs S&P 500, max 120bp on Q4 print confirming DC > $40B with non-GAAP GM > 75%").
- **9.0+ — IC-ready**: polish. Headline cadence, table-to-narrative cross-reference (every table referenced from the prose), appendix completeness (full anchor list with verification timestamps, all S-tags, all G-gate exit codes), audience variant rendering coherent with institutional headline.

The bug catalog B1-B14 in `references/pm-redteam-rubric-us.md` maps each bug class to its gate, score impact, and remediation. B1-B10 are inherited from the China rubric (B1 unit confusion / B2 anchor strength misclassification / B3 scenario weight inconsistency / B4 bridge non-reconciliation / B5 GM taxonomy mixing / B6 segment-to-consolidated drift / B7 SOTP inversion / B8 headline unconditional on weak anchors / B9 trigger handwave / B10 missing anchor sensitivity); B11-B14 are US-specific additions: **B11 = Non-GAAP/GAAP gap not reconciled** (G11), **B12 = SBC not deducted from FCF without explicit flag** (G12), **B13 = Factor exposure unstated** (G13), **B14 = Capacity / ADV / days-to-exit unstated** (G14). **v0.2.0 adds B15-B17**: **B15 = Non-Hold rating without declared load-bearing consensus variance OR explicit "consensus-anchored" headline label** (G15), **B16 = Banks-sector memo missing AOCI bridge + CET1 walk + NIM trajectory + stress capital context** (G16), **B17 = Revision velocity not disclosed when coverage is non-thin (n_analysts ≥ 5)** (G17). The pm-redteam-rubric-us.md reference file will be extended in a follow-up to detail B15-B17 remediation; for v0.2.0 the gate scripts + reference files in Plugin 1 carry the operational discipline.

We do not cite specific historical PM-red-team rounds in this skill because the US methodology stands on the rubric and gate catalog, not on archived case histories. Each new memo runs through the same loop; iterate until score ≥ 8.5 or until three iterations are exhausted (per BUILD_PROMPT Phase E failure handling). The PM red-team loop is the value of the skill — it is not optional.

### Phase 5 — Multi-audience derivatives

After the institutional version stabilizes, build the audience variants. Don't write them in parallel before the institutional version is locked — they all depend on the institutional headline and they will all need to be re-keyed if the institutional headline moves. Per D4, the audience set is institutional / IC pre-read / IC debate script / LP letter / earnings prep / earnings flash / kill memo. **No retail variant.** **No Chinese-language variant.** FINRA Rule 2210 / SEC Reg BI retail-comms compliance is out of scope.

- **Institutional full** — the 12-section memo. The source of truth. All derivatives flow from this.
- **IC pre-read (≤4 page)** — strip narrative; keep headline, scenario table, three-method reconcile summary, what-would-reverse triggers, key risks (top 5), position sizing one-liner, quant overlay summary. Do NOT change numbers; if a number changes here it must propagate back to institutional.
- **IC debate script** — verbal-form: company fundamentals → research methodology → logic chain → anchor evidence → valuation → caveats → 8 likely PM challenges with answers. Timing markers (3min / 5min / 10min variants).
- **LP letter (1-2 page client-facing)** — quarterly LP-letter cadence: attribution narrative, change-in-view since prior letter, position sizing and rationale, what-would-reverse summary, position-level risk in plain language (no S-tags, no Barra factors in surface text). Replaces China's retail variant per D4.
- **Earnings prep** — night-before checklist: consensus snapshot (median + range, dispersion), KPI guide (segment revenue, GM, FCF, guide range), management-commentary watch list (5-7 named items from prior calls), beat/miss scenario tree with 3-6 month implied moves, pre-announcement risk flag.
- **Earnings flash (T+30 min)** — same-day structured response: beat/miss vs consensus on each tracked KPI, guide vs prior, segment color, KPI-by-KPI verdict, headline change (yes/no/conditional), gate-affected anchors list, next-action recommendation.
- **Kill memo** — falsification-triggered exit rationale: which what-would-reverse trigger fired, the evidence (specific S-source), revised headline, exit timing, post-mortem of view (what assumption broke and which layer of the bear/bull bridge it lived in).

Derivation patterns and templates lookup in `references/multi-audience-delivery-us.md`. Templates themselves live in `templates/`: `opinion-letter-section-checklist-us.md`, `ic-debate-script-template-us.md`, `lp-letter-template.md`, `earnings-prep-template.md`, `earnings-flash-template.md` (all authored in Phase B2).

## Verification gates (17 gates as of v0.2.0 — run before claiming any score above 8.0)

These are the gates a PM will check, mechanically. If any gate fails, the score caps at 8.0 regardless of how strong the narrative is. Two gates (G1 EPS × multiple multiplicativity and G3 SOTP monotonicity) cap at 7.0 when they fail because they are critical math errors that destroy the memo's arithmetic credibility. **v0.2.0 adds G15-G17**: G15 (consensus variance) and G16 (bank discipline) cap at 7.0 on fail; G17 (revision velocity) caps at 7.5. Canonical descriptions of all 17 gates live in `schemas/verification_gates.json` under `gate_definitions`; that schema is the contract (schema accepts both 0.1.0 14-gate and 0.2.0 17-gate for grandfathering). Each gate has a Python verification script that exits 0 on pass and non-zero on fail.

1. **G1 — EPS × multiple multiplicativity** (math): for every scenario row in every valuation table, EPS × multiple = target_price within rounding (±0.5%). Cap at 7.0 on fail. Script: `scripts/verify_eps_pe.py`.
2. **G2 — Segment GM reconciliation** (consistency): Σ(segment_revenue × segment_GM) / Σ(segment_revenue) within ±50bp of consolidated GM as reported. `n_a` for single-segment companies. Script: `scripts/verify_segment_gm.py`.
3. **G3 — SOTP monotonicity** (math): for every segment in the SOTP table, NI ≤ OP ≤ GP ≤ Revenue. Any inversion fails. Cap at 7.0 on fail. Script: `scripts/verify_sotp_monotonicity.py`.
4. **G4 — Scenario probabilities sum to 1.00** ±0.01 (math). Script: `scripts/verify_scenario_weights.py`.
5. **G5 — Bear/bull EPS bridge reconciles to base** (math): sum of named adjustments = (base_eps − scenario_eps) within rounding. Script: `scripts/verify_bear_bridge.py`.
6. **G6 — Source tag declared at first use** (source): every specific number tagged S1-S5 or Pending at first appearance in the memo Markdown. Script: `scripts/verify_source_tags.py`.
7. **G7 — Headline conditionality matches anchor strength** (source): if any top-3 anchor is S3 or weaker, headline contains conditional language; if all top-3 are S1-S2, headline can be unconditional. Script: `scripts/verify_headline_conditionality.py`.
8. **G8 — GM taxonomy box exists** (structure): the 5 GM types (T1-T5) are explicitly defined somewhere in the memo and each GM mention is implicitly tagged to one type. Script: `scripts/verify_gm_taxonomy.py`.
9. **G9 — What-would-reverse has numerical denominators** (structure): every directional trigger has a numerical threshold, not a handwave. Script: `scripts/verify_what_would_reverse.py`.
10. **G10 — Anchor weighting impact table exists** (structure): headline impact of ±10pp probability shift on the strongest scenario is shown. Script: `scripts/verify_weighting_sensitivity.py`.
11. **G11 — Non-GAAP to GAAP reconciliation present** (source, US-specific, B11): every non-GAAP number cited has its GAAP counterpart shown with the bridge listed (SBC, restructuring, amortization of acquired intangibles, etc.). `n_a` if no non-GAAP cited. Script: `scripts/verify_non_gaap.py`.
12. **G12 — SBC treatment in FCF disclosed** (source, US-specific, B12): memo states whether SBC is deducted from FCF; if not, dilution effect from RSU/option vest is shown separately. `n_a` if no FCF cited. Script: `scripts/verify_fcf_definition.py`.
13. **G13 — Barra factor exposure stated** (quant_overlay, US-specific, B13): factor tags (Value / Quality / Momentum / Growth / Size / Low-Vol / Liquidity) appear in the §11 quant overlay. Required in every institutional IC memo per D13. Script: `scripts/verify_quant_overlay.py`.
14. **G14 — Capacity / ADV / days-to-exit stated** (quant_overlay, US-specific, B14): days-to-exit at 10% / 20% / 30% participation against the name's 30-day ADV is shown for the recommended position size. Required per D13. Script: `scripts/verify_quant_overlay.py`.
15. **G15 — Consensus variance declared or memo self-labeled consensus-anchored** (source/structure, v0.2.0): for any non-Hold rating (Strong Buy / Buy / Sell / Strong Sell), memo must declare ≥1 load-bearing entry in `source_tags.consensus_variance`: type ∈ {revenue, margin, multiple, scenario_weight, timing}, sizing_impact_pp ≥ 2.0, ≥1 evidence_ref at S1-S3. Hold ratings and memos with headline self-labeled "consensus-anchored" → n_a. Thin coverage (n_analysts < 5) → n_a. Cap at 7.0 on fail. Full discipline in `references/consensus-variance-us.md` (Plugin 1). Script: `scripts/verify_consensus_variance.py`.
16. **G16 — Bank discipline (AOCI + CET1 + NIM + stress capital)** (structure, v0.2.0): for sector ∈ {Financials/Banks, Diversified Banks, Regional Banks, Investment Banking & Brokerage, Insurance, BDC}, `source_tags.bank_metrics` must contain (a) AOCI bridge fields, (b) CET1 walk, (c) NIM trajectory + deposit beta, (d) stress capital context (SCB + capital return capacity + CCAR/DFAST trough; trough optional for Category IV / <$100B). Non-bank sectors → n_a. Cap at 7.0 on fail. Full discipline in `references/phase-1-deep-dive-us.md` §FS-Banks Augmentation (Plugin 1). Script: `scripts/verify_bank_metrics.py`.
17. **G17 — Earnings revision velocity disclosure** (source, v0.2.0): `source_tags.revision_velocity` must populate `fy1_eps_revision_3m_pct` + `breadth_3m` (in [-1.0, 1.0]) + `g17_status="disclosed"`. Thin coverage (n_analysts < 5 OR g17_status="n_a_thin_coverage") → n_a. Cap at 7.5 on fail. Full discipline in `references/phase-2-continuation-us.md` §A6 Earnings Revision Velocity (Plugin 1). Script: `scripts/verify_revision_velocity.py`.
18. **G18 — Quant overlay cross-document consistency** (structure, v0.3.0): within a single memo, the structured `quant_overlay.factor_tags` block in `memo.json` must match any Markdown narrative reference to the same Barra factor within ±0.2 tolerance. Catches authors who quote z-scores in prose that diverge from structured block — common LLM failure mode where the prose is regenerated without re-reading structured data. Pre-v0.3.0 Plugin 2 reference files had NVDA Momentum at +1.8 in `quant-overlay-us.md` but +2.3 in `position-sizing-us.md`; G18 catches the same disease at memo runtime. n_a if no Markdown factor references found OR if `quant_overlay.factor_tags` absent (G13 handles presence separately). Cap at 7.5 on fail. Discipline in `references/quant-overlay-us.md` §"Honest framing." Script: `scripts/verify_quant_cross_doc_consistency.py`.
19. **G19 — Plugin 1 to Plugin 2 provenance manifest** (structure, v0.3.0): memo_metadata must reference an `outputs/<ticker>_manifest.json` file produced by Plugin 1's orchestrator at end of Phase 3, conforming to `schemas/manifest.json`. G19 verifies (a) manifest file exists at the declared path, (b) all required fields populated (manifest_version, ticker, run_id, created_at, plugin_versions, phase_timing, agent_provenance, web_search_log, verification_calls_count, outputs_produced), (c) verification_calls_count >= 12 per D9, (d) web_search_log >= 12 entries, (e) agent_provenance >= 15 entries, (f) **declared output file SHA-256 hashes match actual on-disk hashes** — the critical integrity check that detects post-hoc memo editing or manifest forgery. Memos with `memo_metadata.hand_authored: true` pass G19 with WARNING and rubric capped at 7.5 — the honest path for hand-authored memos. v0.1.x and v0.2.0 memos are grandfathered (G19 = skipped, reason='grandfathered_pre_v0_3'). Cap at 7.5 on fail. Closes the audit finding that Plugin 1 to Plugin 2 handoff was pure filename convention with no provenance enforcement. Script: `scripts/verify_provenance_manifest.py`.
20. **G20 — View defensibility** (structure, v0.3.0): for any memo claiming a rubric score above 8.5, three conjunctive conditions must hold. **(a) Differentiation magnitude**: `recommendation.upside_downside_pct` differs from S4 consensus PT-implied return by at least 8 absolute percentage points. **(b) Evidence strength**: at least one load-bearing `consensus_variance` entry has at least one `evidence_ref` at S1 or S2 (G15 accepts S1-S3; G20 tightens to require primary-source evidence on the strongest claim). **(c) Survival of structured attack**: `adjudication_trail` contains at least one entry with `type='variance_attack'`, `target_variance_id` pointing to a load-bearing variance, `attack_type` in the 5 canonical dimensions (evidence_credibility, triangulation_completeness, base_rate_sanity, catalyst_dependency, timing_arbitrage), and `attack_outcome` in {rebutted, modified}. n_a for Hold ratings, consensus-anchored headlines, and thin coverage (n_analysts < 5). v0.1.x and v0.2.0 memos grandfathered. Caps score at 8.5 on fail (NOT 7.0 — G20 is rubric-discriminating, not memo-killing). Closes the audit's highest-severity finding: the rubric was grading structural completeness instead of view quality. Discipline in `us-equity-research/references/pm-synthesis-adjudication-us.md` §R-v2 attack methodology. Script: `scripts/verify_view_defensibility.py`.

Phase 4 runs all 20 scripts (G13+G14 share `verify_quant_overlay.py`) before sign-off and writes the result to `outputs/<ticker>_verification_gates.json` conforming to `schemas/verification_gates.json`. The `overall_pass` boolean and `blocks_score_above` numeric capture the gate state for the score-band logic above. **v0.1.x memos with schema_version="0.1.0"** are grandfathered to the 14-gate set; G15-G20 are skipped (logged as `skipped: grandfathered_v0_1`). **v0.2.0 memos with schema_version="0.2.0"** are grandfathered to the 17-gate set; G18-G20 are skipped (logged as `skipped: grandfathered_v0_2`). **v0.3.0 memos** run the full 20-gate set with the audit-closing rigor described in items 18-20.

## When the user pushes back on a number, default to red-team mode

If the user's response includes any of: "where does X come from", "this doesn't reconcile", "the math is off", "I'm scoring this 7.x because…", "this is hand-wavy", "Pending should not be a headline anchor", "non-GAAP without GAAP", "FCF without SBC", "what's your factor exposure", "what's the ADV here" — they are doing PM red-team. Switch to **fix-then-justify** mode:

1. Acknowledge the specific gate violation (name the G-number)
2. Locate it in the source (memo file + section, or structured JSON path)
3. Fix the math / source / language / reconciliation
4. Re-run the affected verification script(s); confirm exit 0
5. Rebuild the artifact (Markdown memo + structured JSON)
6. Report what changed and what gate it now passes (cite gate ID and script output)
7. Do NOT defend the broken version — the user has already seen the bug and is testing whether you'll patch it cleanly or flinch

This is the loop that drives score progression. The score-band lookup above tells you which kind of fix moves the score how much.

## What is inherited from China vs. what is US-specific

Inherited 1:1 (English-localized only): the 5-scenario probabilistic framework, S1-S5 source stratification, three-method valuation reconcile structure, GM taxonomy with five types, bear/bull EPS bridge with three layers, what-would-reverse falsification triggers, A0 tail mapping discipline, PM red-team rubric structure (6-9 score bands, fix-then-justify mode), position sizing decoupled from rating, multi-audience derivation pattern, the 12 minimum WebSearch+WebFetch calls per memo (D9), and gates G1-G10.

US-specific (net-new or replaced):

- Document substrate: SEC EDGAR primary (10-K / 10-Q / 8-K / DEF 14A / S-1/3/4 / 20-F / 6-K / Form 4 / 13D/G / 13F) replaces CNINFO / Sina / Eastmoney; FRED replaces NBS / PBoC; sector trade press is US-specific (The Information, STAT, Bank Reg Blog, Counterpoint, IDC, Gartner, etc.)
- Rating taxonomy: 5-band Strong Buy / Buy / Hold / Sell / Strong Sell with ±10% / ±20% bands per D1 replaces 买入 / 增持 / 中性 / 减持 / 卖出 with ±5% / ±15%
- Valuation: sector-branched primary multiple per D8 (P/E mature, EV/EBITDA leveraged, EV/ARR + Rule of 40 SaaS, P/B + ROE banks, P/AFFO + NAV REITs, NPV biotech, EV/EBITDAX E&P, EV/EBITDAR airlines, P/AUM asset managers); WACC inputs from 10Y UST + Damodaran US ERP
- Forensic primary axis: ASC 606 / 842 / 718 + non-GAAP/GAAP discipline + SBC-in-FCF treatment replaces 政府补助 / LP put-call / 亿 unit confusion as the dominant forensic class
- Positioning desk: 13F + Form 4 + short interest + options skew + ETF passive % + activist 13D replaces 北上 / 公募 / 龙虎榜 / 融资融券
- Tail catalog (D12): six US-specific standing A0 events (NBER recession, Fed rate shock, sector regulatory action, sanctions/export control, tariff/trade war, election transition)
- Net-new gates G11-G14 (v0.1.0): non-GAAP reconciliation (G11), SBC-in-FCF disclosure (G12), Barra factor exposure (G13), capacity / ADV / days-to-exit (G14)
- Net-new gates G15-G17 (v0.2.0): consensus variance (G15), bank discipline (G16), revision velocity (G17)
- Net-new templates: LP letter (replaces retail), earnings prep, earnings flash, kill memo
- Net-new mandatory section: quant overlay (D13)
- Dropped: Chinese-language deliverable, retail variant, China-specific data sources, LP put/call construct

The full delta is catalogued in `design/us-vs-china-delta-matrix.md` (read-only after Phase A).

## Composition with marketplace plugins (soft-dependency per D21)

This skill operates standalone — Markdown + JSON in `outputs/` is the source of truth. When the user has the `claude-for-financial-services` plugins installed, the orchestrator (us-equity-research) optionally delegates artifact construction:

- Excel DCF: delegate to `financial-analysis:dcf-model` using the `dcf_components` block of `schemas/memo.json` and the 5→3 scenario mapping in `delegation_outputs.scenarios_3case_for_dcf_plugin` (Bear = strong_bear + bear probability-weighted; Base = base; Bull = bull + strong_bull)
- Excel comps: delegate to `financial-analysis:comps-analysis` using the peer set from `company_qualitative.competitive_landscape.peers`
- Polished 30-50pg DOCX initiation report: delegate to `equity-research:initiating-coverage` Task 5 using `delegation_outputs.company_research_md_path` (Task 1 input, 6-8K word qualitative narrative) + `delegation_outputs.valuation_analysis_md_path` (Task 3 input, 4-6 page valuation narrative)
- Quality gate for any Excel artifact we produce: `financial-analysis:audit-xls`

The JSON contract for each delegation is documented in `us-equity-research/references/tool-composition-us.md`. None of the delegations are required for rigor; they produce presentation artifacts on top of the structured-JSON source of truth. If the user has not installed the marketplace plugins, the skill surfaces a one-line note about how to enable Excel / DOCX outputs and proceeds with Markdown-only.

## Output discipline

- All deliverables in Markdown (.md) per D15. Drop docx generation (Phase A removed `_docx_helpers.js` dependency).
- All outputs in `outputs/` at the workspace root.
- Naming convention:
  - `outputs/<ticker>_IC_memo.md` — institutional full
  - `outputs/<ticker>_IC_preread.md` — IC pre-read variant
  - `outputs/<ticker>_IC_debate.md` — IC debate script
  - `outputs/<ticker>_LP_letter.md` — LP letter
  - `outputs/<ticker>_earnings_prep.md` — earnings prep
  - `outputs/<ticker>_earnings_flash.md` — earnings flash
  - `outputs/<ticker>_kill_memo.md` — kill memo
  - `outputs/<ticker>_structured.json` — conforms to `schemas/memo.json`
  - `outputs/<ticker>_scenarios.json` — conforms to `schemas/scenarios.json`
  - `outputs/<ticker>_source_tags.json` — conforms to `schemas/source_tags.json`
  - `outputs/<ticker>_verification_gates.json` — conforms to `schemas/verification_gates.json`
- Optional Excel / DOCX delegation per D21 (soft-dependency on `claude-for-financial-services` plugins): hand `outputs/<ticker>_Research_Document_<date>.md` and `outputs/<ticker>_Valuation_Analysis_<date>.md` to `equity-research:initiating-coverage` Task 5 for polished DOCX; pass DCF inputs to `financial-analysis:dcf-model` for `outputs/<ticker>_DCF.xlsx`; pass comps data to `financial-analysis:comps-analysis` for `outputs/<ticker>_Comps.xlsx`. The JSON contract for each delegation is documented in `us-equity-research/references/tool-composition-us.md`. Skill operates fully without delegation — Markdown + structured JSON is the source of truth.
- Provide explicit file paths to the user after each build so they can open them in Cursor / Obsidian / GitHub.

## References (load when needed)

- `references/source-stratification-us.md` — S1-S5 + Pending taxonomy, US document types, conditional language patterns A/B/C/D
- `references/five-scenario-framework-us.md` — probabilistic scenarios, weights, per-scenario EPS × multiple construction, sector-branched multiple_type
- `references/three-method-valuation-us.md` — DCF + Comps + SOTP + multi-multiple bear reconciliation discipline; WACC; sector-default multiples per D8
- `references/gm-taxonomy-us.md` — 5 GM types, segment reconciliation rules, non-GAAP/GAAP parallel discipline
- `references/bear-bridge-us.md` — three-layer EPS bridge (soft / clean / strong), US-specific named adjustments
- `references/what-would-reverse-us.md` — falsification trigger framework with numerical denominators, US observables (10-Q Note, FDA letter, FRED series, Form 4 cluster, etc.)
- `references/tail-risk-mapping-us.md` — A0 catalog (6 standing + 2-3 idiosyncratic per D12), probability-shift discipline, downside impact
- `references/position-sizing-us.md` — σ math, Sharpe, Kelly, conviction-adjusted multipliers per D6, 5 mandate types per D3
- `references/pm-redteam-rubric-us.md` — scoring rubric, B1-B14 bug catalog (B11-B14 US-specific), score-band fixes
- `references/multi-audience-delivery-us.md` — institutional / IC pre-read / IC debate / LP letter / earnings prep / earnings flash / kill memo derivation patterns
- `references/quant-overlay-us.md` — Barra factor tags, capacity, edge decay, correlation placeholder, stress overlay (Phase D file, mandatory per D13)

## Templates

- `templates/opinion-letter-section-checklist-us.md` — 12-section institutional memo template (English-only per D4)
- `templates/ic-debate-script-template-us.md` — IC debate script with 8-challenge Q&A bank, 3 / 5 / 10-min timing variants
- `templates/lp-letter-template.md` — LP letter 1-2 page template (replaces China retail variant per D4)
- `templates/earnings-prep-template.md` — night-before earnings checklist
- `templates/earnings-flash-template.md` — T+30min same-day structured response template

## Scripts

- `scripts/verify_eps_pe.py` — G1, EPS × multiple multiplicativity per scenario row
- `scripts/verify_segment_gm.py` — G2, segment-weighted GM ties to consolidated within ±50bp
- `scripts/verify_sotp_monotonicity.py` — G3, NI ≤ OP ≤ GP ≤ Revenue per SOTP segment
- `scripts/verify_scenario_weights.py` — G4, scenario probabilities sum to 1.00 ±0.01
- `scripts/verify_bear_bridge.py` — G5, named-adjustment sum reconciles to (base_eps − scenario_eps)
- `scripts/verify_source_tags.py` — G6, every specific number S-tagged at first use (regex scan)
- `scripts/verify_headline_conditionality.py` — G7, headline conditionality matches top-3 anchor strength
- `scripts/verify_gm_taxonomy.py` — G8, GM taxonomy box present and each GM mention tagged
- `scripts/verify_what_would_reverse.py` — G9, every trigger has numerical threshold + observable_via
- `scripts/verify_weighting_sensitivity.py` — G10, anchor weighting impact table present in structured JSON
- `scripts/verify_non_gaap.py` — G11 (US-specific), every non-GAAP citation has GAAP counterpart + bridge
- `scripts/verify_fcf_definition.py` — G12 (US-specific), FCF definition declares SBC treatment
- `scripts/verify_quant_overlay.py` — G13 + G14 (US-specific), factor tags + capacity / ADV / days-to-exit present
- `scripts/verify_consensus_variance.py` — G15 (v0.2.0), consensus variance declared for non-Hold ratings OR memo self-labeled "consensus-anchored"
- `scripts/verify_bank_metrics.py` — G16 (v0.2.0), AOCI bridge + CET1 walk + NIM trajectory + stress capital context for Banks-sector memos
- `scripts/verify_revision_velocity.py` — G17 (v0.2.0), 3m FY1 EPS revision + breadth disclosed when coverage non-thin
- `scripts/verify_quant_cross_doc_consistency.py` — G18 (v0.3.0), Markdown factor z-score quotes match structured quant_overlay.factor_tags within ±0.2 tolerance
- `scripts/verify_provenance_manifest.py` — G19 (v0.3.0), Plugin 1 provenance manifest present with verified output file hashes; hand-authored escape hatch caps rubric at 7.5
- `scripts/verify_view_defensibility.py` — G20 (v0.3.0), three conjunctive conditions for rubric > 8.5: ≥8pp headline differentiation, ≥1 S1/S2 evidence on load-bearing variance, surviving variance_attack in adjudication_trail
- `scripts/write_manifest.py` — Plugin 1 orchestrator helper (not a gate verifier). Assembles outputs/<ticker>_manifest.json at end of Phase 3 from a seed file + workpapers + output file hashes. Documented in `us-equity-research/SKILL.md` §"Manifest generation".

Scripts for G1-G10 are authored in Phase C. Scripts for G11-G14 are authored in Phase D alongside the quant-overlay reference file. All scripts exit 0 on pass and non-zero on fail; structured stdout conforms to the `evidence` block in `schemas/verification_gates.json`.
