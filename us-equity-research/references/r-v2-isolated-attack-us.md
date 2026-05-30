# R-v2 Isolated Adversarial Attack — Structural Independence Within Claude-Only Infrastructure

This file specifies how R-v2 is run as a *structurally independent* attacker against the declared consensus variances, rather than as an inline specialist sharing the orchestrator's context. It is the Sprint 3a (v0.4.0) tightening of the gap that v0.3.0's G20 left open: G20 verified that R-v2 *attempted* a structured attack per variance, but R-v2 was still running inside the orchestrator session, having read the analyst's own reasoning. An attacker that has already seen the defense's argument tends to rebut the framing, not the underlying claim. This file removes that contamination.

The isolation here is *structural*, not *cross-vendor*. The framework runs on Claude-only infrastructure — there is no GPT or Gemini second opinion, and none is required. Independence is achieved two ways: (1) a hard context partition — R-v2 is spawned as a subagent that receives only machine-readable variance claims and their cited evidence, never the narrative that justifies them; and (2) optional intra-family model diversity — the orchestrator may spawn R-v2 on a different Claude model than the one writing the memo (e.g., Sonnet attacker vs. Opus writer). Item 3 makes condition (2) load-bearing only for memos claiming a score above 9.0; condition (1) applies to every isolated run.

## The isolation gap this closes

Through v0.3.0, R-v2 ran in the same session as A-Consensus and the PM synthesis. Three contamination channels followed:

**Shared narrative.** R-v2 inherited the analyst's framing of each variance. When the framing is the weak point, R-v2 cannot see it — it is attacking a strawman of the analyst's own construction. An isolated R-v2 that sees only "FY27 GM 71.2% vs Visible Alpha median 73.8%, evidence_refs=[Q4 FY26 call, Q1 FY27 transcript]" must *reconstruct* the bridge from the citations. If its reconstruction diverges from the analyst's intended bridge, that divergence is itself a finding — the variance is under-specified.

**Pre-rebuttal anchoring.** Having read the rebuttal in advance (the PM brief already adjudicated R-v1 and the bull findings), an inline R-v2 produces attacks that are pre-answered. The attack and its rebuttal are written by the same context window in the same breath, so survival is mechanical, not earned.

**Effort leakage.** An inline R-v2 has the full memo in context and pattern-matches to "this looks thorough." Thoroughness of the *memo* is not evidence about the *variance*. Isolation forces R-v2 to rebuild the case from primary sources, which is exactly what an external red team does and exactly what makes its survival signal informative.

The design intent: the survival of a variance under *isolated* attack is a stronger signal than survival under inline attack, because the isolated attacker had every structural advantage to break it and could not.

## Where R-v2 sits in the pipeline

R-v2's structural position is the Phase 2 → Phase 3 boundary. The `consensus_variance` set is declared by A-Consensus in Phase 2 and locked by the Phase 2 PM synthesis (which marks each variance `load_bearing` true/false per `phase-2-continuation-us.md` §7b). The framework lists R-v2 among the Phase 3 agents (`phase-3-valuation-us.md`) because its output feeds A7's scenario weighting and the final synthesis. The v0.4.0 change is *how* R-v2 is dispatched — as an isolated subagent — not *when*. The orchestrator dispatches it once the variance set is locked, before the IC memo draft exists.

## Subagent spawn contract

The orchestrator dispatches R-v2 with the Task tool, `description="R-v2 isolated adversarial attack"`, no `subagent_type` (default general-purpose agent). The prompt is constructed from this file's template plus the structured payload below.

The R-v2 prompt MUST contain only:

- the structured `consensus_variance` JSON (the locked variance list from `source_tags.json`);
- the structured `source_tags.top_anchors` JSON (the top-3 anchors and their S-levels);
- the 5-point attack methodology (this file);
- the explicit adversarial framing and win condition (below);
- tool access to WebSearch, WebFetch, and EDGAR.

The R-v2 prompt MUST NOT contain:

- A-Consensus's narrative output (the prose reasoning behind the variances);
- the PM Synthesis brief (Integrated Brief v1 / v2 / v3);
- the bull-thesis narrative;
- the full IC memo draft (which does not yet exist at this boundary — the prohibition is belt-and-suspenders for refresh runs that re-spawn R-v2 after a draft exists).

The boundary is one sentence: **R-v2 sees claims and citations, never arguments.** A claim is a row of numbers with `evidence_refs`. An argument is the prose that says why the analyst believes the row. R-v2 must rebuild the argument from the citation and attack the rebuilt version.

```
TASK DISPATCH (orchestrator, Phase 2→3 boundary):

Task(
  description = "R-v2 isolated adversarial attack",
  prompt = render(r-v2-isolated-attack-us.md template, {
    ticker:                    {TICKER},
    consensus_variance_json:   {locked load_bearing variances, source_tags.json},
    source_tags_top_anchors:   {top_anchors block, source_tags.json},
    attacker_model_choice:     "claude-sonnet-4-6"   (default: cross-size vs Opus orchestrator)
  })
)

The subagent returns: a JSON array of adjudication_trail_entry objects
(type="variance_attack"), one per variance attacked. The orchestrator parses
the array and appends it to the memo's adjudication_trail.
```

## What R-v2 receives — the structured payload

Each `consensus_variance` entry handed to R-v2 carries: `variance_id`, `type` (1–5 per `consensus-variance-us.md`), `line_item`, `your_number`, `consensus_number`, `magnitude_pct`, `sizing_impact_pp`, `load_bearing`, and `evidence_refs[]` — each ref a citation with `s_level` and a retrievable `url` or full locator. R-v2 receives nothing else about the thesis. The `top_anchors` block tells R-v2 which anchors the headline rests on, so it prioritizes attacks on the load-bearing few rather than spreading thin.

Because R-v2 sees only this, A-Consensus must make each variance entry self-contained: every `evidence_ref` retrievable by URL or full citation, no implicit dependence on prose that R-v2 will not see (enforced in `phase-2-continuation-us.md` A-Consensus output discipline).

## The 5-point attack methodology

The canonical definitions live in `pm-synthesis-adjudication-us.md` §"R-v2 attack methodology". This section restates them in *execution* form for the isolated attacker. R-v2 must default to the strongest of these five for each variance type before considering an `other` attack. Each dimension below: what to attack, what rebuts the attack, what makes the attack survive.

### 1. Evidence credibility (`evidence_credibility`)

**What to attack.** Whether the cited S-level is as informative as the variance leans on it being. Pull the cited source and read it. An S3 transcript line that is formal CFO guidance on a numerical range is high-information; the same S3 tag attached to an off-the-cuff Q&A answer is closer to S4 in content. An S2 10-Q footnote with explicit disclosure is strong; an S2 8-K Item 7.01 press-release exhibit is medium. The attack is concrete: "the variance claims S2-grade evidence, but the cited locator is a press-release exhibit, not a financial-statement footnote — its informational content is S3 at best."

**What rebuts the attack.** A stronger source for the same numerical claim — a 10-Q footnote, prepared remarks rather than Q&A, an audited figure rather than a guided one. The analyst cites the harder source and the variance survives at its claimed strength.

**What makes the attack survive.** No stronger source exists, and the variance's `sizing_impact_pp` was computed assuming evidence strength the source does not carry. Outcome: `modified` (down-weight the variance to its true S-level and recompute sizing) or `conceded` if the down-weighted sizing falls below the 2.0pp load-bearing floor.

**Execution.** WebFetch the cited transcript or filing URL, locate the exact passage, and classify its true information content against the S1–S5 stack — do not accept the analyst's S-tag on faith. Worked example: V2 (FY27 GM 71.2% vs Visible Alpha 73.8%) cites a +8% Blackwell-to-Rubin ASP step to an "S3" transcript; the fetched page shows the figure was an analyst's number the CFO explicitly declined to confirm. True content is S4. If that step contributed −80bp of the −260bp GM bridge, removing it cuts variance magnitude by roughly a third and `sizing_impact_pp` falls proportionally — `modified`, and if the residual drops under 2.0pp, `conceded`. Record the fetch in `web_search_log` and increment `attacker_independent_source_reads`.

### 2. Triangulation completeness (`triangulation_completeness`)

**What to attack.** The variance usually claims "consensus has not incorporated this evidence." The counter-claim is that consensus *has* incorporated it and reached a different conclusion through legitimate disagreement — i.e., the variance is a disagreement, not an omission (anti-pattern #6 in `consensus-variance-us.md`). Search for a broker note or consensus revision dated within ~30 days of the cited source that discusses the same datapoint and concludes differently.

**What rebuts the attack.** Evidence that the contrary read misses a specific component — the broker note discusses the hyperscaler capex aggregate but not the procurement-mix split the variance turns on; the consensus revision predates the specific disclosure. The omission claim holds.

**What makes the attack survive.** A credible contemporaneous source reached the opposite conclusion from the same data. The variance is then a *reading*, not an omission; its edge claim collapses. Outcome: `modified` (reframe as a calibrated disagreement and resize down) or `conceded`.

**Execution.** WebSearch for broker notes, initiations, or consensus revisions dated within ~30 days of the cited source on the same line item; the test is whether the Street saw the datapoint, not whether it agreed. Worked example: a Type 1 revenue variance claims the Street has not weighted the MSFT/GOOGL/META/AMZN capex aggregate into datacenter GPU revenue; a search surfaces a sell-side note dated 12 days after the prints that bridges the same capex sum to a *higher* DC revenue number via a different attach-rate assumption. The "consensus has not incorporated this" claim fails — consensus incorporated it and disagreed on attach rate. Reframe as an attach-rate disagreement (which needs its own S1–S3 support) and resize; if none exists, `conceded`.

### 3. Base-rate sanity (`base_rate_sanity`)

**What to attack.** Most relevant to Type 4 (scenario-weight) variances. Reconstruct the analog set independently and check whether the proposed deviation magnitude is actually unusual. "Your scenario-weight variance prices the bull outcome at 12% vs Street-implied 30%; across the 12 analogous transitions I can find, 4 produced the bull outcome — base rate 33%, not 12%." R-v2 must build the analog set from primary or near-primary sources, not accept the analyst's.

**What rebuts the attack.** A defensible refinement of the analog set: "those 12 are not analogous because they predate the export-control regime; the structurally comparable subset is 4, of which 0 produced the bull outcome." The refinement must be specific and sourced, not a redefinition of convenience.

**What makes the attack survive.** The analyst's analog set is gerrymandered to the desired probability, and the honest base rate sits far from the declared weight. Outcome: `modified` (move the weight toward the base rate) or `conceded`.

**Execution.** Rebuild the analog set independently from primary sources — prior-cycle 10-Ks/10-Qs, historical transition prints — rather than inheriting the analyst's list, then compute the empirical outcome frequency. Worked example: a Type 4 variance prices the bull outcome at 12% vs a Street-implied 30%; the comparable-transition set reconstructed independently is 12 cases with 4 bull outcomes (33%). If the analyst cannot defend a narrower truly-analogous subset with a specific structural reason (regime change, different capital intensity), move the weight toward 33%. A 12%→~25% shift can move the headline scenario probabilities by more than the variance's declared `sizing_impact_pp`, so the resize is material, not cosmetic.

### 4. Catalyst dependency (`catalyst_dependency`)

**What to attack.** Most relevant to Type 5 (timing) variances. Does the variance require a specific event to play out exactly as described, on a path the analyst assumed linear? "Your variance assumes the Pioneer synergy run-rate hits $3B by Q2 FY28 on a linear ramp from $0.7B in Q1 FY26 — what is the probability the ramp is front- or back-loaded, and what does a back-loaded path do to the dividend-coverage scenario the sizing depends on?"

**What rebuts the attack.** Specific management commentary on the ramp shape, a disclosed integration milestone schedule, or a contractual trigger that pins the timing. The catalyst dependency is bounded and disclosed.

**What makes the attack survive.** The path is assumed, not disclosed, and a plausible non-linear path materially compresses the sizing. Outcome: `modified` (attach an explicit non-linearity haircut) or `conceded` if the timing is the entire variance and it cannot be pinned.

**Execution.** WebFetch the integration/milestone disclosures (8-K Item 1.01, investor-day decks, CFO ramp commentary) and test the shape, not just the endpoint. Worked example: a $0.7B→$3B synergy run-rate is assumed linear over nine quarters; the disclosed milestone schedule is back-loaded, with most synergies landing after year-2 system integration. A back-loaded path pushes the run-rate past the dividend-reset decision date, which is exactly where the bull-case NPV concentrates. Attach an explicit timing haircut to the bull weight and resize; if the timing claim *is* the variance and no disclosure pins the date, `conceded`.

### 5. Timing arbitrage (`timing_arbitrage`)

**What to attack.** Whether consensus is genuinely missing this or has priced it through a mechanism fundamental sell-side notes do not track — implied-vol term structure, options gamma, prime-broker positioning, short-borrow rates, single-stock skew. "The bear scenario you say Street is under-pricing is visible in the 3-month 25-delta put skew, which implies ~35% probability of that move — the derivatives market already prices what you claim the fundamental notes miss."

**What rebuts the attack.** A reason the derivative pricing reflects different risk than the fundamental thesis — the skew prices a macro/liquidity event, not the company-specific catalyst; the borrow rate reflects index-arb flow, not directional conviction. The fundamental edge is distinct from the priced derivative risk.

**What makes the attack survive.** The variance is real on the fundamental side but already priced elsewhere in the capital structure, so its incremental edge for a fundamental position is small. Outcome: `modified` (resize down for the already-priced component) — rarely `conceded`, because the fundamental claim may still be correct, just not differentiated.

**Execution.** Pull the options surface (3-month 25-delta put/call skew), the single-name short-borrow rate, and any 13F or prime-broker positioning color, then compare the derivative-implied probability to the analyst's. Worked example: a variance says the Street under-prices a bear catalyst at 5% vs the analyst's 35%; the 25-delta put skew already implies ~30%. Unless the skew is explained by a distinct macro or liquidity risk rather than the company-specific catalyst, the edge is mostly priced — resize down for the priced component while preserving the fundamental claim. This dimension most often yields `modified`, because "already priced in derivatives" rarely means "fundamentally wrong."

## Win condition specification

R-v2's prompt states the success criterion explicitly:

> Your success criterion is to find at least one attack point per load-bearing variance, with documented evidence supporting the attack. A run that concludes "the variances look reasonable" or "no specific weaknesses identified" is FAILED. Your incentive is to find what the analyst missed.

This is deliberate incentive design. A red team rewarded for agreement produces agreement. R-v2 is rewarded for finding the specific dimension on which each variance is weaker than claimed. A "modified" or "conceded" outcome is a *successful* R-v2 run; a blanket "rebutted, all variances survive" is the suspicious outcome and should be scrutinized (see Calibration).

## Independent source re-verification requirement

For each attack point, R-v2 must independently pull at least one source document — WebFetch on the cited URL, or WebSearch for the specific `evidence_ref` — and quote the exact passage it is attacking or rebutting with. R-v2 may not attack a citation it has not opened. Every such call is recorded in the manifest's `web_search_log` (schema: `tool`, `query_or_url`, `timestamp`; see `schemas/manifest.json`). The count of independent reads R-v2 made for a given variance is recorded on the attack entry as `attacker_independent_source_reads`, which lets the verifier and the PM distinguish a thorough attack (≥3 independent reads) from a shallow one.

## Bounded context window

R-v2's prompt is bounded to roughly 30–50K tokens of structured inputs plus its own tool use. The bound is a feature, not a constraint to be worked around: it forces R-v2 to be selective and attack the 3–4 load-bearing variances hard rather than 20 thinly. A red team that spreads one paragraph of doubt across every variance produces no usable signal; a red team that pulls four sources to break one variance produces a finding. The `top_anchors` payload tells R-v2 where the headline's weight actually sits so the selection is principled.

## Output schema

R-v2 returns one `adjudication_trail_entry` per variance attacked (schema in `schemas/memo.json` `definitions/adjudication_trail_entry`). Each entry:

- `type` = `"variance_attack"`
- `target_variance_id` = the attacked variance's `variance_id`
- `attack_type` ∈ {`evidence_credibility`, `triangulation_completeness`, `base_rate_sanity`, `catalyst_dependency`, `timing_arbitrage`} (or `other` for a documented additional dimension; G20 may down-weight `other`)
- `attack_description` = what R-v2 specifically attacked, with the quoted passage
- `attack_outcome` ∈ {`rebutted`, `modified`, `conceded`}
- `supporting_evidence_refs` = the citations R-v2 pulled (required when `rebutted`)
- `attacker_model` = the model the orchestrator spawned R-v2 on (v0.4.0 field)
- `attacker_context_isolation` = `true` when R-v2 ran as an isolated subagent per this contract (v0.4.0 field)
- `attacker_independent_source_reads` = count of WebFetch/WebSearch calls R-v2 made for this variance (v0.4.0 field)

The three `attacker_*` fields are added to `adjudication_trail_entry` in Sprint 3a Item 2; they are optional and additive, so pre-v0.4.0 memos validate unchanged.

```json
{
  "entry_id": "AT4",
  "type": "variance_attack",
  "phase": 3,
  "target_variance_id": "V2",
  "attack_type": "evidence_credibility",
  "attack_description": "V2 (FY27 GM 71.2% vs VA 73.8%) cites the Blackwell-to-Rubin +8% ASP step to a Q4 FY26 Q&A answer, tagged S3. The pulled transcript shows the figure was an analyst's number the CFO declined to confirm, not guidance. Informational content is S4, not S3.",
  "attack_outcome": "modified",
  "supporting_evidence_refs": [
    {"s_level": "S3", "url": "https://...q4fy26-transcript", "locator": "Q&A, 47:30"}
  ],
  "attacker_model": "claude-sonnet-4-6",
  "attacker_context_isolation": true,
  "attacker_independent_source_reads": 2
}
```

## Failure modes and remediation

**R-v2 spawn fails.** The orchestrator retries once; on a second failure it does not silently skip the attack. It records the failure in `orchestrator_notes` and treats every load-bearing variance as un-attacked — which propagates to the demotion path below.

**R-v2 returns "no attack points found" on a load-bearing variance.** This is not variance strength; under the win condition it is a failed attack. The orchestrator flags that variance `load_bearing = false` (or removes it from the load-bearing set). The structural consequence is intentional: a variance that no isolated red team can find a specific weakness in is, by construction, either genuinely defensible *or* so vague that no specific dimension bites — and a variance that cannot be attacked on any of the five dimensions is decorative or unfalsifiable. Both should be demoted, not credited.

**G15 may then fail.** Demoting variances can leave the memo without a load-bearing variance carrying adequate S1–S3 evidence. If so, G15 fails and the non-Hold rating is no longer supportable — the analyst must either surface a real variance with real evidence or accept the consensus-anchored Hold. This is the enforcement loop the isolation is for: it pushes back on manufactured edge rather than rubber-stamping it.

## Interaction with the gates

**G20 (graduated rigor, Item 3).** Memos claiming a score in (8.5, 9.0] run the v0.3.0 G20 conditions unchanged. Memos claiming a score above 9.0 additionally require `attacker_context_isolation == true` and `attacker_model != writer_model` on at least one surviving (`rebutted`/`modified`) `variance_attack` entry. The graduated scale means isolation is the price of the top of the rubric, not a blanket requirement.

**G15 (consensus variance).** Interacts via the demotion path above — isolated R-v2 can knock a variance out of the load-bearing set and thereby fail G15 downstream.

## Calibration

Honest base rates for an isolated R-v2 run:

- Variance survival under isolated attack should be **no higher** than under the old inline attack, and usually lower. Isolation gives the attacker every structural advantage; if survival *rises* under isolation, the attacker is not using the advantage and the run is suspect.
- A run that returns `rebutted` on every variance with `attacker_independent_source_reads` of 0–1 per entry is a shallow pass — re-spawn with the win condition re-emphasized.
- Expect 1–2 `modified` or `conceded` outcomes per non-trivial name. Zero concessions across a coverage list means the discipline is decorative.
- `attacker_independent_source_reads` ≥ 3 on the variances that survive is the signal that survival was earned, not assumed.

## Cross-references

- `pm-synthesis-adjudication-us.md` — canonical 5-point attack methodology + adjudication_trail schema discipline
- `consensus-variance-us.md` — variance taxonomy (types 1–5), evidence matrix, sizing rule, load-bearing floor
- `phase-2-continuation-us.md` — A-Consensus specialist; variance set declaration and self-containment requirement
- `phase-3-valuation-us.md` — R-v2 dispatch point and final synthesis integration
- `schemas/memo.json` `definitions/adjudication_trail_entry` — machine-readable output schema (attacker_* fields added Item 2)
- `schemas/manifest.json` `web_search_log` — where R-v2's independent source reads are logged
- Plugin 2 `scripts/verify_view_defensibility.py` — G20 verifier; graduated rigor scale added Item 3
