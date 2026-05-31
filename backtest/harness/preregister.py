"""Pre-registration: freeze and hash the backtest config before any outcomes are
seen, to prevent post-hoc dredging (design/backtest-methodology.md §1).

The hash is canonical (sorted keys, no whitespace), so the same logical config
always produces the same digest. `verify` refuses a run whose config has drifted
from the frozen record unless the operator deliberately re-registers.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical(config: dict[str, Any]) -> str:
    return json.dumps(config, sort_keys=True, separators=(",", ":"))


def config_hash(config: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(config).encode()).hexdigest()


def freeze(config: dict[str, Any], out_path: str | Path) -> str:
    """Write a frozen pre-registration record and return its sha256."""
    digest = config_hash(config)
    record = {"preregistration_sha256": digest, "config": config}
    Path(out_path).write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    return digest


def verify(config: dict[str, Any], frozen_path: str | Path) -> bool:
    """True iff `config` matches the frozen record's hash."""
    rec = json.loads(Path(frozen_path).read_text(encoding="utf-8"))
    return config_hash(config) == rec.get("preregistration_sha256")
