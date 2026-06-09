# Vistra Corp. (VST) — Phase 1 Workpaper A4
## Capacity, Asset Map & Segment Build

**Ticker:** VST (NYSE) | **CIK:** 0001692819 | **Sector:** Utilities / Independent Power Producers (merchant IPP + competitive retail)
**As-of date:** 2026-06-09 | **Specialist:** A4 Capacity, Asset Map & Segment Build
**Primary sources:** Vistra Q1 2026 10-Q & 8-K earnings release (period end 2026-03-31), FY2025 10-K (filed 2026-02-27), FY2025 Q4 earnings release (2026-02-26), Meta/AWS/Cogentrix transaction 8-Ks and press releases, trade press (Utility Dive, Power-Eng, PowerMag, World Nuclear News, ANS). EDGAR XBRL `data.sec.gov` returned HTTP 403 to WebFetch on every attempt; SEC.gov Archives HTML and the investorroom.com PDF cache also 403-blocked WebFetch. Numeric figures were therefore sourced from the PR Newswire press-release mirror (which renders), trade-press aggregators, and the Phase 0 structured JSON (itself EDGAR-derived). This source-substitution is the principal data-quality caveat for A4 and is flagged per item below.

### Source-tier legend (S-tags)
- **S1** = primary SEC filing figure (10-Q / 10-K / 8-K exhibit), obtained via PR Newswire mirror of the company press release or Phase 0 EDGAR-derived JSON.
- **S2** = company IR / press release / investor presentation (non-SEC-form, e.g., transaction announcement).
- **S3** = reputable trade press / specialist aggregator (Utility Dive, Power-Eng, World Nuclear News, ANS, NRC).
- **S4** = third-party financial aggregator / estimate.
- **S5** = analyst-modeled / specialist-inferred (my own arithmetic or allocation; explicitly labeled).

---

## 1. Generation Asset Inventory — Master Fleet Table

### 1.1 Headline fleet size

Vistra's operating generation fleet is **~41,000 MW (≈41 GW) as of the FY2025 10-K / Q1 2026 10-Q** [S1/S3], reduced from the "~50+ GW" Phase 0 shorthand because that larger number is **pro forma for the pending Cogentrix 5,496 MW acquisition** (not yet closed) and counts gross nameplate across all owned interests. Management's own framing: "approximately 50,000 MW of capacity across the US **following** the Cogentrix acquisition" [S3, Utility Dive/Power-Eng]. The Lotus 2,600 MW gas portfolio closed during Q1 2026 and **is** in the current fleet; Cogentrix 5,496 MW is **not yet** in the fleet. I use **~41 GW operating today, ~46–47 GW pro forma Cogentrix**, reconciled in §2.

### 1.2 Master fleet table by fuel and technology (operating, current)

| Fuel / technology | Approx. MW | Share of fleet | Key assets / notes | Tag |
|---|---|---|---|---|
| **Nuclear** | **~6,448** | ~16% | 4 plants / 6 reactors: Comanche Peak (TX, 2 units ~2,400 MW), Beaver Valley (PA, 2 units, 1,872 MW), Perry (OH, 1 unit, 1,268 MW), Davis-Besse (OH, 1 unit, 908 MW). "More than 6,400 MW," 2nd-largest US competitive nuclear fleet. | S2/S3 |
| **Natural gas — CCGT (combined-cycle)** | **~18,000–20,000** | ~45–50% | Largest single bucket. ERCOT, PJM, ISO-NE, NYISO, CAISO. Includes Lotus 2,600 MW (7 plants). | S3/S5 |
| **Natural gas — peakers (CT/simple-cycle)** | included above | — | 10-K splits CCGT vs CT; A4 estimate folds into gas total pending primary-table access (data gap §8). | S5 |
| **Coal (lignite/PRB)** | **~4,578** | ~11% | Baldwin (IL), Coleto Creek (TX), Kincaid (IL), Miami Fort (OH), Newton (IL). All scheduled to retire by 2028. | S1 |
| **Solar (PV)** | **~340** | <1% | Operating utility-scale solar; part of "Vistra Zero" growth platform. | S3 |
| **Battery energy storage (BESS)** | **~1,020** | ~2.5% | 2nd-largest US storage fleet. Moss Landing (CA) was the flagship but Jan-2025 fire damaged the 400 MW/1,600 MWh Phase I — capacity partially impaired (data gap on restored MW, §8). | S3 |
| **Total operating** | **~41,000** | 100% | Pre-Cogentrix. | S1/S3 |

**Caveat (S5):** The precise CCGT-vs-peaker and per-segment fuel split lives in the FY2025 10-K "Generation Facilities" table (Item 2 Properties), which I could not fetch directly (403). The gas split above is my reconciliation of the ~41 GW total minus nuclear/coal/solar/BESS, and is the largest single estimation item in this workpaper.

### 1.3 Capacity by ISO/region (operating, current)

| ISO / market | Region label | Approx. MW | Dominant fuels | Segment | Tag |
|---|---|---|---|---|---|
| **ERCOT** | Texas | ~18,000 dispatchable | Gas (CCGT+CT ~11,300+), nuclear (Comanche Peak 2,400), coal (Coleto Creek), solar, BESS | **Texas** | S3 |
| **PJM** | Mid-Atlantic / East | ~12,000–14,000 | Nuclear (Beaver Valley, Perry, Davis-Besse ~4,048), gas, coal (Miami Fort), uprates | **East** | S3/S5 |
| **ISO-NE** | New England | ~2,000–3,000 | Gas CCGT (incl. Lotus RI asset) | **East** | S3 |
| **NYISO** | New York | ~1,000–2,000 | Gas (incl. Lotus NY asset) | **East** | S3 |
| **CAISO** | California | ~1,500–2,500 | Gas + BESS (Moss Landing) + solar | **West** | S3 |
| **MISO** | Midwest | coal-heavy | Coal (Baldwin, Kincaid, Newton IL) | **Texas/Asset Closure** mapping varies | S3 |

**Segment-to-ISO mapping (S2/S5):** Texas = ERCOT. East = PJM + ISO-NE + NYISO. West = CAISO (and MISO/other). Retail is non-geographic (a load-serving book, mostly ERCOT/PJM). Asset Closure / Sunset = retiring coal + decommissioning. This mapping is load-bearing for the segment-economics build in §3.

---

## 2. Capacity Additions vs Retirements 2026–2028 — Net Trajectory

### 2.1 Schedule

| Event | Fuel | MW | ISO | Timing | Status | Tag |
|---|---|---|---|---|---|---|
| **Lotus acquisition** | Gas (7 plants) | **+2,600** | PJM (DE/PA), ISO-NE (RI), NYISO (NY), CAISO (CA) | Closed Nov 2025 / Q1 2026 | DONE (in fleet) | S1 |
| **Cogentrix acquisition** | Gas (10 plants: 5 CCGT, CTs, 1 cogen) | **+5,496** | PJM ~3,163, ISO-NE ~1,750, ERCOT ~583 (Altura cogen) | Close mid–late 2026 (H2'26) | PENDING (FERC/DOJ) | S2/S3 |
| **Permian Basin gas peakers** | Gas (simple-cycle) | **+860** | ERCOT | ~2027–2028 | Announced/dev | S2/S3 |
| **ERCOT gas/upgrades program** | Gas | **+~1,100** (up to 2,000 MW program) | ERCOT | 2026–2028 | Dev | S2 |
| **Coleto Creek repowering** | Gas (coal-to-gas) | up to +600 | ERCOT | Post-2028 | Evaluating | S3 |
| **Solar + storage ("Vistra Zero")** | Solar/BESS | growth to ~5,000 MW renewables+storage (7,300 MW Zero incl. Comanche Peak) | ERCOT/CAISO/PJM | rolling | Dev pipeline | S3 |
| **Nuclear uprates (Meta-linked)** | Nuclear | **+433** | PJM (Perry, Davis-Besse, Beaver Valley) | phased 2031→2034 | Planned | S2/S3 |
| **Coal retirements** | Coal | **−4,578** | MISO/ERCOT/PJM | by 2028 (2027–2028) | EPA-driven | S1 |

### 2.2 Net capacity trajectory (S5 reconciliation)

| Period | Starting fleet | + Additions | − Retirements | Ending fleet | Net change |
|---|---|---|---|---|---|
| **YE2025 (post-Lotus)** | — | — | — | **~41,000 MW** | baseline |
| **2026** | 41,000 | +5,496 (Cogentrix, H2) + solar/storage trickle | 0 (coal retires later) | **~46,500–47,000** | **+~5.5 GW** |
| **2027** | ~46,500 | +860 (Permian) + solar/storage | begin coal retirements | **~45,000–47,000** | roughly flat to up |
| **2028** | ~46,000 | +ERCOT gas + solar/storage | complete −4,578 coal | **~43,000–45,000** | **−1 to −2 GW vs 2026 peak** |

**Net read:** The fleet **grows ~+5.5 GW in 2026** (Cogentrix dominates), then the **−4.6 GW coal cliff in 2027–2028 roughly offsets** organic gas/solar/storage additions, leaving the **2028 fleet modestly above the YE2025 starting point** but **below the 2026 post-Cogentrix peak**. Critically, the mix **decarbonizes and shifts toward dispatchable gas + nuclear + storage** — the retiring coal is the lowest-margin, highest-ARO/closure-cost capacity, while additions are higher-value PJM/ERCOT gas and contracted nuclear. **Net capacity is not the right scorecard; net contracted EBITDA-quality capacity is** — and that trajectory is strongly positive.

---

## 3. Segment Economics — Revenue / EBITDA Build

### 3.1 Segment Adjusted EBITDA (Ongoing Operations basis)

| Segment | Q1 2026A ($M) | FY2025A ($M) | Carries what | Tag |
|---|---|---|---|---|
| **Texas (ERCOT)** | **586** | **1,834** | Comanche Peak nuclear, ERCOT gas, AWS Comanche Peak PPA (Q4'27 start) | S1 |
| **East (PJM/ISO-NE/NYISO)** | **801** | **2,282** | Beaver Valley/Perry/Davis-Besse nuclear, **Meta PJM nuclear PPA**, PJM capacity revenue | S1 |
| **West (CAISO)** | **56** | **244** | CAISO gas, Moss Landing BESS, solar | S1 |
| **Retail** | **68** | **1,622** | ~5M-customer competitive retail book; natural hedge to generation | S1 |
| **Corporate & Other** | **(17)** | **(70)** | overhead, interest-adjacent items | S1 |
| **Asset Closure / Sunset** | **(19)** | **(74)** | retiring coal, decommissioning, ARO | S1 |
| **Ongoing Operations total** | **1,494** | **5,912** | record Q1; FY25 record | S1 |

### 3.2 Which segment drives EBITDA, and quarterly vs full-year shape

- **East is the largest and fastest-growing EBITDA segment** — Q1'26 $801M (+~56% YoY), FY25 $2,282M. It carries **three of the four nuclear plants (the PJM Ohio/PA fleet, ~4,048 MW)**, the **Meta >2,600 MW PPA**, and **PJM capacity revenue** (capacity auctions cleared at FERC offer caps $329–333/MW-day for 2026/27 and 2027/28). The Q1'26 jump was explicitly driven by **higher PJM capacity revenues + the Lotus contribution**.
- **Texas is #2** — Q1'26 $586M (+~19% YoY), FY25 $1,834M. Carries **Comanche Peak nuclear (~2,400 MW)** and the **AWS 1,200 MW Comanche Peak PPA** (deliveries begin Q4 2027). ERCOT is energy-only (no capacity market), so Texas EBITDA is more weather/spark-spread sensitive — Q1'26 was dampened by "extremely mild weather in ERCOT."
- **Retail is large on a full-year basis ($1,622M FY25) but small in Q1 ($68M)** — highly seasonal (summer-weighted ERCOT load) and acts as the **integrated hedge** that smooths merchant generation volatility (~100% of 2026 generation hedged, partly via the retail book).
- **West is small** ($56M Q1 / $244M FY25) and was impaired by the Moss Landing fire.
- **Generation reporting view (S2):** the company also reports a combined "Generation" Adjusted EBITDA of **$1.426B in Q1'26** (= Texas + East + West essentially), vs Retail $68M.

### 3.3 Nuclear and data-center PPA segment allocation (key forensic mapping)

| Item | Segment | Tag |
|---|---|---|
| **Comanche Peak nuclear (TX)** | **Texas** | S2 |
| **Beaver Valley / Perry / Davis-Besse nuclear (PJM)** | **East** | S2 |
| **AWS 1,200 MW PPA** (Comanche Peak) | **Texas** | S2 |
| **Meta >2,609 MW PPA** (PJM nuclear) | **East** | S2 |
| **PJM capacity revenue** | **East** | S1 |
| **Nuclear PTC (45U) benefit** | spread Texas + East (follows the plants) | S5 |

**So: East carries the Meta nuclear PPA + PJM capacity + 3 nuclear plants; Texas carries the AWS PPA + Comanche Peak.** Both data-center PPA streams live in the generation segments, not Retail.

### 3.4 Capacity vs energy revenue split

The PR/10-Q do not publish a clean consolidated capacity-vs-energy revenue split (**data gap, §8**). Qualitatively (S1/S5): **East has the meaningful capacity-revenue component** (PJM Base Residual Auction at FERC caps; the explicit Q1'26 EBITDA driver). **Texas (ERCOT) has essentially zero capacity revenue** (energy-only market) — its revenue is energy + ancillary + the new contracted PPA layer. Retail revenue is customer energy sales. This asymmetry is why East's EBITDA stepped up with the 2025/26–2027/28 PJM auction clears while Texas is more weather-driven.

---

## 4. Capex Schedule 2026–2028 — Growth vs Maintenance vs ARO; Funding

### 4.1 Capex figures

| Metric | FY2025A ($M) | FY2026E guide ($M) | Q1 2026A ($M) | Tag |
|---|---|---|---|---|
| **Total capex** | **2,752** | — | **883** (incl. nuclear fuel + LTSA prepays) | S1 |
| — Maintenance capex | **1,348** | **~1,536** (the guided "base" capex line) | — | S1 |
| — Growth/development capex | **~1,126** (implied; solar/storage/gas dev) | (growth funded above the $1,536 base) | — | S1/S5 |
| Insurance recoveries (Martin Lake) | (111) offset | — | — | S1 |

**Reading the guidance line (S5):** The "$1,536M 2026 capex" figure in the guidance table is the **maintenance/base run-rate**; it is consistent with the FCFbG definition ("**before Growth**"). **Growth capex — solar/storage build, ERCOT/Permian gas additions, nuclear-uprate spend — sits below the FCFbG line** and is funded separately. FY2025 total capex of $2,752M shows the growth layer roughly doubled the maintenance base.

### 4.2 2026–2028 capex composition (S5 framework)

| Bucket | 2026 | 2027 | 2028 | Notes |
|---|---|---|---|---|
| **Maintenance** (incl. nuclear fuel, LTSA) | ~$1.5B/yr | ~$1.5B | ~$1.5B | Base, in FCFbG |
| **Growth — gas (Permian 860 MW, ERCOT program)** | rising | peak | peak | Above FCFbG |
| **Growth — solar + storage (Vistra Zero)** | ongoing | ongoing | ongoing | Above FCFbG |
| **Growth — nuclear uprates (433 MW, Meta-linked)** | early | building | building | Spend 2026→2031+, output 2031–2034 |
| **Coal retirement / ARO / closure** | low | rising | peak | Asset Closure segment; ARO accretion + decommissioning |
| **Cogentrix acquisition** | **~$4B** ($2.3B cash + 5M shares @ ~$185 + assumed debt) | — | — | M&A, not capex; funded with cash + equity + debt |

### 4.3 Funding (debt vs FCF)

- **FCF engine:** FY2026 **Adjusted FCFbG guide $3.925–4.725B** (midpoint ~$4.3B) on **EBITDA $6.8–7.6B** — a ~60% EBITDA-to-FCFbG conversion, strong for the sector. This funds maintenance capex, the dividend (~$0.91/sh), and most of the buyback.
- **Growth capex + Cogentrix** are funded by a **mix of retained FCF, incremental debt, and (for Cogentrix) ~5M new shares**. Gross debt ~$19.9B / net debt ~$19.3B; net leverage ~3x 2026E EBITDA. **Investment-grade at two agencies as of Q1 2026** materially lowers the marginal cost of the debt-funded growth.
- **Capital return competes with growth:** ~$6.3B buybacks since Nov 2021, ~$1.5B remaining authorization targeted by end-2027. Management is explicitly balancing buyback vs growth-capex vs deleveraging.

---

## 5. Long-Term PPA Book — Contracted vs Merchant Mix

### 5.1 The hyperscaler PPAs

| PPA | Counterparty | MW | Plant(s) / ISO | Term | Delivery start | Full ramp | Tag |
|---|---|---|---|---|---|---|---|
| **AWS** | Amazon Web Services (IG) | **1,200** | Comanche Peak nuclear (TX, ERCOT) | 20 yr (+ up to 20 yr option) | **Q4 2027** | **2032** | S2/S3 |
| **Meta (operating)** | Meta Platforms (IG) | **2,176** | Perry + Davis-Besse (OH, PJM) | 20 yr | **late 2026** (portion); full operating by **YE2027** | — | S2/S3 |
| **Meta (uprate)** | Meta Platforms | **433** | Perry, Davis-Besse, Beaver Valley uprates | 20 yr | **2031** (portion) | **YE2034** | S2/S3 |
| **Meta total** | | **2,609** | PJM nuclear | 20 yr | | | S2 |
| **Combined nuclear PPAs** | | **~3,809 MW** | TX + PJM nuclear | 20 yr | 2026–2034 ramp | | S5 |

### 5.2 Contracted vs merchant mix — two distinct lenses

**Lens A — long-dated PPA contracting of nuclear (the "secular de-risk" story, S5):** ~3,809 MW of long-term hyperscaler PPAs against a ~6,448 MW nuclear fleet ⇒ **~59% of nuclear capacity is (or will be) under 20-year IG-counterparty PPAs once fully ramped (2027 for AWS+Meta operating; 2034 for uprates).** Today (mid-2026) almost none of it is yet delivering — AWS starts Q4'27, Meta operating starts late-2026. So the **realized** long-term-contracted share is still small in 2026 and ramps hard 2027–2028. On a **total fleet** basis (~41 GW operating), ~3.8 GW of 20-yr PPAs ≈ **~9% of the fleet under long-dated structural contracts**, rising as fleet additions are also contracted.

**Lens B — near-term commercial hedging (the cash-flow-visibility story, S1):**
| Year | % of expected generation hedged | Tag |
|---|---|---|
| **2026** | **~100%** (as of Feb 18, 2026) | S1 |
| **2027** | **~89%** (as of May 1, 2026; was ~84% in Feb) | S1 |
| **2028** | **~58%** (as of Feb 2026) | S1 |

**Synthesis:** On a 1–2 year horizon, VST is **almost fully hedged (≈100% 2026, ~89% 2027)** through a combination of the retail book, wholesale forward sales, and the hyperscaler PPAs — so near-term EBITDA is highly visible and **only ~2028+ is materially open to spot.** The hyperscaler PPAs are the *structural, multi-decade* layer (≈9% of fleet / ≈59% of nuclear once ramped); the rolling hedge program is the *tactical* layer that delivers the near-term ~100%/~89% coverage. The bear concern is that 2028+ open length leaves EBITDA exposed to power/gas/capacity mean-reversion.

---

## 6. Nuclear Fleet Detail (with forensic handoff)

| Plant | State | ISO | Reactors | Net MW | NRC license expiry | Tag |
|---|---|---|---|---|---|---|
| **Comanche Peak 1** | TX | ERCOT | 1 | ~1,200 | **2050** | S3 |
| **Comanche Peak 2** | TX | ERCOT | 1 | ~1,200 | **2053** | S3 |
| **Beaver Valley 1** | PA | PJM | 1 | ~940 | **2036** | S3 |
| **Beaver Valley 2** | PA | PJM | 1 | ~932 | **2047** | S3 |
| **Perry 1** | OH | PJM | 1 | **1,268** | **2046** (20-yr renewal granted 2025) | S3 |
| **Davis-Besse 1** | OH | PJM | 1 | **908** | **2037** | S3 |
| **Total** | | | **6** | **~6,448** | | S2/S3 |

- **License status (S3):** All six reactors now hold NRC approval to operate up to 60 years; Perry's 2025 renewal (through 2046) was the last of the fleet to be renewed. Comanche Peak is the longest-dated (2050/2053), which underpins the 20-year AWS PPA tenor.
- **Capacity factors (S1/S3):** Vistra cited **100% nuclear fleet commercial availability during winter storm Fern** (Q1'26). Annual fleet capacity factor is not separately published per plant in the press materials (**data gap, §8**); the US competitive nuclear fleet typically runs ~92–95% CF. Single-unit forced-outage concentration is a real EBITDA tail (a large unit ≈ 1,000–1,200 MW).
- **Decommissioning trust funding (FORENSIC HANDOFF — partial, S2/S5):** The Energy Harbor acquisition brought **~$1,997M of nuclear decommissioning trust assets** reclassified to Investments on acquisition. The **consolidated FY2025 decommissioning-trust fair value (Comanche Peak + Energy Harbor combined) could not be confirmed** from accessible sources — it sits in the 10-K balance sheet / Note (Investments / AROs), which 403-blocked. **HANDOFF TO FORENSIC (B-series):** (i) confirm total NDT fair value and funded-status vs ARO; (ii) trust income flows through "other" and is *excluded* from Adjusted EBITDA (a non-GAAP add-back) — quantify; (iii) ARO accretion sits in Asset Closure / nuclear; (iv) check for any FERC/state trust-adequacy shortfall given license extensions to 2046–2053 push out decommissioning dates favorably.

---

## 7. Tax-Credit Overlay — Nuclear PTC (45U) and IRA Credits

| Item | Figure | Tag |
|---|---|---|
| **Nuclear PTC (45U) in FY2025 Ongoing Adj EBITDA** | **~$545M** | S1/S3 |
| 45U mechanism | Base 0.3¢/kWh; up to **1.5¢/kWh (5x)** with prevailing-wage; credit available for power generated/sold after 12/31/2023, **expires 12/31/2032** | S3 |
| 45U phase-out band | Phases out as gross receipts rise; 2025 band cited **$26.00–$44.75/MWh** (2024: $25.00–$43.75/MWh) — i.e., the credit shrinks when realized nuclear prices are high | S3 |
| FY2024 impact | PTC first recorded Q4 2024; contributed to the +$1,516M YoY FY24 Ongoing EBITDA step-up (alongside Energy Harbor + MTM) | S1 |

**Analysis (S5):** The **$545M 45U PTC is ~9% of FY2025 Ongoing Adjusted EBITDA ($5,912M)** — a large, federally-backed, after-tax-cash-accretive support specific to the ~6.4 GW nuclear fleet, and a key reason the Energy Harbor nuclear acquisition was accretive. **Two tensions:** (1) 45U is a **price-floor-style** credit — it is *largest when power prices are low* and *phases toward zero when realized nuclear revenue is high* (e.g., when AWS/Meta PPAs + tight PJM lift prices), so it partially **offsets** merchant downside but **fades** in the bull-price case; net it dampens EBITDA volatility. (2) 45U **sunsets 12/31/2032**, inside the 20-year horizon of the AWS/Meta PPAs — post-2032 the PPAs must stand on contracted economics without the credit. Other IRA credits (45Q CCS, ITC/PTC on solar+storage build) are smaller and tied to the growth pipeline. Corporate AMT (CAMT, 15% on adjusted book income) is relevant given the large non-cash hedge MTM swings — a forensic cross-check item.

---

## 8. Biggest Data Gaps (for handoff)

1. **Per-segment, per-fuel MW table (10-K Item 2 Properties)** — could not fetch the primary table (403 on data.sec.gov, SEC Archives HTML, and investorroom PDF cache via WebFetch). The **CCGT-vs-peaker split and exact Texas/East/West fuel allocation are S5 estimates.** *Highest-priority gap.*
2. **Nuclear decommissioning trust total fair value (FY2025)** — only the Energy Harbor reclass (~$1,997M) is confirmed; consolidated NDT balance and ARO funded-status unconfirmed. Forensic handoff opened.
3. **Consolidated capacity-revenue vs energy-revenue split** — not published cleanly; qualitatively East-weighted.
4. **Per-plant nuclear capacity factors** (only fleet "100% availability during Fern" confirmed).
5. **Growth-capex schedule by project/year 2026–2028** — only FY25 actual ($2,752M total / $1,348M maint) and FY26 base ($1,536M) confirmed; project-level growth phasing is S5.
6. **Moss Landing post-fire restored MW** — BESS fleet ~1,020 MW headline may overstate currently-available storage.

**Tool-call count: 18** (1 ToolSearch load + 17 WebSearch/WebFetch research calls; data.sec.gov XBRL JSON, SEC Archives HTML, and investorroom PDFs all returned HTTP 403 to WebFetch, so primary figures were sourced via PR Newswire mirrors of company releases, trade press, and the EDGAR-derived Phase 0 JSON).

---

### Source list
- Vistra Q1 2026 results press release (PR Newswire 302765015) and 10-Q/8-K [S1]
- Vistra FY2025 Q4 results press release (PR Newswire 302697962) and FY2025 10-K [S1]
- Vistra–Meta agreement press release (PR Newswire 302656941) and 8-K [S2]
- Vistra–AWS Comanche Peak PPA (Power-Eng, World Nuclear News, company 8-K) [S2/S3]
- Vistra–Cogentrix acquisition (PowerMag, Utility Dive, Power-Eng, company release) [S2/S3]
- NRC license / Perry renewal / Comanche Peak-2053 (Enerdata, World Nuclear News, Vistra IR) [S3]
- 45U nuclear PTC (IRS, Crux Climate, Vistra disclosures) [S3]
- Fleet/ISO breakdown (Utility Dive, Power-Eng, NaturalGasIntel, Wikipedia cross-check) [S3]
- Phase 0 structured JSON (EDGAR XBRL companyfacts-derived) [S1, internal]
