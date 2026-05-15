# Source stratification (S1–S5 + Pending) — US

## Why this matters

The single fastest way to fail a PM challenge in a US buy-side IC is to put a specific number in a headline anchor without being able to point at where it came from. "Hyperscalers are growing capex 30%" / "channel checks suggest Blackwell ramp is ahead of plan" gets you killed unless those numbers carry a source-grade tag and the headline language matches the strongest anchor's grade.

Source stratification forces every specific number (revenue, GM, segment share, customer concentration, ADV, beta, ASP, capex, market share) onto a 6-level reliability scale and forces the headline language to match. If your top-3 anchors are all S3 transcript color, your headline is **not** "Buy, +25% expected return" — it is "**source-conditional Buy** (moderate-positive bias), +25% conditional on [anchor1, anchor2] graduating to S2 in [filing], downgrade to Hold if either falsifies."

This is the discipline that prevents the most common PM red-team kills. It is also the operational reading of D16 (citation regex), D5 (EDGAR-only default), D9 (12 WebSearch verifications), and verification gates G6 (`verify_source_tags.py`) and G7 (`verify_headline_conditionality.py`).

The schema for these tags is in `schemas/source_tags.json`. This document is the prose discipline that humans and the orchestrator skill apply at runtime; the schema is the machine contract.

---

## The 6 levels

### S1 — Audited annual financial statements

- **Definition**: 10-K (US domestic issuer) or 20-F (foreign private issuer / FPI) with unqualified PCAOB-registered auditor opinion under SOX §404(b) (ICFR audit) and §302 (CEO/CFO certification). ASC-compliant.
- **US source_type enum members**: `10-K`, `20-F`.
- **Red-team resistance**: Strongest. Can drive **unconditional** headline anchors.
- **Examples**:
  - "NVDA FY24 datacenter revenue $X B (S1: NVDA 2024 10-K Item 8, Note 13 Segment Information)."
  - "NVDA FY24 GAAP gross margin Y% (S1: NVDA 2024 10-K Item 7 MD&A)."
  - "JPM FY24 net interest income $X B (S1: JPM 2024 10-K Item 7, NII reconciliation)."
- **Verification anchor**: Confirm via EDGAR XBRL company facts API (`data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`) for clean extraction; the XBRL tag (`us-gaap:Revenues`, `us-gaap:GrossProfit`, etc.) is the unambiguous machine-readable reference.
- **Caveats** even at S1:
  - **Non-GAAP vs GAAP**: 10-K reports GAAP. Many companies emphasize non-GAAP. The non-GAAP figure is an S2-S3 management construct *built on top of* the audited GAAP base; the GAAP figure is S1.
  - **ASC 606 timing**: Revenue recognition timing (POB allocation, contract modifications, license front-loading) is an interpretation layer over S1 numbers.
  - **ASC 842 lease cap**: Operating lease right-of-use assets and liabilities on BS were off-BS pre-2019; multi-year comparability requires adjustment.
  - **Segment reporting choices**: How a company defines reportable segments under ASC 280 is management discretion; an S1 segment number can change definition next year.
  - **Restatements**: 8-K Item 4.02 "non-reliance on prior financials" downgrades any S1 number from a restated period. Always check for Item 4.02 lookups.

### S2 — Unaudited public filings

- **Definition**: SEC-filed public documents that are not the annual audited 10-K/20-F. The filings are still subject to SEC review and §302 certification, but no full auditor opinion. Includes auditor-reviewed (not audited) interim financials in 10-Q.
- **US source_type enum members**: `10-Q`, `8-K`, `DEF 14A`, `S-1`, `S-3`, `S-4`, `6-K`, `13D`, `13G`, `13F`, `Form 3`, `Form 4`, `Form 5`, `N-PORT`.
- **Red-team resistance**: Strong. Can drive headline anchors but **cite specific filing + Item/Section** (not just "the 10-Q").
- **Examples**:
  - "NVDA FY25Q3 datacenter revenue +X% YoY (S2: NVDA FY25Q3 10-Q Note 4 Segment Information)."
  - "NVDA announced $50B buyback authorization (S2: NVDA 8-K 2025-08-28 Item 8.01)."
  - "JPM CET1 ratio 15.3% as of Q4 (S2: JPM FY24Q4 8-K Item 2.02 earnings release exhibit + JPM FY24Q4 10-Q)."
  - "CFO departure announced (S2: 8-K Item 5.02 2025-09-15)."
- **8-K is heterogeneous** — Item-by-Item reliability varies materially:
  - **Item 2.02** (results of operations / earnings press release exhibit): high reliability, but note the press release is S2; the call transcript that accompanies it is S3 (see below).
  - **Item 4.02** (non-reliance / restatement): high-info; downgrades prior periods.
  - **Item 5.02** (D&O changes): high reliability for the fact of the change.
  - **Item 7.01** (Reg FD disclosure): high reliability for what was disclosed; the underlying number may still be S3 if it is guidance.
  - **Item 8.01** ("other events"): low-signal; can be press release attached without specific disclosure obligation. Tag carefully.
- **Caveats**: 10-Q is auditor-*reviewed* not audited; review is materially weaker assurance than SOX §404 audit. Restatement risk is real (see B11 in `pm-redteam-rubric-us.md`).

### S3 — Management commentary

- **Definition**: Statements made by company management, on-record but not in an audited or even auditor-reviewed filing. Includes earnings calls (the authoritative source for guidance, NOT the press release per the verification protocol §11 in the delta matrix), investor day presentations, non-deal roadshow notes, company press releases not attached to an 8-K, and any management guidance issued under Reg FD (17 CFR 243 — same-day broad distribution required).
- **US source_type enum members**: `Earnings call transcript`, `Earnings press release`, `Investor day deck`, `Mgmt guidance`, `Non-deal roadshow notes`.
- **Red-team resistance**: Medium. **Should NOT drive unconditional headlines on its own**. Use framing: "per management," "company has guided to," "management indicated on the call."
- **Examples**:
  - "Blackwell ASP uplift of ~30-40% vs Hopper (S3: NVDA FY25Q1 earnings call transcript 2025-05-22 ~22min mark, CFO response to MS analyst question)."
  - "NVDA FY26 datacenter revenue guidance midpoint $X B (S3: NVDA FY25Q4 earnings call 2026-02-26, formal guidance section)."
  - "JPM expects NII of $90B for FY25 (S3: JPM FY24Q4 earnings call 2025-01-14, CFO Q&A response, restated in Investor Day deck 2025-02-25)."
- **Caveats**:
  - **Guidance discrepancy between press release and call**: companies sometimes give different (often wider) ranges on the call than in the 8-K Item 2.02 press release. The call is the authoritative S3 source per delta matrix §11. Verify guidance against the transcript, NOT the press release. Pre-announcements (positive or negative) are S3-ish — see D10 handling.
  - **Reg FD distribution**: management commentary made on a non-broadly-distributed call is potentially a Reg FD violation; the commentary itself is still S3 but flag the distribution issue.
  - **IR-side embellishment risk**: management framing tends to be optimistic at cycle tops, pessimistic at cycle bottoms. Treat S3 color directionally, never as point estimates.

### S4 — Sell-side consensus and broker estimates

- **Definition**: Analyst-aggregated estimates from premium consensus providers and individual sell-side notes. Includes free aggregators where the underlying data is often Refinitiv-derived.
- **US source_type enum members**: `Visible Alpha consensus` (premium, segment-granular), `FactSet consensus`, `Bloomberg EE`, `Refinitiv IBES`, `Capital IQ Pro`, `Yahoo Finance consensus`, `StockAnalysis.com`, `WSJ Markets`, `AlphaSense`, `Motley Fool transcript`, `SeekingAlpha`. Per D5, EDGAR-only mode falls back to Yahoo Finance / StockAnalysis as the free S4 source.
- **Red-team resistance**: Medium-low. Use as **range with dispersion**, never as a point estimate.
- **Examples**:
  - "NVDA FY26 datacenter consensus rev (S4: Visible Alpha NVDA DC FY26E n=42, median $X B, range $Y–$Z, 25th-75th $A–$B)."
  - "JPM consensus EPS FY25E (S4: Yahoo Finance consensus EPS $18.20, n=22, range $16.80–$19.50)."
  - "MRK consensus FY26 Keytruda revenue (S4: FactSet consensus median $X B, n=18, dispersion 12%)."
- **Why dispersion is the signal, not the point**: Narrow dispersion = consensus is pricing it in (less alpha edge available from agreeing). Wide dispersion = analyst disagreement = look for the non-consensus angle (often the source of edge).
- **Caveats**:
  - Sell-side systematically overestimates EPS at cycle peaks and underestimates at troughs; this is structural, not malice.
  - Use **median**, not mean. Mean is distorted by outliers (one stale or buy-side-captive analyst).
  - **Estimate freshness** matters: tag freshness_days in citation object; flag if any constituent estimate is >14 days stale (a "D-flag" in verification).
  - In EDGAR-only mode (D5), Yahoo Finance / StockAnalysis are typically the free S4 fallback. Note: free aggregators often pull from Refinitiv IBES but on a delayed and less-curated basis.

### S5 — Alt-data, industry research, and channel checks

- **Definition**: Third-party industry research firms, alt-data providers, expert networks, supply-chain channel checks. Mature ecosystem in the US.
- **US source_type enum members**: `Gartner`, `IDC`, `IHS Markit / S&P Global`, `NielsenIQ`, `Circana`, `Counterpoint`, `Omdia`, `Yipit`, `Second Measure`, `Earnest Analytics`, `M Science`, `Placer.ai`, `SimilarWeb`, `AppFigures`, `GLG`, `Tegus`, `AlphaSights`, `Third Bridge`.
- **Red-team resistance**: Low-medium. **Always specify provider + methodology + sample size + freshness**.
- **Examples**:
  - "Datacenter GPU TAM 2026 +X% YoY (S5: Gartner DC GPU forecast 2026/03, methodology: hyperscaler capex × GPU-attach × ASP)."
  - "Retail foot traffic at LULU stores +X% YoY (S5: Placer.ai weekly visit panel 2026-04, n=1,200 doors)."
  - "JPM credit card spend YoY (S5: Earnest Analytics card panel 2026-Q1, n=6M households)."
  - "MRK Keytruda script trend (S5: IQVIA Rx data 2026-Q1 weekly)."
- **Caveats**:
  - **Providers disagree by 5–15% on overlapping questions** (e.g., Gartner vs IDC on DC GPU shipments; Yipit vs Second Measure on a given vendor's card share). Always cross-check at least two providers when alt-data drives a top-3 anchor.
  - **Confirmation bias**: channel checks selected to support a pre-existing view are not evidence. Document the sampling protocol if material.
  - **Expert networks**: GLG/Tegus/AlphaSights/Third Bridge calls are anecdotal individual experts; one expert's view is not a statistical signal. Tag with the number of experts consulted and aggregate where possible.
  - **Freshness**: alt-data freshness >30 days is suspect for fast-moving sectors (consumer, tech); freshness >90 days is suspect even for slow-moving sectors.

### Pending — Unverified

- **Definition**: Trade press rumors not confirmed by the company or SEC filing; anonymous-source-only reporting; post-knowledge-cutoff specifics not yet verified via WebSearch/WebFetch within the current run; internally-modeled numbers without a traceable source chain.
- **Red-team resistance**: Zero. **Never a headline anchor.** If unavoidable, mark `(Pending — not used as anchor)` and isolate in a separate "Pending Assumptions" section of the memo.
- **Examples**:
  - "Reportedly NVDA in talks for Mellanox-2 acquisition (Pending — The Information 2026-05-10, anonymous sources, not company-confirmed)."
  - "MRK Phase 3 readout for V940 expected H2 2026 (Pending — sell-side speculation, no company-issued date)."
- **Cross-cutoff verification (D5 + D9)**: any post-Jan-2026 specific number must be verified by WebSearch or WebFetch within the current run. If verification succeeds and resolves to S1-S5 source, upgrade. If verification fails (cannot find independent corroboration), downgrade to Pending and document.

---

## Decision rules

### Rule 1 — Headline conditional gate (the central gate)

Define **top-3 anchors** = the three specific numbers that most directly drive the headline thesis (typically: a revenue/segment number, a margin or unit-economics number, and a market-share or capex/demand number).

- Three anchors all **S1–S2** → headline can be **unconditional** (e.g., "Buy, +18% expected").
- Any one anchor is **S3** → headline must be **source-conditional** (Pattern A or C below).
- Any one anchor is **S4–S5** → headline gives **range, not point** (Pattern D); scenarios labeled "consensus-anchored."
- Any one anchor is **Pending** → that anchor is **excluded** from headline calculation; isolate in Pending Assumptions section.

The schema `schemas/source_tags.json` field `headline_conditionality` (enum: `unconditional` / `source_conditional` / `range_only`) encodes this. Verification gate **G7** (`scripts/verify_headline_conditionality.py`) checks the memo Markdown headline language against the top-3 anchor S-levels and fails the run if they do not match.

### Rule 2 — First-use citation gate (per D16)

Every specific number — revenue, GM, segment share, customer concentration, capacity, ADV, beta, ASP, capex, market share, sensitivity bps — **must carry an S-tag at first appearance** in the memo Markdown.

Citation format (regex-matchable `\((S[1-5]|Pending):.+?\)`):
- `(S1: NVDA 2024 10-K Item 7)`
- `(S2: NVDA FY24Q3 10-Q Note 4)`
- `(S3: NVDA FY24Q4 earnings call 2025-02-26 ~22min mark)`
- `(S4: Visible Alpha NVDA DC FY26E n=42 median $X range $Y-$Z)` or `(S4: Yahoo Finance consensus EPS $X.XX n=22)`
- `(S5: Gartner DC GPU forecast 2026/03)`
- `(Pending — not used as anchor)`

Subsequent mentions of the same number do not require re-citation (first-use only, per D16 recommendation). Verification gate **G6** (`scripts/verify_source_tags.py`) regex-scans the memo for unsourced specifics and fails the run on any uncited number.

### Rule 3 — S3 promotion path

An S3 fact can graduate to S2 when:
- It appears in a subsequent filing — e.g., a segment split disclosed by IR on an earnings call (S3) becomes S2 once it appears in the next 10-Q Segment Information footnote.
- It is independently corroborated by two or more credible sources — not full S2 but stronger than single-source S3 (call this "S3+" informally).

The `promotion_path` field on the citation object documents the expected promotion event ("Next 10-Q filing 2026-08-15 expected to confirm segment split"). Tracking promotion paths feeds the monitoring framework's catalyst calendar.

### Rule 4 — Cross-cutoff verification (per D5 + D9)

Claude knowledge cutoff is **2026-01**. Today is **2026-05-15**. Any specific number with a publication or filing date after the cutoff must be verified via WebSearch or WebFetch within the current run. Verification results attach to the citation object's `verified` (boolean) and `verification_query` (the exact query) fields.

- Verification success (independent corroboration found) → tag stays at its inherent S-level.
- Verification fails (cannot corroborate) → downgrade to Pending.

Per D9, minimum **12 WebSearch+WebFetch calls per memo**. The highest-risk hallucination classes are regulatory designations (Entity List, OFAC SDN, CFIUS), M&A status (announced vs closed vs blocked), and litigation outcomes — these get extra verification weight.

### Rule 5 — Strongest-link, not weakest-link

S1 data is not contaminated by adjacent S3 commentary. Example:
- NVDA FY24 total revenue is S1 (10-K).
- NVDA FY24 datacenter-vs-gaming revenue split is S1 (10-K Note 13 segment table).
- NVDA FY24 datacenter "inference vs training" split is S3 (per management commentary on calls — not in the 10-K segment table at that granularity).

All three coexist in the memo with their own tags. The headline driven by total revenue + segment split rests on S1; a finer thesis on inference/training mix carries the S3 caveat.

---

## Source-conditional headline language patterns

When the top-3 anchors include any S3 or weaker source, use these English patterns (ported from the China Pattern A–D catalog per delta matrix §9).

### Pattern A — Source-conditional bias (overall direction moderate, key anchors weak)

> "**Source-conditional Hold (mild positive bias).** 12-month median expected return +5% conditional on [anchor1: S3], [anchor2: S3], [anchor3: S5] graduating to S2 within [timeframe / next-filing date]. If any anchor is falsified in verification, downgrade to [revised view, e.g., Sell]."

Use when: direction is meaningful but evidence base is mostly transcript color or alt-data. The conditionality is on **source promotion**, not on a triggering event.

### Pattern B — If-then event (direction conditional on a specific upcoming trigger)

> "**Base case neutral-bearish (median −4%).** If FY26Q1 datacenter revenue confirmed >$X B in 10-Q filed [date], upgrade to neutral-mild-bullish (median +6%). If <$Y B, downgrade to bearish (median −12%)."

Use when: a specific upcoming filing or event has the numerical resolution that flips the directional view. The conditionality is on a **measurable trigger**, with explicit numerical thresholds (linked to G9 — `verify_what_would_reverse.py`).

### Pattern C — Anchored to upcoming filing (view dated to the next anchor graduation)

> "This view is anchored to NVDA FY24Q3 10-Q (filed 2024-11-20). We will re-rate after FY24Q4 10-K (expected mid-February 2025), which will graduate [specific S3 anchors: Blackwell mix, hyperscaler-vs-enterprise split] to S2."

Use when: the view is explicitly time-limited to the current filing cycle and re-evaluation is scheduled.

### Pattern D — Consensus-range (S4-anchored, range not point)

> "12-month median expected return +6%; scenario-weighted range [−4%, +18%]. Lower bound anchored to S4 consensus FY26 EPS $X.XX (median, n=42, range $Y.YY–$Z.ZZ); if actual EPS lands at the 25th percentile $A.AA, lower bound shifts to −10%. Upper bound assumes Blackwell mix ≥ Z% by FY26Q3 (S3 management commentary, not yet S2-graduated)."

Use when: the headline is anchored to a consensus number where dispersion is the relevant signal. Always show the 25th and 75th percentile, not just the median.

---

## Worked example — NVDA (illustrative for Phase E self-test)

**Top-3 anchors:**

| # | Claim | Value | S-level | Citation |
|---|---|---|---|---|
| A1 | NVDA FY25 datacenter revenue | $X B | S1 | NVDA 2025 10-K Item 8, Note 13 Segment Information (when filed late Feb 2025) |
| A2 | Hyperscaler aggregate 2026 capex YoY growth | +Y% | S5 | Trade press aggregation (MSFT/GOOG/META/AMZN public commentary, S3-S5) + Gartner DC capex forecast 2026/03 |
| A3 | Blackwell ASP uplift vs Hopper | +30–40% | S3 | NVDA FY25Q1 earnings call transcript 2025-05-22 ~22min mark (CFO Q&A) |

**Headline (Pattern A + B blend):**

> "**Source-conditional Buy (moderate-positive bias).** 12-month median expected return +18%; scenario-weighted range [−5%, +35%], conditional on (i) hyperscaler aggregate 2026 capex YoY > +15% confirmed across MSFT/GOOG/META/AMZN FY26Q1 results filed by 2026-05-15, AND (ii) Blackwell mix visible at ≥40% of DC revenue in NVDA FY26Q1 10-Q segment commentary (expected filed late May 2026). If hyperscaler capex falsifies <+10% OR Blackwell mix <25%, downgrade to Hold (median +2%, range [−12%, +12%])."

**Why this works:**
- A1 is S1 (or will be S1 once FY25 10-K filed) — the revenue base is unconditional.
- A2 is S5 with significant dispersion (Gartner vs IDC differ; hyperscaler commentary itself is S3) — drives the range bottom, not a point estimate, and a Pattern B trigger is supplied.
- A3 is S3 transcript color — drives the upside but cannot stand alone for an unconditional Buy; the Pattern B trigger (≥40% mix in 10-Q) provides the promotion path to S2.

---

## Worked example — JPM (cross-sector portability check)

**Top-3 anchors:**

| # | Claim | Value | S-level | Citation |
|---|---|---|---|---|
| B1 | JPM FY24 net interest income | $X B | S1 | JPM 2024 10-K Item 7 MD&A, NII line |
| B2 | FY25 NII guidance | ~$90B | S3 | JPM FY24Q4 earnings call transcript 2025-01-14 (CFO formal guidance), restated in Investor Day deck 2025-02-25 |
| B3 | Deposit beta (cycle) | ~55% | S4/S5 blend | S4: sell-side consensus deposit beta range 50–60% across BoA, MS, GS, WFC notes; S5: third-party rate-sensitivity modeling (Curinos) |

**Headline (Pattern D + Pattern C blend):**

> "**Source-conditional Hold (slight positive bias).** 12-month median expected return +6%; scenario-weighted range [−8%, +18%]. Lower bound anchored to S3 FY25 NII guidance $90B holding firm; if FY25Q1 10-Q (expected 2025-05-15) reaffirms full-year NII midpoint at or above $90B, upgrade to mild Buy. If FY25Q1 NII run-rate annualizes below $86B (10% below guide midpoint), downgrade to Sell. Deposit beta sensitivity: every +5pp deposit beta vs current 55% reduces NII by ~$1.8B (S4/S5 modeled)."

This shows the framework is sector-portable: the central discipline (anchor S-level → conditional language) ports cleanly from semis to a money-center bank, with sector-specific anchors (NII, deposit beta, CET1) replacing tech-specific anchors (DC revenue, ASP, mix).

---

## Worked example — MRK (biotech / large-cap pharma, secondary cross-sector check)

**Top-3 anchors:**

| # | Claim | Value | S-level | Citation |
|---|---|---|---|---|
| C1 | MRK FY24 Keytruda revenue | $X B | S1 | MRK 2024 10-K Item 7 (product-level disclosure in MD&A) |
| C2 | Keytruda US LOE timing (composition-of-matter patent expiry) | Mid-2028 | S2 | MRK 2024 10-K Item 1 Risk Factors + Item 1A patent disclosures |
| C3 | Subcutaneous Keytruda formulation share assumption post-launch | 30–50% by 2030 | S3/S5 blend | S3: MRK management commentary FY24Q4 call 2025-02-04; S5: IQVIA SC oncology biologics adoption curves |

**Headline (Pattern A + Pattern C blend):**

> "**Source-conditional Hold (mild negative bias).** 12-month median expected return −3%; scenario-weighted range [−18%, +12%]. View anchored to: (a) Keytruda LOE 2028 (S2-confirmed in 10-K Risk Factors), (b) SC Keytruda commercial conversion 30–50% (S3 management aspiration + S5 historical biologics SC-IV conversion analogs). If SC Keytruda Phase 3 head-to-head readout (expected H2 2026) confirms non-inferiority AND label is approved with broad indication, upgrade to mild Buy. If FDA issues CRL or non-inferiority margin missed, downgrade to Sell. View will re-rate after MRK FY26Q3 10-Q (filed Nov 2026) for early SC launch metrics if approved."

This third sector example shows the framework's elasticity: in biotech, S-levels naturally tilt toward S3-S5 (commercial uptake assumptions, pipeline NPV) because the audited 10-K covers only historical revenue. The conditional language and explicit trigger thresholds (FDA outcome, non-inferiority margin) are mandatory.

---

## Anti-patterns (will fail PM red-team)

| Anti-pattern | What's wrong | Fix |
|---|---|---|
| "Street expects EPS of $X" with no source | Unsourced consensus claim — fails G6 | "Consensus FY25 EPS $X (S4: Yahoo Finance n=22, median, range $Y–$Z, freshness 7 days)" |
| "Management expects DC revenue to accelerate" | Wishful + no source + no number | "CFO guided FY26 DC revenue growth to 'meaningfully higher than current run-rate' per transcript (S3: NVDA FY25Q4 call 2026-02-26 ~14min); sell-side consensus FY26 DC growth +X% YoY (S4: Visible Alpha n=42 median, range Y%–Z%)" |
| "Per The Information, NVDA is in talks to acquire X" used as top-3 anchor | Unsourced rumor in headline thesis — fails G7 | Move to "Pending Assumptions" section; tag `(Pending — not used as anchor)`; do not enter scenario weighting |
| "PT $200" with all-S3 top-3 anchors | Over-precise point estimate on weak anchors — fails G7 | Convert to range; add Pattern A conditional language; show 25/50/75th percentiles of scenario outcomes |
| S1 revenue blended with S4 consensus EPS reported as a single "PE" point | Mixing source levels into one synthesized number with no tag | Show both with their own tags; if a synthesized multiple is needed, label as "blend (S1 revenue + S4 EPS path)" |
| Non-GAAP EPS cited as S1 because it's in the 10-K | Non-GAAP EPS is an unaudited management construct on top of the audited GAAP base; the GAAP figure is S1, non-GAAP is S2 (with Reg G reconciliation) at best, often S3 if defined idiosyncratically | Tag GAAP EPS S1; tag non-GAAP EPS S2 with explicit reconciliation reference; flag B11 (non-GAAP/GAAP gap) per `pm-redteam-rubric-us.md` |
| Earnings press release headline guidance cited as S2 | The 8-K Item 2.02 press release attaches financial tables (S2) but management guidance ranges issued same-day are S3 unless they appear verbatim in the press release with specific numerical commitments | Cite the press release for tabular financials (S2); cite the call transcript for the guidance commentary (S3); verify guidance against the transcript not the press release per delta matrix §11 |

---

## Source stratification box template

Every IC memo must contain this box near the top (§2 of the structured memo per `schemas/memo.json` `top_anchors` field). It is the visible, scannable index of what the headline rests on.

```
SOURCE STRATIFICATION BOX — Top-5 Anchors

┌─────┬─────────────────────────────────┬───────────┬──────┬─────────────────────────────────────┬──────────────────────────┐
│ ID  │ Claim                           │ Value     │ S    │ Citation                            │ Promotion Path           │
├─────┼─────────────────────────────────┼───────────┼──────┼─────────────────────────────────────┼──────────────────────────┤
│ A1  │ NVDA FY25 datacenter revenue    │ $X B      │ S1   │ NVDA 2025 10-K Item 8 Note 13       │ (already S1)             │
│ A2  │ Hyperscaler 2026 capex YoY      │ +Y%       │ S5   │ Gartner DC capex forecast 2026/03   │ MSFT/GOOG/META/AMZN      │
│     │                                 │           │      │   + hyperscaler IR commentary (S3)  │   FY26Q1 prints by May   │
│ A3  │ Blackwell ASP uplift vs Hopper  │ +30–40%   │ S3   │ NVDA FY25Q1 call 2025-05-22 ~22min  │ FY26Q1 10-Q segment      │
│     │                                 │           │      │                                     │   commentary (May 2026)  │
│ A4  │ NVDA FY26 GAAP gross margin     │ ~75%      │ S3   │ NVDA FY25Q4 call 2026-02-26 guide   │ FY26 10-K filed Feb 2027 │
│ A5  │ Consensus FY26 DC revenue       │ $X B med  │ S4   │ Visible Alpha n=42 range $Y–$Z      │ (consensus, refresh 14d) │
└─────┴─────────────────────────────────┴───────────┴──────┴─────────────────────────────────────┴──────────────────────────┘

HEADLINE CONDITIONALITY: source_conditional
(Top-3 = A1 S1, A2 S5, A3 S3 → any S3 in top-3 triggers source-conditional headline per Rule 1)
```

Required columns:
1. **ID** — short anchor identifier (A1, A2, ...) referenced in scenario table and sensitivity grid.
2. **Claim** — plain-English statement of what the number is.
3. **Value** — the number with explicit unit ($M / $B / % / bps / etc. — never ambiguous per delta matrix §11 unit-confusion class).
4. **S-level** — S1 / S2 / S3 / S4 / S5 / Pending.
5. **Citation** — specific reference matching the D16 regex format.
6. **Promotion Path** — for S3-S5, the expected event that would graduate the anchor (filing date, next earnings call, etc.); for S1-S2, write "(already at floor)".

Below the table, write the explicit headline conditionality computed from the top-3 anchors. This is the human-readable mirror of `schemas/source_tags.json` field `headline_conditionality`.

---

## Cross-references

- **Schema**: `schemas/source_tags.json` — the machine contract this prose mirrors.
- **Verification scripts**: `scripts/verify_source_tags.py` (G6), `scripts/verify_headline_conditionality.py` (G7), `scripts/verify_what_would_reverse.py` (G9) — Phase C.
- **Verification gates schema**: `schemas/verification_gates.json` — G6 and G7 constants used here.
- **Data source catalog**: `us-equity-research/references/us-data-sources.md` (S-B1-3) — per-tier URL catalog.
- **Verification protocol**: `us-equity-research/references/verification-protocol-us.md` (S-B2-5) — 12 WebSearch minimum (D9), guidance-against-transcript rule (delta matrix §11), unit-confusion class.
- **Forensic checklist**: `us-equity-research/references/forensic-accounting-checklist-us.md` (S-B2-1) — non-GAAP/GAAP discipline (B11), SBC/FCF (B12), restatement triggers (8-K Item 4.02).
- **PM red-team rubric**: `us-equity-ic-rigor/references/pm-redteam-rubric-us.md` (S-B2-6) — B11–B14 US-specific bugs that interact with source stratification.
- **Memo umbrella schema**: `schemas/memo.json` — top_anchors field is the structured form of the Source Stratification Box.
- **Open decisions referenced**: D5 (EDGAR-only default), D9 (12 WebSearch minimum), D16 (citation regex format), D18 (trigger phrases).
