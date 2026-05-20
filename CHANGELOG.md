# Changelog

All notable changes to this project will be documented in this file. Format
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) +
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-20

### Added — initial release

Two plugins released as one project:

- `us-equity-research` — multi-agent orchestrator for buy-side fundamental
  research on US equities. Phase 0 setup → Phase 1 (5 parallel specialists)
  → Phase 2 (5 deepening specialists) → Phase 3 (4 valuation specialists)
  → verification → institutional IC memo. EDGAR-only default; premium
  hooks opt-in.
- `us-equity-ic-rigor` — PM red-team layer. 14 verification gates G1-G14
  (10 inherited from China A-share precedent + 4 US-specific: non-GAAP
  reconciliation, SBC-in-FCF, Barra factor exposure, capacity / ADV /
  days-to-exit). 5-scenario probabilistic framework. 5-band rating per
  D1. Score-band PM rubric (6.0-9.0+).

### Design decisions ratified

24 decisions (D1-D24) documented in `design/open-decisions.md`. Notable:

- D5: EDGAR-only default mode for portability
- D13: quant overlay mandatory in every institutional memo
- D15: Markdown-only mandatory output
- D17 / D22: 4-schema decomposition frozen at end of Phase B0
- D21: soft-dependency composition with claude-for-financial-services
- D24: banks GM-taxonomy + SOTP adaptation (NIM / efficiency-ratio T1-T5;
  PPNR / Pre-Tax SOTP columns)

### Phase E calibration set

5 institutional IC memos produced end-to-end and PM-red-team scored:

- NVDA (mega-cap tech, P/E primary): scored 8.9 after 1 iteration cycle
- JPM (banks, P/B + ROE-implied): scored 8.7
- XOM (integrated E&P, EV/EBITDAX + NAV): scored 9.0
- MRK (large-cap pharma, P/E + NPV pipeline): scored 9.0
- DLR (mid-cap data center REIT, P/AFFO + NAV): scored 9.0

All 5 cleared D20 ≥8.5. Cross-thesis correlation: NVDA-DLR ~0.55-0.65
(shared hyperscaler-capex anchor). See
`design/phase-e-calibration-summary.md` for B13 factor profile baseline
+ B14 capacity threshold tables.

### Test surface

13 verification scripts + 198 pytest tests passing (15 per gate × 14
gates against the single-fault-injected NVDA fixture matrix; +1 calling-
contract test for G3).

### Known follow-ups (post-v0.1.0)

- REIT codification (D25-candidate): DLR memo handled REIT field-
  mapping inline; pending future REIT memo (AMT / PLD / EQIX / etc.) to
  trigger formal codification.
- Strategy-size-aware G14 thresholds: current G14 checks presence
  of `adv_30d_usd_m` + `days_to_exit_10pct_participation`; does not
  yet parameterize mandate-specific thresholds.
- Polish fix-list: ~60 min of polish across the 5 Phase E memos
  documented in calibration summary.
