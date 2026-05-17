# Multi-audience delivery — institutional / IC pre-read / IC debate / LP letter / earnings prep / earnings flash / kill memo (US)

## What this solves

A single memo cannot serve every audience. The institutional 12-section IC memo is too dense for IC pre-read. The pre-read is too compact for verbal debate. The LP letter is too prosaic for an internal IC committee. None of them serve the operational night-before-earnings or T+30 minute use case.

The discipline: build the **institutional version first as the single source of truth**; derive the others. **Numbers must match across all variants** per `pm-redteam-rubric-us.md` B8 (cross-version stale numbers). Only language compresses.

Per **D4**, retail and bilingual variants are **dropped**. The US buy-side does not deliver retail-flavored research routinely, and FINRA Rule 2210 / SEC Reg BI retail-comms rules add compliance burden out of scope for an internal tool. The LP letter replaces retail as the non-IC audience variant. Earnings prep, earnings flash, and kill memo are operational variants triggered by events, not audience derivatives.

Output format per **D15**: **Markdown only.** All variants are `.md` files in `outputs/`. No docx generation.

## The seven variants

The `audience_variant` enum in `schemas/memo.json` is: `institutional_full`, `ic_preread`, `ic_debate_script`, `lp_letter`, `earnings_prep`, `earnings_flash`, `kill_memo`.

### Variant 1 — institutional_full (12-section IC memo, source of truth)

- **Audience**: PM, sector specialist, IC committee for deep prep, equity-research:initiating-coverage Task 5 delegation input.
- **Length**: 25-40 pages rendered.
- **Naming**: `outputs/<ticker>_IC_memo_<author>.md`.
- **Structure**: per `opinion-letter-section-checklist-us.md` and `ic-memo-template-us.md`. 12 sections:

```
§1   Headline + recommendation (rating per D1, conviction tag, time horizon)
§2   Source stratification box (top-5 anchors, S-levels, citations, promotion paths)
§3   Company / industry context
§4   Anchor evidence build-up
§5   Five-scenario valuation table (per five-scenario-framework-us.md)
§6   Three-method reconcile + bear bridge + GM taxonomy box
§7   What-would-reverse triggers (numerical denominators)
§8   A0 tail mapping (5-12 events, bear + bull, prob shifts sum to zero)
§9   Position sizing (across 5 mandate types per D3)
§10  Catalyst calendar (3-8 events with dates)
§11  Quant overlay (Barra factors, capacity, edge decay, stress, correlation placeholder)
§12  Caveats + appendix (full source matrix, scenario assumptions, sensitivities)
```

- **Verification**: all 14 gates G1-G14 must pass per `pm-redteam-rubric-us.md`. Score ≥8.5 per **D20**.
- **Structured-data twin**: `outputs/<ticker>_structured.json` conforming to `schemas/memo.json` is co-produced.

### Variant 2 — ic_preread (≤4 page condensed)

- **Audience**: PM committee members reviewing 10+ memos before an IC meeting; CIO scanning the docket.
- **Length**: 3-4 pages rendered (~1,500-2,500 words).
- **Naming**: `outputs/<ticker>_IC_preread_<author>.md`.
- **Required content** (kept from institutional):
  - Headline + recommendation paragraph (§1)
  - Source stratification box (§2 — this is what they'll challenge)
  - Five-scenario table (§5, all columns)
  - Three-method reconcile (§6, compact form)
  - Bear bridge (§6, layered, abbreviated)
  - What-would-reverse triggers (§7, ≤6 entries)
  - A0 tails (§8, ≤6 entries: 4 bear + 2 bull)
  - Position sizing (§9, with action by mandate)
  - Quant overlay key tags + capacity disclosure (§11 compact)
- **Removed vs institutional**:
  - Industry context narrative (§3)
  - Anchor evidence build-up detail (§4)
  - Full catalyst calendar with sub-events (§10 — keep top 3 only)
  - Appendix (§12)
- **Discipline**: **no number changes from institutional.** If you find a number wrong while building the pre-read, fix the institutional memo first, then re-derive.

### Variant 3 — ic_debate_script (verbal form + Q&A bank)

- **Audience**: presenter (you) standing in front of IC committee for verbal defense.
- **Length**: 4-6 pages rendered (~2,000-3,000 words including Q&A bank).
- **Naming**: `outputs/<ticker>_IC_debate_<author>.md`.
- **Structure** per `ic-debate-script-template-us.md`:
  - **Company fundamentals** (2 min) — what does it do, why does this matter, what's the setup
  - **Research methodology** (1 min) — anchors used, S-levels, scenario framework
  - **Logic chain** (3 min) — anchor → scenario → headline, walked through verbally
  - **Anchor evidence** (4 min) — specific numbers, source citations, conviction
  - **Valuation** (2 min) — three-method reconcile result + headline number + mandate sizing
  - **Caveats / what would reverse** (1 min) — numerical denominators
  - **Recommendation + position sizing** (1 min) — specific bps / NAV %
- **Timing markers** at section starts (3 / 5 / 10 / 14 minute variants for presenter flexibility).
- **Q&A bank**: 8-12 likely PM challenges with prepared answers, sorted by likelihood. Each Q&A maps to a section of the institutional memo for fast lookup.

### Variant 4 — lp_letter (1-2 page client-facing)

- **Audience**: institutional LPs (qualified purchasers, accredited investors, institutional investment advisors). **Not retail.**
- **Length**: 1-2 pages rendered (~800-1,500 words).
- **Naming**: `outputs/<ticker>_LP_letter_<author>.md`.
- **Structure** per `lp-letter-template.md`:
  - Cover paragraph: what we own / shorted / spread, why, current view.
  - Change-in-view narrative: what's new since last quarter; what's reaffirmed; what's flipped.
  - Attribution: contribution to fund return in the quarter (where applicable).
  - Forward catalysts: 3-5 dated events from §10 of institutional, plain-English framing.
  - Risk framing: 2-3 top A0 tails translated to LP-readable language (no Kelly, no σ).
  - Plain-English equivalent of headline ("we expect X to outperform Y over 12-18 months because Z; our largest risk is...").
- **What's removed vs institutional**: full source citations (use "per company filings," "per industry data"), Kelly/σ/Sharpe jargon, full scenario table (substitute "we see upside of X% and downside of Y%"), GM taxonomy, factor tags, capacity math.
- **US compliance notes**:
  - LP letters go to qualified purchasers / accredited investors / institutional advisors — **out of scope for FINRA Rule 2210** retail-communications gates.
  - Recommended disclaimer: "This letter is intended solely for institutional investors and qualified clients of [Fund]. It is not investment advice for any retail investor and is not a solicitation."
  - Performance attribution must conform to GIPS standards if the fund claims GIPS compliance.
  - SEC marketing rule (Rule 206(4)-1) applies if the letter is used in fundraising — review by compliance before circulation.

### Variant 5 — earnings_prep (night-before checklist)

- **Audience**: portfolio manager prepping the morning before earnings; sector analyst writing flash.
- **Length**: 2-3 pages rendered (~1,000-2,000 words).
- **Naming**: `outputs/<ticker>_earnings_prep.md`.
- **Trigger**: T-1 day before scheduled earnings (per `monitoring-framework-us.md` catalyst calendar).
- **Structure** per `earnings-prep-template.md`:
  - Consensus snapshot: revenue, EPS, segment splits with median + dispersion (per `source-stratification-us.md` S4 discipline).
  - KPI watch list: 6-10 metrics PM should watch for (DC revenue, hyperscaler commentary, GM, guidance for next quarter, buyback authorization, etc.).
  - Beat/miss scenario tree: what does +X% beat vs −X% miss imply for next-12mo headline?
  - Management commentary watch list: phrases that would graduate S3 anchors to S2 (per `source-stratification-us.md` Rule 3).
  - Implied move from options market (`positioning_sentiment.options_implied_move_earnings_pct` per `schemas/memo.json`).
  - Position action plan: if X happens trim N%; if Y happens add M%; if Z happens flip to short — concrete decision tree.
- **Not a derivative of institutional**: this is an operational variant triggered by the earnings date.

### Variant 6 — earnings_flash (T+30 min same-day)

- **Audience**: PM during trading hours after earnings print.
- **Length**: 1 page rendered (~500-800 words).
- **Naming**: `outputs/<ticker>_earnings_flash.md`.
- **Trigger**: T+30 minutes after earnings press release; T+90 minutes after call (whichever provides actionable input first).
- **Structure** per `earnings-flash-template.md`:
  - Headline number: beat/miss vs consensus on revenue + EPS + guidance.
  - Segment beat/miss: each material segment vs consensus dispersion.
  - Top 3 anchor verifications: which prior-quarter S3 anchors graduated to S2 with this print? Which fell?
  - Sizing action: re-compute Kelly with updated probabilities; new mandate-specific sizing.
  - Re-rating decision: stays at prior rating, upgrades, downgrades.
  - Catalyst calendar update: next event from §10.
- **Not a derivative of institutional**: this is an operational variant.
- **D10 handling**: if pre-announcement is negative and exceeds −5% beat/miss vs consensus, **kill_memo** is invoked instead of flash. If positive pre-announcement, flash runs.

### Variant 7 — kill_memo (falsification-triggered exit rationale)

- **Audience**: PM committee, post-mortem reviewer.
- **Length**: 2-3 pages rendered (~1,000-1,500 words).
- **Naming**: `outputs/<ticker>_kill_memo.md`.
- **Trigger**: any **Tier 1** trigger firing per `monitoring-framework-us.md` (a what-would-reverse threshold being crossed in the wrong direction, or an A0 event crystallizing).
- **Structure**:
  - Dated trigger event: which what-would-reverse trigger or A0 event fired? When? Cite source (EDGAR filing, FRED data point, Federal Register notice).
  - Original thesis recap: 2-paragraph summary of the institutional memo headline + top-3 anchors at thesis inception.
  - What broke: which anchor falsified? Which probability shift materialized?
  - Headline recompute: what's the new headline at post-falsification probabilities? (Often headline flips sign.)
  - Exit recommendation: full exit, trim to flat, flip to short — with sizing per `position-sizing-us.md`.
  - Post-mortem (≥1 paragraph): what should have been weighted differently? Which S-level was over-trusted? Which A0 event was under-weighted? Lessons learned.
- **Discipline**: kill memo must reference the **dated trigger event** by source channel. No abstract "thesis broke" — name the EDGAR filing, the FRED data point, the court ruling, the agency action.

## Number-consistency discipline

The institutional memo is the **single source of truth**. Derivative variants import constants.

Build script practice: top-of-file constants block. For each derivative variant's build script:

```python
# drawn from institutional v3.0 (locked at 8.8 / 9.0+ per pm-redteam-rubric-us.md)
HEADLINE_RETURN_MID = 0.094         # E[R] = +9.4%
HEADLINE_RANGE = [-0.05, 0.35]      # scenario-weighted P10/P90
RATING = "Buy"                       # per D1 5-band
CONVICTION_TAG = "source_conditional"
CURRENT_PRICE_USD = 142.50           # from FRED / live price feed at write time
PRICE_TARGET_USD = 165.00            # 12-month
SHARPE = 0.21                        # vs FRED DGS10 R_f 4.3%
KELLY_ADJ_PCT_NAV = 0.0033           # 0.33% NAV after conviction × factor crowding
# ... continued for full constants block
```

Every derivative variant's build script imports these constants. Any change to the institutional memo propagates automatically when derivatives are rebuilt.

**Anti-pattern**: hand-typing numbers into each derivative — guaranteed drift, fails B8 verification.

## Build order discipline

The right order is:

1. **Institutional FIRST** (Phases 1-4 of `us-equity-research/SKILL.md`).
2. **Lock institutional**: all 14 verification gates pass; PM red-team rubric score ≥8.5.
3. **Then IC pre-read** (compress; verify numbers identical to institutional).
4. **Then IC debate script** (verbalize; build Q&A bank from PM challenge log).
5. **Then LP letter** (translate to LP-readable; remove jargon; keep numbers).

Earnings prep, earnings flash, and kill memo are **operational variants triggered by events**, not derivatives of a current institutional view. They reference the institutional memo's anchors and catalyst calendar but are produced on different cadences:

- earnings_prep: T-1 day before scheduled earnings.
- earnings_flash: T+30 min after print.
- kill_memo: when a Tier 1 monitoring trigger fires.

Doing institutional and derivatives in parallel before institutional is locked guarantees you'll have to redo derivatives when institutional moves. Same lesson as China; the US version doubles down on it via the constants-block discipline.

## Output discipline per D15

After every build:

1. Verify file produced (check file exists and is non-empty).
2. Provide absolute path to the user.
3. Summarize 1-3 lines what's new vs prior version (if iterating).
4. Confirm structured JSON twin (`<ticker>_structured.json`) is co-produced and conforms to `schemas/memo.json`.

## Naming conventions summary

| Variant            | Filename                                          |
|--------------------|---------------------------------------------------|
| institutional_full | `outputs/<ticker>_IC_memo_<author>.md`            |
| ic_preread         | `outputs/<ticker>_IC_preread_<author>.md`         |
| ic_debate_script   | `outputs/<ticker>_IC_debate_<author>.md`          |
| lp_letter          | `outputs/<ticker>_LP_letter_<author>.md`          |
| earnings_prep      | `outputs/<ticker>_earnings_prep.md`               |
| earnings_flash     | `outputs/<ticker>_earnings_flash.md`              |
| kill_memo          | `outputs/<ticker>_kill_memo.md`                   |
| structured twin    | `outputs/<ticker>_structured.json`                |

## US compliance notes

- **Institutional and IC pre-read / debate script**: internal use only; not external communications.
- **LP letter**: external to institutional LPs only. Qualified purchasers / accredited / institutional advisors. Recommend explicit disclaimer at letter foot. Out of scope for FINRA Rule 2210 retail-comms framework. SEC marketing rule (Rule 206(4)-1) applies if used in fundraising.
- **Earnings flash**: internal use; if any portion reaches LP audience, it must be re-framed in LP-letter style.
- **Kill memo**: internal post-mortem; references in subsequent LP letters should be brief and high-level.
- **No retail variant**: per D4, dropped entirely. If a user explicitly requests retail-flavored output, refuse with reference to FINRA Rule 2210 + SEC Reg BI compliance considerations.

## Worked example — NVDA full deliverable set (illustrative for Phase E)

```
| Variant            | File                                       | Pages | Purpose                                            |
|--------------------|--------------------------------------------|-------|----------------------------------------------------|
| institutional_full | outputs/NVDA_IC_memo_<author>.md           | 25-40 | 12-section IC, source of truth, gates G1-G14 pass  |
| ic_preread         | outputs/NVDA_IC_preread_<author>.md        | 4     | IC committee pre-meeting                           |
| ic_debate_script   | outputs/NVDA_IC_debate_<author>.md         | 6     | Verbal IC + Q&A bank                               |
| lp_letter          | outputs/NVDA_LP_letter_<author>.md         | 2     | LP client-facing quarterly                         |
| earnings_prep      | outputs/NVDA_earnings_prep.md              | 3     | Night-before FY26Q1 (run on T-1)                   |
| earnings_flash     | outputs/NVDA_earnings_flash.md             | 1     | T+30 min after FY26Q1 print                        |
| kill_memo          | outputs/NVDA_kill_memo.md                  | 3     | Triggered if Tier 1 monitor fires                  |
| structured twin    | outputs/NVDA_structured.json               | n/a   | Conforms to schemas/memo.json                      |
```

All variants share the constants block:
- HEADLINE_RETURN_MID
- HEADLINE_RANGE
- RATING (Buy / Hold / etc. per D1)
- CONVICTION_TAG
- CURRENT_PRICE_USD
- PRICE_TARGET_USD
- SHARPE
- KELLY_ADJ_PCT_NAV
- TOP_3_ANCHORS (Source Stratification Box entries)
- TOP_3_A0_TAILS (largest |Δ headline| tails)

## Anti-patterns

| Anti-pattern                                                              | Why wrong                                                                                 |
|---------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Different headline numbers in IC pre-read vs institutional                | Erodes trust; PM will check; violates B8 cross-version stale                              |
| IC debate script reading off institutional verbatim                       | Sounds robotic; misses verbal compression and Q&A bank value                              |
| LP letter using "EPS / Sharpe / Kelly" jargon without translation         | Loses LP audience; fails LP-letter purpose                                                |
| Kill memo without dated trigger event reference                           | Cannot audit post-mortem; fails monitoring framework integration                          |
| Earnings flash that just summarizes the print                             | Misses the purpose — flash exists to update sizing and rating, not narrate                |
| Adding NEW analysis in IC pre-read not in institutional                   | Violates "single source of truth"; pre-read must compress, never extend                   |
| Retail or bilingual variant generated despite D4                          | Out of compliance scope; rejected by `multi-audience-delivery-us.md` defaults             |
| Earnings prep without consensus dispersion                                | Missing the S4 discipline from `source-stratification-us.md`                              |
| Earnings flash without options-implied move comparison                    | Missing the positioning-sentiment integration; can't gauge whether reaction is in line   |
| LP letter with full citation footnotes                                    | Overwhelms LP reader; use "per company filings" / "per industry data" plain-English form  |
| Hand-typed numbers in derivative variants                                 | Guaranteed drift from institutional; fails number-consistency discipline                  |
| Building IC debate before institutional is locked at ≥8.5                 | Will need to redo; institutional re-derive cycles invalidate the debate Q&A bank          |

## Cross-references

- **Memo umbrella schema**: `schemas/memo.json` — `audience_variant` enum and per-section fields.
- **Source discipline**: `source-stratification-us.md` — S1-S5, citations format, headline conditionality.
- **Five-scenario**: `five-scenario-framework-us.md` — drives §5 across all variants.
- **Three-method valuation**: `valuation-discipline-us.md` — §6 reconcile.
- **GM taxonomy**: `gm-taxonomy-us.md` — §6 sub-block.
- **What-would-reverse**: `what-would-reverse-us.md` — §7 numerical denominators.
- **A0 tail mapping**: `tail-risk-mapping-us.md` — §8 bear + bull tails.
- **Position sizing**: `position-sizing-us.md` — §9 across 5 mandate types.
- **PM red-team**: `pm-redteam-rubric-us.md` — score bands, bug catalog, "what does 9.0+ feel like."
- **Monitoring**: `monitoring-framework-us.md` — Tier 1/2/3 triggers; kill memo invocation rule.
- **Institutional template**: `opinion-letter-section-checklist-us.md`, `ic-memo-template-us.md`.
- **Variant templates**: `ic-debate-script-template-us.md`, `lp-letter-template.md`, `earnings-prep-template.md`, `earnings-flash-template.md`.
- **Open decisions**: D4 (retail dropped, LP letter added, earnings variants added), D10 (kill memo invocation rule), D15 (Markdown-only output).
