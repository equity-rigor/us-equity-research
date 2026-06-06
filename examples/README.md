# Examples — Plugin Self-Test Calibration Memos

This directory contains the five calibration memos produced during the framework's v0.1.0 calibration phase. They demonstrate the orchestrator's output format end-to-end on real US-listed equities and exercise the verification gates available at v0.1.x.

## Important disclaimers (read first)

**These memos are NOT investment advice or recommendations.** They are plugin self-test artifacts. They were produced to:

- Validate that the framework produces structurally consistent output across sector types (tech, banks, pharma, energy, REIT)
- Exercise the 14 verification gates available at v0.1.x (G1-G14)
- Provide concrete examples of what the framework's institutional IC memo format looks like
- Generate fixture data for cross-version regression testing of schema and verifier changes

**They do NOT reflect any current or past employment.** The author is a graduate student. These memos were produced for the purposes above and not in connection with any buy-side, sell-side, or research employer.

**Numerical thresholds and methodologies are author-asserted, not empirically validated.** The framework has no backtest. The rubric grades structural completeness and verification gate pass rates — it does NOT measure predictive accuracy. A 9.0-scoring memo in this directory is well-structured, internally consistent, and disciplined in source attribution. It is not, by any empirical measure, a profitable trade idea.

**The numerical figures in these memos may be stale.** They were produced during the v0.1.0 calibration window and have not been refreshed. Treat the dollar figures, scenario probabilities, and PT targets as illustrative of format, not as current views.

## File naming convention

Each ticker has five companion files:

- `<TICKER>_IC_memo.md` — the full institutional IC memo, 12-section structure per `references/ic-memo-template-us.md`
- `<TICKER>_structured.json` — structured representation conforming to `schemas/memo.json`
- `<TICKER>_source_tags.json` — S1-S5 source citations and headline-conditionality declarations per `schemas/source_tags.json`
- `<TICKER>_scenarios.json` — 5-scenario probabilistic valuation per `schemas/scenarios.json`
- `<TICKER>_verification_gates.json` — gate-by-gate pass / fail / n_a audit trail per `schemas/verification_gates.json`

## The five tickers

| Ticker | Sector | What it exercises |
|---|---|---|
| NVDA | Tech / semis | Forward P/E primary; large customer concentration analysis; SBC discipline; export-control regulatory tail |
| JPM | Diversified Banks | P/B + ROE-implied valuation; (pre-v0.2.0 — bank discipline G16 was not yet enforced at the time of writing) |
| MRK | Pharma | EV/Sales + NPV pipeline; IRA Round 1 / Round 2 modeling; LOE cliff bridge |
| XOM | Integrated E&P | EV/EBITDAX + FCF yield; commodity-cycle S5 anchor stress; Pioneer synergy timing variance |
| DLR | Data Center REIT | P/AFFO + NAV; capacity-MW source-tag discipline; hyperscaler customer concentration |

## Schema version and gate applicability

All five memos declare `schema_version: "0.1.0"`. They are grandfathered against the gates added in v0.2.0+ (G15 consensus variance, G16 bank discipline, G17 revision velocity) and v0.3.0+ (G18 quant cross-doc consistency, G19 provenance manifest, G20 view defensibility) and v0.4.0+ (G20 graduated rigor scale).

If you want to exercise the full 20-gate stack including the v0.3.0+ rigor, you'll need to run the framework on a fresh ticker and produce a v0.3.0-grade or v0.4.0-grade memo with an associated provenance manifest. These calibration memos are useful as format examples but they predate the strongest verification discipline.

## Re-running these tickers

Two caveats if you choose to re-run any of these tickers using the framework:

1. **Non-determinism.** The framework has non-deterministic agent dispatch (LLM sampling variance, WebSearch result ranking variance over time). Two runs on the same ticker on the same day will produce different memos. The verification gates verify structural consistency, not run-to-run reproducibility.

2. **Currency.** Many figures in these memos are dated. Re-running pulls current data, which may materially shift scenario probabilities, PT ranges, and even rating. A re-run is a fresh exercise, not an update of the original.

## Why these specific names

The five tickers were chosen during v0.1.0 calibration to span the framework's sector coverage:
- Mega-cap tech with cyclical capex anchor (NVDA)
- Banks for the D24 NIM-as-T1 / PPNR-Pre-Tax SOTP discipline (JPM)
- Pharma for the LOE / pipeline rNPV / IRA modeling (MRK)
- Energy for commodity-S5 anchor + SOTP across E&P / refining / chemicals (XOM)
- REIT for AFFO / NAV / segment MW (DLR)

If you want to validate the framework against a sector not represented here, that's a useful contribution — open an issue or fork.

## Source

These memos were produced in May 2026 during the v0.1.0 calibration phase. See `CHANGELOG.md` for the version history. See `design/phase-e-calibration-summary.md` for the methodology notes from the calibration phase including the B13 factor profile baseline and B14 capacity threshold tables.
