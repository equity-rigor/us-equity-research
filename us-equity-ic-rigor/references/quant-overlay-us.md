# Quant overlay — Barra factor tags, capacity, edge decay, correlation, stress (US)

## Honest framing — what these numbers are, and what they are not (v0.3.0)

**The factor tags in this section are directional estimates, not regression outputs from a calibrated factor model.** The framework labels them "Barra-style" because the seven-factor decomposition (Value / Quality / Momentum / Growth / Size / Low-Vol / Liquidity) follows the structure of MSCI Barra USE4 — but the z-scores in this skill are constructed by analyst judgment over publicly available proxies (B/P, E/P, FCF/EV from XBRL company facts; 12-month trailing return; cross-sectional GICS-sub-industry medians), not by the proprietary daily regression Barra USE4 actually runs. The conviction multipliers and edge decay fields elsewhere in this file are similarly **decreed, not derived** — they reflect institutional rules of thumb, not backtest calibration.

**Operational implication.** Do not size positions in a real book against these numbers without an overlay from a calibrated factor model. The position-sizing math in `position-sizing-us.md` applies discounts based on factor crowding (specifically: three factors with |z| > 1.5 → conviction multiplier × 0.5), which means a guessed +1.8 vs a guessed +1.4 changes the recommended position size by half. That sensitivity is real arithmetic; the input precision is not. If you have access to a calibrated factor feed (Barra Aegis, Axioma, MSCI Beacon, internal multi-factor model), override the values in this section with the feed's output. If you do not, treat the recommended position size as a directional bias not a hard sizing.

**What G13 verifies.** Presence and range-validity only — all seven factor keys present, each value in `[-3, +3]`. G13 does not verify that the z-scores match a real factor model. G13 does not verify cross-document consistency (e.g., that NVDA's Momentum z-score is the same in this file, in `scenarios.json`, and in `position-sizing-us.md`). **G18 (v0.3.0)** adds cross-document consistency: within a single memo, the structured `quant_overlay.barra_factor_tags` block must match any Markdown narrative reference to the same factor within ±0.2 tolerance. G18 still does not verify the z-scores against a real factor model — it verifies internal consistency only. There is no gate that checks the z-scores are *right*.

**Honest external framing.** When describing this section to a buy-side audience, the accurate claim is "we declare Barra-style factor exposure to surface the factor implications of the recommended position." The inaccurate claim would be "the position sizing is calibrated against Barra USE4." It is not. If asked "how are the z-scores computed," the honest answer is "EDGAR-only fallback from XBRL company facts, z-scored against GICS sub-industry medians; not regressions against a daily-rebalanced multi-factor model."

## Why mandatory (per D13)

Buy-side institutional integration requires that every single-name recommendation be expressible at the book level. Two things make that possible: (1) **factor decomposition** — what style exposures the position adds to the book, so the PM can tell whether NVDA on top of MSFT+GOOGL doubles down on Momentum/Growth/Size or diversifies; and (2) **capacity disclosure** — whether the recommended position can actually be entered and exited at the recommended size without market impact, against the name's ADV. A memo that omits either is a single-name view in isolation, not a book-level decision. Per **D13**, the quant overlay (this file) is **mandatory in every institutional IC memo**, not opt-in. The institutional template `ic-memo-template-us.md` carries it as §11; the IC pre-read inherits it via summary; the LP letter omits it (client doesn't see capacity math). The two gates that enforce presence are **G13** (factor tags) and **G14** (capacity), both verified by `scripts/verify_quant_overlay.py` (S-D-4).

## Factor exposure block (G13)

US institutional risk systems (Barra, Axioma, MSCI Barra USE4/USFAST) decompose stock returns into a set of standardized **factor exposures**, each expressed as a **z-score** (standardized cross-sectional rank within the US equity universe, typically truncated to the **−3 to +3** range per `schemas/memo.json` `quant_overlay.factor_tags` minimum/maximum). The memo must declare all seven of the canonical factors below. **|z| > 2.0** indicates extreme exposure; **|z| > 1.5** is meaningful; **|z| < 0.5** is near-neutral.

### The 7 Barra-style factors

#### 1. Value
- **Concept**: cheapness on cash-flow / asset-yield basis. Composite of B/P, E/P, FCF/EV, dividend yield, EBITDA/EV.
- **Z-score scale**: −3 (most expensive) to +3 (cheapest), cross-sectional within Russell 1000 / Russell 3000.
- **US sector examples**: **XOM** Value +1.5 to +2.5 (cheap mid-cycle on E/P + FCF yield), **JPM** Value +0.5 to +1.0 (modestly cheap), **AAPL** Value −0.7, **NVDA** Value −1.5 (NVDA fixture), **most SaaS** Value −1.5 to −2.5.
- **Estimation**: ordinary least-squares regression of name's monthly excess returns vs Russell-1000 Value factor portfolio (HML-equivalent) over trailing 36-60 months; or direct from Barra USE4 / Axioma US4 / MSCI USA Value if premium access. **EDGAR-only fallback**: compute B/P, E/P, FCF/EV from XBRL company facts; z-score against sector median.

#### 2. Quality
- **Concept**: profitability stability + balance-sheet strength. Composite of ROE, ROA, gross-margin stability, debt/equity, earnings variability (inverse).
- **Z-score scale**: −3 (lowest quality, distressed/cyclical-trough) to +3 (highest quality, monopolistic FCF compounders).
- **US sector examples**: **AAPL** Quality +1.5 (high ROE, low debt, stable margins); **MSFT** Quality +1.8; **JPM** Quality +1.0 (high CET1, ROTCE compounding); **NVDA** Quality +1.2 (NVDA fixture; high but offset by SBC dilution + recent ramp instability); **MRK** Quality +1.5; **distressed retailer / capital-intensive cyclical** Quality −1.5 to −2.0.
- **Estimation**: cross-sectional rank on the 5-factor Quality composite within Russell 1000; or premium feed.

#### 3. Momentum
- **Concept**: trailing 12-1 month return (12-month total return excluding the most recent month, the standard Carhart MOM construction).
- **Z-score scale**: −3 (worst trailing-12-1 momentum) to +3 (strongest).
- **US sector examples**: **NVDA** Momentum +1.8 (NVDA fixture; AI cycle); **AAPL** Momentum +0.4 (range-bound); **XOM** Momentum −0.5 (mid-cycle drift); **regional banks during 2023 SVB shock** Momentum −2.5; **biotech post-positive Phase III** Momentum +2.5 spike.
- **Estimation**: standard Carhart 12-1 return ranked cross-sectionally within US large-cap universe; standardized.

#### 4. Growth
- **Concept**: sales / earnings growth velocity. Composite of trailing 3yr revenue CAGR, forward 1yr consensus EPS growth, gross-profit growth.
- **Z-score scale**: −3 (declining revenue / shrinking) to +3 (hyper-growth).
- **US sector examples**: **NVDA** Growth +2.5 (NVDA fixture; +120% YoY revenue in FY24); **MSFT** Growth +1.0; **JPM** Growth +0.2 (bank growth is constrained); **XOM** Growth −0.5 to 0 (cyclical, no secular growth); **mature consumer staples** Growth 0 to +0.5.
- **Estimation**: composite of historical and forward growth metrics; z-scored within universe.

#### 5. Size
- **Concept**: log market capitalization. Mega-caps are high-Size; micro-caps are low-Size.
- **Z-score scale**: −3 (micro-cap, ~$50M-$300M) to +3 (mega-cap, >$1T).
- **US sector examples**: **AAPL/MSFT/NVDA/GOOGL/AMZN** Size +2.5 to +3.0 (NVDA fixture: +3.0, mega-cap); **JPM** Size +2.3; **mid-cap industrial $5-10B** Size 0 to +0.5; **Russell 2000 SMID** Size −1.0 to −2.0.
- **Estimation**: log(market cap) cross-sectionally ranked; standardized.

#### 6. Low-Vol (Low Volatility)
- **Concept**: inverse of trailing realized volatility (typically 12-month daily realized σ). High Low-Vol z-score = low realized vol.
- **Z-score scale**: −3 (highest realized vol, often biotech / SPAC / micro-cap) to +3 (lowest realized vol, utilities / staples).
- **US sector examples**: **utilities (NEE/DUK)** Low-Vol +2.0; **staples (PG/KO)** Low-Vol +1.5; **AAPL** Low-Vol +0.8; **NVDA** Low-Vol +0.2 (NVDA fixture; mega-cap so not extreme, but high realized vol from AI cycle); **regional bank during stress** Low-Vol −2.5; **levered biotech** Low-Vol −2.0 to −3.0.
- **Estimation**: 12-month daily realized vol; inverse-ranked cross-sectionally.

#### 7. Liquidity
- **Concept**: tradability — combination of ADV, bid-ask spread, turnover. High Liquidity z-score = easy to trade.
- **Z-score scale**: −3 (thinly traded, micro-cap, wide spreads) to +3 (mega-cap with deep two-sided market).
- **US sector examples**: **NVDA** Liquidity +2.0 (NVDA fixture; $30B+ ADV); **AAPL/MSFT** Liquidity +2.5; **mid-cap with $50M ADV** Liquidity 0; **micro-cap with $2M ADV** Liquidity −2.0 to −3.0.
- **Estimation**: composite of 30-day ADV (USD), turnover rate (ADV / market cap), and bid-ask spread; cross-sectionally ranked.

### Memo declaration format

The factor block in `quant_overlay.factor_tags` must contain all 7 keys (`value`, `quality`, `momentum`, `growth`, `size`, `low_vol`, `liquidity`), each a float in [−3, +3]. Memo §11 should render as a table:

```
| Factor    | z-score | Interpretation                       |
|-----------|---------|--------------------------------------|
| Value     | −1.5    | Expensive; growth-style tilt         |
| Quality   | +1.2    | Above-average ROE / margin stability |
| Momentum  | +1.8    | Strong trailing-12-1 return          |
| Growth    | +2.5    | Hyper-growth; |z|>2 — extreme        |
| Size      | +3.0    | Mega-cap; |z|>2 — extreme            |
| Low_Vol   | +0.2    | Near-neutral on realized vol         |
| Liquidity | +2.0    | Highly liquid; |z|>2 — extreme       |
```

(Values above are the NVDA fixture per `scripts/tests/fixtures/nvda_v0/clean.json`.)

### G13 scope (explicit; authoritative for verify_quant_overlay.py)

The G13 gate ("Factor exposure stated") **passes** when `quant_overlay.factor_tags` is present in the memo's structured JSON AND all seven required factor keys (`value`, `quality`, `momentum`, `growth`, `size`, `low_vol`, `liquidity`) are present AND each value is a valid float within the closed interval **[−3.0, +3.0]** per `schemas/memo.json` `quant_overlay.factor_tags` `minimum`/`maximum`. The gate **fails** if any of the seven keys is absent, if any value is null, or if any value lies outside [−3, +3] — the latter implies an estimation error in the underlying factor-portfolio regression and forces the analyst to re-check methodology before the memo can score above 8.0. **Scope**: G13 applies to every institutional memo (`audience_variant = institutional_full`) per D13; for `ic_preread` and `ic_debate_script` variants, the factor block is inherited by reference from the parent institutional memo's structured JSON, and G13 is verified against that parent. For `lp_letter` the block is omitted (client-facing comms do not display Barra exposures), and G13 is `n_a` for that variant. The script `verify_quant_overlay.py` enforces this scope: it loads `quant_overlay.factor_tags`, asserts all seven keys present, asserts each value is numeric and within [−3, +3], and emits structured `evidence` per `schemas/verification_gates.json`.

## Capacity analysis block (G14)

Capacity converts the conviction-adjusted Kelly position size (per `position-sizing-us.md`) into a tradability check. A 5% NAV position in a name with $30B ADV is trivial to enter and exit; the same dollar position in a $30M ADV name takes weeks at the market-impact participation rate, and weeks of liquidity risk is itself a thesis-breaking event.

### Required and recommended fields

Per `schemas/memo.json` `quant_overlay.capacity`:

| Field | Required by schema | Required by G14 | Definition |
|---|---|---|---|
| `adv_30d_usd_m` | yes | **yes** | 30-day average daily dollar volume in USD millions; rolling Σ(close × volume) / 30 over 30 trading days |
| `days_to_exit_10pct_participation` | yes | **yes** | (position $) / (0.10 × ADV $); days to liquidate at 10% participation |
| `days_to_exit_20pct_participation` | yes | recommended | (position $) / (0.20 × ADV $); days at 20% participation |
| `days_to_exit_30pct_participation` | no | recommended | (position $) / (0.30 × ADV $); days at 30% participation |
| `max_position_constrained_by_adv_pct_nav` | no | recommended | Max % NAV consistent with days-to-exit ≤ N at chosen participation rate |

The two **G14-required** fields are `adv_30d_usd_m` and `days_to_exit_10pct_participation`. The other three are strongly recommended for institutional memos but do not trip G14 if absent.

### Definitions and math

**30-day ADV (USD millions)**: rolling 30-trading-day average of dollar volume. Computed `Σ(close_i × volume_i) / 30` over the last 30 trading days. Primary free feed: **Yahoo Finance** (`finance.yahoo.com/quote/{ticker}/history?period1=...`) or **FINRA**; XBRL company facts do not include this — must come from market-data feed. Update as part of memo refresh.

**Days-to-exit at p% participation**: `days = position_$ / (p × ADV_$)`. Conventional thresholds:
- **10% participation** — passive, no market impact. Standard institutional default for non-forced exits.
- **20% participation** — moderate impact; tolerable for L/S hedge funds with shorter holding periods.
- **30% participation** — meaningful impact; reserved for forced liquidation (margin call, mandate breach, A0 tail event).

**Max position constrained by ADV (% NAV)**: solve for `position_$` such that `days_to_exit ≤ N_threshold` at chosen participation rate; convert to % NAV. Typical thresholds:
- 10% participation, ≤5 days → `max_position_$ = 0.5 × ADV_$` (i.e., half a day of total volume at 10% participation cap)
- 20% participation, ≤2 days → `max_position_$ = 0.4 × ADV_$`

**Stock loan rate (if shorting)**: hard-to-borrow rate in bps/year (S3 Partners / Ortex premium feed; FINRA stock-loan data partial-free). Adds to short-side carry cost and flags crowding. Captured in `positioning_sentiment.stock_loan_rate_bps`, not in `quant_overlay`, but cross-references here for sizing.

### Worked example (NVDA fixture)

NVDA per `scripts/tests/fixtures/nvda_v0/clean.json`:
- `adv_30d_usd_m`: $30,000M = $30B
- `days_to_exit_10pct_participation`: 0.5 days
- `days_to_exit_20pct_participation`: 0.25 days
- `days_to_exit_30pct_participation`: 0.17 days
- `max_position_constrained_by_adv_pct_nav`: 15.0%

Interpretation: a $1B fund's 5% NAV position ($50M) liquidates in <1 day at 10% participation. NVDA is not capacity-constrained for any but the largest funds. Compare to a hypothetical SMID with $50M ADV — same $50M position would take 10 days at 10% participation, which G14 would flag for explicit capacity-cap disclosure.

### G14 scope (explicit; authoritative for verify_quant_overlay.py)

The G14 gate ("Capacity / ADV / days-to-exit stated") **passes** when `quant_overlay.capacity.adv_30d_usd_m` is present, non-null, and positive AND `quant_overlay.capacity.days_to_exit_10pct_participation` is present, non-null, and positive. These two fields are the **required** trip-wire; the additional fields `days_to_exit_20pct_participation`, `days_to_exit_30pct_participation`, and `max_position_constrained_by_adv_pct_nav` are recommended (institutional memos should include them) but their absence does **not** trip G14. The gate **fails** when either of the two required fields is missing, null, zero, or negative — economically a zero ADV implies the name does not trade and any sized position is non-tradable. **Scope**: G14 applies to `institutional_full` and `ic_preread` variants per D13 (the pre-read inherits capacity from the parent institutional memo and re-renders the summary line); `ic_debate_script` includes it in the Q&A bank; `lp_letter` omits it (client does not see capacity math) and G14 is `n_a` for that variant; `earnings_prep` and `earnings_flash` are operational templates and G14 is `n_a` for them. Threshold severity (e.g., "days-to-exit > 5 days requires explicit cap disclosure") is **strategy-specific** and is **not enforced** by G14 in Phase D — Phase E will calibrate strategy-specific thresholds against real-world fund sizes (a $500M fund vs a $5B fund tolerate very different position-vs-ADV ratios) and may tighten the gate accordingly. The script `verify_quant_overlay.py` enforces the Phase D scope: it loads `quant_overlay.capacity`, asserts the two required fields are present and positive, and emits structured `evidence` per `schemas/verification_gates.json`.

## Edge decay

The edge-decay block tells the PM **when this memo expires**. A view that takes 18 months to play out but is fully priced in within 3 months is not a 12-month long; it's a 3-month trade with risk of giving back gains.

Per `schemas/memo.json` `quant_overlay.edge_decay`:

| Field | Definition |
|---|---|
| `thesis_half_life_months` | Time after publication at which the alpha generated by the memo is half consumed. NVDA fixture: 6 months. |
| `time_to_priced_in_months` | Time at which 90%+ of the alpha is reflected in price (the practical "exit by" date). NVDA fixture: 9 months. |
| `refresh_cadence` | One of `weekly` / `monthly` / `quarterly_print` / `event_driven`. NVDA fixture: `quarterly_print` (10-Q cycle). |
| `primary_decay_driver` | What event causes alpha to decay. NVDA fixture: "Hyperscaler capex print cycle + Blackwell mix disclosure". |

The decay driver narrative should be a one-sentence statement of what observable event consumes the edge — most often a print (10-Q segment GM, earnings call commentary), a peer print (hyperscaler capex guide), or a calendar event (FDA decision, Fed FOMC, election). The refresh cadence in the schema enum drives `monitoring-framework-us.md` Tier-2 trigger frequency.

## Correlation overlay (placeholder per D14)

Per **D14**, the correlation block is a **placeholder in Phase D**; live wiring to a book file is deferred to a future phase. The schema slot exists so memos generated in Phase D forward-compatibly carry the field without requiring a re-render when wiring goes live.

Per `schemas/memo.json` `quant_overlay.correlation`:

| Field | Definition | NVDA fixture value |
|---|---|---|
| `book_file_path` | Path to current book holdings JSON (e.g., `~/book/holdings.json`) | `"n/a (placeholder per D14)"` |
| `top10_pairwise_corr` | Array of `{ticker, corr}` for top-10 book holdings vs this name | `[]` (empty, placeholder) |
| `live_wired` | Boolean — true once integration is live | `false` |

When `live_wired = false`, G13 and G14 are unaffected — the placeholder is acceptable. A future gate (G15 or similar) might enforce correlation population once wiring is delivered; that is out of Phase D scope.

When live: top-10 pairwise correlation uses 60-month monthly returns (or 36-month if name is younger) against each top-10 book name; a **|corr| > 0.7** vs an existing top-10 holding flags book-level crowding that should reduce position size further (cross-references the factor-crowding discount in `position-sizing-us.md`).

## Stress overlay

Four standing scenarios per `schemas/memo.json` `quant_overlay.stress_overlay`. Each is a **signed % stock impact** of the named macro shock. NVDA fixture values shown for reference.

| Scenario | Field | Definition | NVDA fixture |
|---|---|---|---|
| Fed funds +200bp | `fed_funds_plus_200bp` | Impact via cost-of-debt step-up + multiple compression (DCF discount-rate increase); typically larger for long-duration growth names | −18.0% |
| Oil −20% | `oil_minus_20pct` | Impact for E&P / refiners / airlines / consumer. E&P bear; refiners modest bear (crack spread offset); airlines mild bull; consumer mild bull | +2.0% (NVDA neutral-to-positive on oil down → consumer real income up → hyperscaler capex modestly supported) |
| USD +5% | `usd_plus_5pct` | Multinational translation hit; S&P 500 ~40% foreign revenue. Tech megacaps high foreign mix typically take 2-5% EPS hit per 5% USD strengthening | −3.5% |
| Recession dummy | `recession_dummy` | NBER recession / sustained ISM PMI < 48 / negative NFP; composite haircut to demand + multiple compression | −28.0% |

Computation: each shock is applied to the **base case scenario** EPS and multiple, then signed % vs current price. Stress overlay rows are NOT averaged into the 5-scenario weighted expected return — they are robustness checks beside the scenario distribution, not inside it. PMs use them for portfolio stress reports (e.g., "what does the book lose if Fed funds +200bp tomorrow?").

## Anti-patterns (these fail PM red-team)

| Anti-pattern | Why wrong | Gate |
|---|---|---|
| One or more of the 7 factor tags missing | Cannot decompose at book level; G13 fail | G13 |
| Factor z-score outside [−3, +3] | Implies estimation error in factor-portfolio regression; suspect methodology | G13 |
| ADV not stated | Cannot size against capacity; G14 fail | G14 |
| Days-to-exit at 10% participation not stated | Cannot evaluate tradability; G14 fail | G14 |
| Position size implied by sizing math > capacity cap, without disclosure | Strategy mis-sizing; cannot liquidate at thesis-break | G14 (soft) |
| Stress overlay missing | Robustness check skipped; reader cannot evaluate macro tail | (no gate; rubric ding) |
| Correlation slot empty without `book_file_path` reference | Acceptable per D14 but should still set `live_wired: false` and reference path | (no gate) |

## Phase E calibration note (forward-looking)

Phase D ships **defaults**: the seven factor tags, the two G14-required capacity fields, the four stress scenarios. **Phase E will calibrate** strategy-specific thresholds against 3-5 real recent memos with deliberately different factor profiles — for instance: **NVDA** (mega-cap growth + momentum extreme), **JPM** (bank: high Quality, mid Value, low Growth), **XOM** (energy: high Value, negative Momentum mid-cycle), **MRK** (pharma: high Quality, mid Growth, low Momentum during pipeline trough), and a **SMID example** (e.g., a $5-10B specialty industrial: Size near zero, Liquidity low, capacity-binding for large funds). Calibration items deferred to Phase E include: (i) max participation % threshold for tripping a G14 "capacity-binding" sub-flag; (ii) days-to-exit cap (5 days? 3 days?) at which the memo must surface explicit cap disclosure; (iii) factor-extremity threshold (|z| > 2.0 vs > 1.5) at which the factor-crowding discount in `position-sizing-us.md` kicks in. Phase D's `verify_quant_overlay.py` enforces only structural presence and range validity; threshold-based fails are deferred.

## Cross-references

- `position-sizing-us.md` — capacity (G14) feeds sizing math; factor crowding (G13) feeds conviction discount
- `pm-redteam-rubric-us.md` — B13 and B14 bug-catalog entries
- `monitoring-framework-us.md` — re-sizing triggers tied to ADV regime changes and factor reversals
- `five-scenario-framework-us.md` — base-case EPS feeds stress overlay computation
- `tail-risk-mapping-us.md` — A0 events drive the stress overlay scenarios
