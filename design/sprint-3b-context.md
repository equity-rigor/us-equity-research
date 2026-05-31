# Sprint 3b Context — Provable Adversarial Isolation (manifest 0.4.0)

DRAFT for review (Hongyi). Authored 2026-05-31 as the follow-up to the v0.4.0
post-ship review. This file is the contract for Sprint 3b in the same sense
`design/sprint-3a-context.md` was for 3a: a self-contained briefing a scheduled
or interactive session can execute item-by-item. Nothing here is scheduled yet —
creating the scheduled task is a deliberate user action, not assumed by this
draft.

## Why 3b exists — the gap 3a left open

Sprint 3a (v0.4.0) made R-v2 a *structurally independent* attacker by design:
spawn it as an isolated subagent that sees claims-not-arguments, run it under a
different model than the writer, and let G20's graduated rigor scale demand that
isolation for any score claim above 9.0. The design is sound. The **enforcement
is honor-system**: G20 reads three self-reported values off the memo JSON —
`attacker_context_isolation` (bool), `attacker_model` (string), and the writer
model from `memo_metadata.author_model` — and nothing proves an isolated subagent
ever ran. A memo can stamp `attacker_context_isolation: true`,
`attacker_model: "claude-sonnet-4-6"`, `author_model: "claude-opus-4-8"` with R-v2
having run inline, or not having run at all, and clear the 9.0+ tier.

The v0.4.0 review also surfaced that the version bump *removed* the one provenance
backstop the isolation design points at: `verify_provenance_manifest.py` (G19)
gated on the literal `schema_version != "0.3.0"`, so it silently skipped every
v0.4.0 memo — no manifest, no `web_search_log` floor, no on-disk hash integrity
check. That is fixed as Item 0 below (already landed in commit `009a566`), which
is the precondition for everything else here: cross-checking isolation against the
manifest is meaningless if the manifest gate does not run.

Sprint 3b closes the loop: make the isolation claim **reconcile against the
provenance manifest**, which is itself hash-integrity-checked. The 9.0+ tier stops
trusting the memo's self-report and starts requiring the self-report to match an
independently-written, hash-pinned dispatch record and the attacker's logged web
reads.

## Threat model — be honest about the ceiling

This sprint is not cryptographic attestation and must not be sold as such. The
manifest header already concedes "a determined adversary can forge a consistent
fake manifest." What provenance cross-check actually buys:

- **Defends against lazy / accidental non-isolation.** The common real failure is
  an orchestrator that ran R-v2 inline (or skipped it) but stamped
  `isolation: true` because the template told it to. Reconciliation against a
  dispatch record the orchestrator had to assemble — with R-v2's web reads logged
  under `used_by_agent: "R-v2"` and hash-pinned — makes the lazy path fail loudly.
- **Defends against post-hoc memo editing.** G19's existing on-disk sha256 check
  catches a memo whose isolation fields were edited after the run.
- **Raises the cost of a deliberate false claim** from "type `true`" to "fabricate
  a hash-consistent manifest with a fake dispatch record and fake R-v2 web-read
  entries that survive the cross-check" — materially harder, and the kind of thing
  a PM diffing the manifest will notice.

What it does **not** buy: defense against a determined forger who builds the whole
consistent fake. The only true fix is a dispatch ledger written by the runtime/
harness that the orchestrator cannot author directly (subagent id + bounded-context
trace emitted by the Task tool itself). That is infra beyond a plugin sprint;
flag it in the wrap notes as the standing ceiling, do not pretend 3b reaches it.

## Versioning and schema strategy

- **Plugin bump: v0.4.0 → v0.5.0** (minor; additive schema + new enforcement on
  the 9.0+ tier).
- **`manifest.json`: `manifest_version` `const "0.3.0"` → `enum ["0.3.0","0.4.0"]`.**
  This is the first manifest structure change since v0.3.0, so the enum
  grandfathering pattern starts here. v0.3.0 manifests continue to validate and to
  pass G19 unchanged. The new `adversarial_isolation` block and writer-model field
  are **additive and optional** so a 0.3.0 manifest is still valid 0.4.0-clean.
- **`memo.json` `schema_version` stays `0.4.0`** (the `attacker_*` fields already
  landed in Sprint 3a Item 2; no new memo fields needed). The cross-check is gated
  on the *manifest* carrying isolation provenance, not on a memo version bump —
  see Item 3's graceful-migration rule.
- `write_manifest.py` `MANIFEST_VERSION` becomes a function of whether an isolation
  block is present: emit `"0.4.0"` when the seed carries `adversarial_isolation`,
  else `"0.3.0"` for backward-identical output.
- All four memo-side schema_version enums already include `0.4.0`; no change.

## Universal constraints (inherit from Sprint 3a — unchanged)

- Schema changes additive-only with enum grandfathering. v0.1.x / v0.2.0 / v0.3.0 /
  v0.4.0 memos and v0.3.0 manifests must validate clean against the 3b schemas.
- New verifier logic uses the pydantic optional-import shim (try/except
  ModuleNotFoundError). The two verifiers 3b touches (`verify_provenance_manifest.py`,
  `verify_view_defensibility.py`) are stdlib-only today; keep them importable on a
  bare interpreter so their tests run without `/tmp/pylibs`.
- Smoke + committed pytest for every verifier change, multiple branches per gate
  (pass / fail / n_a / grandfathered). 3a shipped a one-line skip bug precisely
  because G18/G19/G20 had no committed tests; 3b does not repeat that — every gate
  change lands with its `test_*.py` in the same commit.
- Heredoc-to-file commit messages (`cat > /tmp/v0.5.0-itemN-msg.txt << 'EOF'` then
  `git commit -F`). Never multi-line `git commit -m`.
- No inline `#` comments in copy-paste shell blocks (user's zsh treats `#` as a
  command).
- **Path A (binding): scheduler/sandbox commits locally and does NOT push.** The
  user pushes accumulated commits manually. The repo mount denies `unlink` on
  `.git/*`; use a uniquely-named alt index on the root fs (`GIT_INDEX_FILE=/tmp/
  ueridx.$(date +%s%N)`; the PID is always 2 in the sandbox so `$$` collides —
  do not use it), rename-aside stale `.git/*.lock`, `git read-tree HEAD`, add only
  explicit deliverable paths, gate the commit on "exactly N staged", `git commit -F`.
  Verify with `git rev-parse main` + `git cat-file`, not `git status` (the real
  `.git/index` is chronically stale from alt-index commits and shows illusory `MM`).
- Red-team voice in commits and docs. State what landed and what stays loose.

## Items

### Item 0 — G19 v0.4.0 fix + first G18/G19/G20 tests (LANDED, commit `009a566`)

Recorded here so this file is the source of truth. `verify_provenance_manifest.py`
now gates on `RUNNABLE_SCHEMA_VERSIONS = {"0.3.0","0.4.0"}`; v0.4.0 memos run G19
again (manifest required, hash integrity enforced). First committed coverage added:
`test_verify_provenance_manifest.py` (7 cases incl. the v0.4.0-not-skipped
regression guard and a hash-tamper case) and `test_verify_view_defensibility.py`
(12 cases promoting the uncollected G20 smoke into the suite). pytest 217 (198 +
19). This is the precondition for Items 1–3.

### Item 1 — manifest 0.4.0 schema: adversarial-isolation provenance block

**Deliverable 1a.** Extend `schemas/manifest.json`:

- `manifest_version`: `const "0.3.0"` → `enum ["0.3.0","0.4.0"]`.
- New optional top-level object `adversarial_isolation` (present iff R-v2 ran
  isolated), `additionalProperties: false`, with:
  - `writer_model` (string, required within the block) — the model that ran
    A-Consensus / authored the memo. This is the manifest-side anchor for the
    diversity check, currently only in `memo_metadata.author_model`; recording it
    in the hash-pinned manifest is what makes the inequality non-self-serving.
  - `dispatches` (array, minItems 1) of dispatch records, each
    `additionalProperties: false`:
    - `subagent_dispatch_id` (string) — Task-tool invocation id / handle.
    - `attacker_model` (string) — model the subagent ran under.
    - `context_isolation` (boolean, must be true to count).
    - `context_token_budget` (integer) — the bounded window (30–50K per
      `r-v2-isolated-attack-us.md`).
    - `inputs_included` / `inputs_excluded` (arrays of enum strings) — declares the
      claims-not-arguments partition actually used (e.g. excluded:
      `["a_consensus_narrative","pm_synthesis_brief","bull_thesis","memo_draft"]`).
    - `target_variance_ids` (array of strings) — which variances this subagent
      attacked.
    - `web_reads` (integer ≥ 0) — count of WebFetch/WebSearch the subagent made,
      which must reconcile with `web_search_log` entries tagged to it.
    - `timestamp` (date-time).
- Reuse the existing `web_search_log` `used_by_agent` field: R-v2's reads are
  logged with `used_by_agent: "R-v2"`, `phase: 3`. No schema change to
  `web_search_entry` needed (it already has `used_by_agent` + `response_hash`).

**Deliverable 1b.** Update `schemas/manifest.json` top `description` to document the
0.4.0 additions and explicitly restate the non-cryptographic threat model (do not
let the schema oversell the guarantee).

**Deliverable 1c.** Confirm grandfathering: a committed v0.3.0 manifest (e.g. the
existing `outputs/*_*.json` provenance fixtures, if any, or a synthetic one)
validates clean against both the pre- and post-edit `manifest.json`.

Commit: `"Sprint 3b Item 1: manifest 0.4.0 adversarial-isolation provenance block (additive, grandfathered)"`

### Item 2 — orchestrator wiring: write the dispatch record + tag R-v2 web reads

**Deliverable 2a.** `scripts/write_manifest.py`: accept an `adversarial_isolation`
key in the seed; when present, emit `manifest_version: "0.4.0"` and pass the block
through; when absent, emit `"0.3.0"` (byte-identical to today). Assemble R-v2
`web_reads` counts by filtering `web_search_log` on `used_by_agent == "R-v2"` and
cross-foot against each dispatch's declared `web_reads` (warn on mismatch).

**Deliverable 2b.** `us-equity-research/SKILL.md` Phase 3 R-v2 dispatch subsection
(added in Sprint 3a Item 4): add the instruction that the orchestrator, after the
isolated R-v2 subagent returns, records a dispatch entry into the manifest seed and
logs the subagent's web reads under `used_by_agent: "R-v2"`. The `attacker_model`,
`context_isolation`, and `attacker_independent_source_reads` it writes onto the
memo's `variance_attack` entries MUST equal what it writes into the manifest
dispatch record — they are the same facts in two places, and Item 3 fails the memo
if they disagree.

**Deliverable 2c.** `references/r-v2-isolated-attack-us.md`: update the "Independent
source re-verification" and "Output schema" sections to state that the attacker's
web reads are logged to the manifest and are the cross-check substrate for G20 9.0+
(today the doc claims this cross-check exists via G19; 3b makes it real).

Commit: `"Sprint 3b Item 2: orchestrator wiring to record R-v2 dispatch + tag attacker web reads in the manifest"`

### Item 3 — G20 9.0+ cross-check against the manifest (the load-bearing item)

**Deliverable 3a.** `verify_view_defensibility.py` takes an optional
`--manifest-json` argument (uniform calling contract: accept and ignore if a caller
does not pass it, like the existing optional `--source-tags-json`). For a memo
claiming a score strictly above 9.0 whose referenced manifest is
`manifest_version == "0.4.0"`:

- The surviving isolated `variance_attack` whose `attacker_context_isolation == true`
  must have a matching `adversarial_isolation.dispatches[]` record with the same
  `attacker_model` and `context_isolation == true`.
- `attacker_model != adversarial_isolation.writer_model` (the diversity check now
  reads the manifest-side writer model, not just `memo_metadata.author_model`; if
  the two writer-model sources disagree, fail — that disagreement is itself a
  provenance smell).
- `attacker_independent_source_reads` on the memo entry must be ≤ the count of
  `web_search_log` entries with `used_by_agent == "R-v2"` (the attacker cannot
  claim more independent reads than the manifest logged).

**Deliverable 3b — graceful migration rule.** If the memo claims > 9.0 but the
manifest is `0.3.0` (no isolation block) OR no manifest is supplied: do NOT hard-pass
on the self-reported fields and do NOT silently skip. Emit `status: fail`,
`blocks_score_above: 9.0`, reason "9.0+ claim requires manifest 0.4.0 isolation
provenance; self-reported attacker fields are insufficient under v0.5.0." This is
the whole point — it removes the honor-system path for the top tier while leaving
the 8.5–9.0 band entirely unchanged (still earned by the v0.3.0 conditions, no
manifest required).

**Deliverable 3c — smoke + committed tests, ≥ 8 branches.** Extend
`test_verify_view_defensibility.py`:
- > 9.0 claim, manifest 0.4.0, matching dispatch + diverse model + reads reconcile → pass.
- > 9.0 claim, manifest 0.4.0, dispatch `attacker_model` ≠ the memo entry's `attacker_model` → fail (provenance mismatch).
- > 9.0 claim, manifest 0.4.0, dispatch model == writer_model → fail (diversity).
- > 9.0 claim, manifest 0.4.0, `attacker_independent_source_reads` > logged R-v2 reads → fail (inflated reads).
- > 9.0 claim, manifest 0.3.0 (no block) → fail, cap 9.0 (graceful-migration rule).
- > 9.0 claim, no `--manifest-json` supplied → fail, cap 9.0.
- ≤ 9.0 claim (e.g. 8.7), any manifest → unchanged pass (8.5–9.0 band untouched).
- v0.3.0 memo → unchanged (graduated check n_a).

Commit: `"Sprint 3b Item 3: G20 9.0+ tier reconciles isolation fields against the hash-pinned manifest (removes honor-system top tier)"`

### Item 4 — harden model-diversity + sweep stale gate counts (debt paydown)

**Deliverable 4a.** Replace G20's literal-string diversity test with a normalized
compare so cosmetic suffixes do not buy diversity: strip trailing qualifiers
(`-with-extended-thinking`, whitespace, casing) before comparison so
`"claude-opus-4-8"` vs `"claude-opus-4-8-with-extended-thinking"` is NOT diverse,
while `"claude-opus-4-8"` vs `"claude-sonnet-4-6"` is. Keep it a string-family
heuristic (no semver parse); document that intra-family diversity (Opus vs Sonnet)
is the floor and cross-vendor is out of scope by design (Claude-only infra).

**Deliverable 4b.** Sweep the stale gate-count rot the review flagged: Plugin 2
SKILL.md frontmatter `description` still says "Enforces the 14 verification gates"
and lists only G1–G14; Plugin 1 SKILL.md says "17-gate" / "14 gates"; README mixes
"20" / "all 17" / "14-gate". Reconcile every human- and model-facing count to the
actual G1–G20 in `verification_gates.json`. The Plugin 2 description omission is
load-bearing (it drives skill triggering and the model's own sense of what to run),
fix it first.

Commit: `"Sprint 3b Item 4: normalize G20 model-diversity check + reconcile stale gate counts to G1-G20"`

### Item 5 — wrap + ship v0.5.0

- Bump both `.claude-plugin/plugin.json` 0.4.0 → 0.5.0.
- `CHANGELOG.md` v0.5.0 entry: provable isolation, manifest 0.4.0, G20 cross-check,
  diversity hardening, gate-count sweep, and the honest threat-model ceiling.
- `README.md`: document the 9.0+ manifest requirement under the graduated rigor
  description; version badge → 0.5.0; gate count stays 20.
- Run pytest (install pytest+pydantic to `/tmp/pylibs`, `PYTHONPATH=/tmp/pylibs`,
  `--basetemp=/tmp/...` since `/sessions` overlay is full). Target ≥ 217 + new 3b
  tests, all green. If regression, fix or set `blocked`.
- Tag `v0.5.0` LOCALLY only (Path A). Do NOT push. Record `pending_user_push`.

Commit: `"v0.5.0 Sprint 3b: provable adversarial isolation via manifest cross-check"` (heredoc-to-file).

## Acceptance criteria

1. A v0.4.0/0.5.0 memo claiming > 9.0 cannot pass G20 on self-reported isolation
   fields alone — it must carry a manifest 0.4.0 with a reconciling dispatch record,
   a manifest-side writer model distinct from the attacker model, and R-v2 web reads
   ≥ the claimed independent-read count.
2. The 8.5–9.0 band and all of G1–G19 behavior are byte-for-byte unchanged for
   existing memos. Grandfathering proven for v0.3.0 manifests and pre-0.4.0 memos.
3. Every verifier change ships with committed `test_*.py` in the same commit; full
   pytest green before the v0.5.0 tag.
4. Docs (SKILL frontmatters, README, manifest schema description) state the count
   (G1–G20) consistently and state the isolation guarantee honestly (reconciliation,
   not attestation).

## What 3b explicitly does NOT do

- It does not attack the consensus *baseline* (R-v2 still attacks deviations from
  consensus, not whether consensus itself is correlated-wrong). That is a separate,
  larger design question — candidate for a future sprint, noted in the review.
- It does not reach runtime-attested isolation (a dispatch ledger the orchestrator
  cannot author). 3b is reconciliation against a self-assembled but hash-pinned and
  cross-footed manifest — a real increase in the cost of a false claim, not a proof.

## Cross-references

- `design/sprint-3a-context.md` — the 3a contract this extends; same execution pattern.
- commit `009a566` — Item 0 (G19 v0.4.0 fix + first G18/G19/G20 tests).
- `scripts/verify_provenance_manifest.py` — G19, now runs on v0.4.0.
- `scripts/verify_view_defensibility.py` — G20, the verifier Item 3 extends.
- `schemas/manifest.json` — the schema Item 1 bumps to 0.4.0.
- `us-equity-research/references/r-v2-isolated-attack-us.md` — the isolation contract
  whose claimed G19 cross-check Item 3 finally makes real.
