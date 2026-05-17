# What-would-reverse — falsification triggers with denominators (US)

## What this solves

Every directional view (bear, bull, neutral) needs an explicit falsification condition. Without it, the view is unfalsifiable opinion. With a vague one ("if margins recover"), it's *still* unfalsifiable — "recover" has no value. The discipline is:

> A trigger that survives PM challenge has a **specific source channel**, a **numerical threshold with a denominator base**, an **observation window**, and an **action mapping**.

The G9 verification gate (`scripts/verify_what_would_reverse.py`) enforces this: every directional trigger must have a numerical denominator, not a handwave.

## Required structure

Each memo's §7 (or equivalent) contains a "What would reverse this view" table:

```
| Signal               | Source channel              | Threshold (with denominator)            | Window     | Action if hit                            |
|----------------------|-----------------------------|-----------------------------------------|------------|------------------------------------------|
| DC Q1 revenue        | NVDA FY27Q1 10-Q Note 17    | ≥$40B AND YoY ≥ +10%                    | by 5/30/27 | Cap bear; weights base +5pp, bear -5pp; |
|                      |                             |                                         |            | upgrade to Hold, hold_long action        |
| 10Y UST yield        | FRED DGS10 daily            | ≥ 5.5% sustained 4 weeks                | open       | Re-rate multiple band: bear PE 25→22;   |
|                      |                             |                                         |            | re-derive scenarios; -3% headline        |
```

Not every entry is identical — but every entry must have all four elements (signal / source / threshold / window / action).

## The four required elements

### 1. Specific source channel

Not "if the company beats" — **what report? Which line item? Which call segment? Which agency docket?** You must specify the *exact* document or event where the signal will appear. US-specific source channels are richer than China's CNINFO-centric pattern:

- **SEC filings**: 10-Q Note N (segment information, contingencies); 10-K Item 7 (MD&A); 8-K Item 2.02 (results), Item 4.02 (restatement), Item 7.01 (Reg FD disclosure), Item 5.02 (officer departures), Item 8.01 (other)
- **Earnings events**: next earnings call (date), management guidance update, investor day, pre-announcement
- **Consensus refresh**: Visible Alpha / FactSet revision; Yahoo Finance EPS consensus shift; sell-side rating change
- **Macro series**: FRED DGS10 (10Y UST), DFF (fed funds), DXY (USD index), CPIAUCSL (CPI), UNRATE (unemployment), USREC (NBER recession dating)
- **Insider activity**: Form 4 cluster (≥3 insiders in 30 days; direction); 10b5-1 plan termination; 13D/13G activist filing
- **Regulatory**: FDA decision letter (PDUFA date); FCC docket order; FERC order on rate case; FTC Second Request status; DOJ Section 1/2 enforcement; OFAC SDN list update; BIS Entity List update; CFIUS clearance / divestiture order
- **Litigation**: PACER docket update on specific case; ITC §337 final determination; Delaware Chancery ruling; class action settlement
- **Industry trackers**: Counterpoint quarterly shipment print; Gartner forecast revision; IDC capex tracker; Yipit Data / Second Measure / Earnest consumer-spend print; Placer.ai foot traffic
- **Macro events**: FOMC date; CPI print date; NFP date; CBO scoring of legislation; SCOTUS argument date

The point is **specificity**. "Next earnings" is acceptable; "the next earnings call on date X covering Y line item" is better; "the segment GP row in 10-Q Note 17" is best.

### 2. Numerical threshold with denominator base

This is the G9 gate. "If margins recover" → fail. "If 4Q segment GM ≥18.5%" → pass. The threshold should be:

- A **specific number** (≥40 not "growth")
- Tied to a **denominator base** when applicable ("DC revenue ≥$40B on revenue ≥$X" — because margin/share/growth without a volume base can be hit in a misleading way)
- **Observable from public sources** — not "if management says so internally"

### 3. Observation window

When does the trigger expire? "By 5/30/27 (NVDA FY28Q1 print)" / "open-ended" / "if observed any time in next 12 months". An open-ended trigger lets you delay action indefinitely.

For US triggers, common window patterns:

- **Next earnings** (date-specific; ~45 days after quarter end for 10-Q; ~60-90 days for 10-K)
- **Next macro print** (CPI = monthly mid-month; NFP = first Friday; FOMC = scheduled 8x/year)
- **Regulatory milestone** (PDUFA date; HSR waiting period expiry; CFIUS 30-day timeline)
- **Index reconstitution window** (Russell late June; S&P committee discretionary; Nasdaq 100 December)
- **Earnings season clustering** (mid-Jan / mid-Apr / mid-Jul / mid-Oct +/- 2 weeks)
- **Open / event-driven** (when an executive order, Form 4 cluster, or SEC enforcement action could occur at any time)

### 4. Action mapping

What specifically do you do when the trigger hits? Not "rethink view" — *what* rethink? This must specify:

- Which scenario probabilities shift, and by how many percentage points (e.g., "base +5pp, bear -5pp")
- What the new headline becomes (target price, expected return, rating)
- What position action you take (`hold_long`, `add_long`, `trim_long_25pct`, `trim_long_50pct`, `exit_long`, `initiate_short`, `cover_short`, `flip_to_long`, etc., per `schemas/scenarios.json` `default_action` enum)
- What conviction tag the new view carries (`high_conviction`, `moderate`, `low`, `source_conditional`, `reactive`)

## Symmetric construction (both directions; mandatory)

If your view is bear, you need **bull triggers** (what would force you to abandon bear). If your view is neutral, you need both. If your view is bull, you need **bear triggers**. A bear-only trigger table on a bear thesis is asymmetric, looks like advocacy, and PM red-team will flag.

### Bear thesis → bull triggers required

> "If NVDA FY27Q1 DC revenue ≥$40B AND YoY ≥+10%, then bear thesis is broken. Action: cover any remaining short, cap further sell, re-rate to base, prepare framework for moderate-bull if FY27Q2 confirms ≥$42B."

### Bull thesis → bear triggers required

> "If hyperscaler capex (CSP-4 aggregate, tracked via Counterpoint) YoY ≤0% through CY26Q2, AND if AMD MI400 share ≥12% in any DC RFP cycle, downgrade to neutral and cut position by 30%."

### Neutral thesis → both required

> "Upgrade trigger: [...]. Downgrade trigger: [...]."

## Tiered triggers (most informative pattern)

Single-threshold triggers are coarse. Tiered triggers map signal magnitude to action magnitude. This is the preferred construction in the US skill because it gives the PM operational guidance for partial responses to partial signals.

```
| Signal level         | Threshold                                    | Action                                                       |
|----------------------|----------------------------------------------|--------------------------------------------------------------|
| Confirming bear      | DC Q1 revenue < $32B AND YoY ≤ -5%           | hold or extend short; weights bear +5pp                      |
| Mild reversal        | DC Q1 revenue $32-37B                        | cap further sell; observe FY27Q2                             |
| Strong reversal      | DC Q1 revenue $37-42B AND YoY 0-10%          | cut bear position 50%; reassess weights, rebuild base case   |
| Full reversal        | DC Q1 revenue ≥$42B AND YoY ≥10%             | exit bear; flip to neutral; prepare to add long              |
```

This is far more informative than a single trigger and is easier to operationalize at the desk level.

## Denominator gotchas (G9 specifics)

Common failures: triggers with implicit or missing denominators. Three patterns:

1. **GM without volume base**: "GM ≥75% next quarter" can be hit by collapsing low-margin SKU volume rather than expanding margin on durable mix. Fix: "GM ≥75% AND DC segment revenue ≥$X" or "GM ≥75% AND Hopper share of DC ≤70%."
2. **YoY growth without absolute base**: "Revenue YoY ≥+10%" off a depressed base may not signify strength. Fix: "Revenue YoY ≥+10% AND absolute quarter revenue ≥$Y."
3. **Margin without product mix**: "Segment GM ≥75%" can be hit by mix shift to a non-strategic high-margin SKU. Fix: "Segment GM ≥75% AND Blackwell share of DC ≥X%."
4. **Single-quarter print vs sustained trend**: "FX hit -3%" on one print can reverse next quarter. Fix: "FX-adjusted constant-currency growth ≤ -3% for 2 consecutive quarters."
5. **Form 4 noise vs cluster**: a single 10b5-1 sale on a routine schedule is noise. Fix: "Discretionary insider selling ≥3 insiders within 30 days, ≥$X aggregate, NOT under existing 10b5-1 plan."

## NVDA worked example: 6-trigger table (covers both bear-to-bull and bull-to-bear)

Current base view: Hold with source_conditional conviction (median +1.7%, range [-39.6%, +72.5%], top-3 anchors mixed S2/S3/S5).

Triggers that would shift this view:

```
| # | Signal                              | Source channel                                  | Threshold                                              | Window         | Action                                                                |
|---|-------------------------------------|-------------------------------------------------|--------------------------------------------------------|----------------|-----------------------------------------------------------------------|
| 1 | DC segment revenue (Q1)             | NVDA FY28Q1 10-Q Note 17 (Aug 2027)            | ≥$42B AND YoY ≥+10%                                    | by 8/30/27     | Bull confirm: weights base −10pp, bull +10pp; rating Hold→Buy;        |
|   |                                     |                                                 |                                                        |                | conviction source_conditional→moderate_bull; default_action add_long  |
| 2 | DC segment revenue (Q1)             | NVDA FY28Q1 10-Q Note 17                       | <$32B AND YoY ≤ -5%                                    | by 8/30/27     | Bear confirm: weights base −10pp, bear +10pp; rating Hold→Sell;       |
|   |                                     |                                                 |                                                        |                | default_action trim_long_50pct                                        |
| 3 | AMD MI400 hyperscaler share         | Counterpoint quarterly DC GPU share print + IR | ≥12% in any CSP-4 RFP cycle, confirmed by 2 sources    | open / quarterly | Strong-bear validation: weights strong_bear +5pp, bear +5pp at base   |
|   |                                     | confirmation                                    |                                                        |                | expense; trim_long_25pct; downgrade conviction to source_conditional  |
| 4 | 10Y UST yield                       | FRED DGS10 daily                                | ≥5.5% sustained 4 consecutive weeks                    | open           | Multiple compression: rebuild base P/E 35→30, bull 40→35, bear 28→24; |
|   |                                     |                                                 |                                                        |                | re-derive scenarios; headline -3% to -5%                              |
| 5 | Insider selling cluster              | Form 4 via openinsider.com / SEC EDGAR          | ≥3 NVDA insiders within 30 days, ≥$50M aggregate,       | open           | Re-examine bear bridge strong layer; weights bear +3pp, base -3pp;    |
|   |                                     |                                                 | NOT under existing 10b5-1 plans                        |                | flag for round 2 red-team                                             |
| 6 | BIS Entity List / OFAC SDN expansion | Federal Register + BIS / OFAC press release    | NVDA-specific export control re-tightening on H20 or   | open           | Strong-bear tail confirm: weights strong_bear +10pp at base expense;  |
|   |                                     |                                                 | successor SKU; revenue impact ≥$8B annualized           |                | trim_long_50pct; rating Hold→Sell; conviction high_bear               |
| 7 | Blackwell ASP / hyperscaler pushback | NVDA FY27Q4 earnings call + Visible Alpha      | NVDA-disclosed Blackwell ASP at full ramp ≥-10% vs     | by 2/28/27     | Clean-layer confirm: weights bear +5pp, base -5pp; conviction         |
|   |                                     | consensus ASP estimate                          | base assumption $40K, OR ≥+10% surprise upside         |                | source_conditional→moderate_bear (or moderate_bull on surprise);      |
|   |                                     |                                                 |                                                        |                | trim_long_25pct or add_long depending on direction                    |
```

Each trigger has all four elements (G9 verified): specific source, numerical threshold with denominator, observation window, action mapping with explicit pp shifts. The set is symmetric (#1 is bull confirm, #2 is bear confirm, #3 is bear validation, #4 is rate sensitivity both ways, #5 is signal-strength check, #6 is tail event bear, #7 is two-sided ASP test).

## Trigger types — taxonomy

For convenience, US triggers cluster into the following types. Memos should include at least 2 from each direction:

- **Earnings-print triggers** (next 10-Q / 10-K specific line items)
- **Macro triggers** (FRED series threshold crossings)
- **Industry-tracker triggers** (S5 alt-data confirms or refutes)
- **Insider / activist triggers** (Form 4 patterns, 13D filings, 10b5-1 terminations)
- **Regulatory triggers** (FDA / FCC / FERC / FTC / DOJ / BIS / OFAC milestones)
- **Litigation triggers** (PACER docket, ITC §337, Delaware Chancery rulings, class action settlements)
- **Anchor-graduation triggers** (S3→S2 anchor upgrades when next filing confirms; specifically called out for source_conditional headlines)

## Anti-patterns (these fail G9)

| Anti-pattern | Why wrong | Fix |
|---|---|---|
| "If conditions improve" | unmeasurable; what is "conditions"? | name specific signal + threshold |
| "If margins recover to historical" | which historical? what number? | "GM ≥73% (5y median) for 2 consecutive quarters" |
| Threshold without source channel | reader can't verify when it hits | name the 10-Q note, the FRED series, the agency docket |
| Single trigger covering 12 months with no gradient | binary; doesn't match how information arrives | use tiered triggers |
| Action = "reassess" or "rethink" | not actionable; what does reassess mean? | specify pp shifts, rating change, position action |
| Bear thesis with no bull triggers (or vice versa) | asymmetric; looks like advocacy | mirror the bear triggers with bull triggers |
| Denominator missing (e.g., "GM ≥X%" without volume base) | trigger can hit in misleading way | always add denominator: "GM ≥X% AND revenue ≥Y" |
| Window = "open" with no escalation milestone | trigger can sit dormant forever | even open-ended triggers should have a re-check cadence (monthly review) |
| Generic "monitor positioning" or "monitor sentiment" trigger | not falsifiable; positioning always moves | specify: "13F next-quarter top-5 holder concentration ≥X%" with denominator |
| Source = "consensus" without provider / dispersion | which consensus? | "Visible Alpha NVDA FY28E revenue consensus median above $230B with n≥30 contributors" |

## How this file ties into the rest of the rigor batch

- The triggers test the strong-layer assumptions built in `bear-bridge-us.md`.
- Triggers should map back to specific anchors from `source-stratification-us.md`; an S3 anchor's graduation trigger is the source channel that would upgrade it to S2.
- Scenario probability shifts in the "action" column flow into `five-scenario-framework-us.md` recomputation.
- Position action language (`trim_long_25pct`, etc.) aligns with `position-sizing-us.md` mandate-specific responses.
- The trigger table itself is one of the line-items in `pm-redteam-rubric-us.md` scoring.
- A0 tail-event triggers (sanctions, recession, sector reg action) reference `tail-risk-mapping-us.md`.
- For source channel specifics (FRED series IDs, EDGAR full-text URLs, agency dockets), see `us-data-sources.md`.
- Monitoring cadence for open-ended triggers is defined in `monitoring-framework-us.md`.
