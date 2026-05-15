# Verification Protocol

The single biggest failure mode in agent-driven research is **unverified hallucination dressed up as primary-source rigor**. Sub-agents will confidently produce plausible-looking URLs, document IDs, note numbers, and specific values that do not exist or are wrong.

This protocol catches and corrects those errors before they reach the user.

## When to Run

**Always.** Verification is mandatory before any IC memo is delivered. There is no version of the workflow where verification is optional.

## What to Verify

Extract every material specific claim from the IC memo. Material = anything that drives the recommendation or is cited as a primary fact. Examples:

- Specific FY revenue / net income / segment numbers
- Specific quarterly results
- Customer share percentages ("X% of Apple's iPhone 17 panels")
- Regulatory designations ("designated on Entity List", "added to 1260H")
- M&A details (counterparty, price, structure, timing)
- Settlement amounts (specific currency amounts in IP/litigation settlements)
- Capacity additions (factory tonnage, mass production dates)
- Specific contractual obligations (put/call clauses, share-swap deadlines)
- Specific stock prices and consensus targets
- Specific industry forecasts ("Counterpoint sees X% YoY decline")

**Do not verify**: framework claims, structural narratives, scenario probabilities, valuation methodology choices. These are analytical interpretations, not facts.

## Verification Method

For each material claim:

1. Run direct WebSearch with **specific terms** including the claim's specific values
   - Bad search: "BOE iPhone share"
   - Good search: `"BOE" "iPhone 17" supplier Samsung shift 2025 yield`
   - Reason: specific search returns confirmation or contradiction; vague search returns generic content

2. Cross-check against **at least two independent sources**
   - Trade press (DigiTimes, OLED-Info, AppleInsider, MacRumors, Counterpoint)
   - Sell-side analysis (Korea Herald, KED Global, Korea-Asia tech sites)
   - Primary disclosures (CNINFO, exchange websites, Federal Register, OFAC)
   - Legal alerts for regulatory matters (Hogan Lovells, Crowell, Squire Patton Boggs, Skadden)

3. Document each as one of:
   - ✅ **Verified** — at least 2 independent sources confirm the specific claim
   - ⚠ **Partially verified** — directional claim correct but specific number / detail is different
   - ❌ **Contradicted** — search returns evidence the claim is wrong
   - ⏳ **Unverifiable** — no public source confirms or contradicts (treat as suspect)

4. Capture the source URL for each verified claim

## High-Risk Claim Categories

These are the categories where hallucination is most common. Scrutinize specifically:

### Regulatory list status

**Most common hallucination**: "Company X was designated on [list] on [date]."

**Reality check**: There's a huge difference between:
- "Lawmaker [Y] requested addition" (advocacy, not designation)
- "Hearing held to consider addition" (process, not designation)
- "Committee voted to recommend addition" (recommendation, not designation)
- "Department added to list on [date]" (actual designation)

Verify by searching the actual government list source PDF / website, not just legal alerts. Read the alert carefully — many describe requests as if they were designations.

### Specific financial note references

**Most common hallucination**: "Per Note V.57 of the FY25 AR, asset impairment was X."

**Reality check**: Sub-agents may invent note numbering and specific values. Verify either:
- Open the actual PDF and check
- Cross-check the specific value via news coverage of the report

### Currency amount conversions

**Most common hallucination**: 10x errors via Chinese 亿 (= 100 million) confusion.

**Reality check**:
- 1 亿 RMB = RMB 100 million = RMB 0.1 billion
- "20.74 亿" = RMB 2.074 billion (NOT RMB 20.74 billion)
- Cross-check by computing as % of net income / market cap — if the percentage is implausible, the conversion is wrong

### Specific transaction amounts

**Most common hallucination**: "Company A bought stake X from B for ¥6.339 billion in CNINFO 2021-005."

**Reality check**: Specific amounts to the third decimal place often invented. Verify either:
- Pull the actual CNINFO announcement (search by date + description)
- Cross-check via news coverage

### Customer-share percentages

**Most common hallucination**: "BOE has X% of iPhone 17 panel supply."

**Reality check**: Cross-check via UBI Research, Display Daily, OLED-Info, AppleInsider — each typically cites specific allocation data with sources. If the same percentage appears in 3+ trade press citations, treat as verified.

### Industry forecast specifics

**Most common hallucination**: Cherry-picked the bearish or bullish data point from a multi-segment forecast.

**Reality check**: When the agent says "Counterpoint sees segment X at -3%", search for the full Counterpoint piece — typically there are multiple sub-segments with different growth rates. The headline may be misleading.

## Independent Sanity Check

After running your own verification, **dispatch an independent sub-agent** that re-verifies using its own web searches. Don't trust the prior verification.

**Sanity check sub-agent prompt template**:

```
You are an independent sanity check analyst on a buy-side research team.
Today is [DATE]. You MUST use WebSearch and WebFetch extensively — minimum 12 calls.

CONTEXT: A research team has produced a long [COMPANY] research report. Your job is
to INDEPENDENTLY verify the key facts using web searches you conduct yourself.
Do NOT trust the prior verification — verify again.

KEY CLAIMS TO INDEPENDENTLY VERIFY (one search per claim minimum):

[List 10-15 claims with specifics]

DELIVERABLES:

A) For each claim, document:
   - Verified / partially verified / contradicted
   - Specific source URL
   - Any discrepancies or nuances

B) Identify any NEW material information the prior research missed

C) Flag suspicious claims you couldn't verify

D) Bottom-line: would you sign off on the report (i.e., use it for IC decision)?
   If not, what changes are needed?

REQUIREMENTS:
- 12+ distinct WebSearch calls
- Cite every source with URL
- Be skeptical — your job is to FIND errors, not confirm
- Length 2,000 words
- Final verdict on whether the report is sound
```

## Verification Report Output

Write a Verification Report with:

1. **Verification matrix** — table of all claims with status and source
2. **Critical corrections** — explicit list of what was wrong, what's actually true, and the implication for the thesis
3. **Unverifiable details** — explicit list of what couldn't be confirmed
4. **Methodology notes** — for the next research project, what to verify proactively

Save as `[Company]_Verification_Report.md`.

## What to Do When Verification Surfaces Errors

If verification finds material errors:

1. **Stop and update the IC memo.** Don't deliver an unverified version.
2. **Document the correction explicitly.** Show what was wrong and what's actually true.
3. **Re-evaluate the thesis.** A correction may make the thesis more bullish (e.g., "actually NOT on Entity List" → lower tail risk) or more bearish (e.g., "actually 1.4% market share, not 18%" → demand is impaired).
4. **Update the position sizing.** Don't keep the same recommendation if the underlying facts changed materially.
5. **Note the correction in the final deliverable.** The user needs to know if previous versions had errors. But don't dwell on the correction process — focus on the corrected conclusion.

## Common Patterns from Past Research

These are recurring verification surprises:

- **Regulatory designations** are frequently misstated. "Lawmakers requested" gets confused with "added to list."
- **Settlement amounts** often have substantial uncertainty. Initial reports may cite one figure; later analysis revises.
- **Customer shares** can change dramatically quarter-to-quarter. Don't anchor to a specific quarter's number; look at trend.
- **Currency unit confusion** (亿 vs. billion) is the most common single error class. Always sanity-check the magnitude.
- **Specific contractual amounts** often have rounding differences. RMB 4.30 bn vs. 4.32 bn vs. 43.0亿 — verify exact.
- **Stock prices** move daily. Always pull live quote at IC meeting; don't rely on weeks-old figures.
- **The most "convenient" finding is often the most suspect.** When a finding strongly supports the bull or bear case, scrutinize extra hard.
