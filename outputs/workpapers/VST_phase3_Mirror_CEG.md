# VST Phase 3 — Mirror Analysis Workpaper: SHORT LEG Constellation Energy (CEG)

**Subject:** Constellation Energy Corp. (NASDAQ: CEG) — verification of the SHORT leg counter to LONG VST
**Desk:** Mirror Analysis — pair-trade counter-leg rigor check
**Date:** 2026-06-09
**Mandate:** Verify CEG fundamentals at the same rigor as the VST long leg; verify/challenge A3-Peers' LONG VST / SHORT CEG (valuation-convergence) thesis.
**Tool calls:** 14 (1 Bash read of A3-Peers carry-forward + 13 WebSearch/WebFetch). Min-12 satisfied.
**Sources:** Public only. **S1** = primary filings / company IR / guidance. **S5** = aggregator / trade-press (provider + freshness inline). Every number S-tagged with date.

> **Carry-forward from A3-Peers (input, partially re-verified here):** Calpine merger CLOSED Jan 7 2026 ($16.4B equity / ~$26.6B net purchase incl. assumed debt). CEG now world's largest private-sector power producer, ~55 GW. FERC/DOJ-mandated PJM divestiture. CEG screens ~11.4x 2026E EV/EBITDA vs VST 9.4x (~2-turn / ~21% premium). This workpaper RE-DERIVES CEG numbers independently and finds several A3-Peers figures need correction (flagged below).

---

## 1. CEG Post-Calpine Financials

| Metric | Value | S-tag |
|---|---|---|
| Price | $250.25 | S5, stockanalysis Jun 9 2026 (via A3 carry-fwd) |
| Market cap | ~$89.4B (other src $89.76B Jun 3) | S5, stockanalysis Jun 9 / companiesmarketcap Jun 3 2026 |
| Shares out | ~357.1M | S5, stockanalysis Jun 9 2026 |
| LT debt (3/31/26) | **$17.5B** | **S1, CEG Q1'26 release, May 2026** |
| Cash (3/31/26) | **$0.8B** | **S1, CEG Q1'26, May 2026** |
| **Net debt** | **~$16.7B** | **S1-derived, Q1'26** |
| EV (mktcap + net debt) | **~$106–107B** | derived; corroborated S5 mlq.ai $107.6B |
| Net leverage (net debt ÷ 2026E EBITDA ~$9.7B) | **~1.7x** | derived |
| Dividend (quarterly) | $0.4265/sh ($1.706 annual); +10% YoY 2026 | S1, CEG 8-K Feb 24 / Apr 28 2026 |
| Dividend yield | ~0.68% | derived |
| Payout ratio | ~14–21% (low) | S5, fullratio/tickeron 2026 |
| Buyback authorization | **$5.0B** ($600M remaining on prior prog; ~$335M YTD) | S1, CEG Q1'26 + 8-K 2026 |
| FCF before growth (2026–27 cumulative) | **>$4.0B** | S1, CEG Q1'26 capital-allocation slide |
| FCF yield (fwd) | **~3.8%** | S5, TIKR May 2026 (A3 carry-fwd) — CONFIRMED low |

### EPS-vs-EBITDA reconciliation (CEG guides EPS, not EBITDA)
- **2026 Adjusted EPS guidance: $11.00–$12.00** (reaffirmed Q1'26). Q1'26 Adj EPS **$2.74** (vs $2.14 Q1'25); GAAP EPS $4.49. (S1, CEG Q1'26, May 2026.)
- **Base EPS growth 20%+ CAGR 2026→2029** (note: through **2029**, not "to 2029E EBITDA"). (S1, CEG 8-K 2026.)
- **EBITDA must be backed into.** Consensus quarterly path: Q4'25 $0.84B → Q1'26 **$2.02B** (+189% YoY, Calpine) → Q3'26E **$2.58B** (S5, TIKR/consensus 2026). Annualizing the post-Calpine quarterly run-rate ⇒ **~$9.5–9.7B 2026E Adj EBITDA**; TTM EBITDA ~$9.71B (S5, valueinvesting.io Jun 9). **2027E ~$10.7B** (synergies + nuclear-PPA premia + 20% EPS CAGR). These are the denominators behind the 11.4x / 10.3x multiples. **Caveat: because CEG does not guide EBITDA, the denominator is an analyst construct — the 2-turn premium is partly an artifact of comparing VST's hard EBITDA guide to a back-solved CEG number.**
- **Fwd P/E ~21x** confirmed: $250.25 ÷ ~$11.75 mid-2026 EPS = **21.3x** (S1 EPS guide + S5 price). A3 "~21x" CONFIRMED. (Note: some S5 sources cite 24–26x off lower/NTM-rolled EPS — the 21x off the $11–12 guide midpoint is the cleanest.)

**CORRECTIONS to A3-Peers:**
1. A3 net-debt note used EV−mktcap ≈ $20.8B. The **filed Q1'26 net debt is ~$16.7B** ($17.5B LT debt − $0.8B cash). EV−mktcap of ~$17–18B is consistent with this; the $20.8B figure over-states CEG leverage. **CEG net leverage is ~1.7x — materially LOWER than VST's ~2.5–3.0x.** This is the single most important correction and it CUTS AGAINST the short thesis (see §4).
2. EV is therefore ~$106–107B, not $110.2B. At ~$9.7B 2026E EBITDA ⇒ **EV/EBITDA ~11.0x** (vs A3's 11.4x). Gap to VST narrows slightly to **~1.6 turns**, not 2.0.

---

## 2. CEG Fleet

| Dimension | Value | S-tag |
|---|---|---|
| Total capacity | **~55 GW** (some PR says "60 GW" platform) | S1/S5, Jan 2026 close |
| Nuclear | **~32.4 GW nameplate (largest US)** — note: ~22 GW produced 183 TWh in 2025 at ~93% CF; the 32.4 GW is gross/owned-incl.-operated | S5, FinancialContent/10-K 2026 |
| Calpine gas | **~26 GW modern CCGT** (+ Geysers geothermal, world's largest, ~0.7 GW) | S5, FinancialContent 2026 |
| Carbon-free % | **PRE-Calpine ~90% of OUTPUT** (nuclear 68% of supply, 183 TWh zero-em in 2025). **Combined "90% carbon-free" is a CEG marketing claim measured by ENERGY OUTPUT, not capacity** — defensible only because nuclear runs ~93% CF baseload while the 26 GW gas runs as mid-merit/peaker at low capacity factor. **By CAPACITY the fleet is now ~58% nuclear / ~42% gas — far less "pure" than pre-merger.** | S1/S5 2026; analyst caveat |

### PJM divestiture status (CORRECTION to A3)
- A3 said "~3.5 GW." The **FERC/DOJ remedy is 3,546 MW of specific plants** (Bethlehem 1,134 / Hay Road 1,136 / Edge Moor 707 / York-1 569). **BUT CEG agreed Mar 2026 to sell ~4.4 GW to LS Power for ~$5.0B** — larger than the FERC minimum, covering all FERC-required + DOJ assets (predominantly PJM gas in DE/PA). **Expected to close later in 2026, subject to regulatory approval.** (S1, CEG press release Mar 2026; S5, Utility Dive / LS Power Mar 2026.)
- **Implication:** the ~$5.0B of sale proceeds is earmarked for **$3.4B deleveraging** in CEG's capital plan — i.e., CEG is actively de-risking the balance sheet, further undercutting the "stale balance-sheet premium" leg of the short thesis. Divestiture is an execution item, but a value-realizing one (gas sold near peak), not a distressed forced sale.

---

## 3. CEG Data-Center / PPA Wins vs VST

| Deal | Size / term | Status | S-tag |
|---|---|---|---|
| **Microsoft / Crane (TMI-1 restart)** | 835 MW, 20-yr | Restart H2-**2027**; ~$1.6B cost; $1B DOE loan; FERC waiver granted | S5, ANS/DCD/NucNet 2025–26 |
| **Meta / Clinton** | 1,121 MW, 20-yr | Begins Jun 2027 (post-ZEC) | S5, power-eng/ESG Dive 2025 |
| Combined CEG long-term clean agreements | **5,650+ MW contracted** | ramping into 2027 | S5, consensus/TIKR 2026 |

**Contracted-growth verdict vs VST:** VST's nuclear-PPA book (AWS/Comanche ~1,200 MW + Meta/PJM ~2,600 MW ≈ **3,800 MW**) is now **comparable in size** to CEG's ~2,000 MW of new nuclear PPAs, though CEG's 5,650+ MW total clean-agreement book (incl. C&I) is broader. **CEG's marquee headline (TMI/Microsoft) carries more "halo," but the incremental contracted MW growth is roughly a wash — VST is NOT clearly behind.** Both deliver into 2027. This neutralizes the "CEG growth-visibility premium" argument materially.

---

## 4. Premium Decomposition — WHY CEG trades ~1.6–2 turns above VST, and how much is now STALE

| Premium driver | Pre-Calpine validity | Post-Calpine status (Jun 2026) |
|---|---|---|
| **Nuclear purity** (32.4 GW carbon-free baseload) | Strong — largest US clean baseload, PTC-floored, PPA-able | **PARTLY STALE.** By capacity the fleet is now ~42% gas; the "pure nuclear" identity is diluted. Output-CF still high, but the equity story is no longer pure-play. ~0.8–1.0 turn still justified. |
| **Scale / largest producer** | Real | **Enhanced** by Calpine — genuine, but scale ≠ multiple; VST is also large. ~0.2 turn. |
| **Lower commodity beta** | Strong (nuclear baseload) | **WEAKENED.** 26 GW merchant gas adds spark-spread/gas beta CEG didn't have. Commodity-beta gap to VST has NARROWED. ~0.3 turn (was higher). |
| **Balance sheet / low leverage** | Strong (de-levered) | **MOSTLY INTACT — this is where A3 was WRONG.** Filed Q1'26 net debt $16.7B / **~1.7x net leverage** vs VST ~2.5–3.0x. CEG is STILL the cleaner balance sheet; the $5B LS Power proceeds fund $3.4B deleveraging. This premium leg is **NOT stale.** ~0.4–0.5 turn justified. |
| **Growth visibility** (20% EPS CAGR, PPA book) | Strong | **PARTLY STALE/MECHANICAL.** Headline 20% CAGR is Calpine-M&A-bought, not organic; VST's growth is organic + accretive. But contracted PPA visibility roughly a wash (§3). ~0.2–0.3 turn. |
| **Integration / divestiture overhang** | n/a | **NEW RISK, mild discount.** CEG carries the bigger ($26.6B) integration + 4.4 GW divestiture execution. But the divestiture is a signed, value-accretive sale, not distressed. −0.2 turn. |

**Net premium verdict: ~1.0–1.3 turns of the ~1.6–2.0-turn premium is STILL JUSTIFIED** (nuclear-output durability + genuinely lower leverage + scale). **Only ~0.3–0.7 turn is stale/mechanical** (commodity-beta convergence, M&A-bought growth optics, purity dilution). **This is a NARROWER mispricing than A3-Peers implied** — primarily because A3 over-stated CEG's leverage (used $20.8B not the filed $16.7B), which inflated the "stale balance-sheet premium" they were counting on.

---

## 5. Pair-Trade Verdict — LONG VST / SHORT CEG

**Spread (Jun 9 2026):** Fwd EV/EBITDA VST 9.4x vs CEG ~11.0–11.4x ⇒ **gap ~1.6–2.0 turns (~17–21%)**. Fwd P/E 13.8x vs 21.3x. FCF yield 7.2% vs 3.8% (VST +340 bps).

**Spread history / regime:** CEG 2026 YTD **−16% to −25%** vs VST **−3% to −4%** (S5, multiple Jun 2026). The convergence trade has **already substantially worked** in 2026 — CEG de-rated hard post-Calpine while VST held. Much of the "easy" convergence is behind us; entering the short now is later-cycle.

**Correlation / beta:** ~0.7–0.85 pairwise (same AI-power demand thesis, overlapping PJM/ERCOT, shared rate/factor sensitivity). A3 carry-fwd 0.7–0.85 CONFIRMED as reasonable for the sub-sector.

**Borrow cost / shortability:** CEG short interest **2.93% of float (~10.5M shares), days-to-cover ~1.6–3.0** (S5, MarketBeat May 15 / Nasdaq 2026). Low SI ⇒ **CEG is a GTC/easy-to-borrow general-collateral name; borrow cost ~0.3–0.5% (GC), not special.** Cheap to short; no squeeze risk from crowding. (Exact CB rate not retrievable — Fintel 403'd — but low SI strongly implies GC.)

**Beta-adjusted hedge ratio:** CEG ($250 px) higher absolute beta to AI-power theme; VST ($145). For a market/theme-neutral pair, weight by beta×notional. If VST beta ≈ CEG beta to the common factor (both high), use ~**$1 long VST : ~$1 short CEG dollar-neutral**, tilting **~1.1–1.2x short-CEG notional** to neutralize CEG's modestly higher AI-power beta (CEG is the higher-multiple, higher-duration name). Practical hedge: **~$1.00 VST long : ~$1.10–1.15 CEG short.**

**What makes the short leg WORK:** (a) further multiple convergence toward ~1.0–1.5 turns as Calpine-gas dilutes the nuclear-purity narrative and merchant-gas beta becomes visible; (b) a soft-AI-capex or PJM-capacity-price disappointment hits CEG's higher multiple harder (more duration); (c) integration/divestiture slippage; (d) VST's retail-hedge + 7.2% FCF yield + buyback re-rates the long.

**What BREAKS it (the asymmetric risk):** a **CEG hyperscaler-nuclear headline** (new Microsoft/Google/Meta GW PPA, an SMR JV, a faster TMI restart, or a sovereign-AI/DOE nuclear award) re-widens the premium violently — nuclear-scarcity headlines re-rate CEG's multiple in single sessions and the short would gap against you. CEG owns the scarcest asset (gigawatts of always-on carbon-free baseload) that hyperscalers are bidding up; **the short leg is structurally exposed to the strongest narrative in the sector.** This is a left-tail-fat short.

---

## 6. Honest Challenge — Is CEG actually the better LONG (invert or avoid)?

**The case CEG is the better long (and the pair should be inverted or avoided):**
1. **Cleaner balance sheet — confirmed by filings, not stale.** ~1.7x net leverage vs VST ~2.5–3.0x. A3's short thesis leaned on a "leverage gap has closed" claim that the **Q1'26 filing contradicts** ($16.7B net debt, not $20.8B). CEG is the de-levered name.
2. **MSFT/TMI halo + scarcest asset.** CEG holds the most coveted nuclear-baseload for AI; this is a re-rating engine, not a fading story.
3. **Lower payout, $5B buyback, 20% EPS CAGR, value-accretive divestiture** funding deleveraging — a high-quality compounder profile.
4. **Output still ~90% carbon-free**, nuclear PTC-floored — genuine downside protection VST's gas lacks.

**The case the pair is still LONG-VST-favorable (but modestly):** VST's ~17–21% discount is wider than the ~1.0–1.3 justified turns; VST's 7.2% FCF yield + integrated retail hedge + organic growth are under-credited; CEG carries real (if value-accretive) integration/divestiture execution.

**MIRROR VERDICT:** **The short-CEG leg is the WEAKER half of the pair and the thesis is THINNER than A3-Peers presented** — chiefly because A3 over-stated CEG leverage and under-weighted (a) the convergence that has ALREADY occurred (CEG −16/−25% YTD), (b) CEG's genuinely lower 1.7x leverage, and (c) the fat left-tail from a hyperscaler-nuclear headline. **Recommendation: the pair is acceptable as a SMALL, beta-hedged relative-value position (long VST / short CEG ~1:1.1), NOT a high-conviction short. Do not size the CEG short aggressively. The honest alternative — owning CEG outright as the higher-quality, lower-leverage, nuclear-scarcity long — is defensible, so a market-neutral pair (which profits from spread compression regardless of direction) is preferable to a directional short of CEG.** If forced to choose a single name, VST is the better VALUE but CEG is the better QUALITY; the pair monetizes value-over-quality convergence, which is a real but lower-conviction edge after the 2026 move.

---

### Source register (S-tags)
- S1: CEG Q1'26 earnings release (May 2026) — Adj EPS $2.74, GAAP $4.49, LT debt $17.5B, cash $0.8B, 2026 guide $11–12, $5B buyback, FCF >$4B 26–27, $3.4B deleverage.
- S1: CEG 8-Ks Feb 24 / Apr 28 2026 — dividend $0.4265/q, +10% 2026; 20%+ base EPS CAGR 2026–29.
- S1: CEG press release Mar 2026 — LS Power 4.4 GW / $5.0B divestiture.
- S5: stockanalysis / companiesmarketcap / mlq.ai (Jun 2026) — price, mktcap, EV.
- S5: TIKR / valueinvesting.io (May–Jun 2026) — EBITDA path, FCF yield, multiples.
- S5: ANS / DCD / NucNet / power-eng (2025–26) — Microsoft/Crane 835 MW, Meta/Clinton 1,121 MW.
- S5: MarketBeat / Nasdaq (May 2026) — short interest 2.93%, DTC 1.6–3.0.
- S5: Utility Dive / Motley Fool / heygotrade (Jun 2026) — YTD performance, CEG/VST comp.
- Carry-forward: outputs/workpapers/VST_phase2_A3Peers.md.
