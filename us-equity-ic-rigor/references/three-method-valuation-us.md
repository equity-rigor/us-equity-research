# Three-method valuation reconciliation (US)

## The core discipline

EPS × multiple, SOTP, and multi-multiple bear floor are **three lenses on the same business** — they are not three independent fair values to average. Treating them as three fair values to average produces nonsense: you would be averaging a forward earnings view, a sum-of-parts view, and a cycle-trough view, and the resulting number has no economic meaning. PMs catch this immediately, and it's a fast path to losing credibility in IC.

The right framing:

- **EPS × multiple** is the primary valuation. It is what you defend in IC. It is the headline.
- **SOTP** is a *cross-check* for segment-level internal consistency. If your scenario EPS does not reconcile to a defensible SOTP, your scenario EPS is wrong.
- **Multi-multiple bear floor** (P/B, EV/EBITDA, FCF yield, EV/ARR floor for SaaS) is a *downside floor check* — it answers "if the market loses faith in forward earnings entirely, where does the stock find support?"

When the three methods disagree by >15%, do **NOT** average. Instead, identify which assumption is doing the work and which scenario the disagreement implies. A 30% spread between EPS × multiple bear and the multi-multiple floor usually signals one of three things:

1. The bear-case EPS has too much hidden cost-cutting baked in (EPS × multiple looks too high vs P/B floor)
2. The asset base has stale book value or impaired goodwill (P/B floor is too high vs forward earnings reality)
3. The market is pricing a regime change that EPS × multiple doesn't capture (FCF yield reads worse than P/E reads)

Identify which one and write it as the "valuation reconcile" subsection of §5.

## Method 1: EPS × multiple (primary)

See `five-scenario-framework-us.md` for the scenario construction. Key disciplines:

- **Forward period must be consistent across rows** (FY+1 or FY+2; pick one and stick with it; we typically use FY+2 for cyclical or capacity-ramp stocks because it captures a meaningful pivot point past current noise).
- **Multiple must reflect both growth quality AND scenario-specific risk premium.** A bull-scenario multiple > base only if growth, ROIC, or capital-intensity profile differs in that scenario; otherwise it's double-counting.
- **Each row's target = EPS × multiple (P/E case) mechanically, not narratively.** G1 gate verifies this with `scripts/verify_eps_pe.py`.
- **Multiple_type follows sector default per D8** — see `valuation-discipline-us.md`:
  - Mature industrial / staples / consumer → **P/E** primary, EV/EBITDA secondary
  - Banks → **P/B** primary, P/E secondary, P/PPNR for normalized earnings
  - Insurance → **P/B** + ROE-implied P/B
  - REITs → **P/AFFO**, NAV, implied cap rate
  - SaaS / software → **EV/ARR** with Rule of 40 overlay; EV/Sales secondary
  - Biotech pre-revenue → **NPV pipeline** (no multiple)
  - E&P → **EV/EBITDAX** + NAV
  - Asset managers → **P/AUM** + P/E
  - Airlines → **EV/EBITDAR** (capitalizes operating leases)
  - High-leverage industrial → **EV/EBITDA**

For NVDA (mature growth large-cap chip designer): **P/E** primary, **EV/Sales** as secondary check given the FY26 ramp distortion.

## Method 2: SOTP — what it's actually for

SOTP is the **internal consistency check**, not a separate fair value. Build the SOTP using the same EPS path you used in EPS × multiple, decompose it segment-by-segment, and verify:

1. **Σ(segment NI) ≈ company NI** (within rounding + minority interest + corporate unallocated)
2. **Per-segment Revenue → GP → OP → NI monotonicity** (G3 gate): for every segment, NI ≤ OP ≤ GP ≤ Revenue. Any inversion fails. The script `scripts/verify_sotp_monotonicity.py` catches this.
3. **Per-segment GM consistent with GM taxonomy** (see `gm-taxonomy-us.md`): the segment GM you use in SOTP must equal the segment GM (T2) declared elsewhere in the memo, within rounding.
4. **Per-segment operating margin within historical bands** — cite the 3-5 year range for each segment.

If any of these fail, your scenario EPS path is fictional. SOTP is not generating new information — it is auditing the EPS you already have.

### SOTP table required columns

```
| Segment | Revenue | GM % | GP | OpEx | OP | Tax | NI | Multiple | Segment EV |
```

The middle columns (Revenue → GP → OP → NI) must reconcile mechanically. NI is the **final** number computed, never an input. If the columns don't reconcile, fix the segment assumption, not the column.

The Multiple / Segment EV columns at the right are for cross-comparing implied multiples across segments. Common usage: show that your sum-of-parts implied EV is within ±15% of company-level EV; if not, either segments are mispriced or company-level valuation is mispriced — investigate which.

### Sector adaptation: banks SOTP (no GP / no OP) — per D24

Banks have no COGS, no GP, no OP in the manufacturing/consumer/tech sense. The SOTP columns adapt to the bank income-statement skeleton:

```
| Segment | Avg Earning Assets | NIM | NII | Non-Interest Income | Total Revenue | NIE | PPNR | Provisions | Pre-Tax Income | Tax | NI | Multiple | Segment EV |
```

Where:
- **NII** = Net Interest Income = Avg Earning Assets × NIM (replaces the Revenue → GP step)
- **Total Revenue** = NII + Non-Interest Income (fee + trading + IB advisory + AWM mgmt fees)
- **NIE** = Non-Interest Expense (the bank's opex; replaces OpEx)
- **PPNR** = Pre-Provision Net Revenue = Total Revenue − NIE (**substitutes GP** in the monotonicity chain)
- **Pre-Tax Income** = PPNR − Provisions (loan loss provisions; replaces OP)
- **NI** = Pre-Tax Income × (1 − tax_rate)

**G3 monotonicity for banks**: NI ≤ Pre-Tax Income ≤ PPNR ≤ Total Revenue for every segment. The script `verify_sotp_monotonicity.py` enforces this chain identically; the modeler stores values in JSON keys `segment_revenue` (= Total Revenue), `segment_gp` (= PPNR), `segment_op` (= Pre-Tax Income), `segment_ni` (= NI). The script does not need code change; the field-name mapping is documented here as the canonical banks adaptation. (If a future refactor introduces explicit banks-fields, this paragraph specifies the equivalence.)

**Provisions discipline**: provisions are NOT a steady-state cost — they swing with credit cycle. In bull / base scenarios, provisions can be **negative** (releases from over-reserved positions); in bear / strong_bear, provisions can spike to **5-10% of loans** (vs ~50-100bp normal). The PPNR row in SOTP isolates the structural earnings power from the credit cycle; this is why PMs use **PPNR-based multiples** (P/PPNR) in addition to P/E for banks.

**Worked example (JPM Phase E SOTP, base case)**:

| Segment | Avg EA $B | NIM | NII $B | Non-Int Inc $B | Revenue $B | NIE $B | PPNR $B | Prov $B | Pre-Tax $B | Tax $B | NI $B |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CCB | 1,250 | 3.85% | 48.1 | 8.2 | 56.3 | 28.5 | 27.8 | 6.5 | 21.3 | 5.1 | 16.2 |
| CIB | 1,800 | 1.75% | 31.5 | 35.0 | 66.5 | 34.0 | 32.5 | 1.5 | 31.0 | 7.4 | 23.6 |
| AWM | 220 | 4.10% (fee-equiv) | 9.0 | 15.5 | 24.5 | 17.2 | 7.3 | 0.2 | 7.1 | 1.7 | 5.4 |
| Corporate | 250 | n/m | 0.5 | 2.0 | 2.5 | 6.0 | (3.5) | 0.0 | (3.5) | (0.8) | (2.7) |
| **Sum** | **3,520** | | **89.1** | **60.7** | **149.8** | **85.7** | **64.1** | **8.2** | **55.9** | **13.4** | **42.5** |

Monotonicity check per segment: CCB NI 16.2 ≤ Pre-Tax 21.3 ≤ PPNR 27.8 ≤ Revenue 56.3 ✓. CIB and AWM identical pattern. Corporate has negative PPNR (typical — corporate segment runs net opex burn) but monotonicity still holds with sign-preserving inequality (NI -2.7 ≤ Pre-Tax -3.5 ≤ PPNR -3.5; G3 script's edge case: ensure negative-PPNR segments are handled by sign-aware comparison — the existing script's `>=` check is correct because for negative chains the more-negative value is the lower bound; see G3 fixture suite).

**Multi-multiple bear floor for banks** is **P/B + P/PPNR**, NOT EV/EBITDA / FCF yield / EV/Sales. Per `valuation-discipline-us.md` sector defaults and per Method 3 below.

### Pitfall 1: SOTP NI > SOTP GP (G3 monotonicity fail)

Happens when the modeler estimates segment NI directly (top-down) without forcing it through the GP → OP → NI mechanical chain. To prevent: **always construct SOTP bottom-up** via the column sequence above. NI is the residual, not an input. This is one of the most common B1-B3 forensic bugs in red-team practice.

### Pitfall 2: Segments don't sum to consolidated (G2 segment GM gate fail)

Common pattern: segment revenues sum to consolidated within ±2%, but segment NI sums to 80% of consolidated NI because corporate overhead / unallocated wasn't modeled. Fix: include an **"Other / Corporate / Unallocated"** row that absorbs the difference, with a one-line explanation (typically "corporate overhead + intercompany eliminations + investment income + SBC not allocated to segments").

### Pitfall 3: Segment GM in SOTP ≠ T2 segment GM elsewhere in memo

Internal contradiction: §5.2 GM taxonomy box says Datacenter T2 GM = 75%, but §5.5 SOTP uses Datacenter GM = 78%. PM red-team flags as B2 (cross-section inconsistency). Fix: GM taxonomy box is source of truth; SOTP inherits from it.

## Method 3: Multi-multiple bear floor

Apply this method **only when constructing the bear / strong_bear scenarios**. The question this method answers: in a true downside, what is the stock worth on metrics that don't depend on forward earnings? Multi-multiple bear is a **floor check**, not a base-scenario valuation tool. Using it as a primary method in the base scenario inflates pessimism into the headline and is an anti-pattern.

### Three multiples to triangulate (US sector mapping)

**P/B floor** (best for banks / insurers / capital-intensive cyclicals)
- Formula: tangible BVPS × historical-trough P/B (cite trough year and value, e.g., "BAC 0.5x P/B at March 2009 trough; current 1.1x; bear floor 0.7x").
- Caveat: if there's impairment risk in the bear, mark down the BV first (goodwill write-down, securities mark-to-market for banks, intangible impairment for tech).

**EV/EBITDA trough** (best for high-leverage industrial, chemicals, transport, telecom)
- Formula: bear-case forward EBITDA × historical-trough EV/EBITDA, then back into equity value (subtract net debt at par or marked).
- Caveat: EBITDA is not cash; if working capital is unwinding, FCF is worse than EBITDA suggests. For pension-heavy industrials, add PBO underfunding as a debt-like liability.

**FCF yield** (best for capex-heavy mature, semis, panels, autos, energy)
- Formula: bear FCF / target market cap. Compare to peer median or to (10Y UST + ERP).
- Caveat: cyclical names have negative FCF in trough; use **mid-cycle FCF** for the floor, not trough.
- **Critical US-specific check** (G12 gate): is SBC deducted from this FCF? If not, the floor is overstated. See `forensic-accounting-checklist-us.md` on FCF discipline.

**EV/ARR floor** (US-specific; for SaaS and software)
- Formula: bear ARR × trough EV/ARR. Trough multiples for high-quality SaaS sit around 4-6x (vs current 8-15x for growth names).
- Pair with **Rule of 40** check: growth% + FCF margin% > 40 → premium; <30 → discount.

### When to apply which (US-localized)

| Situation | Floor multiple | Why |
|---|---|---|
| Banks / insurers (BAC, JPM, MET) | P/B | trough P/B has historical anchor (2008-09, March 2020) |
| Capital-heavy cyclical (steel, aluminum, paper) | P/B | tangible BV is durable |
| High-leverage industrial / chemical (DOW, EMN, MMM) | EV/EBITDA | strips out leverage; useful for credit-stress comp |
| Capex-heavy semis (NVDA, INTC, AMAT, LRCX) | FCF yield + EV/Sales | catches inventory/depreciation cycle distortion; pair with EV/Sales for revenue durability |
| SaaS / software (CRM, NOW, MDB, SNOW) | EV/ARR + Rule of 40 | EBITDA / EPS distorted by SBC; ARR is the durable metric |
| REITs | NAV / implied cap rate | book value irrelevant; appraisal-based NAV more useful |
| Pre-revenue biotech | NPV pipeline (no floor) | bear floor = cash on balance sheet + partnership economics |
| Asset-light brand / consumer staples (KO, PG, COST) | none — stay with EPS × P/E | trough P/B is not meaningful; trough P/E is the floor |

### Triangulation example (NVDA strong_bear floor)

Three floor lenses on NVDA strong_bear (~$52.80 EPS × P/E target):

- **P/E P5 historical analog**: NVDA 5y P/E P5 ≈ 22x (FY23 export-control / inventory trough). FY27E EPS strong_bear $2.40 × 22 = **$52.80**. This is the EPS × multiple primary.
- **EV/Sales trough**: NVDA 5y EV/Sales P5 ≈ 7x (vs current ~22x and 10y median ~12x). FY27E revenue in strong_bear ≈ $145B → EV ≈ $1.02T → equity ≈ $1.05T (cash net) → /24.4B shares ≈ **$43**. Floor analog suggests P/E target may be slightly too forgiving.
- **FCF yield floor**: NVDA strong_bear FCF (post-SBC G12) ≈ $50B; required yield 4% (UST + 200bp ERP) → market cap ≈ $1.25T → **$51**. Roughly consistent.
- **Range**: [$43, $52.80] — midpoint $48. Strong_bear EPS×P/E target $52.80 sits at the high end of this range, which means the strong_bear scenario is *not* a deep distress case — that's an honest disclosure to the IC. If we wanted true distress floor, we'd take $43.

If EPS × multiple strong_bear had said $80 while multi-multiple range was [$43, $53], that would be a red flag: bear EPS too generous, bear multiple too generous, or both. Re-bridge.

## The three-method reconcile table (mandatory in §5.7)

```
| Method                  | Base   | Bear     | Strong_bear | Anchor logic                              |
|-------------------------|--------|----------|-------------|-------------------------------------------|
| EPS × multiple (P/E)    | $168.00| $100.80  | $52.80      | base 4.80×35; strong_bear 2.40×22 (P5)    |
| SOTP                    | $171.50| $98.40   | $51.20      | segment build (DC + Gaming + ProViz)      |
| Multi-multiple — EV/Sales| —      | —        | $43         | 7x trough EV/Sales × FY27E $145B revenue  |
| Multi-multiple — FCF yld| —      | —        | $51         | post-SBC FCF $50B / 4% required yield      |
| **Adopted value**       | $168.00| $100.80  | $52.80      | EPS × multiple primary                    |
```

Bottom row is what flows to the headline. The other rows are the audit trail showing why $52.80 in strong_bear is defensible.

## What to do when methods disagree by >15%

1. **Name the disagreement explicitly.** "EPS × P/E strong_bear $52.80 vs EV/Sales floor $43 → 19% spread."
2. **Locate the source of disagreement.** Usually it's a difference in how aggressively the bear narrative is bitten off. EV/Sales doesn't believe revenue will stay at $145B; EPS×P/E assumes it will but at 22x P/E. Or: the multi-multiple floor is anchored on a historical regime no longer applicable (NVDA FY23 was a pre-AI-boom regime — the P5 anchor may be stale).
3. **Add a "valuation reconcile" subsection** that names the disagreement and resolves it: "EPS×P/E strong_bear implies the bear narrative still produces $145B revenue. EV/Sales floor of $43 implies the market would not let revenue sustain at that level given pricing competition. We adopt EPS×P/E because [reason — e.g., DC capex is already partly committed in 24-month visibility; demand floor higher than EV/Sales P5 era]."
4. **Use the disagreement to inform conviction**: methods agreeing tightens conviction tag; methods disagreeing widens the headline range explicitly in the conditional language.

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| "Fair value = (EPS×P/E + SOTP + multi-multiple) / 3" | averaging incompatible methods; produces a non-economic number; PM red-team kills this on sight |
| Citing only EPS × multiple without SOTP | no internal consistency check; G2/G3 unverifiable |
| SOTP at headline level only (no segment breakdown) | useless — doesn't audit anything; the value of SOTP is the segment columns |
| Multi-multiple bear floor used in base scenario | floor methods only inform downside; using them in base inflates pessimism |
| Using BV without segment-level impairment in bear | overstates floor in real downside (banks: securities mark; tech: goodwill write-down) |
| Mixing GAAP / non-GAAP across methods | EPS×P/E on non-GAAP vs SOTP NI on GAAP → apples / oranges; G11 violation. Pick one accounting basis, disclose, and stick. |
| SOTP segment GM ≠ T2 segment GM in §5.2 box | B2 cross-section bug |
| FCF yield floor with FCF including SBC addback but no disclosure | G12 violation; bull case masquerading as floor |
| EV/Sales floor on a SaaS without Rule of 40 cross-check | over-rewarding pure growth; ignores quality |

## How this file ties into the rest of the rigor batch

- The EPS column feeding Method 1 comes from `five-scenario-framework-us.md` scenario construction.
- Segment GM used in Method 2 (SOTP) is tagged per `gm-taxonomy-us.md` (T2 segment GM).
- Method 3 bear floor depends on the bear-EPS construction in `bear-bridge-us.md` (clean and strong layers).
- Sector-default multiple choice is dictated by `valuation-discipline-us.md`.
- G12 (FCF/SBC discipline) is enforced via `forensic-accounting-checklist-us.md` and the G12 verification script.
- Reconcile-narrative discipline is challenged by `pm-redteam-rubric-us.md` scoring in the Valuation section.
- Source tags for trough multiples (P5 historical analogs) follow `source-stratification-us.md`.
