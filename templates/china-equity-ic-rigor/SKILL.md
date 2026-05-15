---
name: china-equity-ic-rigor
description: Layer PM-grade IC-deliverable rigor on top of china-equity-research for institutional buy-side workflows. Use whenever the user wants an investment opinion letter (投资意见书), IC memo, IC pre-read, IC debate script, or retail-friendly version of equity research, OR is iterating an existing memo through PM red-team review cycles ("score this memo", "find what is broken", "round N review", "push from 8.5 to 9.0"). Also use when the user references S1-S5 source stratification, 5-scenario probabilistic framework, three-method valuation reconciliation, GM taxonomy, bear EPS bridge, source-conditional headline, "what would reverse" triggers, or asks for a multi-audience derivative. Enforces verification gates that catch the bugs real PMs flag — EPS times PE rows that do not multiply, segment GM that does not reconcile, SOTP where NI exceeds GP, mixed GM definitions, headlines unconditional on weak anchors.
---

# China Equity IC-Rigor

This skill is the **PM red-team layer** on top of `china-equity-research`. Use the base skill to do the underlying multi-agent research; use this one to harden the deliverable to the standard a buy-side PM will sign off on.

The core insight encoded here: an institutional-grade equity opinion letter survives PM challenge not because it has a strong view, but because **every specific number is sourced, every transformation reconciles, every headline acknowledges what it's contingent on, and every "what would reverse it" trigger has a numerical denominator**. The bugs that kill a memo in IC are almost always mechanical (math doesn't multiply, definitions don't match, anchors aren't verified) — not directional.

## When to use this skill

Trigger when ANY of the following appear, even in passing:

- Ticker (000XXX / 6XXXXX / H-share) + "投资意见书" / "IC memo" / "意见书"
- "Red team this", "score this memo", "PM review", "round N", "what would push this from 8.x to 9.x"
- Headline-language requests: 中位预期收益, 情景加权区间, 仓位建议, 减仓/加仓
- Explicit references to S1-S5 sources, 强多/多头/基础/空头/强空 scenarios, 三估值法 reconcile, GM taxonomy, bear bridge, what-would-reverse, A0 tail
- Multi-audience derivatives: 精简版 / IC pre-read / IC debate script / 零售版 / 非专业版
- The user is critiquing a memo and the language sounds like a PM ("the math doesn't add up", "where does this number come from", "this is hand-wavy", "you can't make that claim without an S1")

If the request is for *initial fundamental research* (no opinion letter framing yet), use `china-equity-research` directly. Add this skill once the memo construction or red-team phase begins.

## Workflow

The work proceeds in five phases. Phases 0-3 produce the institutional version. Phase 4 hardens it. Phase 5 derives audience variants. Phases can interleave when the user explicitly directs it (e.g. "build the institutional and IC versions in parallel").

### Phase 0 — Foundational research (delegate to china-equity-research)

Use the base skill to produce: industry context, financials, policy/regulatory, positioning, base valuation read, sell-side consensus snapshot. Web-verify any post-cutoff claims with explicit citations. The output of Phase 0 is raw material — not yet shaped into the IC framework.

### Phase 1 — Source stratification gate

Before writing any specific number into the memo, classify it on the **S1-S5 + Pending** scale and decide whether the gate lets it through. See `references/source-stratification.md` for the full taxonomy and decision rules. The short version:

- **S1** = audited financial statement / 经审计年报 → use freely
- **S2** = unaudited public filing (公告, 季报, 投资者关系活动记录表) → use freely with citation
- **S3** = company IR commentary, conference call transcript, management guidance → use with "据公司表示" framing
- **S4** = sell-side consensus, broker estimates, analyst notes → use as range, not point
- **S5** = industry data, supply-chain checks, channel surveys → flag uncertainty band
- **Pending** = unverified rumor, unsourced specifics, cross-cutoff claims you couldn't verify → DO NOT promote to a headline anchor; if it must appear, mark `(Pending — not used as anchor)`

The hard rule: **if the headline thesis depends on an anchor that is S3 or weaker, the headline must be source-conditional**. See `references/source-stratification.md` §3 for the conditional language patterns.

### Phase 2 — Build the analytical pillars

Five pillars, each with its own discipline document. Construct them in parallel when possible; they cross-check each other.

- **5-scenario probabilistic framework** — 强多 / 多头 / 基础 / 空头 / 强空, weights sum to 1, each scenario has its own EPS path AND its own PE multiple AND its own narrative bridge. Detail in `references/five-scenario-framework.md`.
- **Three-method valuation reconcile** — EPS×PE / SOTP / multi-multiple bear (P/B, EV/EBITDA, FCF yield) — these are **cross-checks**, not three independent fair values to average. SOTP exists to test segment-level internal consistency, not to price the stock. Detail in `references/three-method-valuation.md`.
- **GM taxonomy discipline** — there are 5 distinct GM concepts (consolidated / segment / sub-segment / analyst-modeled / marginal) and mixing them is the #1 cause of red-team rejection. Detail in `references/gm-taxonomy.md`.
- **Bear EPS bridge** — three-layer construction (soft adjustments / clean adjustments / strong adjustments) so the reader can see exactly which assumption is doing the work. Detail in `references/bear-bridge.md`.
- **What-would-reverse triggers** — every directional view (bear, bull, neutral) must have a falsification trigger with a numerical denominator: not "if margins recover" but "if 4Q segment GM > 18.5% on volume > X tons". Detail in `references/what-would-reverse.md`.

### Phase 3 — Construct headline + valuation

Output the institutional version of the opinion letter. The 12-section template lives in `templates/opinion-letter-section-checklist.md`. The non-negotiables:

- Headline contains: 12-month 中位 (target return), 情景加权 [low, high] range, 信号倾向 (multi-lebel, e.g. 中性轻偏空 / 中度偏空), 默认仓位动作 (持有/减仓/加仓), and **source-conditionality flag** if any anchor is S3 or weaker.
- Anchor weighting impact table: show how the headline shifts if the probability of the strongest scenario shifts by ±10pp. This is what gets challenged in IC; have it ready in the doc, not in your head.
- A0 tail risk mapping: for each tail event you identify, show its impact on (i) probability shift across the 5 scenarios, (ii) downside in the worst-case scenario. Detail in `references/tail-risk-mapping.md`.
- Volatility math + position sizing: σ → weekly/monthly/quarterly 1σ and 2σ envelopes; Sharpe and Kelly translated to a conviction-adjusted position size, not raw Kelly. Detail in `references/position-sizing.md`.

### Phase 4 — PM red-team review loop

This is the iteration that takes a memo from "looks good" to actually defensible. Score on the rubric in `references/pm-redteam-rubric.md`. Each pass should target a specific score band:

- **6.0-7.5**: math, sourcing, or structural bugs. Fix them.
- **7.5-8.5**: directional view holds but anchor weighting, GM taxonomy, or scenario bridges are inconsistent. Tighten.
- **8.5-9.0**: the memo is defensible but not airtight. Look for the issues PMs catch in IC: cross-section consistency, source-conditional headline language, "what would reverse" denominators, A0 mapping completeness.
- **9.0+**: ready for IC.

Run the **verification gates checklist** at the bottom of this file before claiming any score above 8.0. Most "round N" red-team passes find a gate violation. The two scripts in `scripts/` programmatically check the most-common failures.

### Phase 5 — Multi-audience derivatives

After the institutional version stabilizes, build the audience variants. Don't try to write them in parallel before the institutional version is locked — they all depend on the institutional headline and they will all need to be re-keyed if the institutional version moves.

- **IC pre-read (≤4 page concise)** — strip narrative; keep headline, scenario table, three-method reconcile, what-would-reverse, key risks. Do NOT change numbers; if a number changes here it must propagate back to institutional.
- **IC debate script** — verbal-form: company fundamentals → research methodology → logic chain → anchor evidence → valuation → caveats → 8 likely PM challenges with answers. Timing markers (3min / 5min / 10min variants).
- **Retail / 非专业版 + Q&A script** — full de-jargonification. The translation glossary is in `templates/retail-translation-glossary.md`. Headline numbers stay; framework language collapses to plain Chinese.

The full derivation patterns live in `references/multi-audience-delivery.md`.

## Verification gates (run before claiming any score above 8.0)

These are the gates a PM will check, mechanically. If any gate fails, the score caps at 8.0 regardless of how strong the narrative is.

1. **EPS × PE multiplicativity** — for every scenario row in every valuation table, verify EPS × PE = price (within rounding). Run `scripts/verify_eps_pe.py` against the structured representation.
2. **Segment GM reconciliation** — Σ(segment_revenue × segment_GM) / Σ(segment_revenue) within ±50bp of consolidated GM as reported. Run `scripts/verify_segment_gm.py`.
3. **SOTP monotonicity** — for every segment in the SOTP table, NI ≤ OP ≤ GP ≤ Revenue. Any inversion is an immediate fail.
4. **Scenario probabilities sum to 1.00** (allow ±0.01 for rounding display).
5. **Bear/bull EPS reconciles to base** — the bear bridge starts at base EPS, applies named adjustments, lands on bear EPS. Sum of adjustments must equal (base − bear) within rounding.
6. **Source tag declared at first use** — every specific number (revenue, GM, segment share, customer concentration, capacity, etc.) tagged S1-S5 or Pending at first appearance.
7. **Headline-conditionality matches anchor strength** — if any of the top-3 anchors is S3 or weaker, the headline contains conditional language ("source-conditional", "据公司披露", "若 [anchor] 兑现则"). If all top-3 are S1-S2, the headline can be unconditional.
8. **GM taxonomy box exists** — somewhere in the memo, the 5 GM types are explicitly defined and the doc declares which type each GM mention refers to.
9. **What-would-reverse has numerical denominators** — every trigger has a numerical threshold, not a directional handwave.
10. **Anchor sensitivity table exists** — the headline impact of a ±10pp probability shift on the strongest scenario is shown.

## When the user pushes back on a number, default to red-team mode

If the user's response includes any of: "where does X come from", "this doesn't reconcile", "the math is off", "I'm scoring this 7.x because…", "this is hand-wavy", "Pending should not be a headline anchor" — they are doing PM red-team. Switch to **fix-then-justify** mode:

1. Acknowledge the specific gate violation
2. Locate it in the source build script (file + section)
3. Fix the math/source/language
4. Rebuild the artifact
5. Report what changed and what gate it now passes
6. Do NOT defend the broken version — the user has already seen the bug and is testing whether you'll patch it cleanly or flinch

This is the loop that drove our 300699 memo from 8.6 → 9.0+ over Rounds 11-13 and the BOE memo from 6.5 → 8.8 over Rounds 1-10. The rubric for *which* fixes move the score how much is in `references/pm-redteam-rubric.md`.

## Output discipline

- All deliverables go in `<workspace>/outputs/`
- Build scripts (`build_<ticker>_<variant>.js`) live alongside outputs so the user can re-run them
- Use the shared docx helpers in `_docx_helpers.js` (column-width validation: every table must sum to PAGE_W=9000)
- Naming convention: `<ticker>_<variant>_谷泓毅.docx` for institutional+derivatives
- After each build, write the file using `buildDoc(D, headerText, outPath)` and verify it produced
- Provide `computer://` links for all artifacts so the user can open them

## References (load when needed)

- `references/source-stratification.md` — S1-S5 + Pending taxonomy, conditional language patterns
- `references/five-scenario-framework.md` — probabilistic scenarios, weights, EPS×PE construction
- `references/three-method-valuation.md` — EPS×PE / SOTP / multi-multiple reconciliation discipline
- `references/gm-taxonomy.md` — 5 GM types, segment reconciliation rules
- `references/bear-bridge.md` — three-layer EPS bridge construction
- `references/what-would-reverse.md` — trigger framework with numerical denominators
- `references/tail-risk-mapping.md` — A0 → probability shift → valuation impact mapping
- `references/pm-redteam-rubric.md` — scoring rubric, common bug catalog, score-band fixes
- `references/position-sizing.md` — σ math, Sharpe, Kelly, conviction adjustment
- `references/multi-audience-delivery.md` — institutional / IC / debate / retail derivation patterns

## Templates

- `templates/opinion-letter-section-checklist.md` — 12-section institutional memo structure
- `templates/ic-debate-script-template.md` — IC debate script with Q&A bank
- `templates/retail-translation-glossary.md` — jargon → plain Chinese translation map

## Scripts

- `scripts/verify_eps_pe.py` — checks every scenario row's EPS × PE = price within rounding
- `scripts/verify_segment_gm.py` — checks Σ(segment_revenue × segment_GM) / Σ(segment_revenue) ≈ consolidated GM within ±50bp
