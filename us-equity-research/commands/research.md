---
description: Run Phase 0 buy-side fundamental research on a US-listed ticker (NYSE/Nasdaq/AMEX/OTC) — produces structured JSON + Markdown memo, mandatory web verification, S1-S5 source stratification
argument-hint: "[ticker] [optional: scope notes]"
allowed-tools:
  - Read
  - Write(outputs/**)
  - Edit(outputs/**)
  - WebSearch
  - WebFetch
  - Bash(curl *)
  - Bash(wget *)
  - Bash(python3 *)
  - Bash(python *)
  - Bash(cat *)
  - Bash(ls *)
  - Bash(grep *)
  - Bash(find *)
  - Bash(head *)
  - Bash(tail *)
  - Bash(mkdir *)
  - Bash(echo *)
  - Task
---

Load the `us-equity-research` skill and begin Phase 0 fundamental research on the ticker provided.

If a ticker is provided as the first argument, use it. Otherwise ask the user which US-listed name to research (NYSE/Nasdaq/AMEX/OTC tickers, plus ADRs via 20-F/6-K).

Default mode: EDGAR-only + free-aggregator data (Yahoo Finance, StockAnalysis.com, WSJ Markets). Premium data hooks (Visible Alpha, Capital IQ, AlphaSense, Bloomberg) gate behind explicit user opt-in.

Required Phase 0 minimum per D9: at least 12 WebSearch+WebFetch calls across industry context, SEC filings (10-K/10-Q/8-K/DEF 14A/20-F as relevant), regulatory desk (FTC/DOJ/state AGs/EU CMA/BIS/OFAC/CFIUS/sector regulators per D12), positioning desk (13F clusters, Form 4 net, short interest, options skew, ETF passive %, sell-side distribution, activist 13D), forensic accounting (ASC 606/842/718, non-GAAP/GAAP delta, SBC treatment, goodwill, auditor history, restatement history), and a sector-appropriate baseline valuation per D8.

Output Phase 0 to `outputs/{TICKER}_structured.json` + `outputs/{TICKER}_Research_Document_{date}.md`. Do NOT shape into IC memo or scenario framework — that is the `us-equity-ic-rigor` skill's job.

If the user's request implies an IC memo (memo / opinion letter / PM red-team / score-band language), chain into `us-equity-ic-rigor` immediately after Phase 0 completes. Otherwise stop at Phase 0.
