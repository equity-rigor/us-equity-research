---
name: Feature request
about: Propose a new gate, schema field, reference file, or methodology addition
title: '[Feature] '
labels: enhancement
assignees: ''
---

## What problem does this solve?

A real failure mode the current framework misses, OR a real-world IC memo defect that should be catchable but isn't. Be specific — "the framework should be more rigorous" is not actionable.

Example of a useful framing: "Memos that anchor a non-Hold rating on transcript-only S3 evidence pass G15 but produce weak conviction. Add a gate that further discriminates S3-only variances from S1/S2-backed variances."

Example of a non-actionable framing: "The framework should handle X better."

## Proposed change category

- [ ] New verification gate (with verifier script)
- [ ] Schema field addition (additive-only, with grandfathering)
- [ ] Reference file methodology
- [ ] Orchestrator instruction (SKILL.md)
- [ ] Sister plugin (for paid-data integration, separate repo)
- [ ] Other (specify)

## Sketch of the methodology

How would the gate / field / reference work? What's the verifier check? What's the failure mode it catches?

## Backward compatibility

How does this preserve the additive-only schema policy and the grandfathering pattern? Pre-existing memos at v0.1.x / v0.2.0 / v0.3.0 / v0.4.0 must continue to validate clean against any new schema.

## What gate would verify it?

If you propose new methodology, what programmatic check would Plugin 2 add? Manually-verified discipline is acceptable but a verifier script is preferred.

## Honest scoping

- Is this addressable within Plugin 1 / Plugin 2, or does it require a sister plugin with paid data feeds?
- Does this require empirical calibration (backtest) that the framework currently lacks?
- If yes to either, where on the roadmap should this live?

## Additional context
