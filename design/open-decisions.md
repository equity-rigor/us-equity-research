# Open Decisions — Phase A → Phase B Gate

Each row is a decision that has been **provisionally answered with a stated assumption** so Phase B can proceed. The user can override any assumption before Phase B starts; otherwise the build proceeds with the recommendation. Per BUILD_PROMPT: "Don't ask clarifying questions when assumptions can be stated and proceeded from." This file is the assumption log, not a question list.

For each row: **decision** → **recommended answer** → **rationale** → **what it blocks if wrong**.

---

## D1 — Rating taxonomy: 5-band or 3-band?

**Recommendation**: 5-band — **Strong Buy / Buy / Hold / Sell / Strong Sell** with absolute-return bands.

**Default thresholds (12-month absolute return)**:
- Strong Buy ≥ +20%
- Buy +10% to +20%
- Hold ±10%
- Sell −10% to −20%
- Strong Sell ≤ −20%

**Rationale**: 5-band mirrors China precedent (买入/增持/中性/减持/卖出) and gives finer conviction signal than 3-band. US buy-side IC memos typically need this resolution. Wider thresholds than China (±20% vs ±15%) reflect higher base-rate US single-name vol.

**Blocks if wrong**: `SKILL.md`, `ic-memo-template-us.md`, `pm-redteam-rubric-us.md`, `position-sizing-us.md`. Score-band thresholds in rubric.

**Override path**: User specifies preferred bands; assumption changed in `SKILL.md` and template files before Phase B1 dispatch.

---

## D2 — Default time horizon

**Recommendation**: **12-month primary horizon, 24-month secondary horizon** for institutional memos. **3-6 month earnings prep horizon** for earnings prep/flash templates.

**Rationale**: Buy-side L/S typically 6-18mo; long-only quality 18-36mo. Defaulting to 12mo+24mo covers both with explicit secondary at the longer end. Catalyst calendar in monitoring framework extends to 18mo.

**Blocks if wrong**: `ic-memo-template-us.md`, `valuation-discipline-us.md` (forecast horizon), `monitoring-framework-us.md`, `position-sizing-us.md` (vol time-scaling).

---

## D3 — Default benchmark for position sizing

**Recommendation**: Provide explicit sizing for **four mandate types** in every IC memo:

1. **Long-only large-cap** (benchmark: S&P 500)
2. **Long-only all-cap / SMID** (benchmark: Russell 3000 or Russell 1000/2000)
3. **L/S hedge fund** (gross / net exposure, no single-stock benchmark)
4. **Concentrated specialty / sector fund** (benchmark: sector ETF or custom basket)
5. **Pair-trade structure** (benchmark: pair spread)

**Rationale**: Mirrors China multi-mandate sizing discipline. The pair structure is more common in US L/S than China. **Open question for user**: should we add a sixth mandate type — **"40 Act mutual fund"** (Investment Company Act constraints, 5%/10%/25% concentration rules)?

**Blocks if wrong**: `ic-memo-template-us.md`, `position-sizing-us.md`.

---

## D4 — Audience derivatives: keep retail variant?

**Recommendation**: **DROP retail variant.** Build only:

1. Institutional IC memo (full)
2. IC pre-read (≤4 page)
3. IC debate script (verbal + Q&A bank)
4. LP letter (1-2 page client-facing)
5. Earnings prep + earnings flash (operational, not audience-derived)

**Rationale**: US buy-side rarely delivers retail-flavored research. FINRA/SEC retail-comms rules (FINRA Rule 2210, SEC Reg BI) impose compliance burden that's out of scope for an internal tool. **LP letter** replaces retail as the "non-IC audience" variant.

**Drop**: Chinese-language deliverable entirely. No bilingual mode.

**Blocks if wrong**: `multi-audience-delivery-us.md`, `lp-letter-template.md`, and the absence of `retail-template-us.md`.

---

## D5 — Data-source tier: EDGAR-only vs premium hooks

**Recommendation**: **Plugin operates by default in EDGAR-only mode** (free, portable). Premium-data hooks (Visible Alpha, Capital IQ, AlphaSense, Bloomberg) are surfaced as **optional environment-variable-gated paths** in `us-data-sources.md`. Phase E NVDA self-test runs in EDGAR-only mode.

**Rationale**: Per BUILD_PROMPT — "final plugin must work in EDGAR-only mode for portability, with optional premium-data hooks." NVDA is well-covered enough on EDGAR + free trade press to validate the framework without paid sources.

**Blocks if wrong**: `us-data-sources.md` (tier organization), `SKILL.md` (mode flag and trigger phrases), `verification-protocol-us.md` (which sources count for S4 in EDGAR-only mode — currently Yahoo Finance consensus aggregator).

---

## D6 — Conviction multiplier ranges for US

**Recommendation**: Preserve China's 0.10× to 0.50× range. Calibrate:
- All anchors S1-S2, multi-cycle data: 0.50×
- Mix S1-S3, recent data: 0.25-0.35×
- S3-S5 dominant / source-conditional: 0.10-0.20×
- Heavy tail exposure: × 0.5× further

**Open question for user**: do you want **Kelly fraction caps**? E.g., max position = 5% of NAV regardless of computed Kelly (common at multi-strat funds)? **Default recommendation**: no global cap; let mandate type drive caps in `position-sizing-us.md`.

**Blocks if wrong**: `position-sizing-us.md`.

---

## D7 — Workflow phase structure

**Recommendation**: **Preserve 3 research phases + verification phase + final synthesis.** Phase 1 (5 specialists), Phase 2 (5 deepening), Phase 3 (4 valuation + final). Match China structure exactly.

**Optional simplification**: Could compress to 2 phases given EDGAR is one-stop disclosure (vs China's CNINFO + Sina + Eastmoney + bond market fragmentation). **Reject** because parallel specialization is the architectural value, not the disclosure search complexity.

**Blocks if wrong**: `SKILL.md` structure, all phase reference files.

---

## D8 — Sector-specific valuation defaults

**Recommendation**: `valuation-discipline-us.md` includes a **sector-default-multiple table**:

| Sector | Primary multiple | Secondary | Notes |
|---|---|---|---|
| Mature industrial / consumer / staples | P/E, EV/EBITDA | EV/Sales, P/B | |
| Banks (commercial) | P/B, P/E | P/PPNR, ROTCE-implied | |
| Insurance | P/B, P/E | ROE-implied P/B | |
| REITs | P/AFFO, NAV | Implied cap rate | |
| SaaS / software | EV/ARR, Rule of 40 | EV/Sales, FCF yield | |
| Biotech (pre-revenue) | NPV pipeline | (no multiple) | |
| E&P (oil/gas) | EV/EBITDAX, NAV | FCF yield | |
| Autos | EV/EBITDA, P/E | EV/Sales | |
| Airlines | EV/EBITDAR | P/E (cyclical) | |
| Asset managers | P/AUM, P/E | EV/EBITDA | |

**Rationale**: US sectors have heterogeneous valuation conventions; one-size-fits-all P/E breaks for banks/REITs/biotech/SaaS. The table forces explicit declaration of primary metric per sector.

**Blocks if wrong**: `valuation-discipline-us.md`, `three-method-valuation-us.md`.

---

## D9 — Verification calls minimum

**Recommendation**: **Preserve 12 WebSearch calls minimum per memo** (matches China). With EDGAR full-text search counting as WebFetch+WebSearch equivalent for primary-source verification, this remains the right minimum.

**Open question**: should NVDA self-test (Phase E) be allowed to scale up (e.g., 25-40 calls) to demonstrate the framework? **Recommendation**: yes — Phase E is a demonstration, not a constraint baseline.

**Blocks if wrong**: `verification-protocol-us.md`, Phase E success criteria.

---

## D10 — Pre-announcement and earnings-cycle handling

**Recommendation**: Add **pre-announcement detection** to `monitoring-framework-us.md` and `earnings-prep-template.md`. Pre-announcements (negative or positive) trigger an immediate flash response (within 4 hours of release) regardless of regular earnings date.

**Operational rule**: if pre-announcement is negative and exceeds **−5% beat/miss vs consensus**, the **kill memo template** is invoked (Phase 4 fallback). If positive, the **earnings flash template** runs.

**Blocks if wrong**: `monitoring-framework-us.md`, `earnings-flash-template.md`, `earnings-prep-template.md`.

---

## D11 — Currency handling for ADRs / foreign-issuer US-listed names

**Recommendation**: Default to **USD reporting**; native currency disclosed in appendix only. For ADRs (Toyota, Spotify, BABA, Nestlé, etc.), use **20-F** as the S1 source. Forensic adjustments include FX translation effect attribution.

**Open question**: are foreign-issuer ADRs explicitly in scope? Recommended: **yes — in scope, but flagged as a separate trigger pattern** in `SKILL.md`. Phase E does not test ADRs (NVDA is US-domiciled).

**Blocks if wrong**: `SKILL.md` (trigger patterns), `us-data-sources.md` (20-F/6-K handling), `valuation-discipline-us.md` (FX).

---

## D12 — Tail-risk catalog scope

**Recommendation**: Define **6 standing A0 events** with template probability shifts in `tail-risk-mapping-us.md`:

1. NBER recession trigger (US)
2. Fed rate shock (±200bp)
3. Sector regulatory action (FDA/FCC/FERC/NHTSA/EPA/FAA/CFPB/FTC/DOJ)
4. Sanctions / export control (BIS/OFAC/CFIUS)
5. Tariff / trade war (Section 301/232)
6. Election / political transition

Plus 2-3 **idiosyncratic A0 events** specific to the name (customer loss, IP litigation, M&A counterparty collapse).

**Rationale**: Mirrors China A0 discipline; the universe is sector-dependent so we provide template + instructions to customize.

**Blocks if wrong**: `tail-risk-mapping-us.md`.

---

## D13 — Phase D quant-overlay is institutional-default, not opt-in

**Recommendation**: Quant overlay (factor tags, capacity, edge decay, correlation, stress) is **mandatory in every institutional IC memo**, not opt-in.

**Rationale**: Per BUILD_PROMPT — "Add quant-overlay as a Phase 3 hard requirement." This makes the US skill more rigorous than the China skill, which is the point.

**Blocks if wrong**: `us-equity-ic-rigor/SKILL.md` requirement, `verify_quant_overlay.py` (verification script in Phase D), `ic-memo-template-us.md` (new section).

---

## D14 — Correlation overlay live wiring

**Recommendation**: Phase D delivers a **placeholder** in `quant-overlay-us.md` referencing an external book file (e.g., `~/book/holdings.json`) but **does not wire it live**. Wiring deferred to a future phase. The placeholder ensures the memo template has the slot.

**Blocks if wrong**: `quant-overlay-us.md`, `verify_quant_overlay.py`.

---

## D15 — Memo build artifact format

**Recommendation**: All memos as **Markdown (.md)** in `outputs/`. Drop docx generation (was China-specific via `_docx_helpers.js`). The structured JSON representation lives in `outputs/<ticker>_structured.json` conforming to `schemas/memo.json`.

**Rationale**: Markdown is portable, version-controllable, and toolable. PMs reading in Cursor / Obsidian / GitHub get rendering for free. Removing docx eliminates `_docx_helpers.js` complexity and column-width validation.

**Open question**: should we add an **optional PDF render hook** for client-facing LP letters? Recommendation: **no, not in initial scope.** LP letter as .md is sufficient; PDF render is a Phase G+ extension.

**Blocks if wrong**: `ic-memo-template-us.md`, all template files, NVDA self-test output format in Phase E.

---

## D16 — Source-tag regex format for verification

**Recommendation**: First-use citation format follows China pattern, English-localized:

- `(S1: NVDA 2024 10-K Item 7)`
- `(S2: NVDA FY24Q3 10-Q)`
- `(S3: NVDA FY24Q4 earnings call, 2025-02-26)`
- `(S4: Visible Alpha consensus, n=42, range $X–$Y, median $Z)` or `(S4: Yahoo Finance consensus EPS $X)`
- `(S5: Gartner DC GPU forecast 2026/03)`
- `(Pending — not used as anchor)`

`verify_source_tags.py` uses a regex pattern that matches `\((S[1-5]|Pending):.+?\)` at first appearance of each numeric in the memo.

**Open question**: should we enforce **inline citation on every recurrence** (verbose) or **first-use only** (China pattern)? **Recommendation: first-use only**, matching China discipline.

**Blocks if wrong**: `source-stratification-us.md`, `verify_source_tags.py`, `schemas/memo.json` source-tag field.

---

## D17 — Schema discipline: who owns `schemas/memo.json`?

**Recommendation**: Phase B0 (orchestrator-only) writes `schemas/memo.json`, `schemas/source_tags.json`, `design/file-ownership.md` per BUILD_PROMPT §"Memory and isolation discipline" point 5. **No verification script subagent in Phase C may modify these without orchestrator approval.**

**Blocks if wrong**: Phase B0 commit, all Phase C scripts, Phase E NVDA structured output.

---

## D18 — Trigger phrases in SKILL.md description (description-tuning)

**Recommendation**: `us-equity-research/SKILL.md` description triggers on:

- US tickers: 1-5 uppercase chars on NYSE/Nasdaq/AMEX/OTC (NVDA, AAPL, BRK.B, AMZN.OQ)
- Phrases: "is X a buy", "build me a thesis on", "stock pitch", "buy-side research", "IC memo", "fundamental analysis", "earnings prep for", "kill thesis on", "10-K read on", "pair-trade structure", "long X short Y"
- Sector phrases: "AI infrastructure", "energy transition", "biotech pipeline", "SaaS Rule of 40"

`us-equity-ic-rigor/SKILL.md` description triggers on:

- Score-band requests: "score this memo", "push from 8.x to 9.x", "round N review"
- Framework refs: "S1-S5", "five-scenario", "three-method reconcile", "GM taxonomy", "bear bridge", "what-would-reverse", "A0 tail"
- Audience derivatives: "IC pre-read", "IC debate script", "LP letter"

**Blocks if wrong**: Skill triggering correctness. Phase B SKILL.md scope.

---

## D19 — Conventional commit prefixes

**Recommendation**: Use `phase A:`, `phase B0:`, `phase B1:`, `phase B2:`, `phase C0:`, `phase C1:`, `phase D:`, `phase E:`, `phase F:` as commit prefixes. Each phase ends with a clean working tree per BUILD_PROMPT §"Memory and isolation discipline" point 7.

**Blocks if wrong**: Phase A commit. Git history readability.

---

## D20 — NVDA Phase E success criteria

**Recommendation**: Phase E success = all of:

1. `outputs/NVDA_IC_memo.md` and `outputs/NVDA_structured.json` produced
2. All 11 verification scripts (10 from Phase C + verify_quant_overlay.py from Phase D) exit 0 against the structured JSON
3. Memo scores ≥8.5 on `pm-redteam-rubric-us.md`
4. At least 12 distinct WebSearch+WebFetch calls during the run
5. Source matrix in memo appendix covers every specific number

**Failure handling**: per BUILD_PROMPT — "iterate — identify specific gate violations, fix the memo and/or the rubric, re-score. Loop until ≥ 8.5 or 3 iterations."

**Blocks if wrong**: Phase E iteration logic, when to declare done.

---

## D21 — Composition with newly-installed marketplace plugins

**Context**: After Phase A was committed, the user installed `financial-analysis` and `equity-research` plugins from `claude-for-financial-services`. Full inventory and per-skill choice in `./skill-composition.md`.

**Recommendation**: **Soft-dependency composition.** us-equity-research detects whether those plugins are installed and:
- If installed: delegates Excel DCF, Excel comps, and polished DOCX assembly to `financial-analysis:dcf-model`, `financial-analysis:comps-analysis`, and `equity-research:initiating-coverage` Task 5 respectively
- If not installed: produces Markdown + JSON only; surfaces a one-line note about how to enable Excel/DOCX outputs

**Phase B implications** (additions):
1. New Phase B reference file: **`us-equity-research/references/tool-composition-us.md`** documenting the JSON contract our orchestrator passes to each delegate
2. Phase 3 A7 (valuation) prompt mentions optional Excel DCF delegation
3. Phase 2 A3-Peers prompt mentions optional Excel comps delegation
4. `multi-audience-delivery-us.md` mentions optional polished DOCX delegation
5. `SKILL.md` description mentions optional Excel/DOCX outputs require the dependency plugins

**Skills DELEGATED (not duplicated)**:
- `financial-analysis:dcf-model` for Excel DCF artifact
- `financial-analysis:comps-analysis` for Excel comps artifact
- `equity-research:initiating-coverage` Task 5 for polished 30-50pg DOCX
- `financial-analysis:audit-xls` as quality gate for any Excel artifact we produce
- `financial-analysis:3-statement-model` if user requests a separate 3-statement workbook

**Skills used as REFERENCE TEMPLATES (we adopt structure, add buy-side rigor)**:
- `equity-research:earnings-preview` → informs our `earnings-prep-template.md`
- `equity-research:thesis-tracker` → informs scorecard section in `monitoring-framework-us.md`
- `equity-research:catalyst-calendar` → ensures our §10 catalyst calendar is interop-compatible

**Skills SKIPPED**:
- `lbo-model`, `competitive-analysis` (deck), `ib-check-deck`, `deck-refresh`, `clean-data-xls`, `model-update`, `sector-overview`, `idea-generation`, `valuation-reviewer:ic-memo`, `spglobal:tear-sheet`, `lseg:equity-research`, and all `investment-banking`/`operations`/`wealth-management` skills — out of scope or wrong audience.

**Trigger phrase coordination** (open question — should be ratified):
- Our triggers (D18) own "PM red-team", "score this memo", "round N review", "build me a thesis on", "kill thesis on", "is X a buy", "S1-S5", "five-scenario", "three-method reconcile" — the rigor / multi-agent / buy-side IC territory
- `equity-research:initiating-coverage` owns "initiate coverage on", "create an initiation report for" — the sell-side-format DOCX territory
- `equity-research:earnings-analysis` owns "earnings update for [company]", "Q[N] update", "post-earnings report"
- Risk: ambiguity on "earnings prep" vs "earnings update". Recommendation: our `earnings-prep-template.md` is pre-print preparatory; `equity-research:earnings-analysis` is post-print DOCX. Triggers don't collide if we use "earnings prep for" (pre-print) vs their "earnings update / Q[N] update / post-earnings" (post-print).

**Blocks if wrong**: `SKILL.md` triggers (D18), Phase 3 A7 prompt, Phase 2 A3-Peers prompt, `multi-audience-delivery-us.md`, `tool-composition-us.md` (net-new file), file-ownership table in Phase B0.

**Override path**: User specifies stronger preference — full self-contained (no soft-dependency, duplicate the Excel/DOCX logic) OR hard-dependency (refuse to run if plugins not installed). Recommended default is soft.

---

## Items NOT decided here (deferred)

The following are out of scope for the current build and will not be decided in Phase A:

- **MCP server integration** for Daloopa / Visible Alpha / Bloomberg — referenced as optional hooks in `us-data-sources.md` but not implemented
- **Live correlation wiring** to a real book file — placeholder only
- **Real-time price/quote feeds** — verification protocol relies on web-cited freshness, not direct feed
- **Slack / email notification hooks** — out of scope
- **PDF rendering for LP letter** — out of scope (Markdown only)
- **Compliance review / legal disclaimer auto-generation** — out of scope

---

## Default behavior if user does not respond before Phase B kick-off

If the user gives a `/goal` covering Phase A or otherwise authorizes automatic continuation, proceed with all D1-D20 recommended answers. If the user instead reviews and overrides any answer, the override propagates to:

- `SKILL.md` (D1, D4, D5, D11, D18)
- `ic-memo-template-us.md` (D1, D2, D3, D4, D8, D13, D15)
- `position-sizing-us.md` (D3, D6)
- `valuation-discipline-us.md` (D2, D8, D11)
- `monitoring-framework-us.md` (D10, D12)
- `verification-protocol-us.md` (D5, D9, D16)
- `tail-risk-mapping-us.md` (D12)
- `schemas/memo.json` (D17)
- All commit messages (D19)
- Phase E criteria (D20)

Phase B0 writes shared contracts AFTER any user override is incorporated.
