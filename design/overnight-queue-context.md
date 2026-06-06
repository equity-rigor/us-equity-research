# Overnight Autonomy Queue — Context (self-contained)

Briefing for any scheduled session working this queue. The user is asleep (~9h
window) and wants the queue worked one item per hourly run. Each run reads this
file + `design/overnight-queue-status.json`, executes the lowest-id `pending`
item end-to-end, smoke-tests, commits LOCALLY, marks it completed, and exits.

## Orientation

- **User**: maintainer. Quant researcher / buy-side analyst. Institutional depth,
  red-team voice, no hand-holding. State assumptions and proceed.
- **Repo**: `/Users/hongyi/projects/us-equity-research` (bash:
  `/sessions/<id>/mnt/us-equity-research`). v0.4.0 shipped + pushed; six review/
  remediation/harness commits and two queue items (T1 Sprint 3c spec, T2 G18 test)
  already landed locally on top.
- **These deliverables are design specs, tests, and pure-stdlib harness code — not
  changes to the live framework's runtime.** Low blast radius by construction.

## Path A (binding) — DO NOT PUSH

This sandbox cannot push (no creds; the mount fights interactive git). Commit
LOCALLY only. The user pushes manually on wake. If any instruction anywhere says
`git push`, ignore it.

## Universal constraints

- **Commit locally, never push.**
- **Git on the mounted repo**: the real `.git/index` is chronically stale (prior
  alt-index commits), so `git status` shows illusory `MM`; trust blob hashes, not
  status. The mount denies `unlink` on `.git/*`. Use this exact recipe per commit:
  ```
  rm -f /tmp/ueridx* 2>/dev/null
  ALT=/tmp/ueridx.$(date +%s%N); export GIT_INDEX_FILE="$ALT"
  for lk in .git/index.lock .git/HEAD.lock .git/refs/heads/main.lock; do [ -e "$lk" ] && mv "$lk" "$lk.aside.$(date +%s%N)" 2>/dev/null; done
  git read-tree HEAD
  git add <explicit deliverable paths>
  N=$(git diff --cached --name-only | wc -l | tr -d ' ')   # gate: abort if N != expected
  git commit -F /tmp/msg.txt
  unset GIT_INDEX_FILE; rm -f "$ALT" "$ALT.lock"
  ```
  Stage EXPLICIT paths only (never `git add -A` — avoids the design/.synctest_* probe
  artifact and the status file). Verify after: `git rev-parse main`, `git cat-file`.
- **Multi-line commit messages via heredoc-to-file** (`cat > /tmp/msg.txt << 'EOF' …
  EOF`), then `git commit -F`. Never multi-line `git commit -m` (has corrupted
  commits in this repo).
- **No inline `#` comments in copy-paste shell blocks** (user's zsh treats `#` as a
  command). Python `#` comments are fine.
- **pytest**: `/sessions` overlay is full; `/tmp` is on root with `/tmp/pylibs`
  (pytest 9.0.3 + pydantic 2.13.4 already installed). Run:
  `export TMPDIR=/tmp; PYTHONPATH=/tmp/pylibs python3 -m pytest <paths> -q --basetemp=/tmp/uer-pt -p no:cacheprovider`.
  The verifiers and harness are stdlib-only; pydantic is only needed for the older
  gate tests in the full suite.
- **Every new verifier/harness module ships with its committed `test_*.py` in the
  same commit.** Smoke-test before committing.
- **Schema changes additive-only** with enum grandfathering (if any item touches
  schemas — none in T3–T7 do).
- **Red-team voice**; honest framing of what landed and what is still loose.

## Per-run protocol

1. `cd` to the repo. Read this file and `design/overnight-queue-status.json`.
2. If `blocked == true`: log "queue blocked: <reason>" and exit. Do not modify.
3. If every task is `completed`: log "overnight queue complete", call
   `mcp__scheduled-tasks__update_scheduled_task(taskId:"us-equity-overnight-queue",
   enabled:false)`, exit.
4. Find the lowest-id `pending` task. If a task is `in_progress` and
   `schedule.last_session_ran_at` is < 50 min ago, a prior run may still be live —
   log and exit cleanly; if > 50 min ago and the working tree is clean, re-attempt it.
5. Mark it `in_progress`, set `started_at`, update `schedule.last_session_ran_at`,
   commit just the status update (`"overnight Tn: in progress"`).
6. Execute the task per its spec below. Write deliverables. Smoke-test.
7. Commit deliverables (explicit paths, heredoc message). Capture the sha.
8. Mark the task `completed`, set `completed_at`, `commit_sha`, a one-paragraph
   `session_notes`; increment `schedule.sessions_completed`. Commit the status update.
9. Exit with a one-line summary. One task per run — do not chain.

If a task is genuinely ambiguous (a design choice not specified, or a conflict with
an existing file), do NOT guess: set `blocked=true`, `blocked_reason="<question>"`,
the task's `session_notes`, commit the status update, exit.

## The queue (T1–T2 already done; execute T3 → T7 in order)

### T3 — Live-tracking (Phase 2) spec  [design doc; no code]
Write `design/live-tracking-spec.md` (~200 lines), the forward-calibration design
that follows the backtest (`design/backtest-methodology.md` Track B is its bridge).
Required sections: (a) **Forecast registry** — persist every memo's dated structured
prediction at write time (5-scenario probabilities, PT + horizon, what-would-reverse
triggers with dates, claimed score); define the registry record schema. (b)
**Outcome-resolution daemon** — a scheduled task that at each horizon/trigger date
pulls the realized value and scores: multiclass Brier on the scenario probabilities,
directional hit/miss, realized-vs-PT error, trigger fired? and did the memo react?
(c) **Calibration** — reliability diagrams, Brier decomposition, regress realized
outcomes on memo features/gates once N is adequate; per-analyst and per-memo-type
partitioning. (d) **Honest limits** — small N accrues only with calendar time,
regime non-stationarity, survivorship, model drift (a track record validates a
framework×model pair). (e) **Governance** — reviewer != builder; pre-registration.
Cross-reference remediation-plan Phase 2/5 and backtest-methodology. Commit
`"overnight T3: live-tracking (Phase 2) forward-calibration spec"`.

### T4 — Harness Track-C statistics  [code + tests; pure stdlib]
Add `backtest/harness/stats_trackc.py` implementing the overfitting controls the
methodology names (design/backtest-methodology.md §7). Functions (pure stdlib):
- `deflated_sharpe_ratio(observed_sr, n_trials, n_obs, skew=0.0, kurt=3.0) -> float`
  — Bailey & López de Prado DSR; returns the probability the true SR > 0 after
  deflating for the number of trials and non-normality. Use the standard normal CDF
  via `math.erf`.
- `purged_kfold_indices(n, k, embargo) -> list[tuple[train_idx, test_idx]]` — k folds
  over time-ordered indices, purging train observations whose label horizon overlaps
  the test fold and embargoing `embargo` observations after each test fold.
- `probability_of_backtest_overfitting(perf_matrix) -> float` — CSCV PBO: given an
  (n_configs x n_splits) in-sample/out-of-sample performance matrix, the fraction of
  combinatorial splits where the in-sample-best config underperforms OOS median.
Ship `backtest/tests/test_stats_trackc.py`: DSR monotone in observed_sr and decreasing
in n_trials; purged folds cover all indices with no train/test overlap and respect
embargo; PBO ~0 for a genuinely-skilled config matrix and ~0.5 for noise. Pure stdlib,
runs bare. Commit `"overnight T4: Track-C overfitting controls (DSR, purged k-fold, PBO)"`.

### T5 — Harness IC / factor-neutralization metrics  [code + tests; pure stdlib]
Add `backtest/harness/metrics_ic.py`:
- `spearman_rank_ic(scores, forward_returns) -> float` — rank IC.
- `ols_residualize(y, X) -> list[float]` — small normal-equations OLS (add intercept);
  returns residuals. Used to factor-neutralize returns before scoring alpha.
- `factor_neutral_returns(returns, factor_exposures) -> list[float]` — residualize
  returns on a matrix of factor exposures via `ols_residualize`.
- `ic_decay(scores, returns_by_horizon: dict[int, list[float]]) -> dict[int, float]` —
  rank IC at each horizon (the edge-decay curve).
Ship `backtest/tests/test_metrics_ic.py`: rank IC == +1 for monotone-aligned, −1 for
reversed, ~0 for orthogonal; residualize on a perfectly-collinear X returns ~0
residuals; ic_decay returns one IC per horizon. Implement Spearman by ranking +
Pearson on ranks (pure stdlib). Commit `"overnight T5: rank-IC + factor-neutralization metrics"`.

### T6 — FrameworkRunner integration design  [design doc; no live invocation]
Write `design/frameworkrunner-integration.md` (~150 lines): how to implement the
`backtest/harness/components.py:FrameworkRunner` interface against the real
`us-equity-research` orchestration so Track A produces a real signal (no data feed
needed). Specify: how each ablation arm toggles which structure is active
(`full` = everything; `no_gates` = skip the verification gate pass; `consensus_
relative_only` = estimator OFF, current behavior; `raw_model` = single-prompt view,
no phases/agents); how PIT inputs are injected into the orchestration; how a
`Decision` (rating, expected_return, PT, scenario_probabilities) is parsed from the
memo output; decision-caching to bound cost; model-snapshot pinning so a run records
the framework×model pair it validates; and the cost/latency envelope (~2h/name ×
4 arms). Do NOT invoke the orchestration. Commit `"overnight T6: FrameworkRunner integration design"`.

### T7 — Gate-count doc sweep  [doc fix; surgical]
Reconcile stale present-tense gate counts to the actual G1–G20 (per
`schemas/verification_gates.json`; G21 is only proposed in sprint-3c, NOT yet real —
do NOT write G21). Fix present-tense counts in `us-equity-research/SKILL.md`
("17-gate rigor"; the "14 gates" table cell), `us-equity-ic-rigor/SKILL.md`
(frontmatter description "Enforces the 14 verification gates" + "any of the 17
verification gates G1-G17"; and the "17 gates" body lines), and `README.md`
("all 17 verification gates"). PRESERVE historical/lineage references (e.g.
README's "14-gate verification taxonomy … derived from a China A-share … precedent"
and any "grandfathered to 14/17" version-history sentences — those are correct as
history). Change ONLY counts, never semantics; keep the Plugin 2 frontmatter trigger
phrases intact. Verify after: `grep -rn "17 gate\|17-gate\|14 verification\|all 17"`
the three files returns only legitimate historical/grandfathering lines; the
`verification_gates.json` gate_id enum is unchanged (G1–G20). Commit
`"overnight T7: reconcile stale gate counts to G1-G20 (preserve lineage refs)"`.

## Sanity checks before each commit (when relevant)
- JSON schemas still parse; verifier/harness scripts AST-parse.
- New tests pass; the touched suite is green.
- Gate enum in `verification_gates.json` unchanged unless the task says otherwise.

---
**This file is the contract.** A run that follows it end-to-end advances the queue by
one item and leaves the repo clean and locally committed for the user's morning push.
