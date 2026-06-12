# FCX (Freeport-McMoRan) IC Memo — PM Red-Team, Round 1

**Date:** 2026-06-11 · **Target:** ≥8.5 (D20 default) · **Verdict: PASS — 8.7 / 10** · **Bottleneck: B2/B3 (segment cash-margin modeled) + "Hold at −2.5% — is it a stealth Sell?"**

This is a red-team, not a cheerleader. The memo is **mechanically clean — all 19 applicable gates pass; G15/G16/G20 n_a** — and structurally complete (T1–T5 taxonomy, layered bridges, 6-tail A0 map with zero-sum shifts, 5-mandate sizing, three-method reconcile keyed off an explicit copper deck, 7 Barra factor tags, capacity/ADV, source-conditional headline, 7 numerical triggers, GAAP/non-GAAP frame, declared downward variance). It clears 8.5. It does not reach 9.0 because (a) FCX reports geographic segments, not cash margin, so the GM/SOTP layer is modeled, and (b) the honest tension below.

---

## Step 1 — Mechanical gate sweep (G1–G20)

| Gate | Name | Status | Note |
|---|---|---|---|
| G1 | EPS × multiple multiplicativity | **pass** | 5 scenarios multiply within ±0.5% (2.30×16.0=36.80 … 5.00×21.0=105.00) |
| G2 | Segment GM reconciliation | **pass** | weighted 30.30% vs 30.3% — *but modeled, see B2* |
| G3 | SOTP monotonicity | **pass** | NI≤OP≤GP≤Rev holds all 3 segments — *but see B3* |
| G4 | Scenario probabilities = 1.00 | **pass** | 0.12/0.23/0.40/0.18/0.07 |
| G5 | Bear/bull EPS bridge reconciles | **pass** | strong_bear −1.28, bear −0.63, bull +0.62, strong_bull +1.42 — exact |
| G6 | Source tag at first use | **pass** | copper $/lb, ADV, beta, %-of-revenue tagged |
| G7 | Headline conditionality | **pass** | source_conditional; top-3 led by copper price (S4) + FY26 guide (S3) → conditional required & present |
| G8 | GM taxonomy box | **pass** | T1–T5, mining cash-margin adaptation |
| G9 | What-would-reverse numerical | **pass** | 7 triggers w/ denominators (copper <$4.75, Cu guide <3.0 Blb, cost >$2.10) |
| G10 | Anchor weighting impact table | **pass** | weighting_sensitivity present |
| G11 | Non-GAAP→GAAP reconciliation | **pass** | copper-deck-explicit EBITDA framed vs volatile GAAP; charges/insurance disclosed |
| G12 | SBC treatment in FCF | **pass** | OCF−capex; SBC ~0.5% rev; NCI-vs-cash-flow flag surfaced |
| G13 | Barra factor exposure | **pass** | 7 factors w/ z-scores |
| G14 | Capacity / ADV / days-to-exit | **pass** | ADV $790M; 10/20/30% = 2.5/1.3/0.8 days |
| G15 | Consensus variance | **n/a** | rating=Hold (1 load-bearing downward variance declared anyway, sizing 2.09pp) |
| G16 | Bank metrics | **n/a** | non-bank (Materials/Copper) |
| G17 | Revision velocity | **pass** | n=26; PTs ~flat at +4–6% above spot; EPS flat-to-down on Grasberg |
| G18 | Quant cross-doc consistency | **pass** | MD factor z-scores match JSON within ±0.2 |
| G19 | Provenance manifest | **pass** | SHA-256 verified; 16 web calls, 15 agents, 20 outputs hashed |
| G20 | View defensibility | **n/a** | Hold (base PT $66.23 ≈ spot; below the +50%-implied high-end Street) |

**Zero gate failures.** Mechanical floor cleared → ≥7.5; structures present → ≥8.5.

---

## Step 2 — Rubric scorecard (B1–B14)

| Bug | Dimension | Score | Comment |
|---|---|---:|---|
| B1 | EPS × multiple | 9.5 | Exact; copper-driven EPS path |
| **B2** | **Segment GM reconcile** | **7.0** | **Passes G2, but the 4 LTM segment cash margins are S5-modeled** — FCX reports geographic segments, not a segment cash margin. Honest (S5-tagged), but constructed. |
| **B3** | **SOTP monotonicity** | **7.5** | **Passes G3, but segment GP/OP/NI modeled-to-be-monotonic**; the NAV/minority treatment (Grasberg net of MIND ID 51%) is the analytically important part and is defensible. |
| B4 | GM taxonomy box | 9.0 | T1–T5; mining cash-margin + copper-sensitivity adaptation |
| B5 | Headline conditionality | 9.0 | Source-conditional with explicit if/then copper + Grasberg triggers |
| B6 | Bear EPS bridge | 9.0 | Soft/clean/strong; reconcile exactly; copper-sensitivity-anchored |
| B7 | What-would-reverse | 9.5 | 7 numerical triggers, each with an observable (COMEX curve, guide, 232 report) |
| B8 | Cross-version consistency | 8.5 | Net debt $2.4B (ex project debt) vs EV-implied ~$13B (NCI) explicitly reconciled (§4/§12); base PT $66 vs Street median $70 / high-end $85 owned in §6/§8 |
| B9 | A0 tail map | 8.8 | 6 tails (4 bear + 2 bull), shifts conserve to zero |
| B10 | Position sizing | 9.0 | 5 mandates + Kelly + long-SCCO/short-FCX pair w/ beta hedge |
| B11 | Non-GAAP/GAAP reconcile | 9.0 | Copper-deck EBITDA framing; charges + insurance + provisional pricing explained |
| B12 | SBC in FCF | 9.0 | OCF−capex; SBC immaterial; the real flag (NCI between EBITDA and FCX cash flow) surfaced |
| B13 | Factor exposure | 9.0 | 7 Barra tags + rationale (Momentum + Size, negative Low-Vol — honest for a cyclical at the high) |
| B14 | Capacity / ADV | 9.0 | Days-to-exit at 10/20/30% |

**Weighted overall: 8.7/10.** Band: **8.5–9.0 (IC-grade hardness).** B2/B3 cluster at ~7.5 (intrinsic to a miner that discloses geographic segments, not cash margin).

**What's genuinely good:** the memo correctly identifies that the **load-bearing variable is the copper price** (not a clever multiple), builds the scenarios off an explicit copper deck + the company's own $400M/$0.10 sensitivity, and is honest that **consensus "83% Buy" is belied by PTs only +4–6% above spot** — i.e., it reads the de-rate that the Buy ratings hide. The Grasberg single-asset/Indonesia-nationalism analysis is primary-source and properly weighted.

---

## Step 3 — Residual ceiling + the honest tension

1. **"Hold at −2.5% — is this a stealth Sell?"** The probability-weighted return is mildly *negative* and the distribution is left-skewed (strong_bear −44% at p12 vs strong_bull +59% at p7). A purist could argue −2.5% with fat left-tail = Underweight/Sell. The memo holds the line at **Hold** for two defensible reasons, stated explicitly: (a) −2.5% is inside the ±10% Hold band, and (b) the **structural copper-deficit tail is real** — shorting a structural-demand commodity leader near a supply deficit, with Grasberg recovering in 2027, is a poor risk/reward. That is a legitimate Hold-not-Sell call, but it is the *most bearish-leaning* Hold in the set and the memo says so (52-wk high, peak copper, PTs at spot, modest underweight / −25bps active). A PM who weights the left tail more heavily could rate it Underweight — that's a judgment call the memo surfaces rather than hides.
2. **B2/B3 modeled segment layer** — intrinsic to a miner reporting geographic, not cash-margin, segments. S5-tagged.
3. **Polish:** the precise Grasberg % of consolidated EBITDA and the mid-cycle copper anchor ($4.00–4.50) are conventions, flagged as modeled in §12.

**The memo is IC-ready at 8.7 and clears the 8.5 bar.** The rating is honest and defensible; no edit changes the cautious-Hold call or the −2.5% weighted return. The actionable stance — benchmark-weight/modest-underweight, re-enter on a copper dip or Grasberg de-risk, express conviction via the long-SCCO/short-FCX quality pair — follows directly.

*Gate logs: `outputs/FCX_verification_gates.json` · Manifest (SHA-verified): `outputs/FCX_manifest.json`. Deliverable PDF: `outputs/FCX_IC_memo.pdf`.*
