# Vistra Corp. (VST) — Phase 2 Workpaper A6
## Channel Pulse + Revision Velocity

**Ticker:** VST (NYSE) | **CIK:** 0001692819 | **Sector:** Utilities / Independent Power Producers (merchant IPP + competitive retail)
**As-of date:** 2026-06-09 | **Specialist:** A6 Channel Pulse + Revision Velocity
**Current price (S4):** ~$145–147 (52-wk range $132.66–$219.82; trading ~10% off 52-wk low, ~33% off 52-wk high) [MarketBeat/stockanalysis, 2026-06-08/09]
**Next earnings (S3):** Thursday, **2026-08-06**, before market open [MarketBeat earnings page]

### Source-tier legend (S-tags)
- **S1** = primary SEC filing / company guidance (10-Q/10-K/8-K, press release).
- **S2** = company IR / investor presentation.
- **S3** = reputable trade press / specialist aggregator (Benzinga newsfeed, StockTitan, Nasdaq/Zacks).
- **S4** = third-party financial aggregator / consensus screen (MarketBeat, TipRanks, stockanalysis, Simply Wall St, MarketScreener).
- **S5** = analyst-modeled / specialist-inferred (my own arithmetic; explicitly labeled).

> **Data-quality caveat:** Yahoo Finance `/analysis` (EPS Trend table), Zacks PT page, and TipRanks `/forecast` all returned 403/503/bot-block to WebFetch. EPS-trend deltas below are therefore reconstructed from Simply Wall St's dated revision snapshots, Zacks 30-day % readouts surfaced in search, and dated Benzinga PT actions — all S4, cross-checked across ≥3 aggregators. This is the principal A6 data-quality limitation and is flagged per item.

---

# PART B — REVISION VELOCITY (load-bearing, feeds `revision_velocity` block, gate G17)

## B.1 Coverage breadth — `n_analysts`

Analyst count varies by aggregator scope (PT-issuing vs ratings-only vs estimate-contributing):

| Source | n_analysts | Date | Tag |
|---|---|---|---|
| MarketBeat | **16** | 2026-06-08 | S4 |
| stockanalysis.com | **19** | 2026-05-28 | S4 |
| Simply Wall St (estimate contributors) | **13** | 2026-06 | S4 |
| TIKR | 17 (14 Buy, 4 Outperform, 1 Underperform, 1 Sell — overlapping labels) | 2026-06 | S4 |
| TipRanks (PT-issuing subset) | 11 | 2026-06 | S4 |

**A6 working figure: `n_analysts ≈ 16–19` (use 17 as the central estimate).** [S4/S5] The 13 at Simply Wall St is the *estimate-contributing* panel (narrower); 16 (MarketBeat) and 19 (stockanalysis) are the *ratings/PT* panels. For the structured memo I carry **17 ± 2**.

**Rating mix (MarketBeat, 2026-06-08) [S4]:** 2 Strong Buy, 13 Buy, 1 Hold, 0 Sell → consensus **Buy / Strong Buy**. No sell ratings. Sentiment is intact and bullish despite the price action.

## B.2 Current consensus estimates — FY1 (2026) and FY2 (2027)

| Metric | FY1 (2026) consensus | FY2 (2027) consensus | Tag |
|---|---|---|---|
| **Adj EBITDA** | **~$7.3B** (vs company guidance $6.8–7.6B, midpoint $7.2B) | **~$7.6B** (co. "2027 midpoint opportunity" $7.4–7.8B *ex*-Cogentrix/PPAs) | S4/S1 |
| **EPS (GAAP/adj blended)** | **~$8.6–9.4** (stockanalysis $8.59; Simply Wall St $9.40; MarketBeat fwd implies ~$9.30) → **central ~$9.0** | **~$10.96** (stockanalysis); MarketBeat "$11.18" forward | S4 |
| Revenue | ~$23.3B (+31% y/y) | ~$25.3B (+9% y/y) | S4 |

**Reconciliation note (S5):** The EPS spread ($8.59–$9.40) reflects GAAP-vs-adjusted and timing of when each aggregator last refreshed. The **directionally important fact** is that the FY26 EPS figure has been *moving up*, not down (see B.3). EBITDA consensus (~$7.3B) sits slightly above the $7.2B guidance midpoint — Street is modeling the **upper half** of the guide. Company reaffirmed 2026 Adj EBITDA $6.8–7.6B and FCFbG $3.925–4.725B at Q1 (2026-05-07) [S1].

## B.3 Revision deltas — FY1 EBITDA & FY1 EPS (1mo / 3mo / 6mo)

| Window | FY1 EPS consensus delta | FY1 EBITDA consensus delta | Direction | Tag |
|---|---|---|---|---|
| **1-month** | **+5.1%** (Zacks current-FY readout; one near-term-quarter metric showed −3.3%/−3.6% on the *Q2* line) | flat-to-up (guidance reaffirmed; no cut) | **RISING (annual) / mixed at quarter level** | S4 |
| **3-month** | **EPS $9.01 → $9.40 = +4.3%** (Simply Wall St dated revision, snap to ~2026-05-17) | flat-to-up | **RISING** | S4 |
| **6-month** | Up (FY26 estimate has trended higher off Q3'25 guidance initiation + Q1'26 $2.87 beat vs $1.32) | Up (reaffirmed guide; Lotus + PJM capacity accretion baked in) | **RISING** | S4/S5 |

**Key reconciliation of the apparent contradiction:** Zacks shows the *current-quarter (Q2'26)* EPS line revised **−3.3% / −3.6% over 30 days**, while the *full-year FY26* line is revised **+5.1%** and FY27 **+0.3%**. This is a **mix/timing shift between quarters, not a deterioration of the annual number.** The 98% 2026 hedge coverage [S1] caps full-year variance; quarter-to-quarter shuffling is noise. **Net read: FY1 annual EBITDA and EPS estimates are FLAT-TO-RISING on all three lookbacks. Estimates are NOT being cut.**

## B.4 Breadth — analysts raising vs cutting (last 1–3 months)

| Direction | Count (last ~3mo) | Firms (dated, S3/S4) |
|---|---|---|
| **PT RAISED / EST UP** | ~5–6 | Scotiabank $287→$293 (1/12), UBS $230→$233 (1/12), BMO $230→$244 (1/12), JPM $239→$240 (3/19), Morgan Stanley $208→$212 (5/21), Jefferies upgrade Hold→Buy $191→$203 (2/10) |
| **PT CUT / EST DOWN** | ~4 | BofA $231→$218 (1/12), Wells Fargo $236→$234 (2/27), JPM $240→$231 (4/30), TD Cowen $253→$230 (5/4) |

**Up/down ratio (PT actions, ~3mo): roughly 5–6 up : 4 down ≈ 1.3–1.5 : 1 — modestly skewed UP.** [S5 from S3/S4 dated actions] On *estimates* (not PT), the breadth is cleaner UP: FY26 EPS consensus rose (B.3) and no firm cut its rating. **Zero downgrades; one upgrade (Jefferies).** Breadth is constructive.

## B.5 PT revision velocity — the specific cuts and raises

| Date | Firm | Action | Old PT | New PT | Rating | Tag |
|---|---|---|---|---|---|---|
| 2026-01-12 | Scotiabank | raise | $287 | **$293** | Sector Outperform | S3 |
| 2026-01-12 | UBS | raise | $230 | **$233** | Buy | S3 |
| 2026-01-12 | BMO Capital | raise | $230 | **$244** | Outperform | S3 |
| 2026-01-12 | BofA | **cut** | $231 | **$218** | Buy | S3 |
| 2026-02-10 | Jefferies | **upgrade** | $191 | **$203** | Hold→**Buy** | S3 |
| 2026-02-27 | Wells Fargo | trim | $236 | **$234** | Overweight | S3 |
| 2026-03-19 | JPMorgan | raise | $239 | **$240** | Overweight | S3 |
| **2026-04-30** | **JPMorgan** | **cut** | **$240** | **$231** | Overweight | S3 |
| **2026-05-04** | **TD Cowen** | **cut** | **$253** | **$230** | Buy | S3 |
| **2026-05-21** | **Morgan Stanley** | **RAISE** | **$208** | **$212** | Overweight | S3 |

**Phase 1 correction (important):** Phase 1 logged "Morgan Stanley $212 on 5/21" as a cut. **It was a RAISE ($208→$212)** per Benzinga/aggregators [S3]. MS remains the *lowest* PT in the cluster (~$212) but the 5/21 action was directionally *positive*. JPM ($240→$231, 4/30) and TD Cowen ($253→$230, 5/4) cuts are confirmed.

**Net PT trend 3mo (S5):** Consensus PT drifted from a Jan high cluster (~$233–293) toward a tighter **~$225–234 mean** (MarketBeat $233.33; TipRanks ~$229.50; stockanalysis $225.29; TIKR $225). Net **modestly DOWN (~3–5%)** over 3mo — driven by the two May cuts (JPM/Cowen) partly offset by the MS raise and Jan raises. **Crucially, every revised PT ($212–293) sits 40–80% ABOVE the ~$146 spot.** The PT compression is small relative to the stock's drawdown — the gap *widened*, it did not close. That is the de-rate signature.

## B.6 Pre-print drift & historical 1-day post-earnings move

**Earnings history (MarketBeat) [S4]:**

| Date | Qtr | EPS est | EPS act | Surprise | 1-day move (OptionSlam) [S4] |
|---|---|---|---|---|---|
| 2026-05-07 | Q1'26 | $1.32 | **$2.87** | +$1.55 (big beat) | **−2.74%** (intraday high +6.38%, faded) |
| 2026-02-26 | Q4'25 | $2.45 | $2.18 | −$0.27 (miss) | **+0.83%** (intraday low −6.41%) |
| 2025-11-07 | Q3'25 | $1.78 | $1.75 | −$0.03 (in-line/slt miss) | ~flat (Q3'25 narrowed/initiated guide; stock +13.6% in weeks after) |
| 2025-08-07 | Q2'25 | $1.63 | $1.01 | −$0.62 (miss) | — |

**OptionSlam EVR rating 2.6/10** = relatively **low** post-earnings realized volatility. [S4]

**Pre-print drift read (S5):** The notable pattern is **beats that don't stick and misses that don't hurt** — Q1'26 was a +$1.55 EPS beat that *closed down 2.74%* after spiking +6.4% intraday (sold the rip), while the Q4'25 *miss* closed *up* 0.83%. This tells us: (1) the stock trades on the **secular power-demand/PPA narrative and PT/rate backdrop, not the quarterly print**; (2) hedge-locked EBITDA (98% '26) makes quarters low-information; (3) into the **Aug-6 print**, the setup is a **de-risked beat-and-fade** profile — low implied move, narrative-driven. Drift into recent prints has been *negative-to-flat* (stock grinding toward 52-wk lows through Q1–Q2'26 regardless of fundamentals).

## B.7 Peer comparison — VST vs CEG / NRG / TLN

| Name | YTD'26 stock | FY26 EPS revision | PT trend 3mo | Verdict | Tag |
|---|---|---|---|---|---|
| **VST** | ~−2% to flat YTD, near 52-wk low | **UP** ($9.01→$9.40) | mean ~$233→~$225 (modest cut) | **De-rate, estimates intact/up** | S4 |
| **CEG** | **−14% YTD** | EPS guide reaffirmed $11.00–12.00; Q1 beat ($2.74 vs $2.53); consensus ~$11.63 (steady-to-up); *revenue* trimmed $36.4B→$32.6B | blended PT ~$330→~$293 (bigger cut) | **De-rate, estimates intact** | S4 |
| **NRG** | mixed | consensus steady | mean ~$202 (wide $96–354) | de-rate-ish | S4 |
| **TLN** | mixed | EPS '26 ~$22.84 (steady) | JPM $448→$421 (cut) | de-rate, estimates intact | S4 |

**Peer read (S5):** This is a **sector-wide IPP de-rate, not a VST-specific deterioration.** CEG is *worse* on price (−14% YTD) with similar dynamics (EPS guide held/raised, PTs trimmed, revenue lines cut on lower power-curve/contract assumptions). TLN and NRG show the same shape (PT trims, estimates holding). **VST's estimate revisions are NEUTRAL-to-BETTER than peers** — VST's FY26 EPS was revised *up* (CEG's revenue line was cut, though EPS held). The whole group re-rated lower on **macro/rate + power-curve/long-term P/E compression**, not on company-specific estimate cuts. VST screens as **middle-of-pack to slightly-better** on revision quality.

## B.8 VERDICT — De-rate vs Deterioration

**VERDICT: This is MULTIPLE COMPRESSION with INTACT-to-RISING estimates (a DE-RATE), NOT estimate deterioration.** Phase 1's hypothesis is **VERIFIED.** [S5, high confidence]

Evidence stack:
1. **Estimates UP, not down:** FY26 EPS consensus $9.01→$9.40 (+4.3%, ~3mo); Zacks FY26 +5.1% / FY27 +0.3% (30d); EBITDA consensus ~$7.3B *above* guide midpoint. [S4]
2. **Guidance reaffirmed** at Q1'26 (2026-05-07): Adj EBITDA $6.8–7.6B, FCFbG $3.925–4.725B; 98%/89%/65% hedged '26/'27/'28 — fundamentals locked. [S1]
3. **Stock −33% off highs to ~$146 while PTs only trimmed ~3–5%** to ~$225–233 mean → the **price-to-PT gap widened to +50–80%**. Multiple compressed; numerators (estimates) did not.
4. **Zero downgrades, one upgrade (Jefferies), no sell ratings**, up/down PT breadth ~1.3–1.5:1 skewed up.
5. **Peer-confirmed:** CEG (−14% YTD), TLN, NRG show the same de-rate with held estimates → sector/macro driven (rate backdrop, power-curve & long-term P/E assumption resets, AI-power-trade unwind), not VST idiosyncratic.

**Implication for the memo:** The bear case here must rest on **multiple/de-rate continuation** (the right multiple for hedged merchant-IPP EBITDA) or on a **future** estimate cut (power-curve roll-down, co-lo/FERC adverse, Cogentrix synergy miss) — **not on observable current estimate momentum, which is positive.** The market is voting on the *multiple*, the analysts on the *numbers*, and the two disagree.

---

# PART A — MONITORING DASHBOARD

## A.1 Catalyst calendar (next 6–18 months)

| Date / window | Catalyst | Why it matters | Tag |
|---|---|---|---|
| **2026-08-06** | **Q2'26 earnings** (BMO) | Guidance check; Cogentrix close timing; PPA milestones; hedge roll | S3 |
| **mid-Aug 2026** | **Q2'26 13F filing deadline** (~45d after 6/30) | Institutional positioning; smart-money flows in/out of the IPP de-rate | S4 |
| **H2'26 (mid-to-late)** | **Cogentrix close** (+5,496 MW gas; FERC §203 + DOJ HSR + state) | +~$X EBITDA accretion *not* in guidance/consensus → upside revision catalyst | S2/S3 |
| **2026 (pending)** | **FERC EL25-49-000 co-location compliance** (PJM compliance filing 2026-02-23; paper-hearing record closed mid-Apr'26) | FERC action on PJM compliance language; FTM-blessing framework; read-through to Meta/PJM | S3 |
| **2026 H2 / 2027** | **PJM Base Residual Auction (BRA) capacity clears** | Capacity-price print drives East-segment EBITDA; prior auctions cleared at/near cap | S3 |
| **2026-11 (est.)** | **Q3'26 earnings** | 2027 guidance initiation likely | S3 |
| **Q4'27 onward** | **AWS @ Comanche Peak** deliveries begin (~1,200 MW initial of ~3,800 MW) | Revenue inflection; ERCOT/SB6 regime | S2 |
| **2027-08 + phased** | **Meta PJM nuclear PPAs** start (~2,609 MW; uprates 2031→2034, +433 MW) | Long-dated contracted nuclear cash flows | S2 |
| **2027-02 (est.)** | **Q4'26 / FY26 earnings + FY27 guide** | Full reset of forward numbers | S3 |

**Top 3 by impact (S5):** (1) **Cogentrix close (H2'26)** — only catalyst that mechanically *raises* consensus (deal excluded from guidance); (2) **Q2'26 earnings 2026-08-06** — near-term narrative/positioning reset + Cogentrix timing; (3) **PJM capacity auction clear** — direct East-segment EBITDA driver and the swing factor in the power-curve thesis.

## A.2 Trigger structure (what to watch / thresholds)

| Tier | Trigger | Threshold / action level | Tag |
|---|---|---|---|
| **Tier 1 (thesis-altering)** | Cogentrix deal break / FERC §203 denial | Any DOJ/FERC block → cut consensus, re-rate | S5 |
| | FERC EL25-49 adverse reversal re-imposing full network/capacity cost on FTM contract-demand load | Order on rehearing/appeal against FTM | S5 |
| | FY26 Adj EBITDA guide CUT below $6.8B floor | Any downward guide revision → deterioration confirmed | S1 |
| | Major PPA (Meta/AWS) termination or repricing | Any cancellation | S2 |
| **Tier 2 (estimate-moving)** | PJM capacity auction clears materially below prior | >10% below expected capacity price | S5 |
| | Power-curve (ERCOT/PJM forward) roll-down | >10% move in forward heat-rate-adjusted spark | S5 |
| | ≥3 analysts cut FY26/FY27 EPS estimates in <30d | Breadth flips to net-down | S4 |
| | Net PT trend turns down >10% in 3mo | PT compression accelerates toward spot | S4 |
| **Tier 3 (sentiment/flow)** | 13F net selling by top-10 holders | >5% aggregate reduction | S4 |
| | Cluster of insider Form 4 *open-market sales* | See A.4 | S4 |
| | Single-day move >2× EVR (2.6) on no news | Narrative/flow break | S4 |

## A.3 13F filing-window dates

- **Q1'26 13F** (Mar-31 quarter): filed by **2026-05-15** (45d) — already on file; informs current holder base. [S4]
- **Q2'26 13F** (Jun-30 quarter): due **~2026-08-14/15** — **NEXT window**, coincides with the 8/6 earnings → richest read on whether institutions are buying the de-rate or de-grossing the IPP/AI-power trade. [S4]
- VST has **~1,388 institutional 13D/G/F filers / ~290M shares**; top holders Vanguard, BlackRock, FMR, State Street, JPMorgan. [S4]

## A.4 Form 4 alert thresholds

- **Alert on:** any **open-market SALE** (transaction code **S**, not code F tax-withholding or A grant) by NEO/director, especially CEO/CFO; aggregate insider sales **>$5M in 30d** or **>2 insiders selling in one week**.
- **Recent activity (S3/S4):** routine equity *grants* and **code-F tax-withholding** (Helm, Hudson, EVP grants, director 2,008-sh grant) — **not** open-market sales; **no negative signal** in recent Form 4 flow.
- **Filing latency:** Form 4 due **2 business days** after the transaction — near-real-time monitoring feasible via secform4.com / StockTitan feeds.

---

## Tool-call ledger
14 web calls: WebSearch ×8 (VST consensus/PT, May PT cuts, revision trend, Q1 reaction, TipRanks breadth, current price, CEG/NRG/TLN peers, CEG Q1, 13F/Form 4) + WebFetch ×6 (MarketBeat forecast, Benzinga ratings, stockanalysis forecast, MarketBeat earnings, OptionSlam, TIKR, Simply Wall St) — net 14 successful (3 additional fetches 403/503-blocked: Yahoo /analysis, Zacks PT, TipRanks /forecast; substituted per caveat).

## Key numeric summary (all S4 unless noted)
- n_analysts: **16–19 (central 17)**
- FY26 Adj EBITDA consensus: **~$7.3B**; FY27: **~$7.6B**
- FY26 EPS consensus: **~$9.0 (range $8.59–9.40)**; FY27: **~$10.96**
- FY26 EPS revision: **+4.3% / 3mo ($9.01→$9.40); +5.1% / 30d (Zacks)** — RISING
- Breadth: **~5–6 up : 4 down PT actions; 1 upgrade, 0 downgrades, 0 sells**
- Net PT 3mo: **modestly down (~3–5%) to ~$225–233 mean** — still +50–80% over ~$146 spot
- Next earnings: **2026-08-06**; next 13F window: **~2026-08-14**
- **VERDICT: DE-RATE (multiple compression, intact-to-rising estimates) — Phase 1 verified**
