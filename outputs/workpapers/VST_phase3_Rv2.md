# VST — Phase 3 Red Team v2 (R-v2): Recalibrated Bear Case + What-Would-Reverse Triggers

**Ticker:** Vistra Corp. (NYSE: VST) · **As of:** 2026-06-09 · **Spot:** ~$146.90 (6/8/26 close) [S1]
**Role:** Refreshed Red Team. Update bear with all Phase 2-3 findings, recalibrate scenario weights, produce what-would-reverse triggers with numerical denominators, honest short verdict, A0 tail map.
**Source stratification:** S1 = filings/company/regulator (PJM, EIA, FERC, IRS). S2 = primary-data aggregators / trade press citing primary / statute. S3 = sell-side. Every key claim S-tagged.
**Tool calls this pass:** 10 (WebSearch ×10, WebFetch ×0). Min-8 satisfied. Builds on Phase 2 R (16 calls) + Phase 3 A7 (17 calls).

---

## 0. WHAT CHANGED SINCE PHASE 2 R — the bear must mark to market honestly

The original R (Phase 2) was the strongest good-faith bear. Phase 2-3 verification has **eroded four of its load-bearing legs** and **confirmed three**. An honest red team marks both directions.

| R (Phase 2) claim | R-v2 update (2026-06-09) | Direction for bear |
|---|---|---|
| "PTs being cut into the decline (TD Cowen $253→$230; JPM $240→$231; MS $214→$208)" | **STALE/REVERSED.** Street mean now ~$225 (17 analysts); **MS and JPM RAISED PTs** keeping Overweight; high $320 / low $99 [S2 TIKR, Jun'26]. | **CUTS AGAINST bear** |
| "Credit de-rate; net leverage back >3.0x; IG narrative reverses" | **WEAKENED.** VST now **IG at a second agency (Fitch, after S&P)** per Q1'26 8-K [S1]. NRG's comparable gas-buy targets <3.0x; VST's own anchor ~2.78x. | **CUTS AGAINST bear** |
| "FERC co-location reversal as a risk" | **INVERTED — currently a TAILWIND.** FERC Dec-18-2025 final order DIRECTS PJM to **enable** co-located load (Firm Contract Demand service recognizing on-site gen); FERC to act on large-load ANOPR by **June 2026** [S1 FERC]. The tail is now a *reversal* of an enabling stance, not the base case. | **CUTS AGAINST bear** (re-frames the tail) |
| "2028 is ~42% open to spot (58% hedged)" | **NARROWED.** As of **May 1, 2026, 2028 is ~65% hedged → only ~35% open** (was 58%/42% in Feb'26) [S1]. The load-bearing downward variance is ~35%, not 42%, and shrinking quarterly. | **CUTS AGAINST bear (partially)** |
| "Insider selling; Form 4 = grants/withholding only (per consolidated state)" | **CORRECTED.** There IS a small **open-market** sale: Montemayor (Chief Accounting Officer) sold 4,600 sh on 6/2/26 [S2 StockTitan/GuruFocus]. 29 sells / 0 buys TTM, but tiny size; insiders own 0.92%. | **MILDLY for bear** (de minimis) |
| "Capacity pinned at FERC cap; upside truncated, −46% to floor" | **CONFIRMED.** 2027/28 BRA cleared at the **$333.44/MW-day cap**; floor $179.55. 2028/29 BRA scheduled **~July 2026** (not yet cleared) [S1 PJM]. | **CONFIRMS bear** |
| "Private market values these gas assets at 7-7.5x vs public 9.4x" | **CONFIRMED & SHARPENED.** Cogentrix = **7.25x 2027E EBITDA, ~$730/kW** [S1 VST 8-K]. NRG/LS Power = **7.5x 2026E, 50% of new-build replacement cost** [S1 NRG 8-K]. The anchor is rock-solid. | **CONFIRMS bear** |
| "§45U PTC self-erases at high power prices, cliff pulled forward" | **PARTIALLY CONFIRMED, timing softened.** OBBBA preserves §45U **in full through 2031** (the IRA-2032 cliff is 1yr forward; no 3-yr phase-down) [S2 Steptoe/CRS]. Gross-receipts mechanism intact: credit → **zero at 4.375¢/kWh (~$43.75/MWh)**. ERCOT forwards **>$50/MWh through 2028** [S2] → Comanche Peak PTC **self-erases regardless**. | **CONFIRMS the self-erase, softens the cliff timing** |
| "Margin/liquidity tail: 2× move = $3-4B call vs ~$2.8B dry powder" | **CONFIRMED as a tail, not base.** 2022 actual peak $1.89B [S1]. Covered ~2.9× for the $963M FY25 contingent; a true tail exceeds it. | **CONFIRMS the tail (low-prob)** |

**Net:** The bear is now a **de-rate / valuation-discipline case, not a deterioration case.** Estimates are intact-to-rising (2026 EBITDA $6.8-7.6B reaffirmed, ex-Cogentrix; 2027 opportunity $7.4-7.8B [S1]). Three of the four "narrative-crack" catalysts R relied on (PT cuts, credit reversal, FERC reversal) have moved against the bear. The surviving hard bear edge is the **private-vs-public multiple gap** + **cap-pinned capacity with asymmetric downside** + **PTC self-erase** — all valuation/structural, none deteriorating yet.

---

## 1. RECALIBRATED SCENARIO WEIGHTS

### A7's weights: 10 / 22 / 38 / 22 / 08 → weighted +2.6%, HOLD.

**Is A7 right to put 10% on strong_bear and 32% combined bear tail?** My honest answer after marking to market: **A7's bear tail is slightly too heavy given what de-risked this quarter, but its base is about right.** Three things argue the *left* tail deserves LESS, not more, weight than the consolidated state implied:

1. **The open book shrank** (42%→35% hedged-out), mechanically reducing the 2028 downward variance that is the single largest strong_bear driver.
2. **Second IG rating** removes the credit-accelerant that would turn a de-rate into a forced equity raise.
3. **Street + FERC momentum reversed** — PTs rising, co-location enabling. The "narrative crack" that powers a 9.0x strong_bear print is now less imminent.

**But two things keep the tail from collapsing:**
- The **2028/29 BRA (July 2026)** is a live, binary, near-dated catalyst that can still print toward the floor (−46% capacity line). This is the dominant left tail and it is **un-hedged in time** — it lands in ~4 weeks.
- The **private-market anchor is unbroken** — Cogentrix 7.25x / NRG 7.5x — so the *mechanism* for multiple reversion to 7.5x is fully intact; it is the *trigger probability* that fell, not the *impact*.

### R-v2 proposed weights

| Scenario | Target | 12mo Ret | A7 P | **R-v2 P** | Rationale for change |
|---|---|---|---|---|---|
| strong_bear | $73.80 | −49.8% | 0.10 | **0.09** | −1pp: open book narrowed; 2nd IG removes forced-raise accelerant. |
| bear | $105.60 | −28.1% | 0.22 | **0.23** | +1pp: keep the de-rate-to-private-multiple weight; mechanism intact. |
| base | $153.44 | +4.5% | 0.38 | **0.38** | Unchanged: comps cross-check still centers here; estimates reaffirmed. |
| bull | $194.70 | +32.5% | 0.22 | **0.22** | Unchanged. |
| strong_bull | $236.80 | +61.2% | 0.08 | **0.08** | Unchanged. |

**Weights sum = 1.00 (G4 PASS).**

**R-v2 weighted return** = 0.09(−49.8) + 0.23(−28.1) + 0.38(+4.5) + 0.22(+32.5) + 0.08(+61.2)
= −4.48 − 6.46 + 1.71 + 7.15 + 4.90 = **+2.82% ≈ +2.8%.**

**Verdict on weights:** A7's 10/22/38/22/08 is **defensible and within ~0.2pp of mine.** I shaved 1pp off the extreme left tail (strong_bear 0.10→0.09) and added it to bear, reflecting that the de-rate mechanism survives but the catastrophe-accelerants (credit, forced raise) have weakened. **Net effect: +2.6% → +2.8% — still squarely HOLD.** The bear does NOT earn more left-tail weight this quarter; the honest move is a slight *de-weight* of the catastrophe tail with the *de-rate* tail held intact.

---

## 2. THE SINGLE MOST IMPORTANT WHAT-WOULD-REVERSE TRIGGER (with a number)

**>> PJM 2028/29 Base Residual Auction (clears ~July 2026) prints ABOVE ~$300/MW-day on a tightening supply stack, AND the 2027 Adj EBITDA guide is set ≥$7.6B with the Cogentrix close confirmed. <<**

This is the trigger that flips me from bearish-neutral to constructive, because it simultaneously **falsifies the two surviving bear legs**: (a) a >$300 clear shows capacity is NOT a one-off cap artifact that reverts to the $179.55 floor — it confirms a structural shortage that re-rates the EBITDA base durably; and (b) a ≥$7.6B 2027 guide with Cogentrix closed shows the acquisition treadmill is converting to earned EBITDA, justifying a multiple ABOVE the 7.5x private mark. Conversely, a **<$250/MW-day** clear is the bearish-confirming mirror (see §3.1). The number that matters most in the next 30 days is the **July 2026 BRA clearing price vs. the $250 / $300 goalposts.** [S1 PJM]

---

## 3. WHAT-WOULD-REVERSE TRIGGERS (numerical denominators, split by direction)

### 3.1 Bearish-CONFIRMING (push toward bear/strong_bear, take the multiple to 7.5-9x)

| # | Trigger (numerical denominator) | Why it confirms bear | EPS/EBITDA impact |
|---|---|---|---|
| B1 | **PJM 2028/29 BRA (≈Jul 2026) clears < $250/MW-day** (vs $333.44 cap; floor $179.55) [S1] | Cap-pinning breaking toward floor; capacity-line −46% possible | −$0.6 to −$1.0B EBITDA |
| B2 | **2027 Adj EBITDA guided/realized < $7.0B** (vs $7.4-7.8B opportunity) [S1] | Acquisition-fueled growth not converting; reverts to private 7.5x | de-rate to ~$105 (bear) |
| B3 | **Net leverage > 3.2× post-Cogentrix close** (vs ~2.78× anchor; NRG targets <3.0×) [S1] | Reverses 2nd-IG narrative; credit-driven equity de-rate | multiple −1 to −2 turns |
| B4 | **Margin/collateral posting > $2.8B in any 6-month window** (vs 2022 peak $1.89B; ~$2.8B dry powder) [S1] | Forces buyback halt and/or equity raise at de-rated multiple | dilution at cyclical low |
| B5 | **Any hyperscaler cuts 2026/27 datacenter capex guide by > 10%** (base: Big-4 ~$630-725B 2026, +62-77% YoY, ~100% of OCF) [S2] | AI-power premium evaporates; reframes VST cyclical IPP | multiple → 9-11x |

### 3.2 Bullish-REVERSING (flip me constructive, support re-rate toward 14-16.5x)

| # | Trigger (numerical denominator) | Why it reverses bear | Impact |
|---|---|---|---|
| R1 | **PJM 2028/29 BRA clears > $300/MW-day on a tightening stack** [S1] | Structural shortage durable, not cap artifact; re-rates EBITDA base | base→bull bridge |
| R2 | **Comanche Peak Unit 2 (or a gas unit) signs a > $100/MWh, 15yr+ PPA** | Converts merchant optionality to contracted cash; nuclear-PPA premium | +$0.55 EPS (A7 bull driver) |
| R3 | **2027 Adj EBITDA guide ≥ $7.6B WITH Cogentrix closed & accretive (HSD)** [S1] | Treadmill → earned EBITDA; justifies multiple > 7.5x private mark | base→bull |
| R4 | **ERCOT North Hub 2028 forward sustains > $55/MWh** (currently >$50; bear kill line $45) [S2] | Refutes gas-overbuild collapse thesis (GE Vernova 100GW backlog) | supports open-book value |
| R5 | **Net leverage falls < 2.5× within 12mo of Cogentrix close** (NRG-style rapid deleverage) [S1] | Confirms IG durability; removes credit tail | supports re-rate |

**Asymmetry note on R4:** ERCOT forwards >$50/MWh is bull-supportive for *energy margin* but **bear-confirming for the PTC** — above $43.75/MWh the §45U credit (~$545M) self-erases. This is the genuine "self-cannibalizing" tension: the same high prices that support the bull energy thesis kill the PTC line. Net, at >$50/MWh the energy margin gain (~$0.7-1.0B over a full open book) dwarfs the ~$545M PTC loss, so it nets bull — but the bull cannot claim BOTH high prices AND the PTC.

---

## 4. HONEST BEAR VERDICT — symmetric or skewed? Is there a real SHORT?

### Risk/reward at $147

- Downside to bear/strong_bear: −28% / −50% (P combined 0.32 in R-v2).
- Upside to bull/strong_bull: +33% / +61% (P combined 0.30).
- Base only +4.5% (P 0.38).

**The distribution is close to SYMMETRIC in expectation (+2.8%) but FAT-TAILED on both sides** (−50% / +61%). This supports **HOLD**, not short. After this quarter's de-risking (2nd IG, rising PTs, FERC tailwind, narrowed open book), the **left tail's *probability* fell while its *impact* held** — which is the signature of a name you "don't own" rather than one you "press short."

### Is there an actual SHORT here, or just "don't own it"?

**Mostly "don't own it," with a narrow tactical short window.** Three reasons it is NOT a high-conviction outright short:
1. **Estimates are rising, not falling** — shorting into reaffirmed/raised guidance and rising Street PTs is fighting the revision tape. A de-rate short needs an estimate-cut catalyst the bear cannot yet point to.
2. **No squeeze fuel but no washout either** — SI 3.4% (11.2M sh, +20% MoM) [S2] is moderate; the risk is long-liquidation, not a short pain trade, but there is no positioning *edge* to harvest on the short.
3. **The cleanest expression already converged** — the Mirror correction showed CEG's balance sheet is cleaner (1.7× vs VST 2.78×) and the long-VST/short-CEG spread largely played out; only a small market-neutral residual remains.

**Where I WOULD get short:** a **tactical, catalyst-dated short into the July 2026 BRA**, sized small, IF (a) the stock has rallied back toward ~$170+ on AI-narrative momentum into the print, AND (b) the 2028/29 supply stack looks looser than 2027/28 (GE Vernova 100GW gas backlog [S2]). The thesis: cap-pinned capacity has truncated upside and a sub-cap clear is a binary down-gap. **Entry ~$170+, target the bear $105-110 zone, stop ~$185** (above which the AI re-rate is winning and the multiple thesis is wrong).

**Where I WOULD cover:** (a) BRA clears >$300 (R1 — structural shortage confirmed); (b) a >$100/MWh long-dated PPA signs (R2); (c) net leverage <2.5× post-Cogentrix (R5); or (d) the stock reaches $105-110 on the de-rate (take the win — below that you are betting on deterioration the estimates don't support). **At today's $147, there is no short — the risk/reward is symmetric; I am flat / "don't own."**

---

## 5. A0 TAIL MAP — low-probability / high-impact (prob × impact)

| Tail | Probability (12mo) | Impact if it hits | Prob × Impact | Notes |
|---|---|---|---|---|
| **T1. Margin/liquidity event** (2× forward move → $3-4B collateral call vs ~$2.8B dry powder) | **~8-12%** (ERCOT/PJM winter tail ~1-in-4 to 1-in-6 yr, but only the *severe* tail exceeds liquidity) | **−25 to −40%** (forced buyback halt / equity raise at cyclical-low de-rated multiple; the hedge book that protects EBITDA is the same book that generates the call) [S1] | **~ −3 to −4% EV-weighted** | Highest-conviction *structural* tail. 2nd IG + revolver capacity mitigate but do not eliminate. |
| **T2. FERC co-location REVERSAL** (a future order *restricting* behind-the-meter / firm-contract-demand co-location, reversing the Dec-2025 enabling order; FERC ANOPR action due Jun 2026) [S1] | **~10-15%** (politically/legally contested; current trajectory is *enabling*, so this is a reversal-of-trend tail) | **−15 to −25%** (kills the data-center co-location premium that underpins the bull multiple; reframes VST to grid-dependent merchant) | **~ −2 to −3% EV-weighted** | Inverted from R's framing: base case is now a *tailwind*; the tail is its reversal. |
| **T3. Hyperscaler capex cut** (any Big-4 cuts 2026/27 DC capex >10-15%; base ~$630-725B 2026 at ~100% of OCF vs 40% 10-yr norm) [S2] | **~12-18%** (capex/OCF is historically stretched; FCF turning negative at Amazon) | **−20 to −35%** (AI-power multiple premium evaporates sector-wide; VST → 9-11x cyclical IPP; correlated hit with CEG/TLN/NRG) | **~ −3 to −5% EV-weighted** | The dominant *narrative* tail; correlated, not idiosyncratic — hits the whole AI-power basket. |
| **T4. Nuclear forced outage** (Comanche Peak unit trips / extended forced outage) | **~3-5%** | **−5 to −10%** (lost generation margin + PTC + replacement power cost; bounded, insurable, single-unit) | **~ −0.3 to −0.5% EV-weighted** | Smallest tail — bounded and insurable; included for completeness. |

**A0 read:** The two tails that actually move the bear case are **T3 (hyperscaler capex cut)** and **T1 (margin event)** — combined ~ −6 to −9% EV-weighted drag, already partly embedded in the 0.32 left-tail probability mass. **T2 inverted** from R's framing (FERC is currently pro-VST). **T4 is immaterial.** None individually justifies an outright short at $147; collectively they justify *not owning* and *not pressing short into rising estimates*.

---

## 6. GATE STATUS & TOOL LOG

- **G1** (eps×mult ties): PASS (scenario targets carried from A7, internally consistent).
- **G4** (weights sum 1.00): PASS (0.09+0.23+0.38+0.22+0.08 = 1.00).
- **Three-method reconcile** (from A7, unchanged): DCF ~$107 ($95-121) | SOTP ~$132 | Comps ~$153 ($123-183); convergence band $120-155, spot inside.

**Tool-call log (10, this pass):** WebSearch — (1) VST spot Jun'26; (2) PJM 2028/29 BRA status; (3) Cogentrix 7.25x/$730kW/close 2H26; (4) OBBBA §45U 2031 + gross-receipts phasedown; (5) hyperscaler 2026 capex $630-725B; (6) VST net leverage / 2nd IG (Fitch); (7) Q1'26 EBITDA guide reaffirm + PT direction; (8) ERCOT North 2028 forwards / GE Vernova backlog; (9) NRG/LS Power 7.5x / <3.0× target; (10) FERC PJM co-location order Dec'25; + short interest/insider (folded into call 6/7 search set). **Min-8 satisfied.**

**Source levels touched:** S1 (PJM, FERC, IRS/statute, VST 8-K/10-Q, NRG 8-K), S2 (TIKR, Steptoe/CRS, trade press, aggregators), S3 (sell-side PT direction).
