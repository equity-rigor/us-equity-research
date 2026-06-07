#!/usr/bin/env python3
"""
verify_provenance_manifest.py — Gate G19 (Plugin 1 → Plugin 2 provenance
manifest required for non-hand-authored memos).

Added in v0.3.0. Closes the audit finding that Plugin 1 to Plugin 2
handoff was pure filename convention with no provenance enforcement —
a hand-authored memo could pass all 17 gates without Plugin 1 ever
being invoked.

Logic:
  1. Read memo JSON; extract memo_metadata.hand_authored flag.
  2. If hand_authored=true: G19 passes with WARNING, blocks_score_above
     = 7.5 (the explicit hand-authored path is legitimate but capped).
  3. If hand_authored absent or false: G19 requires manifest_ref to
     point at a real file conforming to schemas/manifest.json.
     Check:
       (a) manifest file exists at the declared path
       (b) manifest has all required fields (per schemas/manifest.json
           top-level required list)
       (c) manifest_version == "0.3.0"
       (d) manifest.ticker matches memo.ticker
       (e) verification_calls_count >= 12 per D9
       (f) web_search_log has >= 12 entries
       (g) agent_provenance has >= 15 entries (Phase 1 + 2 + 3 minimum)
       (h) outputs_produced[].sha256 matches actual sha256 of each
           file on disk (the critical integrity check — detects post-
           hoc file editing or fake manifest)
  4. Grandfathered for v0.1.0 and v0.2.0 memos (manifest didn't exist
     then). G19 runs for schema_version in {0.3.0, 0.4.0}; anything
     outside that set is skipped with reason='grandfathered_pre_v0_3'.

v0.4.0 fix (Sprint 3b Item 0): the original gate was the literal
`schema_version != "0.3.0"`, which silently skipped G19 — and with it
the manifest requirement and the on-disk sha256 integrity check — on
every v0.4.0 memo. That is the same latent skip bug Item 3 caught and
fixed in G20 (verify_view_defensibility.py) but did not sweep into this
sibling verifier, so shipping v0.4.0 disabled provenance enforcement on
the new schema version. The gate now tests membership in
RUNNABLE_SCHEMA_VERSIONS. The manifest schema is unchanged in v0.4.0, so
a v0.4.0 memo legitimately references a manifest_version=="0.3.0"
manifest; only the memo-side schema gate widened.

Usage:
    python scripts/verify_provenance_manifest.py --memo-json <memo.json>

Exit codes:
  0 = G19 passes (or n_a or skipped)
  non-zero = G19 fails
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

GATE_ID = "G19"
MIN_VERIFICATION_CALLS = 12
MIN_WEB_SEARCH_LOG = 12
MIN_AGENT_PROVENANCE = 15
HAND_AUTHORED_CAP = 7.5
FAIL_CAP = 7.5
# Memo schema_versions for which G19 runs. Pre-0.3.0 memos predate the
# manifest and are grandfathered (skipped). v0.4.0 (Sprint 3b fix) is added
# here because the prior literal `schema_version != "0.3.0"` silently skipped
# G19 on every v0.4.0 memo — the same latent bug Item 3 fixed in G20's
# verify_view_defensibility.py but left unpatched in this sibling verifier,
# which disabled provenance + on-disk-hash integrity enforcement for the exact
# schema version v0.4.0 made current. The manifest schema itself is unchanged,
# so v0.4.0 memos still validate against a manifest_version=="0.3.0" manifest
# (see the manifest_version check below); only the memo-side gate is widened.
RUNNABLE_SCHEMA_VERSIONS = {"0.3.0", "0.4.0", "0.5.0"}


def _print_status(status: str, **kwargs: Any) -> None:
    print(f"gate_id: {GATE_ID}")
    print(f"status: {status}")
    for k, v in kwargs.items():
        print(f"{k}: {v}")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(memo_json: dict[str, Any], memo_json_path: Path) -> int:
    schema_version = memo_json.get("schema_version", "0.1.0")
    if schema_version not in RUNNABLE_SCHEMA_VERSIONS:
        _print_status(
            "skipped",
            reason=f"grandfathered_pre_v0_3 (schema_version={schema_version})",
        )
        return 0

    metadata = memo_json.get("memo_metadata") or {}
    hand_authored = bool(metadata.get("hand_authored", False))

    if hand_authored:
        _print_status(
            "pass",
            mode="hand_authored",
            warning=(
                "memo explicitly declares hand_authored=true; provenance "
                "verification skipped; rubric score capped at 7.5 per G19"
            ),
            blocks_score_above=HAND_AUTHORED_CAP,
        )
        return 0

    manifest_ref = metadata.get("manifest_ref")
    if not manifest_ref:
        _print_status(
            "fail",
            failure_reason=(
                "memo_metadata.manifest_ref is absent and "
                "hand_authored is not true. Either: (a) write a "
                "manifest using scripts/write_manifest.py and set "
                "manifest_ref to its path, or (b) explicitly set "
                "memo_metadata.hand_authored=true to use the hand-"
                "authored path (rubric cap 7.5)."
            ),
            remediation_required=(
                "Run python scripts/write_manifest.py "
                "--ticker <TICKER> --outputs-dir outputs/ "
                "and set memo.memo_metadata.manifest_ref to the "
                "produced path."
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 1

    manifest_path = Path(manifest_ref)
    if not manifest_path.is_absolute():
        # Resolve relative to the directory containing the memo JSON.
        manifest_path = (memo_json_path.parent / manifest_path).resolve()
    if not manifest_path.is_file():
        _print_status(
            "fail",
            failure_reason=f"manifest file declared but not found at {manifest_path}",
            blocks_score_above=FAIL_CAP,
        )
        return 2

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _print_status(
            "fail",
            failure_reason=f"cannot parse manifest JSON: {exc}",
            blocks_score_above=FAIL_CAP,
        )
        return 3

    required_fields = {
        "manifest_version",
        "ticker",
        "run_id",
        "created_at",
        "plugin_versions",
        "phase_timing",
        "agent_provenance",
        "web_search_log",
        "verification_calls_count",
        "outputs_produced",
    }
    missing = sorted(required_fields - set(manifest.keys()))
    if missing:
        _print_status(
            "fail",
            failure_reason=f"manifest missing required fields: {missing}",
            blocks_score_above=FAIL_CAP,
        )
        return 4

    if manifest.get("manifest_version") != "0.3.0":
        _print_status(
            "fail",
            failure_reason=(
                f"manifest_version={manifest.get('manifest_version')!r} (expected '0.3.0')"
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 5

    memo_ticker = memo_json.get("ticker")
    if manifest.get("ticker") != memo_ticker:
        _print_status(
            "fail",
            failure_reason=(
                f"manifest.ticker={manifest.get('ticker')!r} != memo.ticker={memo_ticker!r}"
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 6

    vcc = manifest.get("verification_calls_count", 0)
    if not isinstance(vcc, int) or vcc < MIN_VERIFICATION_CALLS:
        _print_status(
            "fail",
            failure_reason=(
                f"verification_calls_count={vcc} below D9 minimum {MIN_VERIFICATION_CALLS}"
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 7

    wsl = manifest.get("web_search_log") or []
    if len(wsl) < MIN_WEB_SEARCH_LOG:
        _print_status(
            "fail",
            failure_reason=(f"web_search_log has {len(wsl)} entries (need >={MIN_WEB_SEARCH_LOG})"),
            blocks_score_above=FAIL_CAP,
        )
        return 8

    ap = manifest.get("agent_provenance") or []
    if len(ap) < MIN_AGENT_PROVENANCE:
        _print_status(
            "fail",
            failure_reason=(
                f"agent_provenance has {len(ap)} entries (need >={MIN_AGENT_PROVENANCE})"
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 9

    # The critical integrity check: declared file hashes match actual.
    outputs = manifest.get("outputs_produced") or []
    base_dir = manifest_path.parent.parent  # repo root if manifest in outputs/
    mismatches: list[tuple[str, str, str]] = []
    missing_files: list[str] = []
    for entry in outputs:
        path_str = entry.get("path", "")
        declared_hash = entry.get("sha256", "")
        # Resolve path relative to repo root if not absolute.
        file_path = Path(path_str)
        if not file_path.is_absolute():
            candidates = [
                base_dir / path_str,
                Path.cwd() / path_str,
                manifest_path.parent / Path(path_str).name,
            ]
            file_path = next((c for c in candidates if c.is_file()), candidates[0])
        if not file_path.is_file():
            missing_files.append(path_str)
            continue
        actual_hash = _sha256_file(file_path)
        if actual_hash != declared_hash:
            mismatches.append((path_str, declared_hash, actual_hash))

    if missing_files:
        _print_status(
            "fail",
            failure_reason=(
                f"manifest declares output files that do not exist: "
                f"{missing_files[:3]}{'...' if len(missing_files) > 3 else ''}"
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 10

    if mismatches:
        first = mismatches[0]
        _print_status(
            "fail",
            failure_reason=(
                f"manifest declared sha256 for {first[0]} = "
                f"{first[1][:16]}... but actual on-disk sha256 = "
                f"{first[2][:16]}... ({len(mismatches)} total mismatches). "
                "This indicates the file was edited after the manifest "
                "was written, OR the manifest is forged."
            ),
            remediation_required=(
                "Rerun python scripts/write_manifest.py to refresh "
                "manifest hashes against current file content. If the "
                "manifest is forged, do not pass this memo through Plugin 2."
            ),
            blocks_score_above=FAIL_CAP,
        )
        return 11

    _print_status(
        "pass",
        manifest_path=str(manifest_path),
        verification_calls=vcc,
        web_search_log_entries=len(wsl),
        agent_provenance_entries=len(ap),
        outputs_verified=len(outputs),
        run_id=manifest.get("run_id"),
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify G19 — Plugin 1 provenance manifest.")
    parser.add_argument("--memo-json", required=True, type=Path)
    parser.add_argument(
        "--memo-md",
        required=False,
        type=Path,
        default=None,
        help="(Unused for G19 — accepted for uniform calling contract)",
    )
    args = parser.parse_args(argv)

    if not args.memo_json.is_file():
        _print_status("fail", failure_reason=f"file not found: {args.memo_json}")
        return 6

    try:
        memo_json = json.loads(args.memo_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _print_status("fail", failure_reason=f"cannot parse memo JSON: {exc}")
        return 7

    return verify(memo_json, args.memo_json)


if __name__ == "__main__":
    sys.exit(main())
