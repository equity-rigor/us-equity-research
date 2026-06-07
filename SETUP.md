# Setup — skip the per-call permission prompts

A normal IC memo run fires 50-100 tool calls (15 specialists × multiple WebSearch/WebFetch/Bash each). By default, Claude Code will prompt you "Yes / Yes-once / No" for each one. Most users want this skipped after the first time. This guide shows you three ways to do it, ranked from least to most permissive.

## TL;DR

If you cloned the repo, you already have the bundled `.claude/settings.json` and most prompts are pre-approved. If you installed via the Claude Code plugin marketplace, you don't have this file — copy the snippet below into your global `~/.claude/settings.json` once, and you're done.

```bash
# Quick check if the bundled settings are active
cat .claude/settings.json | head -5
# If "_comment" or "permissions" appears, you're set
```

---

## Option A — Workspace-level (recommended if you cloned the repo)

The repo ships with `.claude/settings.json` at the root. When you launch Claude Code from inside the repo directory, it picks up these permissions automatically. No action required from you.

This is the most conservative setup — it only allows the specific safe operations the framework needs:

- SEC EDGAR, FRED, BLS, BEA, EIA, Treasury, Federal Reserve, FDIC, OCC, FTC, DOJ, OFAC, BIS Entity List, Census, CBO — all `WebFetch` + `Bash(curl)` patterns
- Finance aggregators — Yahoo Finance, StockAnalysis.com, WSJ, Bloomberg, Reuters, FT, SeekingAlpha, Motley Fool
- `WebSearch` — fully allowed
- Read/Write/Edit on `outputs/**` — for memo, JSON, manifest writing
- `python3 scripts/verify_*` and `python3 scripts/write_manifest.py` — the framework's verifier scripts
- Read-only git operations
- Read-only `cat` and `ls` on framework directories

Anything else still prompts. Dangerous operations (`rm`, `git commit`, `git push`, `Read(.env*)`) are explicitly listed in `ask` or `deny` blocks.

If you want to see exactly what's allowed, open `.claude/settings.json` — every pattern is listed.

---

## Option B — Global / for users who installed via plugin marketplace

If you installed the plugin via `/plugin marketplace add equity-rigor/us-equity-research` rather than cloning the repo, you don't have the workspace settings file. Copy this minimal snippet into your global `~/.claude/settings.json` (create the file if it doesn't exist):

```json
{
  "permissions": {
    "allow": [
      "WebSearch",

      "WebFetch(domain:data.sec.gov)",
      "WebFetch(domain:www.sec.gov)",
      "WebFetch(domain:efts.sec.gov)",
      "WebFetch(domain:fred.stlouisfed.org)",
      "WebFetch(domain:api.fred.stlouisfed.org)",
      "WebFetch(domain:www.bls.gov)",
      "WebFetch(domain:www.bea.gov)",
      "WebFetch(domain:www.eia.gov)",
      "WebFetch(domain:home.treasury.gov)",
      "WebFetch(domain:www.federalreserve.gov)",
      "WebFetch(domain:www.fdic.gov)",
      "WebFetch(domain:www.occ.gov)",
      "WebFetch(domain:www.ftc.gov)",
      "WebFetch(domain:www.justice.gov)",
      "WebFetch(domain:ofac.treasury.gov)",
      "WebFetch(domain:www.bis.doc.gov)",
      "WebFetch(domain:finance.yahoo.com)",
      "WebFetch(domain:stockanalysis.com)",
      "WebFetch(domain:www.wsj.com)",
      "WebFetch(domain:www.bloomberg.com)",
      "WebFetch(domain:www.reuters.com)",
      "WebFetch(domain:www.ft.com)",
      "WebFetch(domain:seekingalpha.com)",
      "WebFetch(domain:www.fool.com)",
      "WebFetch(domain:web.archive.org)",

      "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/verify_*)",
      "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/write_manifest.py *)",
      "Bash(python3 -m json.tool *)",
      "Bash(mkdir -p outputs)",
      "Bash(mkdir -p outputs/*)",
      "Bash(cat outputs/*)",
      "Bash(cat outputs/**)",
      "Bash(ls outputs/)",
      "Bash(ls outputs/*)",

      "Read",
      "Write(outputs/**)",
      "Edit(outputs/**)",
      "Task"
    ],
    "ask": [
      "Bash(rm *)",
      "Bash(git commit *)",
      "Bash(git push *)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.git-credentials)"
    ]
  }
}
```

If you already have a `~/.claude/settings.json` with other allow rules, merge — don't replace. Specifically merge into the `permissions.allow` array.

---

## Option C — Full YOLO mode (not recommended for normal use)

If you want zero prompts at the cost of zero safety checks, you can launch Claude Code with `--dangerously-skip-permissions`:

```bash
claude --dangerously-skip-permissions
```

This bypasses ALL permission checks for the entire session. The framework's gates still run as normal, but Claude can execute any shell command without asking — including ones that write to your home directory, modify git history, or touch sensitive files.

Use this only when:
- You're running the framework in a sandboxed environment (container, VM, ephemeral cloud workspace)
- You're debugging a flow that's hitting prompts you can't easily anticipate
- You explicitly understand and accept the risk

For real desk use, Option A or Option B is the right choice.

---

## What still prompts even with Option A or B configured

Some operations remain prompted for safety:

- `git commit`, `git push`, `git tag` — anything that modifies version-control history
- `rm` — destructive filesystem operations
- `curl` to domains not on the framework's allowlist — agent could otherwise be prompt-injected into fetching arbitrary URLs
- Reading any file matching `.env*` — credentials hygiene
- Any MCP server tools not in the allowlist (Visible Alpha, Capital IQ, AlphaSense, Bloomberg — these require separate per-MCP authorization the first time)

To pre-approve a specific extra command you find yourself approving repeatedly, edit `.claude/settings.json` (workspace) or `~/.claude/settings.json` (global), adding the pattern to `permissions.allow`.

---

## Verifying it worked

After configuring, run the framework on a small ticker:

```bash
/us-equity-research:research NVDA
```

You should see prompts only for:

1. The initial slash-command launch confirmation
2. Any premium-data hooks if you opted into them
3. Final `git commit` if you ask the framework to commit results

If you're still getting prompted on every WebFetch to sec.gov, your settings file didn't load — check that:

- `.claude/settings.json` is at the working directory root, not nested inside a subdirectory
- The JSON parses without syntax errors (`python3 -m json.tool .claude/settings.json` should succeed)
- You launched Claude Code from inside the directory containing `.claude/settings.json`

---

## How this works under the hood

Claude Code's permission model has three layers, applied in this order:

1. **Slash-command frontmatter `allowed-tools`** — pre-approves the listed tool patterns for the lifetime of that command's execution. The plugin's three commands (`/us-equity-research:research`, `/us-equity-ic-rigor:ic-memo`, `/us-equity-ic-rigor:red-team`) all ship with full allowlists in their frontmatter.

2. **Project-level `.claude/settings.json`** — applies to any session launched from inside that directory.

3. **Global `~/.claude/settings.json`** — applies to every Claude Code session you launch.

Anything matched by any of these three (and not denied) gets auto-approved. The framework relies on the same patterns at all three layers, so missing one layer doesn't break it — it just produces a few extra prompts.
