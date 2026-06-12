#!/usr/bin/env bash
#
# sync_plugin_files.sh — Maintain plugin copies of repo-root scripts/ and schemas/.
#
# Purpose: The Claude Code plugin install copies only the plugin directories
# (us-equity-research/ and us-equity-ic-rigor/) into ~/.claude/plugins/. The
# repo-root scripts/ and schemas/ directories are NOT included. This script
# copies them into each plugin directory so they ship with the plugin install.
#
# Usage:
#   bash scripts/sync_plugin_files.sh           # Apply sync (copy files)
#   bash scripts/sync_plugin_files.sh --check   # Dry-run; exit 1 if out of sync
#
# Called by:
#   - Maintainer before any commit touching scripts/ or schemas/
#   - CI workflow as a verification gate (see .github/workflows/pytest.yml)
#
# Design decision: we bundle the FULL scripts/ and schemas/ directories in both
# plugin directories. Storage cost is trivial (<100KB). Eliminates the need to
# classify which scripts belong to which plugin and prevents the bug where a
# new verifier script lands in the repo but doesn't make it into the plugin
# install. Plugin 2 (us-equity-ic-rigor) uses all 20 verifier scripts; Plugin 1
# (us-equity-research) uses write_manifest.py + a subset of verifiers for
# Phase 1-3 sourcing discipline. Both plugins reference all 5 schemas.

set -euo pipefail

# Resolve the repo root regardless of where the script is invoked from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SOURCE_SCRIPTS="$REPO_ROOT/scripts"
SOURCE_SCHEMAS="$REPO_ROOT/schemas"
PLUGIN_1_DIR="$REPO_ROOT/us-equity-research"
PLUGIN_2_DIR="$REPO_ROOT/us-equity-ic-rigor"

CHECK_MODE=0
if [[ "${1:-}" == "--check" ]]; then
  CHECK_MODE=1
fi

# Verify source directories exist.
if [[ ! -d "$SOURCE_SCRIPTS" ]]; then
  echo "ERROR: Source directory $SOURCE_SCRIPTS does not exist." >&2
  exit 2
fi
if [[ ! -d "$SOURCE_SCHEMAS" ]]; then
  echo "ERROR: Source directory $SOURCE_SCHEMAS does not exist." >&2
  exit 2
fi
if [[ ! -d "$PLUGIN_1_DIR" ]]; then
  echo "ERROR: Plugin 1 directory $PLUGIN_1_DIR does not exist." >&2
  exit 2
fi
if [[ ! -d "$PLUGIN_2_DIR" ]]; then
  echo "ERROR: Plugin 2 directory $PLUGIN_2_DIR does not exist." >&2
  exit 2
fi

# What gets copied. Use globs to keep this declarative.
# Scripts: all *.py files at top level of scripts/ (excludes scripts/tests/).
# Schemas: all *.json files in schemas/.
mapfile -t SCRIPT_FILES < <(find "$SOURCE_SCRIPTS" -maxdepth 1 -type f -name "*.py" | sort)
mapfile -t SCHEMA_FILES < <(find "$SOURCE_SCHEMAS" -maxdepth 1 -type f -name "*.json" | sort)

if [[ ${#SCRIPT_FILES[@]} -eq 0 ]]; then
  echo "ERROR: No *.py files found in $SOURCE_SCRIPTS" >&2
  exit 2
fi
if [[ ${#SCHEMA_FILES[@]} -eq 0 ]]; then
  echo "ERROR: No *.json files found in $SOURCE_SCHEMAS" >&2
  exit 2
fi

OUT_OF_SYNC=0

# Function: check or copy a file pair.
# In check mode, prints diff and increments OUT_OF_SYNC.
# In apply mode, copies if missing or different.
sync_or_check() {
  local src="$1"
  local dst="$2"

  if [[ $CHECK_MODE -eq 1 ]]; then
    if [[ ! -f "$dst" ]]; then
      echo "MISSING: $dst (would be copied from $src)"
      OUT_OF_SYNC=1
      return
    fi
    if ! cmp -s "$src" "$dst"; then
      echo "DRIFT: $dst differs from $src"
      OUT_OF_SYNC=1
    fi
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
  fi
}

# Sync scripts and schemas into both plugin directories.
for plugin_dir in "$PLUGIN_1_DIR" "$PLUGIN_2_DIR"; do
  plugin_name="$(basename "$plugin_dir")"

  for src_script in "${SCRIPT_FILES[@]}"; do
    script_name="$(basename "$src_script")"
    dst_script="$plugin_dir/scripts/$script_name"
    sync_or_check "$src_script" "$dst_script"
  done

  for src_schema in "${SCHEMA_FILES[@]}"; do
    schema_name="$(basename "$src_schema")"
    dst_schema="$plugin_dir/schemas/$schema_name"
    sync_or_check "$src_schema" "$dst_schema"
  done

  if [[ $CHECK_MODE -eq 0 ]]; then
    echo "Synced ${#SCRIPT_FILES[@]} scripts and ${#SCHEMA_FILES[@]} schemas to $plugin_name/"
  fi
done

# Final verdict.
if [[ $CHECK_MODE -eq 1 ]]; then
  if [[ $OUT_OF_SYNC -eq 1 ]]; then
    echo ""
    echo "Plugin file sync is out of date. Run: bash scripts/sync_plugin_files.sh"
    exit 1
  else
    echo "Plugin file sync OK (${#SCRIPT_FILES[@]} scripts, ${#SCHEMA_FILES[@]} schemas × 2 plugins)"
    exit 0
  fi
fi

echo "Done. Remember to 'git add' the plugin directories."
