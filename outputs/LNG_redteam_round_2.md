# LNG (Cheniere) IC Memo — PM Red-Team, Round 2 (post-fix)

**Date:** 2026-06-09 · **Target:** ≥8.5 · **Verdict: PASS — 8.9 / 10** (up from 8.6) · **All 19 applicable gates pass; G15/G16/G20 n_a**

Round 1 landed 8.6 and flagged three gate-passing-but-soft items (B11, B9, B2/B3). All three Round-1 fixes were applied to the source artifacts and re-verified. The Hold call, +4.9% expected return, and two-sided risk are unchanged — the fixes harden the *exposition*, not the *view*.

## Fixes applied
| Fix | Bug | Edit | Re-verify | Score |
|---|---|---|---|---|
| 1 | B11 | Added explicit FY2025 **GAAP NI → Consolidated Adj EBITDA → DCF** Reg-G bridge table in `LNG_IC_memo.md` §4 (the −$4.1B unrealized-hedge-MtM removal made visible) | `verify_non_gaap.py` ✅ | 7.5 → **9.0** |
| 2 | B9 | Added 2 standing A0 tails to `LNG_structured.json` `tail_risks` — **DOE/FERC export-policy reversal** + **tariff/trade-war gas-demand** (now 6 rows; every row's shifts conserve to zero) | shift-sum check ✅ (G10 unaffected) | 7.5 → **8.8** |
| 3 | B2/B3 | Relabeled T1/T2 as the **Consolidated-Adjusted-EBITDA-margin analog** (the LNG equivalent of bank NIM per D24), explicitly NOT a GAAP GM, S5-tagged; SOTP noted as platform-EBITDA-driven | `verify_segment_gm.py` ✅ `verify_sotp_monotonicity.py` ✅ | 7.0/7.5 → **8.0/8.3** |

## Gate sweep (post-fix)
All 19 applicable verifier scripts exit 0 under the uniform calling contract (`scripts/run_all_gates.sh LNG`): G1–G14, G17, G18, G19 **pass**; G15 (Hold), G16 (non-bank), G20 (Hold) **n_a**. Manifest regenerated after the edits — G19 SHA-256 integrity re-verified against the edited memo (20 outputs hashed, 16 web-search entries, 15 agent workpapers).

## Updated scorecard
B1 9.5 · **B2 8.0** · **B3 8.3** · B4 9.0 · B5 9.0 · B6 9.0 · B7 9.5 · B8 8.5 · **B9 8.8** · B10 9.0 · **B11 9.0** · B12 9.0 · B13 9.0 · B14 9.0 → **weighted 8.9 / 10 (IC-grade hardness).**

## Residual ceiling (why ~8.9, not 9.2)
The only remaining soft spot is intrinsic to the name: Cheniere discloses neither a GAAP segment gross margin nor a segment GP/OP/NI P&L, so the segment/SOTP layer is an **EBITDA-margin analog** the analyst constructs (now labeled honestly as such, S5). The gates designed for disclosed-GM industrials are satisfied via the documented adaptation, but the inputs are modeled, not filing-derived — an honest ceiling, not a defect. Everything a PM would actually challenge — the multiple-durability variance, the below-Street PT, the source-conditional headline, the bridge math — is hard.

## Bottom line
**8.9 / 10 — comfortably clears the 8.5 bar and is IC-ready.** Source-conditional **Hold**, 12-mo PT **$253.63** (+5.9% to target; +4.9% probability-weighted), ~16% below a crowded +27% Street. The actionable expression is relative-value (long VG / short LNG) and a sub-$200 / new-FID re-entry.

*Gate logs: `outputs/LNG_verification_gates.json` · Manifest (SHA-verified): `outputs/LNG_manifest.json` · Round 1: `outputs/LNG_redteam_round_1.md`. Deliverable PDF: `outputs/LNG_IC_memo.pdf`.*
