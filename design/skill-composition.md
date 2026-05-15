# Skill Composition Strategy

The user installed two plugins after Phase A was committed: `financial-analysis` and `equity-research` from the `claude-for-financial-services` marketplace. These plugins contain skills that overlap with what we're building. This document catalogs every relevant skill in those plugins and states our composition choice for each.

**The bottom-line decision**: `us-equity-research` and `us-equity-ic-rigor` are the **buy-side opinionated framework + verification layer** that's missing from those plugins. They COMPOSE WITH the existing skills as building blocks, not duplicate them. The existing skills are **output primitives** (Excel DCF, Excel comps, polished DOCX assembly); our plugin is the **analytical orchestrator** that produces structured content and delegates output generation.

**Failure mode if dependency missing**: us-equity-research still runs end-to-end and produces Markdown deliverables + structured JSON conforming to `schemas/memo.json`. Excel outputs and polished DOCX assembly are gated behind those plugins being installed.

---

## Inventory: `equity-research` plugin (v0.1.0)

| Skill | What it produces | Sell-side or buy-side flavor? | Composition choice for our plugin |
|---|---|---|---|
| `initiating-coverage` | 30-50pg DOCX initiation report, 5-task pipeline (research → 6-tab Excel model → DCF/comps valuation → 25-35 charts → DOCX assembly). JPM/GS/MS sell-side format. | Sell-side flavor (initiation report format) | **Optional delegate** for client-facing DOCX deliverable. Our institutional memo lives in Markdown; if a user wants a polished 30-50pg DOCX, the orchestrator can dispatch `equity-research:initiating-coverage` Task 5 with our structured content as inputs. Not invoked by default. |
| `earnings-analysis` | 8-12pg DOCX quarterly update, 3-5K words, beat/miss + updated estimates. | Sell-side flavor | **Optional delegate** for a polished DOCX earnings update. Our own `earnings-flash-template.md` (Phase B) is Markdown, real-time, T+30min. Different use case — flash is for the buy-side PM the morning of; earnings-analysis is for distribution. |
| `earnings-preview` | 1-page pre-earnings markdown with bull/base/bear scenarios. | Buy-side flavor (lightweight, opinionated) | **Reference template** for our `earnings-prep-template.md` (Phase B). We adopt its structure (consensus + scenario + catalyst checklist) and add buy-side rigor (S1-S5 anchoring of consensus, options-implied move, what-would-reverse triggers, position-sizing impact). |
| `morning-note` | 1-page morning meeting note, opinionated, tight 2-min read. | Buy-side flavor | **Reference template** for an optional `morning-note-template.md` derivative (Phase B-deferred). Useful for daily portfolio context; can layer on top of monitoring-framework outputs. Not a Phase B priority; may add in Phase F or later. |
| `thesis-tracker` | Markdown thesis scorecard with date-stamped log of pillar/risk/catalyst changes. | Buy-side flavor | **Reference template** for monitoring framework. Our `monitoring-framework-us.md` (Phase B) already covers Tier 1/2/3 triggers; we can add a thesis-tracker-style scorecard section that aligns with this skill's output for portability. |
| `model-update` | Refresh existing financial model with new quarterly data. | Sell-side flavor (Excel mechanic) | **Skip** — not a buy-side IC-rigor concern. The model belongs in `financial-analysis:dcf-model` or `financial-analysis:3-statement-model`. Our `model-update` analog is "re-underwrite at next quarterly print" in `monitoring-framework-us.md`. |
| `sector-overview` | Sector-level analysis. | Sell-side flavor | **Skip** — out of scope. We're single-name fundamental. |
| `catalyst-calendar` | Catalyst calendar maintenance. | Buy-side flavor | **Reference template** — our IC memo §10 catalyst calendar (per opinion-letter-section-checklist) is structurally similar. We can ensure our output is compatible with this skill if user wants to maintain a long-running calendar. |
| `idea-generation` (`screen`) | Stock screen / idea generation. | Buy-side flavor | **Skip** — different use case. We're deep single-name research, not screening. |

## Inventory: `financial-analysis` plugin (v0.1.0)

| Skill | What it produces | Composition choice for our plugin |
|---|---|---|
| `dcf-model` | Institutional Excel DCF with WACC sheet, Bear/Base/Bull scenarios via case selector, 3 sensitivity tables (5×5), formula discipline (blue inputs / black formulas / green links), cell comments with sources, recalc verification. | **PRIMARY DELEGATE for Excel DCF output.** Phase 3 A7 (valuation specialist) produces our structured valuation JSON; if user requests Excel output, orchestrator invokes `financial-analysis:dcf-model` with A7 outputs as inputs. The Excel is a deliverable artifact; the analytical content lives in our IC memo (Markdown) regardless. |
| `comps-analysis` | Excel comps with operating metrics + valuation multiples + Min/25th/Median/75th/Max statistics, cell comments, sources. | **PRIMARY DELEGATE for Excel comps output.** Phase 2 A3-Peers produces our structured peer JSON; orchestrator can dispatch `financial-analysis:comps-analysis` to produce the Excel artifact. |
| `3-statement-model` | Excel 3-statement model template fill-out. | **Optional delegate** if user wants a separate fully-built 3-statement model. Our Phase 1 FS specialist already pulls financials; this skill is for the modeling output layer. |
| `lbo-model` | LBO model. | **Skip** — PE deal flavor, not single-name long/short. Out of scope. |
| `audit-xls` (`debug-model`) | Audits Excel model for formula errors, balance, tie-out. | **Optional delegate** after any Excel artifact we produce. Quality gate. |
| `competitive-analysis` | Competitive landscape deck / presentation. | **Skip by default** — output is presentation (.pptx), not memo. Could be Phase F+ optional output. |
| `ib-check-deck` | IB deck QC (numbers consistency, narrative alignment). | **Skip** — we're producing memos, not banker decks. |
| `deck-refresh` | Update existing deck with new numbers. | **Skip** — same reason. |
| `clean-data-xls` | Data cleaning helper. | **Skip** — utility, not relevant. |
| `xlsx-author`, `pptx-author` | Headless xlsx/pptx file production. | **Used transitively** by dcf-model, comps-analysis, etc. Not directly invoked by us. |
| `skill-creator` | Helper for creating new skills. | **Used during Phase B-F** as a reference if our SKILL.md scaffolding needs guidance, but we're following the China-equity template structure directly so this is a fallback. |
| `ppt-template`, `ppt-template-creator` | PPT template plumbing. | **Skip** — no .pptx outputs in scope. |

## Inventory: other claude-for-financial-services plugins (lower relevance, surveyed for completeness)

| Plugin | Notable skills | Relevance |
|---|---|---|
| `valuation-reviewer` (agent-plugins) | `ic-memo`, `returns-analysis`, `portfolio-monitoring` | `ic-memo` is **PE deal memo** (Proceed/Pass/Conditional proceed), not buy-side equity IC. Different audience. Skip. |
| `spglobal` (partner-built) | `tear-sheet`, `earnings-preview-beta`, `funding-digest` | Data-provider-flavored. Skip; we use EDGAR primary. |
| `lseg` (partner-built) | `equity-research`, `bond-relative-value`, `fx-carry-trade`, etc. | Mostly rates/FI/macro skills; the `equity-research` is LSEG-data-flavored. Skip. |
| `investment-banking` (vertical) | `pitch-deck`, `teaser`, `process-letter`, `buyer-list` | Sell-side IB deal flow, not buy-side research. Skip. |
| `operations`, `wealth-management` (vertical) | KYC, client-report, tax-loss-harvesting | Out of scope. Skip. |

---

## The composition pattern

```
User invokes: /us-equity-research NVDA "build me a thesis"
                    │
                    ▼
        us-equity-research orchestrator (Markdown + JSON)
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    Phase 1-3   Verification  IC-rigor gates
   (5+5+4       (12+ Web)     (11 scripts)
   specialists)
        │
        ▼
   Structured JSON memo  ───────► outputs/NVDA_structured.json
   Markdown IC memo      ───────► outputs/NVDA_IC_memo.md
                    │
                    ▼ (optional, gated on user request + plugin availability)
   ┌─────────────────────────────────────────────────────────────┐
   │ delegated artifact builds:                                  │
   │   financial-analysis:dcf-model  ───► NVDA_DCF.xlsx          │
   │   financial-analysis:comps-analysis ───► NVDA_Comps.xlsx    │
   │   equity-research:initiating-coverage Task 5 ───► NVDA.docx │
   │   financial-analysis:audit-xls  ───► validation report      │
   └─────────────────────────────────────────────────────────────┘
```

**Key invariant**: the Markdown memo + structured JSON are the **single source of truth**. Excel and DOCX artifacts are derived. If a number changes during PM red-team, it propagates from JSON → all artifacts on rebuild. Same discipline as China skill's `<ticker>_投资意见书_<author>.docx` flowing to `<ticker>_精简版`, `<ticker>_IC_Debate_Script`, etc.

## Concrete delegation points (Phase B implementation)

These get baked into Phase B SKILL.md and reference files:

1. **Phase 3 A7 (valuation specialist) prompt** mentions: "After producing the structured DCF/SOTP/peer-multi JSON, if user requested an Excel DCF artifact and `financial-analysis:dcf-model` is available, orchestrator dispatches that skill with the A7 outputs (NOPAT path, WACC components, terminal assumptions, sensitivity ranges) as inputs."

2. **Phase 2 A3-Peers prompt** mentions: "If user requested Excel comps artifact and `financial-analysis:comps-analysis` is available, orchestrator dispatches with peer set + standardized financial fields."

3. **Phase 4 (multi-audience derivative — Phase B `multi-audience-delivery-us.md`)** mentions: "Client-facing DOCX deliverable is OPTIONAL. If requested and `equity-research:initiating-coverage` is installed, orchestrator dispatches Task 5 (Report Assembly) with our IC memo content as the input. Otherwise, only Markdown deliverables are produced."

4. **`us-equity-research/SKILL.md` description** mentions: "Optional polished Excel/DOCX outputs when `financial-analysis` and `equity-research` plugins are also installed."

5. **`us-equity-research/references/tool-composition-us.md`** (NEW file added to Phase B file-ownership): documents the delegation contracts — what JSON our orchestrator passes to each delegate, what artifact it expects back.

## Non-composition: what we keep ourselves

These are NOT delegated because they're the buy-side rigor that doesn't exist in those plugins:

- **All S1-S5 source stratification logic** (`source-stratification-us.md`)
- **5-scenario probabilistic framework with EPS×PE multiplicativity verification** (`five-scenario-framework-us.md`, `verify_eps_pe.py`)
- **Three-method valuation reconcile discipline** (`three-method-valuation-us.md`)
- **GM taxonomy + segment reconciliation** (`gm-taxonomy-us.md`, `verify_segment_gm.py`)
- **Bear bridge with soft/clean/strong layers** (`bear-bridge-us.md`, `verify_bear_bridge.py`)
- **What-would-reverse triggers with numerical denominators** (`what-would-reverse-us.md`, `verify_what_would_reverse.py`)
- **A0 tail mapping with probability conservation** (`tail-risk-mapping-us.md`)
- **Source-conditional headline language** (`source-stratification-us.md` §3)
- **Conviction-adjusted Kelly position sizing** (`position-sizing-us.md`)
- **PM red-team rubric + 6-9 score bands + bug catalog** (`pm-redteam-rubric-us.md`)
- **Multi-agent parallel orchestration with web verification** (`SKILL.md` workflow + `phase-1-deep-dive-us.md`)
- **All 11 verification scripts** (Phase C + Phase D quant overlay)
- **Quant overlay layer** (Phase D — Barra factors, capacity, edge decay, correlation, stress)
- **Forensic accounting checklist for US** (`forensic-accounting-checklist-us.md` — ASC 606/842/718, non-GAAP, restatements, pension, Form 4)
- **Regulatory desk for US** (`regulatory-desk-us.md` — FTC/DOJ/state AGs/EU CMA, BIS/OFAC/CFIUS, sector regulators)
- **Positioning/sentiment desk** (`positioning-sentiment-us.md` — 13F + Form 4 + 13D + short interest + options + ETF flows + index inclusion)
- **Verification protocol** (`verification-protocol-us.md` — EDGAR full-text, transcript-over-press-release)

## Trigger phrase coordination

To avoid trigger conflicts, our SKILL.md descriptions specifically claim the **buy-side PM-rigor + multi-agent + verification** territory, leaving:

- `equity-research:initiating-coverage` claims **client-distributable sell-side-style initiation report**
- `equity-research:earnings-analysis` claims **8-12pg DOCX quarterly update for distribution**
- `equity-research:morning-note` claims **daily 1-page note**
- `financial-analysis:dcf-model` claims **Excel DCF model construction**
- `financial-analysis:comps-analysis` claims **Excel comps construction**

Our triggers (open-decisions.md D18) specifically include:
- "PM red-team", "score this memo", "round N", "push from 8.x to 9.x" → ONLY us-equity-ic-rigor
- "build me a thesis on", "is X a buy", "kill thesis on" → us-equity-research orchestrator
- "S1-S5", "five-scenario", "three-method reconcile" → us-equity-ic-rigor

Pattern: when a user asks "build me a thesis on NVDA", us-equity-research fires (not initiating-coverage); the orchestrator may then delegate to initiating-coverage Task 5 at the end of Phase 3 if user has requested a DOCX deliverable.

## Provisional answer to user: "Should we depend on these plugins?"

**Yes, soft-dependency.** us-equity-research detects whether `financial-analysis` and `equity-research` plugins are installed at runtime (via Skill tool availability) and:
- If installed: delegates Excel + polished DOCX outputs to them
- If not installed: produces Markdown + JSON outputs only; surfaces a one-line note that "Excel DCF / Excel comps / polished DOCX outputs require installing `financial-analysis@claude-for-financial-services` and `equity-research@claude-for-financial-services`."

This matches the BUILD_PROMPT EDGAR-only-mode-portability principle: the plugin works standalone; premium outputs are optional.

## Open decision added to `open-decisions.md`

See **D21** in `./open-decisions.md` for the composition strategy decision.
