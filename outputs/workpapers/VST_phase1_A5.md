# VST — Phase 1 / A5 Regulatory & Policy Workpaper

**Issuer:** Vistra Corp. (NYSE: VST) — CIK 0001692819
**Specialist desk:** A5 Regulatory & Policy
**As-of date:** 2026-06-09
**Business model:** US-domiciled merchant power generator + competitive retailer (TXU Energy etc.); fleet ~41 GW pre-Cogentrix, including 6,400+ MW nuclear (Comanche Peak TX; Beaver Valley PA; Davis-Besse + Perry OH), gas, and a shrinking coal book.

---

## 0. Scope confirmation — Export control / sanctions / CFIUS = N/A

VST is a US-domiciled, US-operating utility-sector issuer with no export of controlled technology, no foreign sanctioned counterparties, and no inbound foreign-acquirer transaction. Its two pending M&A deals are domestic:
- **Cogentrix** (announced 2026-01-05): ~5,500 MW US gas fleet bought from funds managed by **Quantum Capital Group** (US sponsor; Quantum had bought it from Carlyle in Aug-2024). Approvals required are **FERC FPA §203 + DOJ HSR + state** — **no CFIUS** (US buyer, US seller, US assets). Close expected mid-to-late 2026.
- **Lotus Infrastructure** (~2,600 MW, closed Nov-2025) — domestic.

**Conclusion:** BIS/OFAC/CFIUS desk is **not applicable**. The live regulatory exposures are sector-specific (FERC market design, NRC licensing, EPA air/water, RTO capacity construct, federal tax). The remainder of this workpaper addresses those. The one residual "foreign-entity" overlay is the **FEOC** restriction attached to the IRC §45U nuclear PTC (Section 5) — relevant only because it conditions a tax credit, not because VST has foreign-control exposure (it does not).

---

## 1. FERC — Large-load co-location / behind-the-meter (BTM) interconnection — THE LOAD-BEARING ITEM

### 1.1 Why it matters
Whether a datacenter can sit next to a nuclear/gas plant and buy power "behind the meter" (BTM, netting load against on-site generation and avoiding most transmission/capacity charges) versus "front of the meter" (FTM, grid-connected, paying full network + capacity costs) determines the **clearing economics** of co-located datacenter PPAs. A BTM structure that gets rejected forces re-pricing or re-routing through the grid, changing the margin captured by the generator.

### 1.2 The Talen/AWS Susquehanna anchor proceeding
- **Original rejection:** FERC, by **2-1** (Commissioners Christie + See majority; Chairman Phillips dissenting; Rosner + Chang not participating), **rejected** PJM's filed amended Interconnection Service Agreement (ISA) that would have expanded co-located BTM load at Talen's Susquehanna nuclear plant serving AWS from 300 MW to 480 MW (with a path to 960 MW). FERC found PJM failed its burden of proof under FPA §205 — no demonstrated "specific reliability concerns, novel legal issues, or other unique factors" justifying non-conforming ISA provisions. **Order date: 2024-11-01.** (Docket centered on the Susquehanna ISA; Constellation filed a related complaint, **EL25-20-000**.)
- **Market response — the workaround that actually matters:** Rather than litigate BTM, Talen and Amazon **restructured to a front-of-the-meter (FTM) retail arrangement**. Under the new structure Susquehanna delivers to the PJM grid, **Talen acts as the licensed PA retail electric supplier to AWS**, and PPL Electric provides transmission/delivery. Transition completes **Spring 2026**, concurrent with Susquehanna's refueling outage and transmission reconfiguration. Amazon committed to a 1,900 MW FTM PPA (forgoing the 480 MW cap). **This proved the FTM template is bankable** and is the single most important read-through for VST.

### 1.3 The December 18, 2025 FERC order — the current governing framework
- **Citation:** *PJM Interconnection, L.L.C.*, **193 FERC ¶ 61,217 (Dec. 18, 2025)**, Item **E-1**, lead docket **EL25-49-000** (plus AD24-11-000 technical conference; show-cause antecedent **190 FERC ¶ 61,115**).
- **Holding:** PJM's existing tariff is **unjust and unreasonable** (FPA §206) for lack of clarity/consistency on rates, terms and conditions for serving co-located load.
- **Three new transmission-service options FERC directed PJM to create:**
  1. **Interim Non-Firm Service** (bridge while NITS network upgrades are built);
  2. **Firm Contract Demand** (reserved MW, firm curtailment priority, ≥1-yr terms);
  3. **Non-Firm Contract Demand** (interruptible, 1 hour–1 month flexibility).
- **BTMG treatment — the constraint:** FERC found existing behind-the-meter generation (BTMG) netting rules **no longer just and reasonable** (cost-shifting to other customers; load not captured in resource-adequacy planning). PJM must impose a **materiality (MW) threshold** above which BTMG loads face full cost responsibility, with a **three-year transition** for existing retail BTMG arrangements.
- **Net characterization (cross-checked across ≥5 law-firm alerts):** Mayer Brown — "most concrete Commission guidance to date." K&L Gates — "a pivotal development… potentially opens new pathways… cost-effective project configurations." Baker Botts — net-withdrawals service lets generators serve adjacent load with fewer upgrades. Day Pitney — "mixed": clarity + new service tiers, but cost obligations shift onto large loads. **Synthesis: the order BLESSES front-of-the-meter / contract-demand co-location and RESTRICTS pure BTMG load-netting.** It is net-favorable to grid-connected structures, adverse to islanded BTM netting.
- **Compliance / procedural timeline (PJM, Docket EL25-49):**
  - 2026-01-20: PJM filed generator-interconnection tariff revisions + informational report on CIFP stakeholder proposals.
  - 2026-01 (Jan): PJM Board "Decisional Letter" — six principles; large load defined as ≥50 MW at a single POI; "Bring Your Own Generation" (BYOG) expedited track; reliability-backstop procurement.
  - 2026-02-16: PJM compliance filing + initial paper-hearing brief due; **PJM filed its compliance filing on 2026-02-23.**
  - 2026-03-18: responses due. 2026-04-17: replies due.
- **Current status (mid-2026):** The paper-hearing record closed mid-April 2026; PJM's compliance filing (Feb-2026) is **pending FERC action on compliance**. The substantive policy is **settled and favorable**; what remains is tariff-language compliance review. This is execution risk, not existential risk.

### 1.4 Read-through to VST's two flagship structures
- **AWS @ Comanche Peak (Texas / ERCOT, NOT PJM):** 20-yr PPA, up to ~1,200 MW initial (part of ~3,800 MW total AWS relationship at Comanche Peak), deliveries from Q4-2027. **This sits in ERCOT, outside FERC §205/§206 RTO jurisdiction over co-location** (ERCOT is intrastate, PUCT/SB6-governed — Section 4.2). The PJM co-location fight does **not** directly govern Comanche Peak. Texas SB6 (Section 4.2) is the relevant regime, and it is permissive toward co-located generation while imposing interconnection cost discipline.
- **Meta @ PJM nuclear (Perry, Davis-Besse, Beaver Valley):** Announced **2026-01-09** — 20-yr PPAs for ~2,609 MW: 1,268 MW from Perry + 908 MW from Davis-Besse (energy + capacity), plus uprate energy (213 MW Perry, 80 MW Davis-Besse, 140 MW Beaver Valley = 433 MW uprate). **This is a FRONT-OF-THE-METER, grid-connected PPA + uprate structure — it is NOT a behind-the-meter co-location deal.** Meta buys grid-delivered nuclear energy/capacity; VST retains the plants and the capacity revenue. The Dec-2025 FERC order's BTMG restrictions are therefore **largely irrelevant** to the Meta deal — and the order's blessing of FTM/contract-demand service is mildly supportive.

### 1.5 FERC co-location verdict
**Threat level: LOW-to-MODERATE, and declining.** The Dec-18-2025 order (193 FERC ¶ 61,217, EL25-49-000) resolved the central uncertainty in a **net-favorable, FTM-blessing direction**. VST's two marquee deals are structured FTM (Meta/PJM) or sit outside PJM jurisdiction (AWS/Comanche Peak/ERCOT). VST carries **far less BTM co-location risk than Talen** because it never bet the thesis on BTM netting. **Kill-criterion (see Section 8):** a FERC reversal on rehearing or D.C. Circuit appeal that re-imposes full network/capacity cost responsibility on FTM contract-demand load AND a parallel ERCOT/PUCT SB6 rule that strands Comanche Peak co-location economics — joint probability low.

---

## 2. NRC — Licenses, renewals, uprates, enforcement

| Plant | State / RTO | NRC license status | Expiration |
|---|---|---|---|
| Comanche Peak 1 & 2 | TX / ERCOT | **Subsequent license renewal APPROVED 2024-07-30** (operate to 2053). Original licenses expired 2030/2033; renewed +20 yrs. | **2050 (U1) / 2053 (U2)** |
| Perry 1 | OH / PJM | **Renewal APPROVED 2025-07-07** (60-yr operation) | **2046-11-07** |
| Davis-Besse 1 | OH / PJM | Licensed | **2037** |
| Beaver Valley 1 & 2 | PA / PJM | Licensed | **2036 (U1) / 2047 (U2)** |

- **License-renewal pipeline:** With the Meta announcement (2026-01-09), VST stated it will **begin planning subsequent license renewals at Perry, Davis-Besse, and Beaver Valley** (each another +20 yrs). Davis-Besse (2037) is the nearest-term renewal need; SLR processing typically runs 3–5 yrs, so a filing in the late-2020s is comfortably ahead of expiry. Federal Register exemption (2024-09-25) covered Beaver Valley/Davis-Besse/Perry administrative items post-Energy Harbor transfer.
- **Uprates (Meta deal):** 433 MW combined uprate (213 Perry / 80 Davis-Besse / 140 Beaver Valley) — described as the **largest corporate-customer-supported nuclear uprate package in the US**. These require NRC license-amendment approvals (typically 18–30 months each). **Approval timeline is the gating risk** to the uprate MW (~433 MW of the 2,609 MW Meta total); the base 2,176 MW of operating generation is **not** contingent on uprate approval. Uprate energy is contracted to ramp through 2034.
- **Enforcement / inspection:** **No material open enforcement findings.** Comanche Peak operated safely through 2025 — all findings/PIs **green / very-low safety significance**, no violations above minor significance (NRC public-outreach doc 26-002-IV, 2026). Davis-Besse historically had a special inspection (legacy; not current). No current Yellow/Red findings identified across the fleet. NRC oversight posture is benign.

**NRC verdict:** **LOW risk.** Comanche Peak fully renewed to 2053; Perry renewed to 2046; Davis-Besse/Beaver Valley have headroom with renewals planned. The live item is **uprate license-amendment timing**, which affects ~433 MW of incremental Meta volume, not the core thesis.

---

## 3. EPA — GHG / MATS / ELG / CCR and the coal retirement question

### 3.1 The rules and the 2025-2026 reversal
- **GHG / Section 111 (Clean Power Plan 2.0):** EPA issued a **proposed REPEAL of all §111 GHG standards** for fossil EGUs — *Repeal of Greenhouse Gas Emissions Standards for Fossil Fuel-Fired EGUs*, **90 Fed. Reg. 25752 (proposed 2025-06-17)**. EPA additionally **rescinded the Endangerment Finding on 2026-02-12**, removing the legal basis for power-sector GHG regulation. **Final repeal sent to OMB/OIRA 2026-05-14** — finalization imminent as of mid-2026.
- **MATS:** EPA proposed to **repeal the May-2024 MATS amendments** (revert to 2012 standards). Separately, an **2025-04-08 Presidential proclamation granted ~47 facilities a two-year MATS compliance exemption (2027-07-08 to 2029-07-08)** — including multiple coal units (e.g., Baldwin).
- **Effluent Limitations Guidelines (ELG):** stricter steam-electric wastewater limits scheduled to bite **2028**; subject to the same deregulatory reconsideration.
- **CCR (coal combustion residuals):** legacy surface-impoundment rule remains, but enforcement posture has softened.

### 3.2 What actually drives VST's ~4.6 GW of 2027-28 coal retirements
VST's coal retirements (Kincaid, Newton in IL; legacy Baldwin/Joppa; Miami Fort/Zimmer OH) are **predominantly ECONOMICALLY driven** — VST itself blamed the "irreparably dysfunctional MISO market." EPA rules were a *secondary accelerant*. **The current deregulatory wave REMOVES the regulatory STICK** (GHG repeal, MATS rollback, MATS exemptions), which means:
- **Forced-retirement risk is REDUCED**, not increased. EPA is no longer pushing units off the grid.
- **Counter-risk — DOE 202(c) emergency orders:** The DOE has issued **16+ FPA §202(c) "must-run" orders since May-2025, freezing ≥4.4 GW of coal retirements** (Campbell MI, Centralia WA, Craig CO, etc.). These can **DELAY** retirements VST *wants* to execute. The economics cut both ways: a 202(c) order forcing an uneconomic unit to run is a **cost/working-capital drag** (Campbell ran at a ~$180M net loss over 10 months) unless FERC approves full cost recovery to ratepayers. For VST, a 202(c) order on a unit it planned to retire is a **modest negative** (delayed decommissioning, uneconomic run-hours) partly offset by cost-recovery filings.
- EIA: US coal capacity falls 172 GW (May-2025) → 145 GW (end-2028), 58% of retirements in MISO/PJM. VST is a participant in that secular decline.

**EPA verdict:** **NET-NEUTRAL to mildly FAVORABLE.** The deregulatory pivot removes the regulatory threat that could have *forced* faster/costlier coal closures and de-risks the gas fleet's long-run GHG exposure (relevant to the Cogentrix gas acquisition). The one wildcard is **DOE 202(c)** forcing retention of units VST wants closed — a manageable cost item, not a thesis-breaker. Retirement *timing* is now more a market/economic decision than a regulatory mandate.

---

## 4. PJM & ERCOT market design — durability of capacity revenue

### 4.1 PJM capacity construct
- **Auction outcomes:** 2025/26 cleared **$269.92/MW-day** RTO (BGE $466.35; Dominion $444.26). **2026/27 BRA (Jul-2025) cleared at the FERC-approved CAP, $329.17/MW-day** RTO-wide (would have been ~$389 absent the cap). **2027/28 BRA (Dec-2025) cleared at the cap, $333.44/MW-day** (+1.3%).
- **Price cap/floor:** FERC approved (**2025-04-21**) a **cap (~$325/MW-day UCAP) and floor (~$175/MW-day)** for the 2026/27 and 2027/28 delivery years — a settlement tied to PA Gov. Shapiro. **This caps upside but FLOORS downside** — net stabilizing for VST capacity revenue. Both recent auctions cleared *at the cap*, signaling structural scarcity.
- **Reform/mitigation:** must-offer exemption for intermittent/storage/hybrids eliminated (from 2026/27); DR availability window widened to 24h (from 2027/28). **2027/28 was the first auction where the entire RTO fell short of the reliability requirement** — scarcity is real, supportive of sustained high capacity prices. PJM trimmed near-term load forecasts (-4.4 GW summer-2028, -4 GW summer-2027) on stricter datacenter vetting, modestly easing the shortfall.
- **Durability:** Capacity revenue is **structurally well-supported** — tight reserve margins + datacenter load growth (94% of PJM's 2024-30 load growth) keep prices at/near caps. Cap/floor collar expires after 2027/28; post-2028 auctions could clear **above** today's cap absent a new collar — a potential *upside*, with renewed political pressure for caps a modest offsetting risk.

### 4.2 ERCOT market design
- **PCM (Performance Credit Mechanism):** **Effectively SHELVED.** PUCT moved away from the ~$1B/yr PCM, redirecting effort to **Real-Time Co-Optimization (RTC, target ~2026-12-31)** and a **Dispatchable Reliability Reserve Service**. A reliability standard was adopted (Aug-2024); a triennial assessment launches 2026. **The reliability standard does NOT require a PCM.** Net effect for VST: ERCOT remains an **energy-and-ancillary-only, scarcity-priced (ORDC) market** — high-volatility, high-upside for VST's large ERCOT gas/coal/nuclear fleet, with no new capacity-payment overlay materializing.
- **Texas SB6 / large-load interconnection (PUCT Project 58481):** SB6 requires standardized interconnection rules for loads ≥75 MW. Draft rule **16 TAC §25.194 published 2026-03-12** (comments due 2026-04-17): **non-refundable $50,000/MW interconnection fee + 100% direct interconnection cost responsibility** on large loads, plus curtailment/demand-reduction obligations and improved load forecasting. SB6 is **permissive toward co-located generation** (Baker Botts) while disciplining speculative queue entries. ERCOT's large-load queue ~233 GW (>70% datacenters), up ~300% YoY. **Implication for VST:** SB6 imposes costs on the *datacenter*, not the generator, and legitimizes co-located structures like AWS@Comanche Peak — net supportive, with cost-allocation rules still being finalized through 2026.

**Market-design verdict:** **SUPPORTIVE / durable.** PJM capacity revenue is floored and at-cap with structural scarcity; ERCOT stays scarcity-priced with SB6 blessing co-location. No reform on the horizon materially erodes VST capacity/energy revenue.

---

## 5. Tax / policy — §45U nuclear PTC and IRA status

- **IRC §45U Zero-Emission Nuclear PTC:** Base 0.3¢/kWh, **5× to 1.5¢/kWh (≈$15/MWh) with prevailing-wage compliance**, inflation-adjusted from 2024; **phases down as a facility's gross receipts exceed 2.5¢/kWh** (reduces by 16% of the excess). Window: tax years 2024–**through 2032** (expires after 2032-12-31).
- **OBBBA (One Big Beautiful Bill Act, enacted mid-2025) treatment:** §45U **PRESERVED through 2032**, **transferability (§6418) retained**, **direct-pay (§6417) retained**. OBBBA's only change: layered on **FEOC restrictions** (no claims by "specified foreign entities"/"foreign-influenced entities") — but **NOT** the broader "effective control" / "material assistance" tests applied to renewables; the imported-nuclear-fuel prohibition was **removed**. OBBBA even **added an energy-community bonus** for nuclear communities. Cross-checked Morgan Lewis ("fared relatively well… relatively intact"), Steptoe ("remained unscathed"), Akin, Sidley.
- **Read-through to VST:** As a **US public company with no foreign control**, VST is **not impaired by FEOC** and qualifies for the full §45U benefit on Comanche Peak, Perry, Davis-Besse, Beaver Valley through 2032. The PTC acts as a **revenue floor** when power prices are low (credit highest when gross receipts low) and phases out when prices/PPAs are high — i.e., it is **counter-cyclical insurance** on the nuclear fleet. Given VST's high contracted PPA prices (AWS/Meta), much of the fleet likely sits in the phase-out band in strong years, so 45U is more a *downside hedge* than a baseline earnings driver.
- **Federal posture:** Strongly **pro-nuclear and pro-datacenter-power** (executive actions accelerating nuclear, DOE reactor support, FERC co-location facilitation). Gas is favored (GHG repeal). **The policy wind is at VST's back across nuclear and gas.**

**Tax/policy verdict:** **FAVORABLE / durable.** 45U intact, transferable, direct-pay-eligible through 2032; FEOC immaterial to VST; federal posture pro-nuclear/gas. Post-2032 sunset is a known, distant cliff (mitigated by high contracted PPA prices that would have phased the credit out anyway).

---

## 6. Securities / governance enforcement (quick check)

- **No active SEC or PCAOB enforcement action against VST identified.** FY2025 10-K (filed early 2026) and Q1-2026 earnings filed routinely; no restatement, no material-weakness disclosure surfaced. General SEC FY2025 enforcement (456 actions) is industry-wide, not VST-specific. SEC posture under current leadership is lighter-touch (Skadden/Cooley/Skadden 2026 alerts). **No governance red flags.** Routine merger-related antitrust/FERC review (Cogentrix, Lotus) is ordinary-course, not enforcement.

**Verdict:** **LOW / immaterial.**

---

## 7. Regulatory scenario tree (probabilities sum to 1.00)

| Scenario | Prob. | Specific trigger | Impact on VST EBITDA/FCF |
|---|---|---:|---|
| **Status quo (base)** | **0.50** | FERC compliance review under EL25-49 finalizes FTM/contract-demand framework as ordered; Meta/AWS deals proceed FTM; PJM cap/floor holds through 2027/28; 45U intact; EPA repeal finalizes; NRC uprates approve on ~24-mo cadence. | **Neutral-to-mildly positive.** Contracted PPA cash flows ramp as planned; capacity revenue at-cap; no incremental regulatory cost. EBITDA trajectory intact (mgmt mid-$6B+ adj. EBITDA path). |
| **Favorable** | **0.22** | Post-2027/28 PJM capacity clears **above** current cap (no new collar) on structural scarcity; FERC fully blesses contract-demand co-location enabling additional VST datacenter PPAs; SB6 finalizes permissively; faster uprate approvals. | **+5% to +15% EBITDA** vs base over 2028+ from higher uncapped capacity + incremental co-location PPAs + full 433 MW uprate. FCF accretion. |
| **Modest tightening** | **0.20** | FERC compliance order narrows contract-demand benefits / re-imposes more network-cost responsibility on co-located FTM load; PJM reinstates/extends a tighter capacity cap under political pressure; DOE 202(c) forces retention of 1–2 VST coal units at a net loss; uprate approvals slip 12–18 mo. | **-3% to -8% EBITDA/FCF.** Higher co-location transmission/capacity costs compress PPA margins at the edges; 202(c) drag ~$50–150M/unit-yr unless recovered; delayed uprate volume. Thesis intact. |
| **Severe** | **0.08** | FERC reverses on rehearing/appeal and treats FTM contract-demand co-located load as full-network NITS (kills the cost advantage) AND ERCOT/PUCT SB6 strands Comanche Peak co-location; OR a new administration/Congress repeals 45U early or re-imposes binding GHG/MATS forcing accelerated, costly coal closures; OR a Yellow/Red NRC finding takes a nuclear unit offline. | **-15% to -30% EBITDA/FCF.** Co-location PPA economics re-cut; nuclear PTC floor lost; or forced outage at a contracted nuclear unit triggers PPA replacement-power liability. Thesis materially impaired. |

*Probabilities: 0.50 + 0.22 + 0.20 + 0.08 = 1.00.*

**Skew:** Right-tailed (favorable 0.22 vs severe 0.08). The regulatory environment in mid-2026 is, on balance, **a tailwind** for VST — FERC blessed FTM co-location, EPA deregulated, 45U survived, capacity is floored, federal posture is pro-nuclear/gas.

---

## 8. Regulatory kill criteria (Tier 1 — forcing thesis exit)

A Tier-1 event is a binding, durable regulatory change that structurally impairs contracted cash flow or fleet availability. Exit (or materially cut) the thesis on any of:

1. **FERC reversal of the co-location framework** — a rehearing order or D.C. Circuit decision vacating 193 FERC ¶ 61,217 that re-imposes full network/capacity cost responsibility on front-of-the-meter contract-demand co-located load, *materially* re-pricing the Meta PJM structure. (Monitor docket **EL25-49-000** rehearing/appeal through 2026-2027.)
2. **Early repeal or gutting of IRC §45U** before 2032 (legislative), removing the nuclear PTC floor — OR a FEOC re-interpretation that ensnares VST (low, given no foreign control). (Monitor reconciliation/tax legislation.)
3. **Nuclear forced outage from a Tier-1 NRC enforcement action** (Yellow/Red finding, license suspension, or denied uprate that voids contracted Meta/AWS volume) at Comanche Peak, Perry, Davis-Besse, or Beaver Valley — triggering PPA replacement-power liability.
4. **Binding reversal of EPA deregulation** (re-finalized §111 GHG + MATS with no exemptions) under a future administration **combined with** DOE *declining* further 202(c) relief — forcing accelerated, uneconomic coal closures and stranding gas-fleet GHG economics (relevant to Cogentrix).
5. **PJM capacity-construct collapse** — FERC-ordered structural reform (e.g., move to a long-term centralized procurement that strips merchant capacity revenue) materially below current cap/floor band.
6. **ERCOT/Texas SB6 final rule** that strands co-located generation economics at Comanche Peak (e.g., prohibitive cost allocation on the generator side) — kills the AWS Comanche Peak structure.

**None of items 1–6 has triggered as of 2026-06-09.** Item 1's risk is *declining* (compliance phase, favorable order); items 2 and 4 are *low* given current federal posture; item 3 is idiosyncratic/insurable-adjacent; items 5–6 are remote.

---

## Source register (S1/S2 anchored)

**S1 — Government / regulator primary:**
- FERC, *PJM Interconnection, L.L.C.*, **193 FERC ¶ 61,217 (Dec. 18, 2025)**, Docket **EL25-49-000** (+ AD24-11-000, EL25-20-000; antecedent 190 FERC ¶ 61,115). FERC Fact Sheet & Presentation E-1 (ferc.gov).
- FERC Talen/AWS Susquehanna ISA rejection, **2024-11-01** (2-1; Christie/See maj., Phillips diss.).
- FERC capacity cap/floor approval **2025-04-21**; PJM BRA results 2026/27 ($329.17/MW-day, Jul-2025) & 2027/28 ($333.44/MW-day, Dec-2025) — pjm.com / insidelines.pjm.com.
- NRC: Comanche Peak SLR approval 2024-07-30 (to 2050/2053); Perry renewal 2025-07-07 (to 2046-11-07); Fed. Reg. 2024-09-25 exemption (Beaver Valley/Davis-Besse/Perry); NRC doc 26-002-IV (2026, Comanche Peak all-green).
- EPA, *Repeal of GHG Emissions Standards for Fossil Fuel-Fired EGUs*, **90 Fed. Reg. 25752 (2025-06-17)**; Endangerment Finding rescission 2026-02-12; MATS exemption proclamation 2025-04-08; final repeal to OMB 2026-05-14.
- DOE FPA §202(c) orders (16+ since May-2025, ≥4.4 GW frozen) — energy.gov.
- PUCT Project 58481, draft **16 TAC §25.194** published 2026-03-12 (comments 2026-04-17); ERCOT large-load updates (Mar/Apr-2026).
- IRC §45U (26 USC 45U); IRS Zero-Emission Nuclear PTC guidance; OBBBA (enacted mid-2025).
- EIA Today-in-Energy id=65744, id=67344 (coal capacity 172→145 GW by 2028).
- VST 8-Ks/press releases: Meta deal 2026-01-09; Cogentrix 2026-01-05; FY2025 10-K (filed early 2026); Q1-2026 earnings.

**S2 — Independent law-firm / trade-press cross-checks (≥2 per major claim):**
- Co-location order: Mayer Brown, K&L Gates, Baker Botts, Day Pitney, Akin Gump, Blank Rome, Beveridge & Diamond, White & Case, Nixon Peabody (all Dec-2025/Jan-2026).
- 45U/OBBBA: Morgan Lewis, Steptoe, Akin, Sidley, Pillsbury.
- SB6: Baker Botts, Perkins Coie, Greenberg Traurig.
- Trade press: Utility Dive, POWER Magazine, RTO Insider, E&E News, ANS Nuclear Newswire, World Nuclear News, DCD.

---
*Workpaper prepared by A5 Regulatory & Policy desk. Tool calls executed this session: 20 (WebSearch ×13 query-batches, WebFetch ×7, incl. direct fetches of FERC, Federal Register/EPA, EIA, ANS, and multiple law-firm primary alerts). SEC Archives HTML not fetched (403); anchored to regulator + trade-press sources per protocol.*
