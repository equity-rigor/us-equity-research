#!/usr/bin/env python3
"""
write_manifest.py — Plugin 1 orchestrator helper that assembles the
provenance manifest at end of Phase 3.

Added in v0.3.0. Full discipline in schemas/manifest.json + Plugin 1
SKILL.md §"Manifest generation (v0.3.0)".

The orchestrator (Claude executing the us-equity-research skill) calls
this at the end of Phase 3, after all specialist workpapers + IC memo +
structured JSON outputs have been written. The script:

  1. Walks outputs/workpapers/<ticker>_*.md (one per specialist agent).
  2. Walks outputs/<ticker>_*.{md,json} for the main deliverables.
  3. Reads a partial manifest seed file at outputs/<ticker>_manifest_seed.json
     (written incrementally by the orchestrator during the run) containing
     run_id, plugin_versions, phase_timing, web_search_log,
     verification_calls_count, and orchestrator_notes.
  4. Computes SHA-256 over each output file's content.
  5. Assembles agent_provenance from the workpaper files (one entry per
     specialist; status='completed' if file exists and is >500 bytes,
     'framework_only' if <500 bytes, 'skipped' if no file).
  6. Writes outputs/<ticker>_manifest.json conforming to
     schemas/manifest.json.

Usage:
    python scripts/write_manifest.py \\
        --ticker NVDA \\
        --outputs-dir outputs/ \\
        --seed outputs/NVDA_manifest_seed.json

The seed file contract is documented inline in the orchestrator
instructions. If the seed is missing, the script writes a manifest with
placeholder fields and emits a WARNING — this is a degraded path for
users who skipped the incremental logging during the run. The resulting
manifest will fail G19 unless the user adds the missing fields by hand.

Exit codes:
  0 = manifest written successfully
  non-zero = error (seed missing + --strict, output dir not found, etc.)
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import uuid
from pathlib import Path
from typing import Any

MANIFEST_VERSION = "0.3.0"
FRAMEWORK_ONLY_BYTE_THRESHOLD = 500

EXPECTED_AGENTS_BY_PHASE = {
    1: ["A1", "A4", "A5", "A8", "FS"],
    2: ["A2", "A3", "A3-Peers", "R", "A6", "A-Consensus"],
    3: ["A7", "Mirror", "Topic-Forensic", "R-v2"],
}
ALL_AGENT_IDS = [a for ids in EXPECTED_AGENTS_BY_PHASE.values() for a in ids]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _classify_output(path: Path) -> str:
    name = path.name
    if name.endswith("_IC_memo.md"):
        return "ic_memo_md"
    if name.endswith("_structured.json"):
        return "structured_json"
    if name.endswith("_source_tags.json"):
        return "source_tags_json"
    if name.endswith("_scenarios.json"):
        return "scenarios_json"
    if name.endswith("_verification_gates.json"):
        return "verification_gates_json"
    if name.endswith("_manifest.json"):
        return "manifest_json"
    if "workpaper" in str(path) or path.parent.name == "workpapers":
        return "workpaper_md"
    return "workpaper_md"


def _walk_outputs(outputs_dir: Path, ticker: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    patterns = [
        f"{ticker}_IC_memo.md",
        f"{ticker}_structured.json",
        f"{ticker}_source_tags.json",
        f"{ticker}_scenarios.json",
        f"{ticker}_verification_gates.json",
    ]
    for pat in patterns:
        p = outputs_dir / pat
        if p.is_file():
            entries.append(
                {
                    "path": str(p),
                    "sha256": _sha256_file(p),
                    "size_bytes": p.stat().st_size,
                    "file_type": _classify_output(p),
                }
            )
    workpapers_dir = outputs_dir / "workpapers"
    if workpapers_dir.is_dir():
        for wp in sorted(workpapers_dir.glob(f"{ticker}_*.md")):
            entries.append(
                {
                    "path": str(wp),
                    "sha256": _sha256_file(wp),
                    "size_bytes": wp.stat().st_size,
                    "file_type": "workpaper_md",
                }
            )
    return entries


def _build_agent_provenance(outputs_dir: Path, ticker: str) -> list[dict[str, Any]]:
    """Assemble agent_provenance from workpaper files. One entry per agent_id."""
    workpapers_dir = outputs_dir / "workpapers"
    entries: list[dict[str, Any]] = []
    for phase, agent_ids in EXPECTED_AGENTS_BY_PHASE.items():
        for agent_id in agent_ids:
            safe_id = agent_id.replace("-", "_")
            candidates = [
                workpapers_dir / f"{ticker}_phase{phase}_{safe_id}.md",
                workpapers_dir / f"{ticker}_phase{phase}_{agent_id}.md",
                workpapers_dir / f"{ticker}_{safe_id}.md",
            ]
            wp = next((c for c in candidates if c.is_file()), None)
            if wp is None:
                entries.append({"agent_id": agent_id, "phase": phase, "status": "skipped"})
                continue
            size = wp.stat().st_size
            status = (
                "framework_only" if size < FRAMEWORK_ONLY_BYTE_THRESHOLD else "completed"
            )
            entries.append(
                {
                    "agent_id": agent_id,
                    "phase": phase,
                    "status": status,
                    "output_path": str(wp),
                    "output_sha256": _sha256_file(wp),
                }
            )
    return entries


def build_manifest(
    ticker: str,
    outputs_dir: Path,
    seed: dict[str, Any] | None,
    strict: bool,
) -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if seed is None:
        seed = {}
    manifest: dict[str, Any] = {
        "manifest_version": MANIFEST_VERSION,
        "ticker": ticker,
        "run_id": seed.get("run_id") or str(uuid.uuid4()),
        "created_at": now,
        "plugin_versions": seed.get(
            "plugin_versions",
            {"us_equity_research": "0.3.0", "us_equity_ic_rigor": "0.3.0"},
        ),
        "phase_timing": seed.get(
            "phase_timing",
            {
                "phase_0": {"start": now, "end": now},
                "phase_1": {"start": now, "end": now},
                "phase_2": {"start": now, "end": now},
                "phase_3": {"start": now, "end": now},
                "verification": {"start": now, "end": now},
            },
        ),
        "agent_provenance": _build_agent_provenance(outputs_dir, ticker),
        "web_search_log": seed.get("web_search_log", []),
        "verification_calls_count": seed.get("verification_calls_count", 0),
        "outputs_produced": _walk_outputs(outputs_dir, ticker),
    }
    if seed.get("orchestrator_notes"):
        manifest["orchestrator_notes"] = seed["orchestrator_notes"]

    warnings: list[str] = []
    if not seed:
        warnings.append("seed file absent — manifest written with placeholder phase timing and empty web_search_log")
    if manifest["verification_calls_count"] < 12:
        warnings.append(
            f"verification_calls_count={manifest['verification_calls_count']} below D9 minimum of 12 — G19 will fail"
        )
    if len(manifest["web_search_log"]) < 12:
        warnings.append(
            f"web_search_log has {len(manifest['web_search_log'])} entries (need >=12) — G19 will fail"
        )
    if len(manifest["agent_provenance"]) < 15:
        warnings.append(
            f"agent_provenance has {len(manifest['agent_provenance'])} entries (need >=15) — likely workpapers/ directory was not populated"
        )
    if warnings and strict:
        raise RuntimeError("strict mode: " + "; ".join(warnings))
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Assemble Plugin 1 provenance manifest at end of Phase 3."
    )
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--outputs-dir", required=True, type=Path)
    parser.add_argument("--seed", type=Path, default=None,
                        help="Path to seed JSON written incrementally during the run")
    parser.add_argument("--strict", action="store_true",
                        help="Fail if required seed fields are missing")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output path; defaults to <outputs-dir>/<ticker>_manifest.json")
    args = parser.parse_args(argv)

    if not args.outputs_dir.is_dir():
        print(f"ERROR: outputs-dir not found: {args.outputs_dir}", file=sys.stderr)
        return 2

    seed: dict[str, Any] | None = None
    if args.seed is not None:
        if not args.seed.is_file():
            print(f"ERROR: seed file not found: {args.seed}", file=sys.stderr)
            if args.strict:
                return 3
        else:
            try:
                seed = json.loads(args.seed.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                print(f"ERROR: cannot parse seed: {exc}", file=sys.stderr)
                return 4

    try:
        manifest = build_manifest(args.ticker, args.outputs_dir, seed, args.strict)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 5

    out_path = args.output or (args.outputs_dir / f"{args.ticker}_manifest.json")
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote manifest: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
