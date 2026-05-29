# us-equity-research

> Institutional buy-side fundamental research framework for US-listed equities, with a PM-grade red-team rigor layer.

![License](https://img.shields.io/badge/license-MIT-blue) ![Version](https://img.shields.io/badge/version-0.2.0-green) ![Tests](https://img.shields.io/badge/pytest-198%20passing-brightgreen)

## What this is

A two-plugin framework for doing single-name fundamental work on US equities at institutional buy-side quality. Plugin one (`us-equity-research`) orchestrates a multi-agent workflow that produces a Markdown IC memo and structured JSON outputs from a single ticker. Plugin two (`us-equity-ic-rigor`) layers a 17-gate PM red-team review (was 14 through v0.1.x; v0.2.0 adds G15 consensus variance / G16 bank discipline / G17 revision velocity) on top of that output, applying the kind of mechanical checks (segment GM ties to consolidated, EPS × multiple ties to target price, scenario probabilities sum to 1.00, non-GAAP reconciles to GAAP, FCF includes SBC, non-Hold ratings declare specific consensus variance with S1-S3 evidence, bank memos disclose AOCI bridge + CET1 walk + NIM trajectory + stress capital context) that catch the bugs that actually kill IC memos.

The framework is designed for buy-side analysts, quant-fundamental researchers, and PM-track associates who need disciplined single-name workflows with verified citations on every numeric claim. It composes with the `claude-for-financial-services` marketplace plugins from Anthropic FSI — delegating Excel DCF, Excel comps, and polished 30-50pg DOCX assembly to those plugins when installed — but produces Markdown + JSON outputs as the single source of truth regardless.

## Two-plugin architecture

| Plugin | Role | Phase coverage |
|---|---|---|
| `us-equity-research` | Multi-agent orchestrator | Phase 0 (setup) → Phase 1 (5 parallel discovery specialists; FS-Banks Augmentation when sector=Banks per v0.2.0) → Phase 2 (**6** deepening specialists as of v0.2.0; A-Consensus added) → Phase 3 (4 valuation specialists) → verification → IC memo assembly |
| `us-equity-ic-rigor` | PM red-team layer | 17 verification gates (G1-G17 as of v0.2.0; G15 consensus variance / G16 bank discipline / G17 revision velocity added) + 5-scenario probabilistic framework + 5-band rating per D1 + position sizing across 5 mandate types |

The two plugins compose: run `us-equity-research` to produce the raw IC memo + structured JSON; then run `us-equity-ic-rigor` to score it against the rubric and surface mechanical defects across the gates.

## Install paths

### Claude Code

```bash
# 1. Add the optional dependencies marketplace (provides financial-analysis + equity-research)
/plugin marketplace add anthropics/claude-for-financial-services

# 2. Add this project's marketplace (publish path TBD; for development use the manual install below)
/plugin install us-equity-research@<marketplace-when-published>
/plugin install us-equity-ic-rigor@<marketplace-when-published>
```

### Cowork

Same commands work in Cowork chat: `/plugin marketplace add`, `/plugin install`.

### Development / manual install

```bash
git clone <this-repo-url>
cd us-equity-research
cp -R us-equity-research us-equity-ic-rigor ~/.claude/plugins/
```

## Quick start

Two invocation paths — both work, pick whichever fits the moment.

### Path A — auto-discovered skills (probabilistic trigger)

```
You: "Build me a thesis on NVDA"
→ Triggers us-equity-research skill (matches ticker pattern + thesis intent)
→ Phase 0 setup, Phase 1-3 specialists, verification, IC memo
→ Outputs: outputs/NVDA_IC_memo.md + 4 JSON artifacts (memo, source_tags,
   scenarios, verification_gates)

You: "Score this memo. Push it from 8.x to 9.x."
→ Triggers us-equity-ic-rigor skill (matches "score this memo" + "push X to Y")
→ Runs 17 verification gates G1-G17 (as of v0.2.0) + scores against the PM rubric
→ Returns gate-by-gate findings + iteration plan
```

### Path B — explicit slash commands (deterministic trigger, v0.1.1+)

```
/us-equity-research:research NVDA
→ Runs Phase 0 only. Produces outputs/NVDA_structured.json
   + outputs/NVDA_Research_Document_<date>.md. Does NOT shape into IC memo.

/us-equity-ic-rigor:ic-memo NVDA
→ Chains Phase 0 (delegates to us-equity-research) → Phases 1-3 → enforces
   all 17 verification gates (v0.2.0+) → produces full IC memo + structured JSON outputs.

/us-equity-ic-rigor:red-team NVDA [target-score]
→ Phase 4 only. Assumes outputs/NVDA_IC_memo.md + structured JSON exist.
   Runs all applicable gates (17 as of v0.2.0; v0.1.x memos grandfathered to 14),
   scores against pm-redteam-rubric, produces ordered
   push-from-N-to-N+1 fix list. Default target score 8.5 per D20.
```

The slash commands and the auto-discovery triggers point at the same underlying skills — they are different entry points to identical pipelines. Use the slash commands when you want deterministic invocation (e.g. in a daily research routine); use the conversational triggers when the request is naturally phrased.

## Standing context

A condensed reference; see `design/build-log.md` for full design history.

- **17 verification gates G1-G17** (as of v0.2.0): G1 EPS × P/E reconcile, G2 segment GM reconcile, G3 SOTP NI ≤ GP, G4 scenario probabilities sum to 1.00, G5 bear bridge reconcile, G6 unsourced specifics, G7 unconditional S3-anchored headlines, G8 mixed GM definitions, G9 missing what-would-reverse denominators, G10 missing anchor sensitivity, G11 non-GAAP without GAAP reconciliation, G12 SBC excluded from FCF without flag, G13 missing Barra factor exposure, G14 missing capacity / ADV / days-to-exit, **G15 non-Hold rating without declared load-bearing consensus variance or "consensus-anchored" headline label** (v0.2.0), **G16 Banks-sector memo without AOCI bridge + CET1 walk + NIM trajectory + stress capital context** (v0.2.0), **G17 revision velocity not disclosed when n_analysts ≥ 5** (v0.2.0). G11-G14 are US-specific additions over the China A-share precedent; G15-G17 are v0.2.0 Sprint 1 additions closing the "where is consensus wrong" / "banks aren't depository institutions to this framework" / "revisions aren't first-class" gaps. v0.1.x memos with `schema_version="0.1.0"` are grandfathered to the 14-gate set.
- **5 scenarios** (per `schemas/scenarios.json`): `strong_bear` / `bear` / `base` / `bull` / `strong_bull`. Probabilities must sum to 1.00 within ±0.01.
- **5 mandate types** (per D3): `long_only_large_cap` / `long_only_smid` / `long_short_hedge_fund` / `sector_specialty` / `pair_trade`. Position sizing rubric in `us-equity-ic-rigor/references/position-sizing-us.md`.
- **6 source levels** (per `schemas/source_tags.json`): `S1` (audited primary) / `S2` (auditor / regulator) / `S3` (reputable secondary) / `S4` (industry / vendor) / `S5` (commentary / opinion) / `Pending` (placeholder). `Pending` cannot anchor an unconditional headline (G7).
- **5 GM taxonomy types** (T1-T5): T1 consolidated / T2 segment / T3 sub-segment / T4 modeled / T5 marginal. Banks adaptation (D24): NIM / efficiency ratio mapped to T1-T5 plus PPNR / Pre-Tax SOTP columns. See `us-equity-ic-rigor/references/gm-taxonomy-us.md`.
- **D16 citation regex** enforced on every numeric at first appearance.
- **12 WebSearch + WebFetch minimum** per memo (per D9).
- **EDGAR-only default mode** (per D5); premium hooks (Visible Alpha, Capital IQ, AlphaSense, Bloomberg) gate behind explicit user signaling.
- **Markdown-only mandatory output** (per D15); Excel / DOCX optional via marketplace plugin delegation.

## Phase E methodology validation

> This is a methodology validation, **not** a score guarantee. The framework was end-to-end tested by building five institutional IC memos and PM-red-team scoring each one. All five cleared the D20 success threshold (≥8.5). Future memo scores depend on web-data freshness, scorer subagent reasoning paths, and gate-scope interpretation. The intent of publishing the calibration set is to anchor the rubric, not to promise a numeric outcome.

| Ticker | Sector | Primary multiple | Phase E outcome |
|---|---|---|---|
| NVDA | Mega-cap tech | P/E | Cleared D20 |
| JPM | Money-center bank | P/B + ROE-implied | Cleared D20 |
| XOM | Integrated E&P | EV/EBITDAX + NAV | Cleared D20 |
| MRK | Large-cap pharma | P/E + NPV pipeline | Cleared D20 |
| DLR | Data center REIT | P/AFFO + NAV | Cleared D20 |

Rubric anchor and per-ticker score context: `design/phase-e-calibration-summary.md`.

## Composition with marketplace plugins

Per D21, this project produces Markdown + structured JSON regardless of what else is installed. Other artifacts are optional delegations:

| Optional output | Delegate plugin | Notes |
|---|---|---|
| Excel DCF model | `claude-for-financial-services/financial-analysis:dcf-model` | 5-scenario set collapses to 3-scenario DCF input (bear / base / bull). Mapping documented in `us-equity-research/references/tool-composition-us.md`. |
| Excel comps analysis | `claude-for-financial-services/financial-analysis:comps-analysis` | Comp-set definition flows from Phase 3 valuation specialist output. |
| Polished 30-50pg DOCX report | `claude-for-financial-services/equity-research:initiating-coverage` (Task 5) | Markdown IC memo + structured JSON are the input. |

When the marketplace plugins are not installed, the framework still completes — it just stops at the Markdown / JSON layer.

## Recreating `reference/anthropic-official/`

Per D23, the `reference/anthropic-official/` directory contains upstream marketplace plugin source code, gitignored to avoid committing third-party code into this repo. To recreate locally:

```bash
# 1. Install the upstream marketplace
/plugin marketplace add anthropics/claude-for-financial-services

# 2. Install the two upstream plugins this project composes with
/plugin install financial-analysis@claude-for-financial-services
/plugin install equity-research@claude-for-financial-services

# 3. Mirror into reference/
mkdir -p reference/anthropic-official
cp -R ~/.claude/plugins/marketplaces/claude-for-financial-services/plugins/vertical-plugins/equity-research \
      ~/.claude/plugins/marketplaces/claude-for-financial-services/plugins/vertical-plugins/financial-analysis \
      reference/anthropic-official/
```

This project was developed and tested against `claude-for-financial-services` marketplace at SHA `379e414` (May 2026 cut). Newer upstream releases should remain compatible — the integration surface is the SKILL.md description triggers, which are stable.

## Project structure

```
.
├── design/                                # decisions D1-D24, schema-conformance, calibration summary, build log
│   ├── build-log.md
│   ├── open-decisions.md
│   ├── phase-e-calibration-summary.md
│   └── ...
├── schemas/                               # 4 frozen schemas (memo, source_tags, scenarios, verification_gates)
├── us-equity-research/                    # plugin 1: multi-agent orchestrator
│   ├── .claude-plugin/plugin.json
│   ├── SKILL.md
│   └── references/                        # 14 reference docs (data sources, regulatory, valuation, phases, etc.)
├── us-equity-ic-rigor/                    # plugin 2: PM red-team layer
│   ├── .claude-plugin/plugin.json
│   ├── SKILL.md
│   ├── references/                        # 10 rigor refs (S1-S5, scenarios, GM taxonomy, bridges, A0, sizing, rubric, quant overlay, ...)
│   └── templates/                         # opinion letter checklist + IC debate script template
├── scripts/                               # 16 verification scripts (G1-G17 as of v0.2.0; G13+G14 share verify_quant_overlay.py) + pytest fixtures
│   └── tests/                             # 13 test files, 198 tests
├── outputs/                               # Phase E IC memos (NVDA / JPM / XOM / MRK / DLR) + structured JSON
├── reference/                             # gitignored upstream plugin source (D23)
├── templates/                             # gitignored China A-share precedent templates
├── README.md
├── CHANGELOG.md
└── BUILD_PROMPT.md
```

## Contributing

PRs welcome. Conventions:

- **Conventional commits** with phase prefix where applicable (`phase F.3: ...`)
- **One concept per commit** (D19)
- **pytest** must remain green: `pytest -q` should report `198 passed`
- **Schema invariants** (D17, D22) — the 4 schemas in `schemas/` are frozen; changes require explicit decision entry in `design/open-decisions.md`
- **One owner per file** (D2) — coordinate before touching shared docs

## License

MIT — see [LICENSE](LICENSE) if present, or use this notice:

```
MIT License

Copyright (c) 2026 Hongyi Gu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Disclaimer

This software produces investment research opinions for analytical workflows. It is provided for research and educational purposes only and does not constitute investment advice or a recommendation to buy or sell any security. Users assume full responsibility for any trading or investment decisions made on the basis of memos produced by this software; the methodologies encoded reflect institutional buy-side discipline but require independent verification of all specific numerical claims against primary sources before use in investment decisions.

## No Anthropic endorsement

This is an independent project. It composes with `claude-for-financial-services` marketplace plugins but is not endorsed by, sponsored by, or affiliated with Anthropic or their financial services partners. "Claude Code", "Anthropic", and "claude-for-financial-services" are trademarks of Anthropic; their use here is descriptive only.

## Citation

If you reference this framework in published work:

```bibtex
@software{gu_us_equity_research_2026,
  author = {Gu, Hongyi},
  title  = {us-equity-research: institutional buy-side fundamental research framework},
  year   = {2026},
  version = {0.1.0},
  url    = {https://github.com/<repo-path>}
}
```

## Acknowledgments

The architecture is derived from a China A-share buy-side research skill (precedent templates retained in `templates/`, gitignored). The 14-gate verification taxonomy, S1-S5 stratification convention, 5-scenario probabilistic framework, and 5-mandate position sizing rubric all originated in that precedent and were ported + adapted for the US regulatory and disclosure environment over the course of Phases A through E of this project (see `design/build-log.md`).
