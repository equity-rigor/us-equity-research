I'm building a Claude Code plugin called `us-equity-research` — an opinionated, automated framework for fundamental research on US listed equities. It will replace ad-hoc analyst workflows on my buy-side desk.

Goal: produce IC-grade research notes, earnings flashes, kill memos, and quarterly updates for US single-name longs and shorts, with PM red-team rigor enforced by verification gates that run programmatically. The final deliverable must withstand a PM challenge that probes the math, the sources, the anchor weighting, and the falsification triggers — not just the directional view.

Starting material: in `templates/` I've placed two reference skills from the China A-share world that solve the same problem on a different market:
- `templates/china-equity-research/` — multi-agent orchestrator (5 specialists per phase, 3 phases, mandatory web verification, bilingual IC memo)
- `templates/china-equity-ic-rigor/` — PM red-team hardening layer (S1-S5 source stratification, 5-scenario probabilistic framework, three-method valuation reconciliation, GM taxonomy, bear EPS bridge, what-would-reverse triggers, 10 verification gates, two Python verification scripts)

Read both SKILL.md files and ALL files under their `references/`, `templates/`, `scripts/` subdirectories before writing anything. The architectural pattern is what I want to inherit. The China-specific layers (regulatory, data sources, rating taxonomy, language) are what I want to replace.

Use Superpowers methodology: invoke `brainstorming` first to map the US-vs-China deltas before any file is touched. Then use `subagent-driven-development` to build the components in parallel. Use `test-driven-development` on every verification script — tests before implementation. Use `skill-creator` discipline for the SKILL.md description-tuning so triggering is correct.

Treat this as a quant researcher's framework, not a generalist's. I am a buy-side analyst / quant researcher. Default to institutional depth. Don't ask permission to go deep. Don't ask clarifying questions when assumptions can be stated and proceeded from. Be a red team, not a cheerleader.

---

## Memory and isolation discipline (applies to every phase)

This governs every parallel subagent dispatch in this build. Inherit the China skill's PM-synthesis pattern: agents don't talk to each other directly; they communicate only via files curated by the orchestrator.

1. **Before any parallel subagent dispatch in a phase, the orchestrator (you, the main Claude Code instance) writes a single SHARED CONTRACT file** that all subagents in that phase will read. The contract specifies:
   - Schema of any data structure they produce (JSON shape, pytest fixture format, etc.)
   - File path conventions
   - Any cross-file dependencies they must respect

2. **Each parallel subagent receives, in its spawn prompt**:
   - Path to the shared contract file (MUST read first)
   - Path to the ONE China analog file it's adapting (MUST read second)
   - Path to the ONE output file it owns
   - Its assignment in 3-5 sentences
   - Explicit constraint: "Do not read any other subagent's output during your run. Do not write to any path outside your assigned output file."

3. **After all parallel subagents in a phase return, dispatch a single SYNTHESIS subagent** with:
   - Paths to all outputs from that phase
   - Instruction: "Identify contradictions, terminology drift, schema violations, or coverage gaps across these files. Produce a fix-up dispatch plan as a JSON list of {agent_role, file_to_fix, instruction}. Do NOT edit any file yourself."

4. **Orchestrator then re-dispatches the fix-up plan in parallel.** Same isolation rules. Loop until synthesis returns zero contradictions or three rounds pass (whichever first).

5. **Specific shared contracts to write**:
   - `schemas/memo.json` — JSON Schema for the structured memo representation that all 10 verification scripts will validate against. Written ONCE in Phase B before any verification script is built. All script subagents receive this path. None may modify it without orchestrator approval.
   - `schemas/source_tags.json` — enum of {S1, S2, S3, S4, S5, Pending} with definitions. Referenced by source-tag verification and by ic-memo template subagents.
   - `design/file-ownership.md` — table mapping every output file to its owning subagent role. Each subagent role is mentioned in exactly one row. Cross-file edits require orchestrator dispatch.

6. **Forward-only memory sharing through synthesis briefs.** Phase N+1 subagents receive Phase N's synthesis brief, NOT Phase N's raw subagent outputs. This matches the China skill's PM synthesis discipline and prevents context contamination across phases.

7. **Commit after each phase** with a conventional-commit message: `git add -A && git commit -m "phase X: <one-line summary>"`. Each phase ends with a clean working tree.

---

## Phase A: Hypothesis tree + data spec

- Read all template files. Produce `./design/us-vs-china-delta-matrix.md`: a row for every China-specific layer (data sources, regulatory desk, rating taxonomy, source stratification, valuation conventions, forensic accounting checklist, positioning desk, language) mapped to its US equivalent.
- Specify the canonical US data source for every analytical task: SEC EDGAR (10-K/10-Q/8-K/DEF 14A/13F/13D/13G/Form 4/S-1) as primary, Daloopa/Visible Alpha/FactSet/Bloomberg as secondary, earnings call transcripts (Capital IQ / AlphaSense / SeekingAlpha) for management commentary, FRED for macro, alternative data providers for channel checks. Mark each as "premium subscription required" or "public free" — final plugin must work in EDGAR-only mode for portability, with optional premium-data hooks.
- Build the US source stratification: S1 = audited 10-K, S2 = 10-Q/8-K/proxy, S3 = earnings call / management guidance / investor day, S4 = Visible Alpha consensus / sell-side, S5 = channel checks / alt data, Pending = unverified.
- Output `./design/us-vs-china-delta-matrix.md` plus `./design/open-decisions.md` listing every assumption that needs my confirmation. Do not create files outside `./design/` in this phase.

## Phase B: Skill scaffolding + shared contracts (parallel)

Step B0 (orchestrator only, before any parallel dispatch): write `schemas/memo.json`, `schemas/source_tags.json`, `design/file-ownership.md` per the memory discipline above. Commit B0 separately.

Step B1 (parallel dispatch with isolation rules): create the two top-level SKILL.md files and the references/, templates/ subdirectories. One subagent per file:

- `us-equity-research/SKILL.md` — mirrors China structure; US-specific descriptions and triggers (ticker patterns: 1-5 char US tickers on NYSE/Nasdaq/AMEX/OTC; trigger phrases: "is X a buy", "build me a thesis on", "earnings prep for", "kill thesis on", "10-K read on").
- `us-equity-research/references/us-data-sources.md` — EDGAR endpoints, Daloopa MCP setup if used, Visible Alpha access, transcript providers, alt-data vendors by sector.
- `us-equity-research/references/forensic-accounting-checklist-us.md` — ASC 606 revenue recognition red flags, ASC 842 lease capitalization, SBC normalization, goodwill impairment risk, non-GAAP-to-GAAP gaps, DSO/DIO/DPO trend breaks, deferred revenue declines, auditor changes/restatements, pension/OPEB underfunding, Form 4 insider selling patterns, 13D activist filings.
- `us-equity-research/references/regulatory-desk-us.md` — antitrust (FTC/DOJ/state AGs/EU CMA), sanctions/Entity List (BIS, OFAC), tariff/trade (Section 301/232), SEC enforcement, 10b-5/derivative litigation, sector-specific regulators (FDA/FCC/FERC/NHTSA/EPA/FAA/CFPB), state-level (CA CCPA, NY DFS), tax policy (BEAT/GILTI/corporate rate).
- `us-equity-research/references/positioning-sentiment-us.md` — 13F holder concentration, hedge-fund cluster analysis, short interest + DTC, insider Form 4 net activity, options skew & IV regime, sell-side rating distribution & PT range, S&P/Russell index inclusion risk, passive ETF flow exposure.
- `us-equity-research/references/valuation-discipline-us.md` — DCF (unlevered FCF; Gordon vs exit-multiple terminal; WACC build with US Treasury risk-free, ERP source, beta from regression), EV/EBITDA & EV/Sales & EV/FCF (when each is appropriate by sector), P/E & PEG (growth-stock framing), SOTP for diversified, LTM vs NTM vs forward, trading comps + precedent M&A transactions, implied-multiple analysis.
- `us-equity-research/references/monitoring-framework-us.md` — weekly/monthly KPIs by sector, earnings dates calendar integration, Form 4 alerts, 13F filing windows, sell-side estimate revision dashboards, kill criteria with numerical triggers.
- `us-equity-research/references/verification-protocol-us.md` — adapt the China verification protocol to US sources; minimum 12 WebSearch calls per memo; SEC EDGAR full-text search as primary verification; emphasize verifying mgmt guidance against transcript, not press release.
- `us-equity-research/references/ic-memo-template-us.md` — 12-section institutional structure: thesis / valuation triangulation / scenario weighting / position sizing across mandate types (long-only vs L/S vs concentrated specialty vs pair) / kill criteria / catalysts / risks / sources matrix.
- `us-equity-research/references/lp-letter-template.md` — client-facing 1-2 page variant.
- `us-equity-research/references/earnings-prep-template.md` — night-before checklist (consensus snapshot, KPI guide, mgmt-commentary watch list, beat/miss scenario tree).
- `us-equity-research/references/earnings-flash-template.md` — same-day, T+30min post-print structured response.

And for the IC-rigor skill:

- `us-equity-ic-rigor/SKILL.md`
- `us-equity-ic-rigor/references/source-stratification-us.md` — US S1-S5 with explicit document mapping; conditional headline language patterns for English.
- `us-equity-ic-rigor/references/five-scenario-framework-us.md` — strong-bull / bull / base / bear / strong-bear; weights sum to 1; each scenario has EPS path + multiple + narrative bridge.
- `us-equity-ic-rigor/references/three-method-valuation-us.md` — DCF / SOTP / multi-multiple reconciliation discipline (cross-checks, not averaging).
- `us-equity-ic-rigor/references/gm-taxonomy-us.md` — consolidated / segment / sub-segment / analyst-modeled / marginal GM, plus parallel non-GAAP-vs-GAAP discipline.
- `us-equity-ic-rigor/references/bear-bridge-us.md` — three-layer EPS adjustment (soft / clean / strong) with named drivers.
- `us-equity-ic-rigor/references/what-would-reverse-us.md` — numerical-denominator triggers for every directional view.
- `us-equity-ic-rigor/references/tail-risk-mapping-us.md` — A0 events specific to US (recession, rates, antitrust, sanctions, sector regulatory shock) → probability shifts → downside in worst case.
- `us-equity-ic-rigor/references/position-sizing-us.md` — sigma math, Sharpe, conviction-adjusted Kelly, factor-aware sizing (beta-adjusted vs S&P 500, sector-neutral vs sector ETF, pair-trade structures).
- `us-equity-ic-rigor/references/pm-redteam-rubric-us.md` — adapt the 6.0-9.0+ scoring bands; common US-specific bug catalog.
- `us-equity-ic-rigor/references/multi-audience-delivery-us.md` — institutional / IC pre-read / IC debate / LP letter / sell-side feedback note.

Step B2: synthesis pass — spawn one synthesis subagent that reads all B1 outputs and produces `./design/phase-b-synthesis.md` listing contradictions, gaps, terminology drift. Re-dispatch fix-ups per the memory discipline. Loop ≤3 rounds. Commit when synthesis returns zero contradictions.

## Phase C: Verification scripts (TDD)

Step C0 (orchestrator only): confirm `schemas/memo.json` and a fixture JSON memo `scripts/tests/fixtures/nvda_v0.json` exist. The fixture is a hand-crafted memo for NVDA with deliberate bugs embedded (one bug per verification gate). Document each bug in `scripts/tests/fixtures/nvda_v0_bugs.md`.

Step C1 (parallel dispatch, one subagent per script): for each of the 10 verification gates, write a Python script in `us-equity-ic-rigor/scripts/` that takes a structured JSON memo and returns pass/fail with detailed diff. TDD discipline: write the test in `scripts/tests/test_<gate>.py` FIRST (must fail without bug, pass with bug fixed), then write the implementation. Use pytest + pydantic for schema validation. Each script reads `schemas/memo.json` for shape.

Scripts:
- `verify_eps_pe.py` — adapt from `templates/china-equity-ic-rigor/scripts/verify_eps_pe.py`
- `verify_segment_gm.py` — adapt from China analog
- `verify_sotp_monotonicity.py` — NI ≤ OP ≤ GP ≤ Revenue per segment
- `verify_scenario_weights.py` — sum to 1.00 ± 0.01
- `verify_bear_bridge.py` — base → bear adjustment chain reconciles
- `verify_source_tags.py` — every specific number has S1-S5 or Pending tag at first appearance (regex-based)
- `verify_headline_conditionality.py` — if any top-3 anchor is S3 or weaker, headline must contain conditional language (regex match against a phrase library)
- `verify_gm_taxonomy_box.py` — checks 5 GM types defined + each usage tagged
- `verify_what_would_reverse.py` — every reverse trigger has a numerical denominator
- `verify_anchor_sensitivity.py` — required ±10pp probability-shift table exists for the strongest scenario

Step C2: run `pytest -q` from repo root. Must exit 0 with ≥30 tests passing. Print the output. Step C3: synthesis subagent reviews all scripts for consistency (same I/O signature, same error-message format, all read from `schemas/memo.json`). Fix-up as needed.

## Phase D: Quant-overlay layer (the "more refined" piece)

Add `us-equity-ic-rigor/references/quant-overlay-us.md`:
- Barra-style factor exposure tagging (value / quality / momentum / growth / size / low-vol / liquidity) — required for every memo; show how the name's factor profile interacts with the directional view
- Capacity analysis: ADV-based max position size, free-float availability, days-to-exit at 10% ADV
- Edge decay model: information half-life of the thesis, time-to-priced-in estimate, refresh cadence
- Correlation overlay: required pairwise correlation of this name with existing top-10 book positions (placeholder — to be wired to a live book file later)
- Stress overlay: scripted scenarios for +200bp rates, -20% oil, +5% USD, recession dummy; per-scenario downside

Update `us-equity-ic-rigor/SKILL.md` to reference the new file and add quant-overlay as a Phase 3 hard requirement. Add `verify_quant_overlay.py` to the verification scripts (factor tags, capacity table, stress table all present). Re-run pytest.

## Phase E: Self-test on NVDA

- Run the `us-equity-research` skill end-to-end on NVDA following the full multi-agent workflow with web verification.
- Produce `./outputs/NVDA_IC_memo.md` (institutional memo) and `./outputs/NVDA_structured.json` (the JSON memo representation conforming to `schemas/memo.json`).
- Run all 11 verification scripts against the structured JSON. All must pass.
- Score the memo on `us-equity-ic-rigor/references/pm-redteam-rubric-us.md`. Document in `./outputs/NVDA_score.md`. Score must be ≥ 8.5. If lower, iterate — identify specific gate violations, fix the memo and/or the rubric, re-score. Loop until ≥ 8.5 or 3 iterations.
- Print: final score, all script outputs, the rubric breakdown by section.

## Phase F: Plugin packaging

- Create `.claude-plugin/plugin.json` with marketplace metadata.
- Create `README.md` with installation instructions for both Claude Code (`/plugin install us-equity-research@<marketplace>`) and Cowork (manual skill install path).
- `git status` must be clean. Print the git log of all commits made during the build.

---

## Constraints (apply globally)

- Every reference file is ≤500 lines (context budget).
- Every SKILL.md description is concrete enough to trigger correctly (name specific triggers, ticker formats, phrases; not vague "use when doing US equity research").
- Verification scripts: pure Python 3.11, stdlib + pytest + pydantic only.
- All code passes `ruff check` and `pytest -q` before commit.
- Conventional commit messages, one commit per phase minimum (more granular within phases is fine).
- Never modify `./templates/` (read-only reference).
- Subagents follow memory-isolation discipline as defined above.

## Kickoff

Begin with Phase A. Show me the US-vs-China delta matrix in `./design/us-vs-china-delta-matrix.md` and the open-decisions log in `./design/open-decisions.md` before touching any file in the new skill directories. Commit Phase A. Then await my confirmation before starting Phase B, OR — if I have set a `/goal` covering Phase A — surface the delta matrix in the conversation and proceed automatically to Phase B once Phase A is committed.
