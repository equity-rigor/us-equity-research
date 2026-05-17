# Verification Protocol (US)

The single biggest failure mode in agent-driven research is **unverified hallucination dressed up as primary-source rigor**. Sub-agents will confidently produce plausible-looking URLs, EDGAR accession numbers, document Item / Note references, regulatory designations, and specific dollar figures that do not exist or are wrong. This is more acute for US research than for China research because (a) the EDGAR corpus is larger and more variegated, (b) US events post the model's January 2026 knowledge cutoff need active verification (today's session date is 2026-05-15), and (c) US regulatory designations span more agencies (BIS, OFAC, CFIUS, FDA, FTC, DOJ, ITC, state AGs, EU CMA) than China's primary regulators.

This protocol catches and corrects errors before they reach the user. It is the operational reading of D9 (minimum 12 WebSearch+WebFetch calls per memo), D5 (EDGAR-only default), D16 (citation regex), and gates G6 (`verify_source_tags.py`), G7 (`verify_headline_conditionality.py`), G10 (`verify_weighting_sensitivity.py`).

---

## When to Run

**Always.** Verification is mandatory before any IC memo is delivered. There is no version of the workflow where verification is optional. This applies to every deliverable from `phase-3-valuation-us.md` — institutional IC memo, IC pre-read, IC debate script, LP letter, earnings prep, earnings flash.

If the user pushes for "skip verification, I need this in an hour" — push back. An unverified memo with a hallucinated regulatory designation in the headline is worse than no memo. Negotiate a smaller scope, not weaker verification.

---

## What to Verify

Extract every material specific claim from the IC memo. Material = anything that drives the recommendation, anchors a scenario, or is cited as a primary fact. Examples:

- Specific FY revenue / net income / segment numbers
- Specific quarterly results (FY+0Q+1 through current)
- Segment revenue and GM breakdown (rows from Phase 1 A4 revenue_by_product / revenue_by_geography)
- Customer concentration percentages (e.g., "Customer X is 14% of revenue")
- Regulatory designation status (BIS Entity List, OFAC SDN, CFIUS forced divestiture, DoD 1260H)
- M&A status (announced vs Second Request issued vs cleared vs blocked vs closed)
- FDA action status (PDUFA met / CRL issued / AdCom outcome / 510(k) cleared)
- Antitrust matter status (consent decree vs litigation vs cleared)
- Settlement amounts (specific dollar amounts in IP / antitrust / securities class action)
- Capacity additions (specific GW / wafers / tons / $ capex)
- Specific contractual obligations (8-K Item 1.01 details)
- Specific stock prices and consensus targets (pull live within 24h of publication)
- Industry forecasts (Gartner / IDC / Counterpoint / Omdia / IQVIA / Yipit specific numbers)
- Management guidance (verify against earnings call transcript, NOT press release — see below)

## What NOT to Verify

These are analytical interpretations, not facts. Do not verify them:

- Framework claims (e.g., "this is a quality compounder," "this is a deep-value name")
- Structural narratives (e.g., "the moat is durable")
- Scenario probabilities (analyst-assigned)
- Valuation methodology choices (e.g., "we use SOTP because the conglomerate discount is wide")
- Position sizing recommendations (these reflect conviction, not external fact)

---

## Verification Method

For each material specific claim:

1. **Run direct WebSearch with specific terms** — not vague terms.
   - Bad: "NVDA datacenter revenue"
   - Good: `"NVIDIA" "datacenter" Q4 2025 segment revenue 10-K`
   - Better: EDGAR full-text search `https://efts.sec.gov/LATEST/search-index?q=%22datacenter%22&forms=10-K&ciks=0001045810`
   - Reason: specific search returns confirmation or contradiction; vague search returns generic content.

2. **Cross-check against at least 2 independent sources**.
   - SEC primary (EDGAR filing, XBRL company facts API)
   - Trade press (The Information / STAT / Wards Auto / Energy Intel / sector-specific)
   - Sell-side notes (where accessible — Yahoo Finance / StockAnalysis / TipRanks free; AlphaSense / Capital IQ Pro premium)
   - Government primary (BIS Entity List page, OFAC SDN search, FDA dashboards, Federal Register notice)
   - Legal alerts only as supplementary (Hogan Lovells, Crowell & Moring, Skadden, Arnold & Porter, Squire Patton Boggs)

3. **Classify each claim**:
   - ✅ **Verified** — at least 2 independent sources confirm the specific claim
   - ⚠ **Partially verified** — directional claim correct but specific number / detail differs
   - ❌ **Contradicted** — search returns evidence the claim is wrong
   - ⏳ **Unverifiable** — no public source confirms or contradicts (treat as suspect; downgrade to Pending per `source-stratification-us.md`)

4. **Capture source URL** for each verified claim.
   - For EDGAR documents: the direct filing accession URL (e.g., `https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nodash}/`)
   - For trade press: the article URL with publication date
   - For government sources: the official agency page URL with capture date

5. **Per D9, minimum 12 distinct WebSearch+WebFetch calls** per memo. This is the floor, not the ceiling. Complex names (multi-segment, multi-regulatory-jurisdiction, M&A-pending) typically need 20-40 verification calls.

---

## High-Risk Hallucination Categories (US-Specific)

These categories drive most verification failures. Scrutinize specifically.

### Regulatory designation status

**Most common hallucination**: "Company X was designated on the Entity List on [date]" — when the actual fact is "lawmakers requested addition" or "company is under preliminary investigation."

**Distinctions to enforce**:
- "Lawmaker [Y] requested addition" — advocacy, not designation
- "Hearing held to consider addition" — process, not designation
- "Committee voted to recommend addition" — recommendation, not designation
- "Department added to list on [date]" — actual designation

**Verification**:
- BIS Entity List: open the actual page at `https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list`. Cross-reference the Federal Register notice number for the most recent update.
- OFAC SDN: query `https://sanctionssearch.ofac.treasury.gov` directly; do not rely on legal alerts.
- CFIUS: forced divestitures are usually disclosed via Treasury press + company 8-K Item 8.01.
- DoD 1260H: pull the official DoD PDF; the public list lags by 30-60 days vs. internal designation.

### FDA decisions

**Most common hallucination**: "FDA approved drug X on [date]" — when the actual fact is "PDUFA date set, but CRL issued" or "AdCom recommended approval but FDA delayed decision."

**Distinctions to enforce**:
- "PDUFA date" — the FDA's self-imposed deadline (10-12 months from filing); a date, not a decision
- "AdCom vote" — advisory committee recommendation (e.g., 14-1 to approve); FDA can override
- "Approved" — FDA approval letter issued
- "CRL issued" — Complete Response Letter, refusal to approve with specified deficiencies
- "PDUFA delayed" — FDA extends action date (often signals additional review needed)
- "REMS imposed" — Risk Evaluation and Mitigation Strategy requirement

**Verification**:
- FDA approval letter: `https://www.accessdata.fda.gov/scripts/cder/daf/`
- FDA press announcements: `https://www.fda.gov/news-events/press-announcements`
- 8-K Item 8.01 from company on the same day as decision
- Cross-check against STAT News, BioPharma Dive, Endpoints, FierceBiotech

### M&A status

**Most common hallucination**: "Deal closed at $X per share" — when the actual fact is "deal announced but DOJ Second Request issued, closing delayed."

**Distinctions to enforce**:
- "Announced" — definitive agreement signed; 8-K Item 1.01
- "HSR filed" — pre-merger notification submitted
- "Second Request issued" — agency wants more data; deep antitrust review
- "Consent decree" — agency clears with conditions (divestitures)
- "Litigation filed" — agency suing to block
- "Cleared" — agency closed investigation without action
- "Closed" — transaction consummated; 8-K Item 2.01
- "Terminated" — deal dead; 8-K Item 1.02

**Verification**:
- 8-K filings on both sides (target + acquirer)
- FTC + DOJ press releases (ftc.gov/news-events, justice.gov/atr)
- EU CMA Phase I / Phase II decisions
- Mergermarket / DealReporter (premium)

### Antitrust outcomes

**Most common hallucination**: "FTC blocked the deal" — when the actual fact is "FTC sued to block, court denied preliminary injunction, deal proceeded."

**Distinctions to enforce**:
- "Sued to block" — agency filed complaint
- "PI granted" — preliminary injunction; deal effectively blocked
- "PI denied" — court declines to halt; deal can proceed
- "Consent decree" — agency clears with structural remedy
- "Cleared" — no action taken

**Verification**:
- FTC press: `https://www.ftc.gov/news-events/press-releases`
- DOJ ATR press: `https://www.justice.gov/atr/press-releases`
- PACER docket (CourtListener / RECAP wrapper for free): `https://www.courtlistener.com`

### Specific note / Item references

**Most common hallucination**: "Per Note V.57 of FY25 10-K, asset impairment was $X" — sub-agents may invent note numbering and specific values.

**Verification**:
- Open the actual 10-K filing on EDGAR and check the Note number + page
- 10-K notes are typically numbered 1 through ~25, organized by topic (Revenue Recognition, Leases, SBC, Income Taxes, Debt, Segments, Commitments and Contingencies, Subsequent Events)
- "Note V.57" with Roman numerals is a Chinese-filing convention (用罗马数字), not US-filing convention — flag as likely hallucination
- US convention: cite by topical name + page, e.g., "10-K Note 13 Segment Information, p. F-32"

### $M vs $B vs thousands unit confusion (B1-class)

**Most common hallucination**: Citing a number in the wrong unit by 10x or 1000x.

**Verification**:
- Always check the cover-page unit declaration (e.g., "(in millions, except per-share data)")
- Some smaller filers report in thousands; some in millions; rarely in billions
- Sanity-check: compute the number as % of market cap or % of net income. If the percentage is implausible (e.g., a single quarter expense > market cap), the unit is wrong.
- This is the US analog of the China 亿 unit confusion (delta matrix §11)

### Stock prices and consensus targets

**Most common hallucination**: Using a stale price or a model-cutoff price.

**Verification**:
- Pull live within 24 hours of memo publication
- Sources: Yahoo Finance `finance.yahoo.com/quote/{ticker}`, StockAnalysis `stockanalysis.com/stocks/{ticker_lower}/`, WSJ Markets, MarketWatch
- For consensus: pull live; cite n=, range, freshness
- Today's session date is 2026-05-15; any post-cutoff (Jan 2026) specific must be live-verified

---

## Transcript-Over-Press-Release Rule (Delta Matrix §11)

**Management guidance MUST be verified against the earnings call transcript, NOT the press release.**

The 8-K Item 2.02 press release attaches the financial tables (S2-grade), but management guidance ranges are often given on the call with broader or different language than the headline number in the press release. Reg FD §17 CFR 243 requires same-day broad distribution of material non-public information, which makes guidance a contractual disclosure — but the call commentary IS the broad distribution, not the press release.

**Operational rule**:
- For any guidance claim (revenue range, EPS range, margin trajectory, capex guidance, segment growth target), pull the earnings call transcript and verify the exact range / language given on the call.
- Sources for transcripts: AlphaSense / Capital IQ Pro / SeekingAlpha Pro (premium), Motley Fool transcripts `fool.com/earnings/call-transcripts/` (free, T+1 to T+3 lag), company IR page raw webcast replay.
- In citation: tag with the transcript timestamp and the specific speaker:
  `(S3: NVDA FY25Q4 earnings call 2026-02-26 ~22min mark, CFO Q&A response)`

**Failure mode**: An analyst anchors PT to "FY26 EPS guide of $5.20" from the press release, but on the call the CFO said "we now see FY26 EPS in the $5.00-$5.30 range with significant Q1 lumpiness." The range, not the midpoint, is the real S3 anchor.

---

## Independent Sanity Check Sub-Agent

After running your own verification, dispatch an independent sub-agent that re-verifies using its own web searches. Do not trust the prior verification. This catches confirmation-bias compounding (delta matrix §10).

**Sanity check sub-agent prompt template**:

```
You are an independent sanity-check analyst on a buy-side research team.
Today is [DATE]. You MUST use WebSearch and WebFetch extensively — minimum
12 distinct calls.

CONTEXT: A research team has produced a long [COMPANY] research report.
Your job is to INDEPENDENTLY verify the key facts using web searches you
conduct yourself. Do NOT trust the prior verification — verify again.

KEY CLAIMS TO INDEPENDENTLY VERIFY (one search per claim minimum):

[List 10-15 claims with specific values, dates, citations]

DELIVERABLES:

A) For each claim, document:
   - Verified ✅ / partially verified ⚠ / contradicted ❌ / unverifiable ⏳
   - Specific source URL
   - Any discrepancies or nuances

B) Identify any NEW material information the prior research missed

C) Flag suspicious claims you couldn't verify

D) Bottom-line: would you sign off on the report (i.e., use it for IC
   decision)? If not, what changes are needed?

REQUIREMENTS:
- 12+ distinct WebSearch + WebFetch calls
- Cite every source with URL
- Be skeptical — your job is to FIND errors, not confirm
- For regulatory matters: verify against actual government source PDF /
  search tool, not legal alerts (per delta matrix §11)
- For guidance: verify against earnings call transcript, NOT press release
- Length 2,000 words
- Final verdict on whether the report is sound
```

---

## Verification Report Output

Write a Verification Report with:

1. **Verification matrix** — table of all claims with status (✅ / ⚠ / ❌ / ⏳) and source URL
2. **Critical corrections** — explicit list of what was wrong, what's actually true, and the implication for the thesis (e.g., bear PT shifts, scenario weights re-balance, headline conditionality changes from unconditional to source-conditional)
3. **Unverifiable details** — explicit list of what couldn't be confirmed; these get tagged `(Pending — not used as anchor)` per `source-stratification-us.md` and isolated in a Pending Assumptions section
4. **Methodology notes** — for the next research project on this name, what to verify proactively

Save as `outputs/{ticker}_Verification_Report.md`.

The report conforms to `schemas/verification_gates.json` evidence object structure. Specifically, the 14 verification gates (G1-G14 per `schemas/verification_gates.json`) each produce a structured pass/fail record with evidence + remediation if failed.

---

## What to Do When Verification Surfaces Errors

If verification finds material errors:

1. **Stop and update the IC memo.** Do not deliver an unverified version.
2. **Document the correction explicitly.** Show what was wrong and what's actually true. Tag with the corrected source URL.
3. **Re-evaluate the thesis.** A correction may make the thesis more bullish (e.g., "actually NOT on Entity List" → lower tail risk → bull case strengthens) or more bearish (e.g., "actually 1.4% market share, not 18%" → demand-side impaired → bear case strengthens).
4. **Update position sizing.** Do not keep the same recommendation if the underlying facts changed materially. Per `position-sizing-us.md`, sizing reflects conviction × volatility × capacity — a corrected fact materially shifts conviction.
5. **Re-run gates G1-G14.** Particularly G6 (source tags), G7 (headline conditionality), G9 (what-would-reverse triggers), G11 (non-GAAP/GAAP), G12 (FCF / SBC).
6. **Note the correction in the final deliverable.** The user needs to know if previous versions had errors. But do not dwell on the correction process — focus on the corrected conclusion.

---

## Common Verification Patterns from Past US Research

These are recurring surprises that catch sub-agents repeatedly:

- **Regulatory designations** are frequently misstated. "Lawmakers requested" gets confused with "added to list." Verify against the actual government source page, not just legal alerts.
- **FDA decision status** changes by date. A drug that was "PDUFA scheduled" three months ago may now be "CRL issued" or "approved with REMS." Always pull the freshest FDA action letter.
- **Settlement amounts** often have substantial uncertainty. Initial reports may cite one figure; later 10-Q / 10-K updates revise. Verify against the most-recent 10-Q Note "Commitments and Contingencies."
- **Customer concentration** can change quarter-to-quarter. Don't anchor to a specific quarter's 10% disclosure; look at trend across 8 quarters.
- **$M vs $B confusion** is the most common single error class. Always sanity-check the magnitude as % of revenue / market cap / net income.
- **Specific transaction amounts** often have rounding differences ($1.30B vs $1.32B vs $1.295B). Verify exact value against the 8-K Item 1.01 attached agreement (not the press release summary).
- **Stock prices** move daily. Always pull live at IC publication time; don't rely on weeks-old figures. Gates G7 and G10 may invalidate on stale pricing.
- **Insider Form 4 patterns** can flip mid-cycle. Refresh openinsider.com on the day of memo publication.
- **Sell-side consensus** drifts across aggregators (Yahoo / Refinitiv / Zacks / StockAnalysis). Cite the aggregator explicitly with the snapshot timestamp.
- **The most "convenient" finding is often the most suspect.** When a finding strongly supports the bull or bear case, scrutinize extra hard — confirmation bias loves a clean narrative.
- **13F filing windows** mean positioning data is always 45-day-lagged. For current crowding, supplement with options OI + short interest (per `positioning-sentiment-us.md`).
- **Cross-cutoff verification.** Anything dated after Jan 2026 (Claude knowledge cutoff) needs active WebSearch. Do not trust training-data recall for FY25Q4, FY26Q1, FY26Q2 specifics.

---

## Cross-References

- For S1-S5 + Pending citation discipline, see `source-stratification-us.md`.
- For the 12-call minimum per memo (D9), see `us-data-sources.md` §"Source verification protocol per D9."
- For the 14 verification gates schema, see `schemas/verification_gates.json` and the gate scripts at `scripts/verify_*.py`.
- For monitoring post-IC delivery, see `monitoring-framework-us.md`.
- For the PM red-team rubric (6-9 score bands, B11-B14 US bugs), see `pm-redteam-rubric-us.md`.
