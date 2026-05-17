# Earnings Prep Template (US)

NET-NEW for the US skill (per D10). Audience variant `earnings_prep` per memo.json. Night-before checklist for a single coverage-name earnings print.

This is operational, not audience-derived. The template forces the analyst to land specific scenarios with stock-reaction mappings BEFORE the print, so that the T+30min flash response (per `earnings-flash-template.md`) is a pre-rehearsed reflex, not a panic improvisation.

Composition note: this template covers the **pre-print** workflow. Post-print rapid response is `earnings-flash-template.md` (T+30min). Post-print full update report (8-12 page DOCX) is delegated to `equity-research:earnings-analysis` per `tool-composition-us.md`. The three-step composition is: earnings_prep → earnings_flash → delegated earnings update.

Output as Markdown (.md). File path: `outputs/<TICKER>_earnings_prep_<quarter>.md`.

---

## Required structure (rendered)

```markdown
# Earnings Prep — [TICKER] [Q[N] FY[NN]]

**Author**: [Author]
**Print date**: [YYYY-MM-DD] [pre-market | after-hours] | **Release time**: [HH:MM ET]
**Conference call**: [HH:MM ET, same day | next morning]
**Audience variant**: `earnings_prep`
**Prepared as of**: [YYYY-MM-DD HH:MM ET]

## Consensus snapshot

**Source ladder** (per D5 — EDGAR default; premium hooks optional):
- Primary: [Visible Alpha if accessible | FactSet | Bloomberg EE | Refinitiv IBES] (S4)
- Fallback: [Yahoo Finance Analysis tab | StockAnalysis.com forecasts | WSJ Markets] (S4)
- Freshness: estimates dated [YYYY-MM-DD]; [N] analysts; consensus freshness [days] from print date

| Metric | Consensus median | Range (low–high) | Sample size (n=) | Source S-tag |
|---|---|---|---|---|
| Revenue ($M) | | | | |
| EPS diluted (GAAP) $ | | | | |
| EPS diluted (non-GAAP) $ | | | | |
| Gross margin % | | | | |
| Operating margin % | | | | |
| [Segment 1 revenue $M] | | | | |
| [Segment 2 revenue $M] | | | | |
| [Key KPI 1, sector-specific] | | | | |
| [Key KPI 2, sector-specific] | | | | |

Citation example: `(S4: Visible Alpha NVDA FY[NN]Q[N] consensus, n=42, median $X, range $Y-$Z, refreshed 2026-05-14)` per D16.

## Whisper number (if any)

[Buy-side surveyed whisper — typically more bullish than published consensus in tech / growth names; more bearish in cyclicals approaching cycle peak. Source: AlphaSense / Estimize / sell-side trader notes / chat channel summaries.]

- Whisper revenue: $[X]M (vs published consensus $[Y]M; gap [Z]bps)
- Whisper EPS: $[X] (vs published $[Y])
- Citation: `(S5: [source description], surveyed [date])`

If no whisper available: state "No whisper number sourced; using published consensus as base".

## Implied move from options market

- Front-month straddle implied move: ±[X]% on print
- Historical realized move on prior 8 earnings: median ±[Y]%, range ±[low]% to ±[high]%
- Skew (25-delta put IV − call IV): [Z] (positive = downside premium, market priced for asymmetric downside)
- IV rank: [percentile] (high IV rank = market expects volatile print)

Citation: `(S5: CBOE / ORATS / SpotGamma, options snapshot as of [date])`

Compare to historical: is the implied move richer or cheaper than realized? Richer = market pricing event premium; cheaper = market complacent.

## KPI guide (sector-specific)

Choose the right KPI block for the sector and delete the rest:

**SaaS / software**:
- ARR ($M) and ARR growth YoY/QoQ
- Net retention rate % (NRR / DBNRR)
- Gross retention rate %
- RPO (remaining performance obligations) $M
- cRPO (current RPO) $M
- CAC payback months
- FCF margin %
- Rule of 40 (revenue growth % + FCF margin %)
- Customers >$100K ARR count

**Retail / consumer**:
- Same-store sales % (SSS)
- Comp transaction count YoY %
- Basket size % YoY
- Traffic YoY
- Inventory turns or weeks of inventory
- Gross margin bridge (mix / shrink / promotional intensity)

**Banks / financials**:
- Net interest margin (NIM) bps
- Loan growth YoY %
- Deposit growth + cost of deposits
- Net charge-offs (NCO) bps
- Allowance for loan losses (ALLL) / loans
- CET1 ratio
- ROTCE %
- Efficiency ratio %

**Healthcare**:
- Scripts (Rx) YoY
- Medical loss ratio (MLR) % for managed care
- Pipeline updates (Phase III readouts)
- Patient volumes / admissions for providers
- Reimbursement rate changes (CMS schedule)

**Semis / hardware**:
- Backlog $M
- Book-to-bill ratio
- Inventory days
- ASP YoY %
- Unit volume YoY %
- Capacity utilization %
- Customer mix (hyperscaler / enterprise / consumer)

**Industrials / cyclicals**:
- Orders YoY %
- Backlog $M
- Book-to-bill
- Price vs volume contribution
- Mix shift
- Capacity utilization

## Management commentary watch list

Specific items to listen for on the call (rank-ordered, time-stamped where prior call gave a marker):

1. **Guidance shift** — prior guidance was [revenue $X-$Y / EPS $A-$B / segment growth Z%] per [Q-1 8-K Item 2.02 / call transcript at MM:SS]. Watch for: maintained / raised / lowered / withdrawn. **Verify against the transcript, not just the press release** — per `verification-protocol-us.md` mgmt sometimes gives different guidance on call vs in 8-K.
2. **Capital allocation** — buyback pace, dividend, M&A hints, debt issuance/repayment plans.
3. **Competitive positioning** — share gain/loss commentary; specific competitor mentions.
4. **Hyperscaler / large-customer commentary** (if applicable) — customer concentration risk read.
5. **Tone on macro** — language shift on demand environment, pricing, mix.
6. **Sector-specific** — [e.g. for biotech: pipeline timeline confirms; for banks: credit normalization; for SaaS: net retention trajectory; for autos: pricing discipline]

## Beat / miss scenario tree

Pre-mapped per scenarios.json — 5-scenario internal framework maps to 3-case beat/miss for the prep (compresses to bear / base / bull per `tool-composition-us.md` 5→3 mapping).

| Scenario | Revenue vs cons | EPS vs cons | Implied stock reaction | Thesis impact |
|---|---|---|---|---|
| Strong bull (Beat-and-raise big) | Beat by >5% | Beat by >10% | +[implied move × 1.3 to 1.5] | [Which leg confirms; conviction tag → high_conviction] |
| Bull (Beat-and-raise modest) | Beat by 2-5% | Beat by 3-10% | +[implied move × 1.0 to 1.3] | [Confirms base case; modest probability shift to bull] |
| Base (In-line) | ±2% | ±3% | ±[implied move × 0.3 to 0.7] | [Thesis intact, no re-rating needed] |
| Bear (Beat-but-cut OR Miss-but-maintain) | ±3% mixed | ±5% mixed | −[implied move × 0.8 to 1.2] | [Modest probability shift to bear; watch Tier 3 triggers] |
| Strong bear (Miss-and-cut OR pre-announce-style) | Miss by >5% | Miss by >10% OR guidance cut | −[implied move × 1.3 to 1.8] | [Tier 2 trigger fires; invoke `kill_memo` template if pre-announcement-negative pattern per D10] |

## What-would-reverse triggers ready for this print

Specific numerical thresholds from `what-would-reverse-us.md` that THIS print could fire:

- **Bear-to-bull reverse trigger**: [specific number from §7 of IC memo, e.g. "Datacenter revenue >$40B"] — observable via this print's [segment table in earnings release / 10-Q Note 4 / call commentary]
- **Bull-to-bear reverse trigger**: [specific number, e.g. "GM <70% for two consecutive quarters"] — this would be the second consecutive quarter if it lands; watch for cumulative trigger fire
- **Tier 1 auto-exit candidate**: [if any restatement / 8-K Item 4.02 risk / going-concern flag — typically not at routine prints, but check]

## Position sizing impact gradient

Pre-rehearsed actions by mandate per D3, contingent on print outcome:

| Print outcome | Long-only large-cap | Long-only SMID | L/S hedge fund | Sector specialty | Pair-trade |
|---|---|---|---|---|---|
| Strong bull (Beat-and-raise big) | Add [X bps] vs S&P | Add [X bps] | Add to long, ±beta-rebalance hedge | Add to active overweight | Widen long / short ratio if pair |
| Bull (Beat-and-raise modest) | Hold or add [X bps] | Hold | Hold long; consider light add | Hold | Hold pair |
| Base (In-line) | Hold | Hold | Hold | Hold | Hold |
| Bear (Beat-but-cut / Miss-but-maintain) | Trim [X bps] | Trim [X bps] | Trim long; consider short overlay | Trim active overweight | Tighten pair or invert |
| Strong bear (Miss-and-cut) | Exit position | Exit | Cover long + initiate short if Tier 2 fires | Exit active overweight | Invert pair |

The action above is the **prep recommendation**, to be re-validated post-print with verified actuals (the flash response per `earnings-flash-template.md` runs through the same gradient with the actual numbers).

## Pre-call checklist (T−30 min before release)

- [ ] Verify consensus is fresh (≤14 days; per source_tags.json freshness flag)
- [ ] Refresh implied move from options market (last 30 min before close on pre-print day)
- [ ] Confirm earnings release time (8-K Item 2.02 sometimes drifts ±15 min)
- [ ] Have the transcript service queue ready (Motley Fool / SeekingAlpha / Capital IQ / AlphaSense) — guidance verified against transcript not press release per D10
- [ ] Have prior-quarter call key timestamps open for guidance cross-check
- [ ] Have IC memo open to §7 What-would-reverse and §10 Catalyst calendar
- [ ] Have `outputs/<TICKER>_scenarios.json` accessible for live updating
- [ ] Pre-write the headline of the flash response in three variants (Beat / In-line / Miss) — fill in the numbers post-print
```

---

## Time discipline

- **Earnings prep** runs the **night before** the print. Material assembled and scenarios pre-mapped.
- **Earnings flash** (per `earnings-flash-template.md`) runs **T+30 minutes** after the call ends, after guidance is verified against transcript.
- **Earnings update report** (8-12 page DOCX) is **T+24-48 hours** and is delegated to `equity-research:earnings-analysis` per `tool-composition-us.md`.

The earnings_prep template is NOT the earnings update report. It is the pre-print operational scaffolding that makes the flash response a reflex.

## Source ladder discipline

- Consensus snapshot is S4 — must include median + range + sample size per D16 example
- Whisper number is S5 — survey or chat channel; never a headline anchor
- Guidance pre-print is S3 prior (from last quarter's call / 8-K Item 7.01)
- Implied move from options is S5 — market-implied is not management-confirmed

## Pre-announcement detection (per D10)

If a pre-announcement is detected (negative or positive) between the prep template being completed and the scheduled print date, escalate immediately:
- Negative pre-announcement with beat/miss >−5% vs consensus → invoke `kill_memo` template (out of scope here; per delta matrix §8)
- Positive pre-announcement → run the earnings_flash template within 4 hours of release regardless of regular earnings date
- Anything else (in-line pre-announcement, guidance reaffirm) → continue with the regular print prep
