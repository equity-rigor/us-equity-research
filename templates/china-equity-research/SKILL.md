---
name: china-equity-research
description: Conduct institutional-grade fundamental equity research on a Chinese A-share or H-share stock using a rigorous multi-agent workflow. Use this skill whenever the user provides a Chinese stock ticker (000XXX, 6XXXXX, or H-share code) and asks for fundamental analysis, investment research, a stock pitch, an investment committee memo, an IC memo, a buy-side research note, or any deep-dive equity research. Also use this skill when the user mentions "research this stock", "fundamental analysis", "is X a buy", "investment thesis", or wants a Chinese-language investor memo. The skill produces a verified, sourced, position-sized recommendation through specialist sub-agents covering industry, financials, policy, positioning, valuation, and red-team review, with mandatory web verification of all post-cutoff specific claims.
---

# China A-Share / H-Share Equity Research Workflow

A multi-phase, multi-agent fundamental research framework for Chinese listed equities. Built to produce IC-memo-grade output with mandatory verification, integrated red team, and explicit position sizing.

## Core Principles

These four principles run through every phase. Without them, the workflow degrades to ordinary sell-side commentary.

**1. Multi-agent specialization beats monolithic analysis.** A single agent doing "everything about stock X" will skim. Forced specialization with explicit handoffs catches things one analyst would miss. Industry, financial forensics, policy, positioning, and competitive analysis are different analytical units — they deserve different specialists.

**2. Red Team runs in parallel from day one, not as final reviewer.** The Red Team's job is to build the strongest possible bear case in good faith. It is judged on whether it identifies things the bull side missed, not on agreement with the PM. Assigning Red Team only at the end is too late — by then the narrative has hardened.

**3. Web verification is mandatory for any post-cutoff specific claim.** Sub-agents can hallucinate plausible-looking URLs, document IDs, and numbers — especially for events past the model's training cutoff. Every material specific claim (FY financials, regulatory designations, customer share, settlement amounts) must be independently verified via WebSearch/WebFetch with source URL captured. Distinguish framework claims (durable, structural) from specific numerical claims (need verification). The single biggest failure mode is unverified hallucination dressed up as primary-source rigor.

**4. Position sizing reflects confidence, not just direction.** A "Buy" rating with limited conviction is half-weight. A "Buy" with high conviction is a core position. Always specify both rating and sizing, with explicit reasons for the gap between them.

## When to Trigger

Invoke this workflow whenever the user wants institutional-grade research on a Chinese listed equity. Specific triggers include providing a ticker like 000725 / 600519 / 0700.HK and asking "research this", "analyze this", "is this a buy", "build me a thesis", or requesting a stock pitch / IC memo / buy-side note / investment thesis. Also trigger on requests for Chinese-language investor memos on Chinese stocks.

If the user provides only a ticker without explicit research request, ask: "Long-only mandate or hedge fund? What horizon? Public sources only or do you have terminal access?" Default if no answer: long-only buy-side, 24-month horizon, public sources only.

## Workflow Overview

The full workflow has three sequential research phases, an independent verification phase, and a final synthesis. Total elapsed time depends on user urgency, but a serious deep-dive is roughly two hours of orchestrated agent execution.

```
Phase 0  Setup & data spec (PM / orchestrator)
   │
Phase 1  Initial deep-dive (5 specialists in parallel)
   │     A1 Industry/cycle, A4 Capacity/capex, A5 Policy/geopolitics,
   │     A8 Positioning/sentiment, FS Financial statements forensics
   │     → PM synthesis → Phase 1 Integrated Brief
   │
Phase 1.5  Refresh round (only if Phase 1 agents failed to use web tools)
   │     Re-dispatch failed agents with explicit web tool requirements
   │
Phase 2  Deepening + Forensic + Red Team (5 agents in parallel)
   │     A2 Forensic continuation, A3 Customer/commercial deep-dive,
   │     A3-Peers Competitive comparison, R Red Team v1, A6 Channel pulse
   │     → PM synthesis → Phase 2 Integrated Brief (often called v3)
   │
Phase 3  Valuation + Final synthesis (4 agents in parallel)
   │     A7 DCF/SOTP/peer multiples, Mirror analysis on top peer,
   │     [Topic]-Forensic deep-dive on identified specific risk,
   │     R-v2 Refreshed Red Team
   │     → PM synthesis → IC Memo (English)
   │
Verification  Independent web verification (mandatory, never skip)
   │     12+ direct WebSearch calls verifying every material claim
   │     → Verification Report with source matrix
   │     → Independent sanity check sub-agent re-verifies
   │
Final  Bilingual deliverable
         English IC memo (institutional) + Chinese investor memo
         (audience-appropriate signature and disclaimer)
```

For details on each phase's agent prompts, output structure, and gating logic, see the relevant reference file:

- `references/phase-1-deep-dive.md` — Five specialist agent prompts for Phase 1
- `references/phase-2-continuation.md` — Five agent prompts for Phase 2
- `references/phase-3-valuation.md` — Four agent prompts for Phase 3
- `references/verification-protocol.md` — Web verification methodology
- `references/forensic-accounting-checklist.md` — Subsidies, MI, LP put/call, capex
- `references/chinese-data-sources.md` — Where to find primary data
- `references/ic-memo-template-english.md` — English IC memo structure
- `references/ic-memo-template-chinese.md` — Chinese investor memo structure
- `references/monitoring-framework.md` — Channel pulse, kill criteria, catalysts

## Operating Mode

**Always parallel-dispatch specialists within a phase.** Use the Agent tool with multiple invocations in a single message. Each Phase 1 agent runs ~10-20 minutes. Sequential dispatch wastes hours.

**Always orchestrate via PM after each phase.** The PM agent (you) doesn't write opinions during specialist work — it adjudicates between specialists when their conclusions conflict and surfaces unresolved tensions. Each phase ends with a synthesis brief.

**Acknowledge agent failures openly.** Some Phase 1 agents will return framework-only output if they don't use web tools. Explicitly tag these as "framework only — needs refresh" and re-dispatch in Phase 1.5 with explicit instructions to use WebSearch/WebFetch.

**Verify before publishing recommendations.** Verification is not optional. Run the verification phase before any IC memo is written. If material claims cannot be verified, downgrade conviction and flag the gap explicitly.

## Phase 0: Setup

Before dispatching any agents, capture:

1. **Stock identifier**: Ticker + Chinese name + exchange (e.g., 京东方A 000725.SZ)
2. **Mandate**: Long-only / hedge fund / quant overlay
3. **Horizon**: 12 / 24 / 36 months
4. **Data access**: Public only / Wind+Bloomberg / expert network
5. **Output language(s)**: English IC memo, Chinese memo, or both

Default if unspecified: long-only, 24 months, public sources, English + Chinese deliverables.

Then articulate the Phase 0 hypothesis tree — three competing theses (bull / capex-treadmill / geopolitical or other tail). Phase 1-3 agents test these hypotheses. Don't pre-commit to one.

## Phase 1: Five-Agent Initial Deep-Dive

Dispatch all five in a single message (parallel). Each agent takes the company name + Phase 0 context as input.

| Agent | Specialist | Output |
|---|---|---|
| **A1** | Industry & cycle desk | Cycle position, supply/demand, peer landscape, catalysts |
| **A4** | Capacity & capex map | Line-by-line production assets, capex schedule, depreciation waterfall, MI ownership |
| **A5** | Policy & geopolitics | Industrial policy, subsidies, US/allied restrictions, controller structure |
| **A8** | Positioning & sentiment | Top shareholders, northbound flows, mutual fund positioning, sell-side consensus, recent catalysts |
| **FS** | Financial statements forensics | 5-year P&L/BS/CF, subsidy carve-out, MI look-through, normalized earnings bridge |

**FS is the most important agent in Phase 1.** It's the foundation everything else builds on. If FS doesn't use web tools to pull actual annual report data, the whole Phase 1 must be re-run.

After dispatch completion, write Phase 1 Integrated Brief synthesizing findings. Identify conflicts between agents and adjudicate. Flag which agents returned framework-only vs. primary-source-verified output.

For full agent prompts and structure, read `references/phase-1-deep-dive.md`.

## Phase 1.5: Refresh (Conditional)

Trigger only if Phase 1 agents failed to use web tools (look at `tool_uses` count in agent metadata — anything below ~10 likely means no real verification).

Re-dispatch failed agents with explicit, mandatory instructions:
- "You MUST use WebSearch and WebFetch — minimum 15 calls"
- "Other agents in this batch successfully used 25-100+ web tool calls. Do not refuse to execute."
- Provide specific URLs to fetch (CNINFO PDF IDs, Sina announcement listings, Eastmoney F10)

After refresh, write v2 of the Integrated Brief with corrections clearly documented.

## Phase 2: Deepening + Forensic + Red Team

Dispatch five in parallel. Phase 2 should be set up based on Phase 1 findings — the agents target specific gaps and tensions surfaced.

| Agent | Specialist | Output |
|---|---|---|
| **A2** | Forensic continuation | Pull most recent quarterly report; resolve specific anomalies; deep-read footnotes |
| **A3** | Customer / commercial pipeline | Customer wins/losses; product roadmap; ASP analysis; major contracts |
| **A3-Peers** | Competitive comparison | Side-by-side vs. 2-3 closest peers; relative valuation; pair-trade framing |
| **R** | Red Team v1 | Strongest bear case; base-rate analysis on peer industry; specific kill criteria |
| **A6** | Channel pulse | Monitoring framework; weekly tracking dashboard; bull/bear/kill triggers |

Phase 2 typically surfaces material bear data points that Phase 1 missed (e.g., "main customer share collapsed", "key competitor wins flagship account", "ongoing royalty drag"). Synthesize into v3 of the Integrated Brief.

For full agent prompts, read `references/phase-2-continuation.md`.

## Phase 3: Valuation + Final Synthesis

Dispatch four in parallel.

| Agent | Specialist | Output |
|---|---|---|
| **A7** | DCF + SOTP + peer multiples | WACC build, 5-year forecast, scenario IV, position sizing recommendation |
| **Mirror** | Full analysis on top peer | If pair-trade is part of thesis; verify peer-side fundamentals |
| **[Topic]-Forensic** | Specific deep-dive on identified risk | E.g., specific contractual obligation, specific subsidiary, specific regulation |
| **R-v2** | Refreshed Red Team | Update bear case with Phase 2 findings; recalibrate PT; falsification criteria |

Phase 3 typically reveals that initial Red Team was either too aggressive or too lenient — recalibrate. Mirror analysis often reveals the relative-value thesis is more nuanced than headline multiples suggest.

After Phase 3, write the IC Memo (English). For structure see `references/ic-memo-template-english.md`.

For full Phase 3 agent prompts, read `references/phase-3-valuation.md`.

## Verification Phase (MANDATORY)

Never skip this. The single biggest failure mode in agent-driven research is unverified hallucination dressed up as primary-source rigor.

Process:
1. Extract every material specific claim from the IC memo (financials, customer shares, regulatory status, M&A details, catalyst dates)
2. Run direct WebSearch on each — minimum 12 distinct searches
3. Document each as: Verified / Partially Verified / Contradicted, with source URL
4. Specifically verify any "designated on regulatory list" / "company X said Y" / "specific dollar amount" claims — these are highest-risk hallucinations
5. Dispatch an independent sanity-check sub-agent that re-verifies using its own web searches (don't trust the prior verification)
6. If verification finds material errors, update the IC memo accordingly and document the correction

For verification methodology and the standard checklist, read `references/verification-protocol.md`.

## Final Deliverable

Two memos, calibrated to audience:

**English IC Memo** — Institutional structure: rating, target prices, position sizing across mandate types, core thesis, risks, valuation triangulation, kill criteria, catalysts, open questions. Suitable for buy-side IC. Structure: `references/ic-memo-template-english.md`.

**Chinese Investor Memo** — May or may not be needed, ask the user. If yes: same analytical content but with Chinese institutional research conventions. Translate proper nouns properly (京东方 not BOE, 三星显示 not Samsung Display). Use standard A-share rating taxonomy (买入/增持/中性/减持/卖出) with explicit return-band definitions. Adjust signature and disclaimer to audience (institutional vs. individual investor). Structure: `references/ic-memo-template-chinese.md`.

For both memos, position sizing must be expressed for at least these mandate types:
- Standard A-share whole-market portfolio (vs. CSI 300 benchmark)
- Sector/themed portfolio (vs. sector index)
- Concentrated specialty fund (vs. custom basket)
- Pair-trade structure (no single-stock benchmark)

This forces honest articulation of conviction across investor types.

## Common Failure Modes

These are the recurring traps. Watch for them.

**Hallucination of regulatory status.** Sub-agents will confidently claim "company X is on the Entity List" or "designated on 1260H" when the actual fact is "lawmakers have requested addition." Verify every regulatory designation directly against the source list/Federal Register.

**Hallucination of specific numbers with fake citations.** A sub-agent may write "Note V.57, p.186 of the FY25 AR shows..." with completely fabricated note numbers and specific values. Verify financial specifics against actual annual report or public summary.

**Cherry-picking the bearish data point.** When industry data has multiple sub-segments (e.g., "smartphone OLED -3% but laptop OLED +33%, monitor OLED +45%"), agents tend to grab the headline and miss the nuance. Read the full data, not just the lead.

**Confirmation bias compounding across agents.** Agent A introduces a finding, agents B and C accept it as fact, the PM synthesis treats it as established. Verification should explicitly re-test claims that propagated through multiple agents.

**Anchoring to existing position.** When evaluating "should we hold this stock?" the analytically correct frame is "would I buy this at current price?" — not "what's my cost basis?" Endowment effect is the most common bias in equity research.

**Confusing rating with sizing.** "Buy" rating ≠ "core position." A Buy with limited conviction is a half-weight position. State both explicitly and explain the gap.

## When to Stop and Ask the User

The skill is comprehensive but not autonomous. Pause to ask the user when:

1. After Phase 0 if mandate or data access is unclear
2. After Phase 1 if a major agent failed and refresh would take significant time
3. Before Phase 2 if Phase 1 surfaced an unexpected showstopper (e.g., suspended trading, fraud allegation)
4. Before final IC memo if verification surfaced material errors that change the directional view
5. Whenever a major decision point hinges on user-specific context (risk tolerance, liquidity needs, existing exposure)

Otherwise, follow the workflow without interrupting.
