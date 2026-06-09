# VST Phase 3 — Topic-Forensic Deep-Dive: 2027–2028 Open-Generation Power-Price & Capacity Sensitivity + 45U PTC Phase-Out

**Subject:** Vistra Corp. (NYSE: VST, CIK 0001692819) — the load-bearing downward consensus variance, quantified
**Desk:** Topic-Forensic (single-risk deep-dive)
**Date:** 2026-06-09 | **Price ref:** ~$146.90
**Mandate:** Build a quantified sensitivity model for the variable that decides whether out-year EBITDA is a contracted annuity (bull) or a power-price bet (bear): the ~35–42%-open 2028 generation book, the PJM capacity cap/collar trajectory, ERCOT energy margin, the power-price normalization downside, the 45U PTC anti-double-count, and the two-sided (data-center) upside.

**Source stratification.** **S1-gov** = EIA / PJM / ERCOT / FERC / IRS / statute (primary government). **S1** = SEC filings / VST IR releases / transcripts. **S4** = sell-side / consensus aggregators. **S5** = trade press / modeled. Every numeric is S-tagged inline.

---

## 0. The single sentence this workpaper defends

> Consensus carries VST revenue to **$26.8B by 2028** and net income to **~$3.9B** (S4, Simply Wall St) by extrapolating 14.7% revenue CAGR + a 17x exit P/E (S4, TIKR) — i.e., it monetizes the **open ~35–42% of the 2028 generation book at sustained cycle-peak power AND clears PJM capacity at the regulatory cap as a durable annuity.** Primary government modeling (EIA, PJM, ERCOT, FERC, IRS) shows that construction is a **power-price bet, not an annuity** — and the bet is genuinely two-tailed.

---

## 1. 2028 OPEN-BOOK EXPOSURE — how many TWh / MW ride spot, and at what implied price is consensus set?

### 1.1 Hedge ratios — the open slice (S1)

| As-of | 2026 hedged | 2027 hedged | 2028 hedged | 2028 OPEN |
|---|---|---|---|---|
| **Feb 18, 2026** (Q4'25 / 10-K) | ~100% | ~84% | **~58%** | **~42%** |
| **May 1, 2026** (Q1'26) | ~98% | ~89% | **~65%** | **~35%** |

[S1, VST Q4'25 + Q1'26 disclosures, via SEC 8-K / PRNewswire]. **KEY REFINEMENT vs Phase 2:** the 2028 open book **shrank from 42% → ~35%** between Feb and May 2026 as VST layered in hedges/PPAs. The risk window is real but narrowing — VST is actively de-risking 2028 quarter-by-quarter. I model BOTH 42% (Phase-2 anchor) and 35% (latest) so the sensitivity brackets the live number.

### 1.2 Generation volume → open TWh (S1/S5 reconciled)

- Fleet: **~41 GW operating** (~46–47 GW pro forma Cogentrix, closing H2'26) [S1/S5].
- VST does not publish a clean total-generation-TWh line in press materials (data gap). Reconstruction: ~41 GW × blended ~40–42% capacity factor (gas mid-cycle CF ~35–45%, nuclear ~93%, coal declining, solar/BESS low CF) ≈ **~145–150 TWh/yr**. Corroborant: Energy Harbor nuclear alone supplies **~33 TWh/yr to PJM** [S5, Utility Dive]; the ~6.4 GW nuclear fleet at ~93% CF ≈ ~52 TWh, leaving ~93–98 TWh from gas/coal/other — internally consistent with ~145–150 TWh total.

| Open scenario | Open % | Open TWh (on ~148 TWh) | Open MW-equiv |
|---|---|---|---|
| Phase-2 anchor (Feb'26) | 42% | **~62 TWh** | ~17 GW-equiv |
| Latest (May'26) | 35% | **~52 TWh** | ~14 GW-equiv |

### 1.3 At what implied power price is consensus 2028 EBITDA set? (S4 + modeled)

Consensus 2028 revenue **$26.8B** / net income **~$3.9B** (S4) is built off the company's **2027 Adj EBITDA "opportunity" of $7.4–7.8B (mid $7.6B)** — which **explicitly EXCLUDES Cogentrix and the new Meta/AWS PPAs** [S1, confirmed Q1'26]. Loading Cogentrix (~$0.55B+ EBITDA at the disclosed 7.25x on ~$4.0B) + ramping PPAs pushes a base 2028 figure to **~$7.8–8.3B**. The open ~52–62 TWh is the swing factor.

**Implied open-book price:** Consensus's continued-growth-into-2028 ($26.8B rev) requires the open slice to clear near **2025–2026 cycle-peak realized prices** — i.e., ERCOT North in the ~$50s+/MWh and PJM energy + cap-level capacity. EIA's base STEO 2027 ERCOT North is **$47.39/MWh** [S1-gov]; "the other major hubs … baseline average **$48/MWh**" [S1-gov, EIA id=67344]. So consensus is implicitly marking the open book at or above the **~$47–50/MWh** STEO base — and the bull PT spine ("unhedged volumes rolling into an increasingly tight market," S5) marks it **above** base. **That is the bet.**

---

## 2. PJM CAPACITY TRAJECTORY — cap / collar mechanism, floor, and uncapped clearing

### 2.1 The mechanism (S1-gov, FERC/PJM)

- **Collar = $325/MW-day cap (≈$256.75 ICAP) / $175/MW-day floor (≈$138.25 ICAP)**, originally from the **Shapiro (PA Gov.) settlement**, cap/floor indexed to the PJM reference-resource net CONE so the **realized 2027/28 UCAP cap printed $333.44 and the floor $179.55** [S1-gov, PJM 2027/28 BRA report / IMM].
- **Delivery years covered: 2026/27, 2027/28, AND (FERC-extended Apr 28 2026) 2028/29 + 2029/30** [S1-gov, PJM Inside Lines / Utility Dive]. **The collar EXPIRES AFTER 2029/30.**
- Auction calendar: **2028/29 BRA closes July 7, 2026; 2029/30 BRA closes Dec 15, 2026** [S1-gov].
- **Without the extension, the 2028/29 cap would have been ~$550/MW-day with NO floor** [S1-gov] — and PJM-internal/forecaster models put uncapped clearing at **$400–500+/MW-day in some zones** [S5, Diversegy].

### 2.2 Clearing record — at the cap, twice, AND short of reliability (S1-gov)

| Delivery year | Cleared UCAP price | vs cap | Reliability |
|---|---|---|---|
| 2026/27 | $329.17/MW-day | at cap | — |
| **2027/28** | **$333.44/MW-day** | **at cap (+1.3%)** | **cleared 6,623 MW SHORT of reliability requirement** [S1-gov, RTOInsider] |

**The decisive signal:** clearing **at the cap two years running while still 6,623 MW short of the reliability requirement** means the **uncapped equilibrium price wanted to be ABOVE $333.44.** The cap is suppressing a structurally tight market — which cuts BOTH ways: (a) downside is administratively floored at $179.55 through 2029/30 (collar protects the bear), but (b) **when the collar expires after 2029/30, an uncapped tight PJM could re-rate capacity materially higher** (the bull's 2030+ optionality).

### 2.3 Sizing VST's PJM capacity revenue — cap vs floor vs uncapped (S1)

**VST cleared 10,566 MW (UCAP) in the 2027/28 BRA at $333.44/MW-day = $1.3B capacity revenue for 2027/28** [S1, VST 8-K Dec 17 2025 / Investing.com]. This is a hard, disclosed number — the load-bearing capacity figure.

| Capacity-price regime | $/MW-day | VST PJM capacity revenue (10,566 MW × 365) | Δ vs cap |
|---|---|---|---|
| **At cap (2027/28 actual)** | $333.44 | **~$1.29B** | — |
| **At floor** | $179.55 | **~$0.69B** | **−$0.60B** |
| **Midpoint of collar** | ~$256 | ~$0.99B | −$0.30B |
| **Uncapped tight-market (≈$450)** | ~$450 | ~$1.74B | **+$0.45B** |
| **Uncapped stressed (≈$550 old cap)** | ~$550 | ~$2.12B | **+$0.83B** |

**Read:** PJM capacity revenue is a **~$1.3B annuity that East-segment EBITDA leans on heavily** — East FY25 Adj EBITDA was **$2,282M** [S1], so cap-level capacity is **~55–57% of East EBITDA** and the Q1'26 East step-up (+~56% YoY) was explicitly "higher PJM capacity revenues + Lotus" [S1]. **PJM capacity revenue grew ~32% YoY in Q2/Q3 2026** [S5]. With Cogentrix adding ~3,163 MW of PJM gas, VST's cleared UCAP rises further in 28/29–29/30 auctions — so the capacity line is BOTH bigger and more cap-sensitive going forward.

**The variance:** if the 28/29 BRA (Jul 7 2026) or 29/30 BRA (Dec 15 2026) prints toward the **$179.55 floor** rather than the cap, the downside on VST's (then larger) PJM book is **−$0.6 to −$0.9B**. Conversely, the 6,623 MW reliability shortfall says equilibrium is **above** the cap — so **base case is the collar stays binding at/near the cap through 2029/30**, with the real cliff being the **post-2029/30 expiry**, an uncertain step (could be higher uncapped OR re-imposed political limits).

---

## 3. ERCOT ENERGY MARGIN — energy-only, weather-levered, reserve-margin-pivoting

### 3.1 The setup (S1-gov)

ERCOT has **no capacity market** — Texas-segment EBITDA (FY25 **$1,834M**, carrying Comanche Peak ~2,400 MW nuclear + ~11,300 MW ERCOT gas) is **pure energy + ancillary + the new AWS PPA layer** [S1]. It is therefore the most weather/spark-spread-sensitive slice. Q1'26 Texas was explicitly "dampened by extremely mild weather in ERCOT" [S1].

### 3.2 Forward prices, heat rates, reserve margin (S1-gov + S5)

- **EIA STEO base 2027 ERCOT North = $47.39/MWh** [S1-gov, EIA id=67344 / Utility Dive].
- **High-demand (data-center) scenario 2027 = ~$84.78/MWh (+78.9%, +$37/MWh)** — **scenario-conditional, concentrated in late-summer low-wind peak hours** [S1-gov]. NOT the base case.
- **Reserve-margin trajectory (ERCOT CDR May'25, S1-gov):** summer Planning Reserve Margin **17.2% (2026) → 9.0% (2027) → −4.4% (2028)** under protocol-prescribed; conservative case **12.8% → −0.1% → −14.6%.** **Crosses NEGATIVE in 2028** — the structural tightening that powers the upside tail.
- **Counter-signal (S5, Ascend Analytics):** ERCOT **forwards are over-priced** for 2026–27 because solar+storage additions keep widening reserve margins; "forwards missed badly in 2024 and 2025 as scarcity events failed to emerge"; scarcity now "once every five or ten years." GE Vernova gas backlog jumped 55→100 GW [S5, R-bear]. This is the **downside** energy view.

### 3.3 Texas-segment EBITDA: normal vs hot summer

ERCOT energy margin is convex in weather — the bulk of annual merchant margin is earned in a handful of summer scarcity hours. Rough sensitivity on the ERCOT open energy slice (Texas ~18 GW, large open share given energy-only):
- **Hot summer / high-demand 2028 (ERCOT North → ~$60–85/MWh):** Texas-segment EBITDA up **+$0.4 to +$0.8B** vs base.
- **Mild summer + solar/storage glut (Ascend case, ERCOT North → ~$38–44/MWh):** Texas-segment EBITDA down **−$0.3 to −$0.5B** vs base.
- **Net:** Texas EBITDA carries a **~±$0.5–0.8B weather/scarcity band on 2028** — the single most volatile segment, and the one the bull's "tight market" thesis most depends on.

---

## 4. POWER-PRICE NORMALIZATION SCENARIO — the 2028 EBITDA hit ($B)

**Scenario:** open generation reprices DOWN 15–20% AND PJM capacity reverts toward the floor. Built on the ~52–62 TWh open book and the 10,566 MW (rising) PJM UCAP.

| Driver | Basis | Δ 2028 EBITDA |
|---|---|---|
| Open ~35–42% energy reprices −15–20% (~52–62 TWh × ~$10–15/MWh off peak) | EIA thin PJM upside (+4%) + Ascend ERCOT softening [S1-gov/S5] | **−$0.6 to −$0.9B** |
| PJM capacity reverts cap→floor ($333→$180 on ≥10,566 MW, rising w/ Cogentrix) | PJM floor $179.55 vs cap $333.44 [S1-gov] | **−$0.6 to −$0.9B** |
| Retail normalization ($1.622B record → ~$1.3–1.4B medium-term) | mgmt-guided [S1] | **−$0.2B** |
| 45U PTC partial fade (see §5) — only in the *higher-price* leg | §45U mechanic [S1-gov] | **−$0.0 to −$0.3B** |
| **Total downward (full bear)** | | **−$1.4 to −$2.3B** |

**Reconciliation:**
- **R-bear 2028 Adj EBITDA ~$5.3–5.7B** = base ~$7.6B − (~$0.8–1.2B capacity floor) − (~$0.7–1.0B open repricing) − $0.2B retail − $0.2–0.3B PTC ≈ **$5.5B**. ✔ My model reproduces R within rounding — the bear stacks BOTH the capacity-floor AND the open-repricing AND the PTC fade simultaneously (a coherent but full-tail outcome).
- **A-Consensus −$0.6 to −$0.9B** = the **open-energy-repricing leg ALONE** (the cleanest, most-defensible single variance), holding capacity at/near cap and NOT stacking the PTC. ✔
- **The two are consistent:** A-Consensus isolates the one S1-evidenced, directionally-clean variance (−$0.6–0.9B); R stacks the full bear (capacity floor + energy + PTC) to reach ~$5.5B. The **honest mid-bear** (capacity holds above floor but off peak + modest open repricing) lands **~−$0.6 to −$1.0B → 2028 EBITDA ~$6.6–7.2B** — matching the scenarios.json `bear` node (−$0.6B) and `strong_bear` (−$0.9B + capacity + PTC).

**Punchline:** a **full normalization is a ~$1.4–2.3B (≈18–28%) 2028 EBITDA hit**; the **defensible-single-variance** (open energy only) is **~$0.6–0.9B (≈8–12%)**. The difference is whether capacity ALSO reverts to floor — which the **6,623 MW reliability shortfall argues against through 2029/30** (collar likely stays binding near cap). So the *most-likely* bear is the **milder** −$0.6–0.9B, with the −$2B+ tail gated on the post-2029/30 collar expiry going the wrong way.

---

## 5. 45U PTC PHASE-OUT — the anti-double-count, quantified

### 5.1 The mechanic (S1-gov, IRS / 26 USC 45U / OBBBA)

- **Base credit 0.3¢/kWh** (= $3.00/MWh), inflation-adjusted; up to **1.5¢/kWh (5×) with prevailing wage** [S1-gov, IRS].
- **Gross-receipts phase-out:** credit reduced by **16% of gross receipts above $25/MWh ($0.025/kWh)**, hitting **ZERO at ~$43.75/MWh** ($25 + $3.00/0.16 = $25 + $18.75) [S1-gov, Crux / IRS]. VST's cited 2025 band: **$26.00–$44.75/MWh** [S1].
- **Sunset (OBBBA, P.L. 119-21, signed 7/4/2025):** the **House-draft graduated phase-out (20%/40%/60% in 2029–31) was STRIPPED** in the final bill; 45U runs at **FULL value through 2031, hard termination end-2031**; existing pre-Aug-2022 facilities **through 2032** with new foreign-fuel-sourcing (FEOC) restrictions [S1-gov, Steptoe / Mintz / Grant Thornton]. **No graduated fade — a cliff at end-2031/2032.**
- VST FY25: 45U ≈ **$545M ≈ 9% of FY25 Ongoing Adj EBITDA ($5,912M)**, ~95%+ margin / near-100% FCF [S1].

### 5.2 The anti-double-count (the load-bearing analytical point)

45U is a **contract-for-differences that ERASES at high power prices.** Comanche Peak (ERCOT) or the PJM nuclear fleet realizing power **above ~$43.75/MWh wipes the credit on those MWh entirely** — and EIA's STEO base already has ERCOT North at **$47.39/MWh** (already above the zero-line) [S1-gov]. Therefore:

> **The bull CANNOT simultaneously model (a) sustained peak power on the open book / a tight ERCOT (§3–4 upside) AND (b) a full $545M PTC. They are inversely correlated by statute.** High-power bull ⇒ PTC fades toward zero. Low-power bear ⇒ PTC floors the downside (partial offset). **This caps the claimed upside symmetry: peak power and full PTC cannot coexist.**

### 5.3 Quantified TV headwind

- **In the bull/high-price world:** PTC fades **−$0.2 to −$0.4B** as nuclear realized prices clear well above $43.75/MWh — a **self-imposed haircut on the bull's own EBITDA** (the anti-double-count). Net upside is the gross power gain MINUS the PTC erosion.
- **In any world, end-2031/2032:** the residual ~$545M (whatever survives the price-fade) **steps to ZERO.** At ~9.4x, $545M ≈ **~$5.1B EV / ~$15–17/share** of value that structurally vanishes [S5 modeled on R-bear]. In DCF terms a 2032 step-down 6 yrs out is **~5–7% of NPV**, partly offset (in the high-price leg) by the power prices that caused the fade.

**Net:** the PTC is **not a standalone bear thesis** — it is the **discipline device** that prevents double-counting peak power + full credit, and a **modest (~5–7% NPV / ~$15/sh) terminal-value headwind** that the Street's 17x-exit extrapolation tends to ignore.

---

## 6. THE TWO-SIDED TRUTH — is the variance genuinely two-tailed? (YES)

The same primary sources that support the downside ALSO contain a real upside tail. This is **not a one-way short.**

| Lever | DOWNSIDE evidence (S) | UPSIDE evidence (S) |
|---|---|---|
| **ERCOT energy** | Ascend: forwards over-priced, solar+storage glut, scarcity "1-in-5/10-yr" [S5] | ERCOT CDR: reserve margin **−4.4% by 2028** (−14.6% conservative); data-center load +10%/yr [S1-gov]; EIA high-demand **+79% ($85/MWh)** [S1-gov] |
| **PJM capacity** | Collar floors at $179.55; political fragility (Shapiro); cap CUT $550→$325 [S1-gov] | Cleared at cap **6,623 MW short of reliability** → uncapped equilibrium **above** cap; collar **expires after 2029/30** → potential re-rate higher [S1-gov] |
| **PJM energy** | EIA: high-demand only **+4%** ($2.60/MWh) — thin [S1-gov] | Interconnected access caps downside too; data-center load +3%/yr [S1-gov] |
| **Open-book contracting** | 42% open = power-price bet [S1] | Open shrank **42%→35% (Feb→May'26)**; ~3.8 GW PPAs ramping; Comanche U2 ~1,200 MW + gas co-loc optionality [S1] |
| **45U PTC** | Sunsets end-2031/32; fades at high prices [S1-gov] | Floors downside when prices low (offsets bear) [S1-gov] |

**The UPSIDE case (data-center-driven high-demand):** if ERCOT reserve margin goes negative in 2028 as the CDR projects and the EIA high-demand scenario realizes, the **~52–62 TWh open book reprices UP** toward $60–85/MWh and ERCOT scarcity hours fatten Texas margin. Sizing: open energy +$10–20/MWh on ~52–62 TWh ≈ **+$0.6 to +$1.2B**, PLUS ERCOT scarcity convexity (+$0.4–0.8B Texas), PLUS (if collar expires into a tight market) capacity uncapped upside (+$0.4–0.8B). **Gross 2028 upside ≈ +$1.4 to +$2.8B** — BUT **net of the PTC fade (−$0.2–0.4B)** in that same high-price world, **net upside ≈ +$1.2 to +$2.4B.**

**Verdict — TWO-TAILED, slight downward skew:**
- Downside (full normalization): **−$1.4 to −$2.3B** (2028 EBITDA → ~$5.5–6.6B).
- Upside (high-demand, net of PTC fade): **+$1.2 to +$2.4B** (2028 EBITDA → ~$9.0–10.4B).
- Defensible-single-variance downside (A-Consensus): **−$0.6 to −$0.9B** (P≈60%).
- The skew is **mildly downward** because (a) EIA's *base* (not high-demand) is the modal case and PJM upside is thin (+4%), (b) Ascend's solar/storage glut argues ERCOT forwards are too high, (c) the collar floors capacity downside but caps capacity upside through 2029/30, and (d) the PTC anti-double-count **truncates the high-price upside** (peak power ⇒ lose $545M). But the **ERCOT-negative-reserve-margin tail is real and S1-gov** — so a high-conviction SHORT is not warranted; a **below-consensus, source-conditional Hold with a wider-than-Street 2028 band** is.

---

## 7. Sensitivity summary table (2028 Adj EBITDA, $B)

| Scenario | Open energy | PJM capacity | 45U PTC | Retail | **2028 Adj EBITDA** | vs base ~$7.6–8.3B |
|---|---|---|---|---|---|---|
| **Strong-bear (full normalization)** | −15–20% | → floor $179.55 | partial fade | →$1.3B | **~$5.5B** | **−$1.4 to −$2.3B** |
| **Bear (mid)** | −10–15% | above floor, off peak | small fade | →$1.4B | **~$6.6–7.0B** | **−$0.6 to −$1.0B** |
| **A-Consensus single variance** | −10–15% | at/near cap | held | held | **~$7.0–7.4B** | **−$0.6 to −$0.9B** |
| **Base (consensus)** | flat at STEO base | at/near cap ($333) | full $545M | $1.4–1.6B | **~$7.8–8.3B** | — |
| **Bull / high-demand (net of PTC fade)** | +$10–20/MWh | cap (then uncapped 2030+) | **fades** −$0.2–0.4B | held | **~$9.0–10.4B** | **+$1.2 to +$2.4B** |

---

## 8. Tool-call ledger

WebSearch: 9 | WebFetch: 7 | **Total web research calls: 16** (≥12 minimum met). File Reads: 4 (Phase 2 AConsensus, R, Phase 1 A4, scenarios.json — not counted as web).

## 9. Source list (S-tagged, representative)

- **EIA Today in Energy id=67344** — PJM +4%/$2.60, ERCOT +79%/$37 (base $47.39 → $84.78), high-demand-only, late-summer/low-wind concentrated; NYISO/ISO-NE +5%; no 2028 published (**S1-gov**)
- **Utility Dive** — EIA ERCOT 79% writeup; VST 4.5 GW capacity / load-growth 5–6% ERCOT, 2–3% PJM (**S1-gov / S1**)
- **PJM Inside Lines / 2027/28 BRA report / IMM / RTOInsider** — cleared $333.44 at cap, floor $179.55 ($138.25 ICAP), 6,623 MW short of reliability, 134,479 MW UCAP, collar→2029/30 (**S1-gov**)
- **PJM Inside Lines / Utility Dive / Diversegy** — collar $325/$175, extended to 28/29 + 29/30, 28/29 BRA Jul 7 2026, 29/30 BRA Dec 15 2026, uncapped would-be $550 / $400–500+ zonal (**S1-gov / S5**)
- **VST 8-K Dec 17 2025 / Investing.com** — VST cleared **10,566 MW PJM 27/28 at $333.44 = $1.3B capacity revenue** (**S1**)
- **VST Q4'25 / Q1'26 releases** — hedge 100/84/58% (Feb) → 98/89/65% (May); 2027 opportunity $7.4–7.8B excl Cogentrix+PPAs; Cogentrix 7.25x; East $2,282M / Texas $1,834M / Retail $1,622M FY25; PTC ~$545M (**S1**)
- **ERCOT CDR May'25** — summer PRM 17.2/9.0/−4.4% (2026/27/28); winter 22.1/4.3%/neg; data-center-driven (**S1-gov**)
- **Ascend Analytics** — ERCOT forwards over-priced, solar+storage glut, scarcity 1-in-5/10-yr (**S5**)
- **IRS 26 USC 45U / Crux / Steptoe / Mintz / Grant Thornton** — 0.3¢/kWh base, 16% reduction above $25/MWh, zero at $43.75/MWh; OBBBA stripped graduated phase-out, hard end-2031, existing facilities 2032 + FEOC (**S1-gov**)
- **Simply Wall St / TIKR / stockanalysis** — consensus rev $23.3/25.3/26.8B, NI ~$3.9B 2028, path-to-231 = 14.7% CAGR + 17x exit (**S4**)
