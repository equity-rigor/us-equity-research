---
name: us-equity-research
description: Conduct institutional buy-side fundamental research on a single-name US-listed equity using a multi-agent workflow with mandatory web verification, S1-S5 source stratification, and 5-scenario probabilistic valuation. Use this skill whenever the user provides a US ticker (1-5 uppercase chars on NYSE/Nasdaq/AMEX/OTC such as NVDA, AAPL, JPM, XOM, MRK, BRK.B, AMZN) and asks for fundamental analysis, an investment thesis, a stock pitch, an IC memo, buy-side research, a 10-K read, an earnings prep, a kill thesis, a long/short pair-trade structure, or any institutional-grade deep-dive. Triggers include "is X a buy", "build me a thesis on", "stock pitch for X", "buy-side research on X", "IC memo for X", "fundamental analysis of X", "earnings prep for X", "kill thesis on X", "10-K read on X", "pair-trade structure long X short Y", "long X short Y", "fundamental work on X". Also triggers on sector phrases including "AI infrastructure", "datacenter capex", "energy transition", "biotech pipeline", "SaaS Rule of 40", "bank stress capital", "REIT AFFO", "E&P FCF yield". In scope: US-domiciled common equity and foreign-issuer ADRs (Toyota, Spotify, BABA, Nestlé). Out of scope: PE deals (use lbo-model), sell-side initiation report format (use equity-research:initiating-coverage directly), retail-investor commentary (FINRA Rule 2210 scope). Default mode is EDGAR-only and free-aggregator data; optional premium hooks (Visible Alpha, Capital IQ, AlphaSense, Bloomberg) gate behind explicit user signaling. Optional polished Excel DCF, Excel comps, and 30-50pg DOCX outputs delegate to financial-analysis and equity-research plugins when installed.
---

## CRITICAL: Verifier Script Path Resolution

This plugin bundles its verifier scripts at `${CLAUDE_PLUGIN_ROOT}/scripts/` and JSON schemas at `${CLAUDE_PLUGIN_ROOT}/schemas/`. All `scripts/verify_*.py` and `scripts/write_manifest.py` references in this SKILL resolve to that location.

### Execution requirements (non-negotiable)

**1. Use the explicit plugin-root path for every script invocation.**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/verify_eps_pe.py --memo-json outputs/<TICKER>_structured.json
python ${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest.py --ticker <TICKER> --outputs-dir outputs/
```

If `${CLAUDE_PLUGIN_ROOT}` is not set in the current Claude Code version, the plugin is installed at `~/.claude/plugins/<plugin-name>/<version>/` (e.g., `~/.claude/plugins/us-equity-research/0.5.0/`). Use that absolute path as a fallback.

**2. NEVER fall back to "evaluate gates analytically."**

If you cannot reach a verifier script for any reason (file not found, permission denied, Python import error, missing pydantic dependency, etc.), STOP execution of the current phase. Report the error to the user with the exact command attempted, the exact error message returned, and a request to either (a) clone the repo at `https://github.com/equity-rigor/us-equity-research` and run Claude Code from that directory, OR (b) manually copy the missing scripts to the plugin install location.

Do NOT proceed to produce a memo with gate statuses you judged yourself. Self-graded gates are not gates. They are LLM opinions about LLM output.

**3. The verifier scripts are this framework's distinguishing feature.** A memo produced without programmatic verification has no claim to the "20-gate verification" rigor advertised in the README. Self-graded gates produce a memo of the same quality as a careful prompt template — useful, but not what was promised.

**4. Operator-explicit override (the only allowed degradation path).** If the user explicitly says "I understand the verifiers won't run; proceed analytically anyway," THEN you may produce the memo with analytically-judged gate statuses. In that case you MUST set `memo_metadata.gates_evaluated_analytically: true` in `<TICKER>_structured.json`, include the disclaimer *"Gate statuses in this memo were evaluated analytically by the language model; the programmatic verifier scripts did not execute for this output"* in the IC memo header, set every gate's `evaluation_method` field to `"analytical_llm"`, and cap the rubric score at 7.5 regardless of mechanical compliance.

This preamble was added in v0.5.0 after the v0.4.0 MU run (2026-06-06) revealed the framework was silently degrading to LLM-analytical gate evaluation when verifier scripts were not reachable from the user's working directory. The structural mechanism preventing silent degradation is this preamble plus the bundled `scripts/` and `schemas/` directories inside each plugin.

---

# US Single-Name Equity Research Workflow

A multi-phase, multi-agent fundamental research framework for US-listed equities. Produces IC-memo-grade output with mandatory web verification, integrated red team, S1-S5 source stratification, 5-scenario probabilistic valuation, and explicit position sizing across mandate types. Designed to compose with the buy-side PM rigor layer `us-equity-ic-rigor` and to delegate Excel/DOCX artifact construction to marketplace plugins `financial-analysis` and `equity-research` when installed.

## Core Principles

These four principles run through every phase. Without them, the workflow degrades to ordinary sell-side commentary.

**1. Multi-agent specialization beats monolithic analysis.** A single agent doing "everything about NVDA" will skim. Forced specialization with explicit handoffs catches things one analyst would miss. Industry/cycle, forensic accounting, regulatory/policy, positioning/sentiment, and competitive analysis are different analytical units — they deserve different specialists. Per D7, this is preserved exactly from the China precedent.

**2. Red Team runs in parallel from day one, not as final reviewer.** The Red Team's job is to build the strongest possible bear case in good faith. It is judged on whether it identifies things the bull side missed, not on agreement with the PM. Assigning Red Team only at the end is too late — by then the narrative has hardened.

**3. Web verification is mandatory for any post-cutoff specific claim.** Sub-agents can hallucinate plausible-looking URLs, EDGAR accession numbers, regulatory designations, and dollar figures — especially for events past the model's January 2026 knowledge cutoff. Every material specific claim (FY financials, Entity List / OFAC SDN status, antitrust action status, FDA outcomes, customer share, settlement amounts, guidance numbers) must be independently verified via WebSearch / WebFetch / EDGAR full-text search with source URL captured. Distinguish framework claims (durable, structural) from specific numerical claims (need verification). The single biggest failure mode is unverified hallucination dressed up as primary-source rigor. Per D9 the minimum is 12 distinct WebSearch+WebFetch calls per memo.

**4. Position sizing reflects confidence, not just direction.** A "Buy" rating with limited conviction is half-weight. A "Buy" with high conviction is a core position. Always specify both rating and sizing, with explicit reasons for the gap between them. Per D1, ratings are 5-band (Strong Buy / Buy / Hold / Sell / Strong Sell) with ±20% / ±10% return-band thresholds; per D3, sizing is reported across 5 mandate types.

## When to Trigger

Invoke this workflow whenever the user wants institutional buy-side research on a US-listed equity. Specific triggers include providing a ticker like NVDA, AAPL, JPM, XOM, MRK, BRK.B and asking "is this a buy", "build me a thesis", "research this", "kill thesis on this", or requesting a stock pitch / IC memo / buy-side note / fundamental analysis. Sector-themed requests ("AI infrastructure exposure", "SaaS Rule of 40 screen on X", "biotech pipeline NPV on X") also trigger. Pair-trade requests ("long NVDA short AMD") trigger this skill on each leg with the pair structure carried into Phase 3.

If the user provides only a ticker without an explicit research request, ask: "Long-only or L/S mandate? Horizon — default 12mo primary / 24mo secondary? Data access tier — EDGAR-only (default) or premium (Visible Alpha / Capital IQ / Bloomberg)?" Default if no answer: long-only L/S-friendly, 12mo primary + 24mo secondary (per D2), EDGAR-only (per D5).

Trigger boundaries: when the user asks for a polished sell-side-format 30-50pg initiation DOCX, that's `equity-research:initiating-coverage`'s territory — this skill produces the structured content and delegates Task 5 at the end. When the user asks for a post-print earnings update DOCX ("Q3 update for NVDA"), `equity-research:earnings-analysis` is preferred. This skill owns pre-print earnings prep, IC memos, kill memos, LP letters, and the verification rigor.

## Scope and Limitations (read before invoking on a name that doesn't fit the fundamental-thesis pattern)

This skill is **fundamental, single-name, US-listed equity research**. Its 20-gate rigor, scenario discipline, and multi-agent specialization are calibrated to that use case. It is NOT appropriate for several adjacent use cases that look superficially similar but have different load-bearing inputs. Invoking the skill on these will produce output that is well-structured, gate-clean, and category-wrong.

**Out of scope — use a different tool, or supplement this output substantially:**

- **Pure event-driven trades** where alpha lives in the timing of a single binary event — FDA decision (PDUFA / AdCom), FTC ruling, Fed pivot, M&A close-or-block, ITC §337 ruling. The fundamental analysis here is downstream of the event prediction; this skill cannot predict event outcomes or model implied-probability mispricing in derivatives.
- **Pure technical / momentum / mean-reversion trades** where alpha lives in price action, volume profile, support/resistance, or quantitative trend signals. The skill's positioning_sentiment block is a snapshot, not a price-series model.
- **Pair-trade-on-flow** where alpha lives in spread convergence / basis dynamics / leg correlation / borrow costs / hedge ratio drift, not in fundamental dispersion between the two legs. The skill handles fundamental pair-trade framing (e.g., long NVDA short AMD on share-shift thesis); it does NOT handle a pair where the trade is about basis or technical convergence (e.g., long PLTR short COIN on factor crowding).
- **Activist / proxy-fight situations** where alpha lives in voting math, shareholder agreement structure (ROFR, drag-along, tag-along), 13D group formation, or board-composition arithmetic. The skill's regulatory_status block touches 13D filings but does not model voting outcomes.
- **Pre-IPO / private market analysis** — different disclosure regime (no 10-K, no XBRL), different valuation conventions (last-round mark, secondary trades, 409A), different deal-by-deal terms. Use a private-market skill.
- **Bond / credit-side analysis** — different fundamental priorities (downside skew, covenant structure, capital stack seniority, default-recovery distributions). Use a credit skill.
- **Pre-revenue biotech where the bet is binary clinical outcome** — Phase 3 readout / FDA decision dominates the rNPV. Until v0.4.0 ships the biotech-rNPV reference file, the skill handles such names poorly; even after, single-binary-readout names lean closer to event-driven than fundamental.
- **Catalyst-driven momentum on a name where you have no view on the catalyst** — if the question is "should I buy NVDA into earnings" and the answer requires modeling consensus positioning, options-implied move, prime-broker book positioning, and dealer GEX, this skill produces well-disciplined but irrelevant fundamental analysis.

**Within scope but with named limitations** (the skill produces output but the output is incomplete by construction):

- **Names where alpha lives in positioning** (crowded long, crowded short, factor exposure cascade) — the skill's positioning_sentiment captures 13F clusters, short interest, options skew, and ETF passive %, but not real-time order flow, dark-pool prints, prime-broker book data, or live factor crowding. For such names the skill is informative but not load-bearing.
- **Cyclicals at inflection** — the skill cannot mechanically call the cycle turn. Reference content (book-to-bill, SAAR, rig count, channel inventory months) is gestural through v0.3.0; v0.4.0+ may extend. Until then, treat cyclical inflection calls as analyst judgment with framework support, not framework outputs.
- **Small-cap with thin disclosure** (<3 covering analysts, <$500M cap, <2 segments disclosed in 10-K Item 7) — the skill degrades gracefully into headline-conditionality "range_only" labeling per G7, but the underlying alpha case is undercooked. Use peer-comparative and channel-check methods more heavily than the skill prescribes.
- **Non-US issuers via ADR** — the skill accepts 20-F filings and notes ADR-vs-ordinary share treatment in Phase 0, but does NOT model China VIE structure, F-share accounting nuances, or jurisdiction-specific governance overlays. For ADRs of names with material VIE exposure (BABA, JD, BIDU, NTES, etc.), supplement with the china-equity-research skill.

**Honest framing.** A 9.0-scored output from this skill on an in-scope name is institutionally defensible fundamental analysis. A 9.0-scored output on an out-of-scope name is well-structured wrong-category work. The framework cannot detect out-of-scope use itself — that determination is the user's. When in doubt, use the categorization above before invoking.

## Workflow Overview

The full workflow has three sequential research phases, a mandatory independent verification phase, and a final synthesis. Total elapsed time depends on user urgency, but a serious deep-dive is roughly two hours of orchestrated agent execution.

```
Phase 0   Setup & data spec (PM / orchestrator)
   |
Phase 1   Initial deep-dive (5 specialists in parallel)
   |      A1 Industry/cycle, A4 Capacity/capex, A5 Regulatory/policy,
   |      A8 Positioning/sentiment, FS Forensic accounting
   |      -> PM synthesis -> Phase 1 Integrated Brief
   |
Phase 1.5 Refresh round (only if Phase 1 agents failed to use web tools)
   |
Phase 2   Deepening + Forensic + Red Team + Consensus (6 agents in parallel; A-Consensus new in v0.2.0)
   |      A2 Forensic continuation, A3 Customer/commercial pipeline,
   |      A3-Peers Competitive comparison, R Red Team v1, A6 Channel pulse,
   |      A-Consensus Variance identification (forces G15-eligible variance or
   |      "consensus-anchored" labeling per `consensus-variance-us.md`)
   |      -> PM synthesis -> Phase 2 Integrated Brief (v3)
   |
Phase 3   Valuation + Final synthesis (4 agents in parallel)
   |      A7 DCF + SOTP + sector-appropriate multiples + quant overlay,
   |      Mirror analysis on top peer (if pair-trade),
   |      [Topic]-Forensic deep-dive on identified specific risk,
   |      R-v2 Refreshed Red Team
   |      -> PM synthesis -> IC Memo (English)
   |
Verify    Independent web verification (mandatory, never skip)
   |      12+ WebSearch+WebFetch calls; EDGAR full-text search; 20 gates
   |      -> Verification Report with source matrix and structured JSON
   |
Final     Multi-audience deliverables
          Institutional IC memo (full) + IC pre-read + IC debate script +
          LP letter + earnings prep + earnings flash (English only)
          Optional Excel DCF / comps / polished DOCX delegated to marketplace plugins
```

Phase reference files (read on demand, not at skill load):

- `references/phase-1-deep-dive-us.md` — Five specialist agent prompts for Phase 1 + sector-conditional Bank Discipline augmentation under FS (new in v0.2.0; gated by G16 for sector=Financials/Banks)
- `references/phase-2-continuation-us.md` — Six agent prompts for Phase 2 (A2/A3/A3-Peers/R/A6 + A-Consensus new in v0.2.0); A6 includes revision velocity discipline (new in v0.2.0; G17)
- `references/phase-3-valuation-us.md` — Four agent prompts for Phase 3
- `references/consensus-variance-us.md` — **(new in v0.2.0)** Variance taxonomy, evidence-required matrix, sizing rule, calibration. Gated by G15.
- `references/pm-synthesis-adjudication-us.md` — **(new in v0.3.0)** Weighting principles for specialist conflict adjudication (Forensic dominates structural; Regulatory dominates if material; Industry is base-case; Positioning is technical overlay; Channel is timing). R-v2 attack methodology (5-point checklist: evidence credibility, triangulation completeness, base-rate sanity, catalyst dependency, timing arbitrage). Adjudication trail schema. Consumed by G20 (Sprint 2 Item 6).
- `references/r-v2-isolated-attack-us.md` — **(new in v0.4.0)** Isolated R-v2 subagent spawn contract: structural-independence rationale, the 5-point attack methodology in execution form, win condition, independent-source re-verification requirement, bounded context window, the `variance_attack` output schema with the `attacker_*` fields, and the spawn-failure → demote → G15 remediation path. Dispatched at the Phase 2→3 boundary; consumed by G20's graduated rigor scale (Sprint 3a).
- `references/verification-protocol-us.md` — Web verification methodology
- `references/us-data-sources.md` — EDGAR, FRED, Federal Register, regulators, free vs premium tiering
- `references/source-stratification-us.md` — S1-S5 + Pending taxonomy ported to US filings
- `references/forensic-accounting-checklist-us.md` — ASC 606/842/718, non-GAAP, SBC, restatements, Form 4, RPT
- `references/regulatory-desk-us.md` — FTC/DOJ/State AGs/EU CMA, BIS/OFAC/CFIUS, FDA/FCC/FERC/NHTSA/EPA/FAA/CFPB, USTR 301/232, BEAT/GILTI/§174
- `references/positioning-sentiment-us.md` — 13F clusters, Form 4 patterns, 13D activists, short interest + DTC, options skew, ETF passive %, index inclusion
- `references/valuation-discipline-us.md` — Sector-default multiple table (P/E, EV/EBITDA, P/B, AFFO, ARR + Rule of 40, NPV pipeline, EBITDAX, etc.) per D8
- `references/monitoring-framework-us.md` — Catalyst calendar, Tier 1/2/3 triggers, kill criteria, earnings cycle
- `references/ic-memo-template-us.md` — Full institutional memo template (v0.2.0 adds §CONSENSUS VARIANCE & REVISION VELOCITY between INVESTMENT THESIS and VALUATION FRAMEWORK; adds Bank Metrics subsection under KEY FINANCIAL DATA)
- `references/lp-letter-template.md` — 1-2 page LP communication variant
- `references/earnings-prep-template.md` — Night-before earnings checklist
- `references/earnings-flash-template.md` — T+30min same-day structured response
- `references/tool-composition-us.md` — JSON delegation contracts for `financial-analysis:dcf-model`, `financial-analysis:comps-analysis`, `equity-research:initiating-coverage` Task 5

Sister skill: `us-equity-ic-rigor` is the PM red-team rigor layer that hardens the deliverable produced by this skill. Invoke it after Phase 3 for IC defense — it scores the memo on the 6-9 rubric, audits the 5-scenario framework, three-method valuation reconcile, GM taxonomy, bear bridge, what-would-reverse triggers, A0 tail mapping, and position sizing. Pass it the same structured JSON this skill produces.

## Operating Mode

**Always parallel-dispatch specialists within a phase.** Use the Agent tool with multiple invocations in a single message. Each Phase 1 agent runs ~10-20 minutes. Sequential dispatch wastes hours.

**Always orchestrate via PM after each phase.** The PM agent (you) does not write opinions during specialist work — it adjudicates between specialists when their conclusions conflict and surfaces unresolved tensions. Each phase ends with a synthesis brief.

**Acknowledge agent failures openly.** Some Phase 1 agents will return framework-only output if they fail to use web tools. Explicitly tag these as "framework only — needs refresh" and re-dispatch in Phase 1.5 with explicit instructions to use WebSearch / WebFetch / EDGAR full-text search.

**Verify before publishing.** Verification is not optional. Run the verification phase before any IC memo is written. If material claims cannot be verified, downgrade conviction and flag the gap explicitly with a Pending tag per `source-stratification-us.md`.

**Default to EDGAR-only mode** (D5). Premium hooks (Visible Alpha, Capital IQ, AlphaSense, Bloomberg) require explicit user signaling or env-var gating documented in `us-data-sources.md`. The skill must produce a complete, defensible memo in EDGAR-only mode; premium data improves S4 consensus quality but is never load-bearing on the framework.

## Phase 0: Setup

Before dispatching any agents, capture:

1. **Stock identifier**: Ticker + exchange + company legal name + CIK (e.g., NVDA / Nasdaq / NVIDIA Corporation / CIK 0001045810). For ADRs (Toyota / TM, Spotify / SPOT, Alibaba / BABA), note the 20-F filing as the S1 source instead of 10-K (per D11).
2. **Mandate**: Long-only large-cap / long-only SMID / L/S hedge fund / sector specialty / pair-trade structure (per D3). Drives which sizing column gets featured in the headline.
3. **Horizon**: 12-month primary + 24-month secondary (default per D2). Earnings prep / flash use 3-6 month horizon.
4. **Data access tier**: EDGAR-only (default) / premium hooks enabled (with env var indication).
5. **Sector**: GICS Level-2 or Level-4 — drives the primary valuation multiple per the `valuation-discipline-us.md` sector table (D8). E.g., NVDA = Tech > Semis > P/E primary; JPM = Financials > Diversified Banks > P/B + ROE-implied P/B; XOM = Energy > Integrated > EV/EBITDAX + FCF yield; MRK = Healthcare > Pharma > EV/Sales + NPV pipeline; AMT = REITs > Tower > P/AFFO + NAV. **Load-bearing in v0.2.0+**: sector ∈ {Financials/Banks, Diversified Banks, Regional Banks, Investment Banking & Brokerage, Insurance, BDC} triggers the FS-Banks Augmentation in Phase 1 and bank-specific G16 verification. Incorrect sector classification cascades into wrong specialist activation — cross-check ticker against NASDAQ Symbol Directory or company 10-K cover page Item 1 if uncertain.
6. **Pair-trade flag** (if applicable): partner ticker, pair-spread benchmark, expected hedge ratio.

Default if unspecified: long-only L/S-friendly, 12mo primary + 24mo secondary, EDGAR-only, sector inferred from ticker.

Then articulate the Phase 0 hypothesis tree — three competing theses (bull / capex-treadmill or quality-trap / regulatory or tail). Phase 1-3 agents test these hypotheses. Do not pre-commit to one.

## Phase 1: Five-Agent Initial Deep-Dive

Dispatch all five in a single message (parallel). Each agent takes ticker + Phase 0 context as input.

| Agent | Specialist | Output |
|---|---|---|
| **A1** | Industry & cycle desk | Cycle position, supply/demand, end-market segmentation (e.g., NVDA: DC vs gaming vs auto vs pro-viz), peer landscape, catalysts. Cites trade-press S5 sources (Gartner / IDC / Counterpoint / Omdia / Yipit / Placer.ai). |
| **A4** | Capacity & capex map | Line-by-line production assets, capex schedule, depreciation waterfall, ROIC trajectory. For asset-heavy names (XOM, T, INTC) this is load-bearing; for asset-light SaaS or financials it shifts to working-capital + AUM/AUA + customer cohort economics. |
| **A5** | Regulatory & policy desk | FTC/DOJ/state AGs/EU CMA antitrust status; BIS Entity List / OFAC SDN / CFIUS export-control status; sector regulator open matters (FDA CRL/AdCom for pharma; FCC docket for telecom; FERC order for energy; NHTSA recall for autos; EPA enforcement; FAA grounding; CFPB action); USTR Section 301/232 tariff exposure; BEAT/GILTI/§174 R&D capitalization / Pillar 2 GMT tax exposure. Cites Federal Register, agency dockets, PACER. |
| **A8** | Positioning & sentiment | 13F holdings clusters and concentration (Whale Wisdom / fintel / sec.gov direct); Form 4 net insider activity last 90d/6mo/12mo and 10b5-1 plan structure; 13D activist filings; short interest + days-to-cover; options skew + IV term structure + gamma; ETF passive ownership %; S&P 500 / Russell / Nasdaq 100 index status; sell-side rating distribution + PT dispersion + revision trend. |
| **FS** | Financial statements forensics | 5-year P&L / BS / CF from EDGAR XBRL company facts API (data.sec.gov/api/xbrl/companyfacts/CIK*.json); ASC 606 revenue-recognition red flags; ASC 842 lease PV; ASC 718 SBC % of revenue and buyback-offset ratio; non-GAAP vs GAAP delta as % of net income over 5y; FCF construction (does it deduct SBC?); goodwill vs net assets; auditor changes (8-K Item 4.01); restatements (8-K Item 4.02); PCAOB inspection findings; pension PBO funding ratio; VIE disclosures. |

**FS is the most important agent in Phase 1.** It is the foundation everything else builds on. If FS does not pull actual 10-K / 10-Q data via EDGAR XBRL API, the whole Phase 1 must be re-run. The US-specific gate: non-GAAP vs GAAP gap must be quantified; SBC treatment in FCF must be explicit; restatement and going-concern checks must be performed (delta matrix §6, gates G11/G12).

After dispatch completion, write Phase 1 Integrated Brief synthesizing findings. Identify conflicts between agents and adjudicate. Flag which agents returned framework-only vs primary-source-verified output.

For full agent prompts and structure, read `references/phase-1-deep-dive-us.md`.

## Phase 1.5: Refresh (Conditional)

Trigger only if Phase 1 agents failed to use web tools (look at `tool_uses` count in agent metadata — anything below ~10 likely means no real verification).

Re-dispatch failed agents with explicit, mandatory instructions:

- "You MUST use WebSearch, WebFetch, and EDGAR full-text search (efts.sec.gov/LATEST/search-index?q=...) — minimum 15 calls"
- "Other agents in this batch successfully used 25-100+ web tool calls. Do not refuse to execute."
- Provide specific URLs to fetch (EDGAR company filing page, XBRL companyfacts JSON, Federal Register agency docket, FRED series for macro, IR transcript URL)

After refresh, write v2 of the Integrated Brief with corrections clearly documented.

## Phase 2: Deepening + Forensic + Red Team + Consensus

Dispatch **six** in parallel (A-Consensus added v0.2.0). Phase 2 is set up based on Phase 1 findings — the agents target specific gaps and tensions surfaced.

| Agent | Specialist | Output |
|---|---|---|
| **A2** | Forensic continuation | Pull most recent 10-Q (or 8-K Item 2.02 results release); resolve specific anomalies (DSO/DIO/DPO trend breaks, deferred-revenue declines, segment GM unexplained shifts); deep-read 10-K Notes (Commitments and Contingencies, Off-Balance-Sheet Arrangements, Subsequent Events); DEF 14A Item 404 related-party check. |
| **A3** | Customer / commercial pipeline | Customer wins/losses; product roadmap; ASP and unit dynamics; major contracts (10-K Item 1.01 disclosures); customer concentration % (10-K risk factors); net retention / churn for SaaS; pipeline coverage for biotech. |
| **A3-Peers** | Competitive comparison | Side-by-side vs 2-3 closest peers (GICS sub-industry); relative valuation; pair-trade framing; segment-level peer comparison. Optional delegation to `financial-analysis:comps-analysis` for Excel comps artifact if user requested and plugin installed (see `references/tool-composition-us.md`). |
| **R** | Red Team v1 | Strongest bear case in good faith; base-rate analysis on peer industry (e.g., what % of high-growth SaaS at 80x EV/ARR retained that multiple 24mo later?); specific kill criteria with numerical denominators; identify the strongest S1-S2 fact the bull case ignores. |
| **A6** | Channel pulse + revision velocity (G17) | Monitoring framework; weekly / monthly tracking dashboard; Tier 1/2/3 trigger structure; pre-announcement risk; 13F filing-window awareness (mid-Feb, mid-May, mid-Aug, mid-Nov); Form 4 alert thresholds. **v0.2.0**: load-bearing earnings revision velocity disclosure (1m/3m/6m FY1 EPS delta + breadth + peer comparison + pre-print drift) per G17. Cross with crowding score to surface revision-down/crowded-long short setups and revision-up/crowded-short squeeze setups. |
| **A-Consensus** (new v0.2.0) | Consensus variance identification (G15) | Pull FactSet / Visible Alpha / Bloomberg EE consensus snapshot; for each material disagreement on revenue / margin / multiple / scenario-weight / catalyst-timing, classify variance type, evidence with S1-S3 sources per `consensus-variance-us.md` evidence matrix, size impact in pp on scenario weights. If no defensible variance: recommend "consensus-anchored" labeling and Hold rating ceiling. The agent that forces the memo to claim edge specifically or admit absence honestly. |

Phase 2 typically surfaces material bear data points that Phase 1 missed — e.g., for NVDA: a meaningful Form 4 cluster of C-suite selling, a non-GAAP-to-GAAP gap widening to 35% of net income, a specific 8-K Item 1.01 customer-contract loss, or a pending FTC/DOJ investigation surfaced in Federal Register. Synthesize into v3 of the Integrated Brief.

For full agent prompts, read `references/phase-2-continuation-us.md`.

## Phase 3: Valuation + Final Synthesis

Dispatch four in parallel.

| Agent | Specialist | Output |
|---|---|---|
| **A7** | Valuation + quant overlay | DCF (WACC = Rf from 10Y UST via FRED `DGS10` + Damodaran implied US ERP + 5y weekly beta vs S&P 500 + after-tax cost of debt; terminal growth 2.0-2.5%; 5y explicit forecast or 3y + 7y fade for high-growth or 10y normalized for cyclicals); peer multiples per sector default (D8); SOTP if multi-segment; precedent M&A if relevant; **5-scenario probabilistic framework** with each scenario carrying its own EPS path, multiple, and bridge (per `schemas/scenarios.json`); **quant overlay** (Barra factor tags, capacity / ADV / days-to-exit at 10%/20%/30% participation, edge decay, correlation placeholder, stress overlay — mandatory per D13); position sizing across 5 mandate types (D3). Optional delegation to `financial-analysis:dcf-model` for Excel DCF artifact (see `references/tool-composition-us.md`); the 5-scenario block collapses to 3-case (Bear = strong_bear+bear weighted; Base; Bull = bull+strong_bull weighted) at the delegation boundary. |
| **Mirror** | Full analysis on top peer | If pair-trade is part of thesis; verify peer-side fundamentals at same S1-S2 rigor as primary leg; reconcile pair spread expectation. |
| **[Topic]-Forensic** | Specific deep-dive on identified risk | E.g., specific 10-K Note V item, specific subsidiary's VIE structure, specific regulatory matter (FDA CRL trajectory, FTC Second Request signal, OFAC SDN sub-list), specific contractual obligation, specific patent litigation at ITC §337 or Delaware Chancery. |
| **R-v2** | Refreshed Red Team | Update bear case with Phase 2 findings; recalibrate scenario weights; surface what-would-reverse triggers with numerical denominators (e.g., "DC revenue growth <X% for two consecutive quarters" not "growth slows"). **v0.4.0**: the structured variance-attack pass — one `variance_attack` adjudication-trail entry per consensus variance, the input to G20 — runs as a structurally isolated subagent, dispatched per the subsection below, not inline. |

Phase 3 typically reveals that initial Red Team was either too aggressive or too lenient — recalibrate. Mirror analysis often shows the relative-value thesis is more nuanced than headline multiples suggest.

After Phase 3, write the IC Memo (English). For structure see `references/ic-memo-template-us.md`. Hand off to `us-equity-ic-rigor` for PM red-team scoring on the 6-9 rubric (B11-B14 US-specific bugs included).

For full Phase 3 agent prompts, read `references/phase-3-valuation-us.md`.

### R-v2 isolated adversarial attack — subagent dispatch (v0.4.0)

R-v2 wears two hats. Hat (1), the bear-case / bear-PT refresh in the table above, may run inline in the orchestrator session. Hat (2), the structured attack that writes one `variance_attack` adjudication-trail entry per consensus variance (the input G20 reads), runs as a **structurally isolated subagent** as of v0.4.0 — not inline. Isolation is structural, not cross-vendor: the framework is Claude-only, and independence comes from a hard context partition (R-v2 sees machine-readable variance claims and their citations, never the narrative that justifies them) plus optional intra-family model diversity (a different Claude model for the attacker than for the writer).

Dispatch hat (2) once the Phase 2 PM synthesis has **locked** the `consensus_variance` set — each variance marked `load_bearing` true/false — and before the IC memo draft exists. Use the Task tool with no `subagent_type` (default general-purpose agent):

```
Task(
  description = "R-v2 isolated adversarial attack",
  prompt = render(references/r-v2-isolated-attack-us.md template, {
    ticker:                  <TICKER>,
    consensus_variance_json: <locked load_bearing variances, from source_tags.json>,
    source_tags_top_anchors: <top_anchors block, from source_tags.json>,
    attacker_model_choice:   "claude-sonnet-4-6"
  })
)
```

The orchestrator declares `attacker_model_choice`; the default `claude-sonnet-4-6` gives cross-size diversity against the Opus-class orchestrator that runs A-Consensus and writes the memo. Declaring a model distinct from the writer is what lets a memo clear G20's graduated-rigor bar for a claimed score **above 9.0** — the 8.5-9.0 band still clears on the v0.3.0 G20 conditions alone. The rendered prompt carries only the locked `consensus_variance` JSON, the `source_tags.top_anchors` JSON, the 5-point attack methodology, and the explicit win condition; it withholds A-Consensus's narrative, the PM synthesis briefs (Integrated Brief v1/v2/v3), the bull-thesis narrative, and any memo draft. R-v2 attacks claims and citations, never the arguments behind them.

**Expected output and integration.** R-v2 returns a JSON array of `adjudication_trail_entry` objects (`type="variance_attack"`, one per variance attacked), each conforming to `schemas/memo.json` `definitions/adjudication_trail_entry` and carrying the v0.4.0 fields `attacker_model`, `attacker_context_isolation=true`, and `attacker_independent_source_reads`. The orchestrator parses the array and appends each entry to the memo's `adjudication_trail` — these are exactly the entries G20 reads during the Verification Phase.

**Failure path (structural enforcement, not cosmetic).** If the spawn fails, the orchestrator retries once, then records the failure in `orchestrator_notes` and treats every load-bearing variance as un-attacked. If R-v2 returns zero attack points on a load-bearing variance — including a blanket "the variances look reasonable," which the win condition defines as a FAILED run, not variance strength — the orchestrator flags that variance `load_bearing = false` and re-runs G15. G15 may then fail, because the memo can be left without any load-bearing variance carrying adequate S1-S3 evidence and a non-Hold rating is no longer supportable; the analyst must surface a real variance with real evidence or accept the consensus-anchored Hold. This is the intended enforcement loop — isolation pushes back on manufactured edge rather than rubber-stamping it. The full spawn contract, structured-payload spec, per-dimension execution guidance, output schema, and remediation path are in `references/r-v2-isolated-attack-us.md`.

## Manifest generation (v0.3.0+, end of Phase 3, before Verification Phase)

Starting in v0.3.0, the orchestrator (you, running this skill) **must** produce a provenance manifest at the end of Phase 3. The manifest is what makes Plugin 2's claim "layers rigor on top of Plugin 1" architecturally true rather than editorially true — without it, a hand-authored memo can pass all 20 verification gates without ever invoking this skill. Plugin 2 gate **G19** verifies the manifest exists, has the right shape, declares >= 12 verification calls, references >= 15 specialist agents, and has valid SHA-256 hashes against the output files on disk.

**Incremental logging during the run.** From Phase 0 start through Verification Phase end, maintain a seed file at `outputs/<ticker>_manifest_seed.json` with this growing structure:

```json
{
  "run_id": "<UUID v4 generated at Phase 0 start>",
  "plugin_versions": {"us_equity_research": "0.3.0", "us_equity_ic_rigor": "0.3.0"},
  "phase_timing": {
    "phase_0": {"start": "<ISO 8601>", "end": "<ISO 8601>"},
    "phase_1": {"start": "...", "end": "..."},
    "phase_1_5": {"start": "...", "end": "..."},
    "phase_2": {"start": "...", "end": "..."},
    "phase_3": {"start": "...", "end": "..."},
    "verification": {"start": "...", "end": "..."}
  },
  "web_search_log": [
    {"tool": "WebSearch", "query_or_url": "...", "timestamp": "...", "response_hash": "<sha256>", "used_by_agent": "A1", "phase": 1}
  ],
  "verification_calls_count": 0,
  "orchestrator_notes": "Phase 1.5 triggered because A5 returned framework-only (web_calls_count==0)"
}
```

Append to `web_search_log` after each WebSearch / WebFetch / EDGAR / FRED / XBRL call. Increment `verification_calls_count` for each call made during Phase 4 (Verification Phase) specifically. Note phase start / end timestamps at boundaries.

**Specialist workpaper convention.** Each Phase 1/2/3 specialist agent writes its workpaper to `outputs/workpapers/<ticker>_phase<N>_<AGENT_ID>.md` (e.g., `outputs/workpapers/NVDA_phase1_FS.md`, `outputs/workpapers/NVDA_phase2_A-Consensus.md`). The manifest writer scans this directory to build `agent_provenance`. Workpapers under 500 bytes are flagged `framework_only` automatically — if Phase 1.5 was triggered and refreshed the agent, ensure the refreshed workpaper overwrites the framework-only stub (it should).

**Manifest write step (end of Phase 3).** Run:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest.py \
    --ticker <TICKER> \
    --outputs-dir outputs/ \
    --seed outputs/<TICKER>_manifest_seed.json
```

This writes `outputs/<TICKER>_manifest.json` conforming to `schemas/manifest.json`. The script computes SHA-256 over each output file, assembles agent_provenance from the workpapers directory, merges with the seed, and writes the final manifest. If the seed is missing it falls back to placeholder values and emits warnings to stderr — that manifest will fail G19, which is intentional.

**Cross-link from memo.** Set `memo_metadata.manifest_ref` in the structured memo to `"outputs/<TICKER>_manifest.json"`. G19 reads this path during verification.

**Hand-authored escape hatch.** If you (the analyst, not the orchestrator) are writing a memo by hand without running this skill, set `memo_metadata.hand_authored: true` in the structured memo. G19 will pass with a WARNING and the rubric score is capped at 7.5. This is the honest path for analysts who want to use the gates on their own work product without pretending it came from Plugin 1.

## Verification Phase (MANDATORY)

Never skip this. The single biggest failure mode in agent-driven research is unverified hallucination dressed up as primary-source rigor.

Process:

1. Extract every material specific claim from the IC memo — financials, segment revenue / GM, customer concentration, regulatory designation status (Entity List, OFAC SDN, FDA outcome, antitrust matter), M&A status, settlement amounts, catalyst dates, management guidance numbers.
2. Run direct WebSearch + WebFetch + EDGAR full-text search (efts.sec.gov/LATEST/search-index?q=...) on each — **minimum 12 distinct searches per memo (D9)**.
3. Document each as Verified / Partially Verified / Contradicted, with source URL and date, conforming to `schemas/source_tags.json` citation structure.
4. **Verify management guidance against the earnings call transcript, NOT the press release.** Companies sometimes provide different ranges on the call vs in the 8-K Item 7.01 press release. The call is the authoritative S3 source for guidance per delta matrix §11.
5. Specifically verify any "designated on regulatory list" / "company X said Y" / "specific dollar amount" claims — these are highest-risk hallucinations. For Entity List status, query bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list. For OFAC SDN, query sanctionssearch.ofac.treas.gov. For FDA action letters, query fda.gov/drugs/development-approval-process-drugs.
6. Dispatch an independent sanity-check sub-agent that re-verifies using its own web searches — do not trust the prior verification.
7. Run the **17** verification gates (G1-G10 inherited from china-equity-ic-rigor; G11-G14 US-specific: non-GAAP/GAAP reconciliation, FCF SBC treatment, Barra factor exposure stated, capacity / ADV days-to-exit stated; **G15-G17 added v0.2.0**: G15 consensus variance declared or "consensus-anchored" labeled, G16 bank-specific AOCI bridge + CET1 walk + NIM trajectory + stress capital context when sector=Banks, G17 revision velocity 3m FY1 EPS delta + breadth disclosed when n_analysts ≥ 5). Per `schemas/verification_gates.json` — a memo cannot claim score >8.0 with any gate failing.
8. If verification finds material errors, update the IC memo and document the correction.

For verification methodology and the standard checklist, read `references/verification-protocol-us.md`.

## Final Deliverable

Five audience-derived deliverables, English only (per D4 — no retail variant, no Chinese variant):

**1. Institutional IC Memo (full)** — 12-section structure per `references/ic-memo-template-us.md`. Rating (5-band Strong Buy / Buy / Hold / Sell / Strong Sell per D1), 12mo and 24mo target prices, position sizing across 5 mandate types, core thesis with anchor S-levels, 5-scenario valuation, three-method reconcile (DCF / comps / SOTP or precedent), GM taxonomy, bear bridge, what-would-reverse triggers, A0 tail map, kill criteria, catalyst calendar, quant overlay, source matrix appendix. Suitable for buy-side IC discussion.

**2. IC Pre-Read** — 3-4 page condensed for IC committee pre-circulation. Page 1: rating, sizing, three-sentence thesis, three what-would-reverse triggers. Pages 2-4: scenario table, key forensic flags, source matrix excerpt.

**3. IC Debate Script** — Verbal script + 20-question Q&A bank covering the strongest objections from the Red Team plus PM-typical pushback (what would reverse, why this size, why not the obvious pair, factor exposure).

**4. LP Letter** — 1-2 page quarterly LP communication variant per `references/lp-letter-template.md`. Focus on attribution narrative, change-in-view, position adjustments. Conforms to common buy-side LP comms norms.

**5. Earnings Prep + Earnings Flash** — Pre-earnings night-before checklist (`earnings-prep-template.md`) covering consensus snapshot, KPI guide, management-commentary watch list, beat/miss scenario tree, options-implied move. Same-day T+30min structured response (`earnings-flash-template.md`) covering print-vs-consensus, guidance change, KPI delta, scenario weight update, what-would-reverse trigger check, position-sizing recommendation. Pre-announcement detection rule per D10: if pre-announcement is negative and exceeds -5% beat/miss vs consensus, invoke kill-memo flow.

Position sizing must be expressed for at least the 5 mandate types per D3:

- Long-only large-cap (benchmark: S&P 500)
- Long-only SMID / all-cap (benchmark: Russell 3000 or Russell 1000/2000)
- L/S hedge fund (gross / net exposure, no single-stock benchmark)
- Sector specialty (benchmark: sector ETF or custom basket)
- Pair-trade structure (benchmark: pair spread)

**Optional artifact delegation** (gated on plugin availability — `financial-analysis` and `equity-research` from `claude-for-financial-services`):

- Excel DCF: orchestrator dispatches `financial-analysis:dcf-model` with the A7 5-scenario block collapsed to 3-case (Bear / Base / Bull) per the contract in `references/tool-composition-us.md`. Output: `outputs/<ticker>_DCF.xlsx`.
- Excel comps: orchestrator dispatches `financial-analysis:comps-analysis` with the A3-Peers peer set and standardized financial fields. Output: `outputs/<ticker>_Comps.xlsx`.
- Polished 30-50pg DOCX: orchestrator dispatches `equity-research:initiating-coverage` Task 5 with intermediate Markdown files (`<ticker>_Research_Document_<date>.md`, `<ticker>_Valuation_Analysis_<date>.md`) plus the Excel model. Output: `outputs/<ticker>_Initiation_Report_<date>.docx`.
- Excel audit: any Excel artifact this skill produces can be quality-gated through `financial-analysis:audit-xls`.

If the plugins are not installed, the skill produces complete Markdown + structured JSON deliverables and surfaces a one-line note that Excel / DOCX outputs require installing `financial-analysis@claude-for-financial-services` and `equity-research@claude-for-financial-services`.

The Markdown memo and structured JSON (`outputs/<ticker>_IC_memo.md` + `outputs/<ticker>_structured.json` conforming to `schemas/memo.json`) are the **single source of truth**. Excel and DOCX artifacts are derived. If a number changes during PM red-team via `us-equity-ic-rigor`, it propagates from JSON to all artifacts on rebuild.

## Common Failure Modes

These are the recurring traps. Watch for them.

**Hallucination of regulatory designation.** Sub-agents will confidently claim "company X is on the Entity List" or "company Y is on the OFAC SDN list" when the actual fact is "lawmakers have requested addition" or "the company is under preliminary investigation." Verify every regulatory designation directly against BIS / OFAC / Federal Register / FDA action-letter database. Same discipline applies to antitrust ("FTC has filed suit" vs "FTC has opened an investigation"), M&A ("deal announced" vs "deal closed" vs "deal blocked"), and litigation ("class action filed" vs "class certified" vs "settled").

**$M vs $B unit confusion.** US analog of China 亿/billion confusion. A 10x error here destroys the memo. Some filings report in thousands; some in millions; some in billions. Always check the unit declaration in the financial statements header. Also watch for basis-points vs percent confusion (100x error).

**Pre-cutoff stale earnings call reference.** Model cutoff is January 2026. Any earnings call after that cutoff must be web-verified; do not rely on training-data recall for FY25Q4, FY26Q1, or later transcripts. The current session date is 2026-05-15.

**Non-GAAP / GAAP gap obscuring earnings quality.** US filers report both. Analysts often anchor to non-GAAP without reconciliation. If non-GAAP-to-GAAP delta is >25% of net income sustained over 5 years, that is a red flag — common abuses include persistent "one-time" restructuring charges, "adjusted EBITDA" excluding SBC and recurring acquisition costs, idiosyncratic "FCF" definitions. Gate G11 verifies reconciliation.

**SBC excluded from FCF making cash generation look stronger than it is.** Many companies define "FCF" as operating cash flow minus capex, with SBC fully added back at the OCF line and never re-charged. This is a free pass on real economic dilution. Gate G12 verifies that the memo's FCF definition treats SBC consistently with the bear bridge.

**Cherry-picking the bearish data point.** When industry data has multiple sub-segments (e.g., "data center capex +30% but networking -15%, switching +45%"), agents tend to grab the headline and miss the nuance. Read the full data, not just the lead.

**Confirmation bias compounding across agents.** Agent A introduces a finding, agents B and C accept it as fact, the PM synthesis treats it as established. Verification must explicitly re-test claims that propagated through multiple agents.

**Anchoring to existing position (endowment effect).** When evaluating "should we hold this stock?" the analytically correct frame is "would I buy this at current price?" — not "what is my cost basis?" Endowment effect is the most common bias in equity research. Same trap as China skill; preserved verbatim.

**Confusing rating with sizing.** "Buy" rating does not equal "core position." A Buy with limited conviction is a half-weight position. State both explicitly and explain the gap. The 5-band rating per D1 reflects 12mo expected return; the per-mandate sizing per D3 reflects conviction times volatility times capacity.

**Anchoring guidance to the press release instead of the transcript.** Companies sometimes give different ranges on the call vs in the 8-K Item 7.01 press release. Verify against the transcript per delta matrix §11.

**R-v2 spawn fails or returns weak attacks (v0.4.0).** If the isolated R-v2 cannot find specific attack points on a declared consensus variance, the structural enforcement is to demote the variance, not to soften R-v2's requirements. A variance that no isolated red team can find a specific weakness in is, by construction, defensible — keep it load-bearing. A variance that cannot be attacked on any of the five canonical dimensions is, by construction, decorative or unfalsifiable — demote it (`load_bearing = false`), which may then fail G15 and pull the rating back toward a consensus-anchored Hold. Both outcomes are correct. The wrong move is to relax the win condition so R-v2 "passes" a variance it could not actually break — that re-imports the very contamination the isolated dispatch exists to remove. See the Phase 3 R-v2 dispatch subsection and `references/r-v2-isolated-attack-us.md`.

## When to Stop and Ask the User

The skill is comprehensive but not autonomous. Pause to ask the user when:

1. After Phase 0 if mandate, sector, or data access is unclear and defaults would materially shift the answer (e.g., pair-trade benchmark, ADR vs US-domiciled treatment).
2. After Phase 1 if a major agent failed and refresh would take significant time, OR if FS forensics surfaced a material restatement or going-concern flag that changes the entire frame.
3. Before Phase 2 if Phase 1 surfaced an unexpected showstopper — fraud allegation, suspended trading, pending acquisition, surprise Entity List addition.
4. Before final IC memo if verification surfaced material errors that change the directional view, or if any of the 20 verification gates fails and remediation requires user input.
5. Before invoking artifact delegation (Excel DCF / comps / polished DOCX) — these are opt-in per D21; ask whether user wants them.
6. Whenever a major decision point hinges on user-specific context (risk tolerance, liquidity needs, existing book exposure, factor correlations).

Otherwise, follow the workflow without interrupting.
