# Tail-risk mapping (A0) — probability shift × valuation impact (US)

## What this solves

Every IC memo has a "risks" section. The weak version is a generic list ("regulatory risk, customer concentration, technology shift"). The institutional version answers four questions for each tail event:

1. **Trigger** — what specific, measurable event would activate the tail?
2. **Probability shift** — how does the 5-scenario distribution redistribute mass?
3. **Δ headline** — what does the post-shift expected return become?
4. **Worst- or best-case price** — if the tail crystallizes and the extreme scenario realizes, what's the price?

This is the A0 mapping. It belongs in the risks section of the memo and pre-empts the standard PM challenge "what about tail X." A0 hooks **gate G10** (anchor weighting + probability shift consistency) and informs sizing math in `position-sizing-us.md`.

## Required structure

```
| Event class                | Name                        | Trigger                                                            | Prob shift (Δpp: SB / B / Base / Bu / SBu)   | Δ headline | Worst-/Best-case |
|----------------------------|-----------------------------|--------------------------------------------------------------------|----------------------------------------------|------------|------------------|
| sanctions_export_control   | BIS adds advanced AI GPUs   | BIS Federal Register notice + Entity List update                   | +8 / +7 / -10 / -3 / -2                      | -9%        | SB $X (-42%)     |
| sector_regulatory_action   | DOJ blocks pending M&A      | DOJ complaint filed or HSR Second Request closed adverse           | +5 / +5 / -8 / -1 / -1                       | -4%        | SB $X (-42%)     |
```

Sum of probability shifts across the five-scenario row MUST equal zero per **G10** (probability conservation). Verified by `scripts/verify_weighting_sensitivity.py`.

## Required dimensions per A0 event

### 1. Event class

One of the nine enums in `schemas/memo.json` `tail_risk_a0_event.event_class`: `NBER_recession`, `Fed_rate_shock`, `sector_regulatory_action`, `sanctions_export_control`, `tariff_trade_war`, `election_political_transition`, `FX_shock`, `commodity_shock`, `idiosyncratic`. Per D12, the first six are **standing** events present in every memo; the rest are conditionally included if material.

### 2. Name

The specific event description ("BIS adds Blackwell to advanced-computing license rule," not "export control risk").

### 3. Trigger

Same discipline as `what-would-reverse-us.md` — measurable signal plus source channel. Examples:

- **NBER recession**: 10Y-2Y UST inversion >150bp for 6+ months + ISM PMI <48 for 2+ consecutive months + nonfarm payrolls negative in any month. Source: FRED `T10Y2Y`, `NAPM`, `PAYEMS`.
- **Fed rate shock**: Fed funds target moves ±200bp sustained 6 months, or 10Y UST moves ±150bp in 6 months. Source: FRED `FEDFUNDS`, `DGS10`, FOMC SEP.
- **FDA action**: CRL letter, approval with REMS, or accelerated approval revocation. Source: FDA dashboards.fda.gov + 8-K Item 8.01.
- **DOJ/FTC antitrust block**: Complaint filed in district court or HSR Second Request closed adverse. Source: justice.gov Antitrust press releases, FTC.gov enforcement actions.
- **BIS Entity List addition**: Federal Register notice + bis.doc.gov Entity List update. Verified for hallucination per `verification-protocol-us.md` cross-cutoff rule.
- **OFAC SDN addition**: Treasury OFAC daily SDN list update.
- **CFIUS forced divestiture**: Order from Committee on Foreign Investment, typically via Treasury press release + 8-K Item 8.01.
- **USTR §301 escalation**: USTR Federal Register notice; tariff schedule update.
- **§232 expansion**: Commerce notice + presidential proclamation.
- **EU CMA action**: European Commission Phase I/II decision; ec.europa.eu/competition.
- **Presidential transition**: January 20 inauguration after election; sector-specific EO within first 100 days.
- **Midterm Congress flip**: Election night results; committee chair changes affecting sector oversight.
- **State AG action**: NY DFS, CA DOJ, TX AG civil complaint.
- **Idiosyncratic — named customer loss**: Customer 8-K announcing supplier switch, or our company's 8-K Item 1.02 (termination of material agreement).
- **Idiosyncratic — ITC §337 import ban**: ITC investigation institution notice + Section 337 limited exclusion order.
- **Idiosyncratic — major patent loss**: District court ruling or PTAB IPR final written decision invalidating asserted claims.
- **Idiosyncratic — class action settlement**: 8-K Item 8.01 with material settlement amount; PACER docket confirmation.
- **Idiosyncratic — product liability ruling**: Federal MDL ruling or state court verdict above litigation reserve.

### 4. Probability shift across 5 scenarios

The core analytic content. A tail event redistributes probability mass; it does not simply "raise risk."

Discipline:
- Shifts must **sum to zero** (G10 hook). Verified.
- Magnitude reflects severity: large tails shift +5-10pp into Strong Bear directly; smaller tails shift +3-5pp into Bear with smaller Strong Bear movement.
- Symmetric structure for bull tails (mass moves into Strong Bull / Bull).
- A tail at the **base** typically draws mass away from base and bull side; a tail at **strong bear** pulls heavily from base.

Example for "BIS adds advanced AI GPUs to license rule" (bear tail):
- Strong Bear: +8pp (the world it describes)
- Bear: +7pp (export pressure deepens cycle)
- Base: -10pp (no longer the modal outcome)
- Bull: -3pp (Blackwell ramp degraded)
- Strong Bull: -2pp (sovereign-AI demand pulled forward unlikely)
- Sum: 0 ✓

### 5. Δ headline (post-tail expected return)

Recompute Σ(P_scenario × R_scenario) using the post-shift probabilities. The Δ vs current headline is the headline impact.

If current headline is +18% and post-tail is +9%, state impact as "Δ headline −9pp" or "post-tail headline +9%."

### 6. Worst- or best-case scenario value

Cite the **Strong Bear** row from the 5-scenario table for bear tails; **Strong Bull** for bull tails. This is the "max loss / max gain" reference if the tail crystallizes.

## Asymmetry: bear tails vs bull tails

A complete A0 table has both. PMs particularly value explicit bull tails because they prevent the analyst from anchoring on bear. Bull tails are usually harder to model because real upside surprises are non-linear (network effects, regulatory tailwind, share-gain acceleration). Discipline still applies: specific trigger + probability shift summing to zero + recomputed headline.

```
| Bull tail (event class)        | Name                           | Trigger                                              | Prob shift (SB / B / Base / Bu / SBu) | Δ headline | Best-case   |
|--------------------------------|--------------------------------|------------------------------------------------------|---------------------------------------|------------|-------------|
| sector_regulatory_action       | IRA §45X expansion to AI infra | Treasury rulemaking + Federal Register notice        | -2 / -3 / -10 / +7 / +8               | +9%        | SBu $X (+44%) |
| idiosyncratic                  | Sovereign-AI cluster wins      | Foreign government PR + NVDA 8-K Item 8.01           | -2 / -3 / -10 / +8 / +7               | +10%       | SBu $X (+44%) |
```

## Tail count discipline

Memos with 10+ tails listed look unfocused. Per D12 and `schemas/memo.json` `tail_risks` `minItems: 5, maxItems: 12`:

- **6 standing events** (always present, even if probability is small): NBER recession, Fed rate shock, sector regulatory action, sanctions/export control, tariff/trade war, election/political transition.
- **2-3 idiosyncratic** (per name): customer loss, ITC §337, patent loss, product liability, M&A counterparty collapse.
- **2-3 bull tails** (named, not generic).

Anything beyond moves to a "watching list" annex.

The tails should be **identifiable, specific events** — not "macroeconomic downturn" (too broad) but "NBER recession triggered by yield-curve inversion + ISM PMI <48 + payrolls negative" (concrete and verifiable per `verification-protocol-us.md`).

## Threshold for inclusion

A tail belongs in A0 if:

- **Probability of trigger ≥3%** over 12 months (low-prob is OK; noise is not).
- **Δ headline impact ≥3pp** (otherwise it's not actually moving the case).
- **Identifiable trigger source** (Federal Register, EDGAR, FRED, FDA dashboard, court docket, etc.).

If a tail fails any of these, demote to "minor risks" or annex; do not consume an A0 slot.

## Worked example — NVDA A0 (illustrative for Phase E)

```
| Event class                | Name                              | Trigger                                                                 | Prob shift (SB/B/Base/Bu/SBu)         | Δ headline | Worst-/Best-case |
|----------------------------|-----------------------------------|-------------------------------------------------------------------------|---------------------------------------|------------|------------------|
| sanctions_export_control   | BIS advanced-GPU license rule     | Federal Register notice + Entity List update; bis.doc.gov daily update | +8 / +7 / -10 / -3 / -2               | -9%        | SB $X (-42%)     |
| sector_regulatory_action   | DOJ blocks NVDA-Arm-like deal     | DOJ complaint filed in district court; justice.gov press release        | +4 / +5 / -8 / -1 / 0                 | -3%        | SB $X (-42%)     |
| idiosyncratic              | Hyperscaler capex collapse        | MSFT/GOOG/META/AMZN aggregate FY26 capex YoY < +5% confirmed in 10-Q   | +6 / +6 / -10 / -1 / -1               | -7%        | SB $X (-42%)     |
| idiosyncratic              | AMD MI400 sudden share gain       | AMD FY26Q3 10-Q discloses DC revenue +X% sequential; consensus revised  | +3 / +4 / -8 / +1 / 0                 | -3%        | SB $X (-42%)     |
| idiosyncratic              | ITC §337 patent suit (Blackwell)  | ITC investigation institution notice; limited exclusion order risk      | +2 / +3 / -6 / +1 / 0                 | -2%        | SB $X (-42%)     |
| BULL                       |                                   |                                                                          |                                       |            |                  |
| sector_regulatory_action   | DC sovereign-AI buildout (US/EU)  | US/EU government RFP + NVDA 8-K Item 8.01 contract award                | -2 / -3 / -10 / +8 / +7               | +9%        | SBu $X (+44%)    |
| idiosyncratic              | Automotive AI inflection          | NVDA 8-K Item 8.01 — Tier-1 OEM design-win >$5B TCV                     | -1 / -2 / -8 / +6 / +5                | +6%        | SBu $X (+44%)    |
```

Each row: trigger specific and source-cited, prob shift sums to zero, headline impact recomputed, worst-/best-case from the Strong Bear / Strong Bull rows of the 5-scenario table in `five-scenario-framework-us.md`.

Discipline checks:
- Five bear tails + two bull tails = 7 named A0 events (within 5-12 band).
- All triggers are observable via filings (EDGAR), Federal Register, FRED, FDA dashboard, or PACER (per `source-stratification-us.md` and `verification-protocol-us.md`).
- The bear-side Δ headline aggregate (−9 −3 −7 −3 −2 = −24pp) vs bull-side (+9 +6 = +15pp) shows the asymmetry which feeds sizing.

## How A0 connects to position sizing

The A0 table feeds `position-sizing-us.md` in two ways:

1. **Range widening**: if A0 has high-impact tails on both sides, the headline range [P10, P90] widens. Position sizing should respect the widened range — the conviction multiplier should drop one notch (e.g., 0.35× to 0.20×) per D6.
2. **Asymmetric tails**: if bear-tail aggregate Δ headline is −24pp but bull-tail aggregate is +15pp, the asymmetry argues for smaller position even if base-case return is positive. The conviction multiplier additionally halves per D6's "heavy tail exposure" rule.

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| Generic tails ("regulatory risk," "execution risk") | Not actionable; can't be triggered or falsified |
| Tail listed without prob shift | Shows no analytic content; can't compute Δ headline |
| Probability shifts that don't sum to zero | G10 fails; verified by script |
| Only bear tails on a bear thesis (or only bull on a bull) | Asymmetric framework; PM will ask for the other side |
| Δ headline not computed | Reader cannot gauge how much each tail actually matters |
| 10+ tails | Unfocused; signals the analyst doesn't know which dominate |
| Tail trigger without source channel | Cannot be operationalized into monitoring per `monitoring-framework-us.md` |
| "Recession" as a tail without NBER definition or measurable signal | Fails specificity discipline; bundle with the standing NBER_recession event with explicit FRED triggers |
| Standing-event probability shifts copied uncalibrated across all memos | A0 must be tuned per name; NVDA recession-shift differs from JPM recession-shift |
