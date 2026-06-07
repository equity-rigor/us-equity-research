#!/usr/bin/env python3
"""
verify_fcf_definition.py — Gate G12 (FCF definition disclosure; SBC-in-FCF treatment).

Owns bug B12: `financials.ltm.fcf_includes_sbc_addback=true` while
`forensic_flags.fcf_definition="OCF_minus_capex"` (declaration conflicts with addback
flag — SBC silently added back, dilution masked, no B12 red flag carried).

G12 checks on structured memo JSON:
  a) forensic_flags.fcf_definition present, non-null, in schema enum.
  b) financials.ltm.fcf_includes_sbc_addback present and non-null (boolean).
  c) Consistency: OCF_minus_capex / OCF_minus_capex_minus_sbc → addback MUST be false;
     EBITDA_minus_capex → addback=true is non-standard (must redeclare); non_standard
     → boolean present is sufficient.

Usage:
    python scripts/verify_fcf_definition.py --memo-json <memo.json> [--memo-md <path>]

G12 is JSON-only; --memo-md accepted as a no-op for uniform calling contract.

Exit codes: 0 = pass; non-zero = fail (structured evidence printed per
schemas/verification_gates.json).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError

_FCF_DEFINITION_ENUM = {
    "OCF_minus_capex",
    "OCF_minus_capex_minus_sbc",
    "EBITDA_minus_capex",
    "non_standard",
}


class _LtmBlock(BaseModel):
    fcf_includes_sbc_addback: bool
    fcf_usd_m: float | None = Field(default=None)
    sbc_usd_m: float | None = Field(default=None)
    buyback_offsets_sbc_ratio: float | None = Field(default=None)


class _ForensicFlags(BaseModel):
    fcf_definition: str


def _print_fail(reason: str, remediation: str) -> None:
    print("gate_id: G12")
    print("status: fail")
    print(f"failure_reason: {reason}")
    print(f"remediation_required: {remediation}")


def _print_pass(definition: str, addback: bool, alert: str | None) -> None:
    print("gate_id: G12")
    print("status: pass")
    print(f"fcf_definition: {definition}")
    print(f"fcf_includes_sbc_addback: {addback}")
    if alert is not None:
        print(f"forensic_alert: {alert}")


def verify(payload: dict[str, Any]) -> int:
    """Return 0 on pass, non-zero on fail. Prints structured G12 evidence."""
    # (a) forensic_flags.fcf_definition present and valid
    forensic = payload.get("forensic_flags")
    if not isinstance(forensic, dict):
        _print_fail(
            "forensic_flags block is missing or not an object; G12 cannot verify FCF definition disclosure",
            "forensic_flags.fcf_definition — declare per schemas/memo.json enum",
        )
        return 1

    fcf_definition = forensic.get("fcf_definition")
    if fcf_definition is None or fcf_definition == "":
        _print_fail(
            "forensic_flags.fcf_definition is missing or null; required disclosure per G12",
            "forensic_flags.fcf_definition — set to one of "
            "OCF_minus_capex | OCF_minus_capex_minus_sbc | EBITDA_minus_capex | non_standard",
        )
        return 2

    if fcf_definition not in _FCF_DEFINITION_ENUM:
        _print_fail(
            f"forensic_flags.fcf_definition='{fcf_definition}' not in allowed enum",
            "forensic_flags.fcf_definition — use one of "
            "OCF_minus_capex | OCF_minus_capex_minus_sbc | EBITDA_minus_capex | non_standard",
        )
        return 3

    # (b) financials.ltm.fcf_includes_sbc_addback present and non-null
    financials = payload.get("financials")
    if not isinstance(financials, dict):
        _print_fail(
            "financials block is missing or not an object",
            "financials.ltm.fcf_includes_sbc_addback — populate per schemas/memo.json",
        )
        return 4

    ltm = financials.get("ltm")
    if not isinstance(ltm, dict):
        _print_fail(
            "financials.ltm block is missing or not an object",
            "financials.ltm.fcf_includes_sbc_addback — populate per schemas/memo.json",
        )
        return 5

    if "fcf_includes_sbc_addback" not in ltm or ltm["fcf_includes_sbc_addback"] is None:
        _print_fail(
            "financials.ltm.fcf_includes_sbc_addback missing or null; required disclosure per G12",
            "financials.ltm.fcf_includes_sbc_addback — set explicit true/false per references/forensic-accounting-checklist-us.md Item 3",
        )
        return 6

    try:
        ltm_model = _LtmBlock(**{k: ltm.get(k) for k in ltm.keys() if k in _LtmBlock.model_fields})
        _ForensicFlags(fcf_definition=fcf_definition)
    except ValidationError as exc:
        _print_fail(
            f"FCF disclosure shape invalid: {exc.errors()[0]['msg']}",
            "financials.ltm + forensic_flags — align types per schemas/memo.json",
        )
        return 7

    addback = ltm_model.fcf_includes_sbc_addback

    # (c) Consistency check (primary B12 detection)
    if fcf_definition == "OCF_minus_capex" and addback is True:
        _print_fail(
            f"financials.ltm.fcf_includes_sbc_addback=true but forensic_flags.fcf_definition='{fcf_definition}' "
            "(inconsistent — definition implies SBC NOT added back; should be 'OCF_minus_capex_minus_sbc' or carry explicit B12 red flag)",
            "financials.ltm.fcf_includes_sbc_addback OR forensic_flags.fcf_definition — align disclosure per references/forensic-accounting-checklist-us.md B12 / Item 3",
        )
        return 8

    if fcf_definition == "OCF_minus_capex_minus_sbc" and addback is True:
        _print_fail(
            f"financials.ltm.fcf_includes_sbc_addback=true but forensic_flags.fcf_definition='{fcf_definition}' "
            "(inconsistent — 'OCF_minus_capex_minus_sbc' deducts SBC, so addback flag must be false)",
            "financials.ltm.fcf_includes_sbc_addback OR forensic_flags.fcf_definition — align disclosure per references/forensic-accounting-checklist-us.md B12",
        )
        return 9

    if fcf_definition == "EBITDA_minus_capex" and addback is True:
        _print_fail(
            f"financials.ltm.fcf_includes_sbc_addback=true under fcf_definition='{fcf_definition}' "
            "is non-standard; declare 'non_standard' fcf_definition or carry explicit B12 red flag",
            "forensic_flags.fcf_definition → 'non_standard' OR financials.ltm.fcf_includes_sbc_addback → false",
        )
        return 10

    # Soft-alert: SBC addback declared (explicit non_standard) AND buyback ratio < 1.0 / missing.
    alert: str | None = None
    if addback is True and fcf_definition == "non_standard":
        ratio = ltm_model.buyback_offsets_sbc_ratio
        if ratio is None or ratio < 1.0:
            alert = (
                "SBC added back to FCF AND buyback_offsets_sbc_ratio<1.0 (or null) — dilution masking risk; "
                "non-gate forensic note per references/forensic-accounting-checklist-us.md Item 3"
            )

    _print_pass(fcf_definition, addback, alert)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify G12 — FCF definition disclosure & SBC-in-FCF treatment.",
    )
    parser.add_argument(
        "--memo-json",
        required=True,
        type=Path,
        help="Path to structured memo JSON (schemas/memo.json shape)",
    )
    parser.add_argument(
        "--memo-md",
        required=False,
        type=Path,
        default=None,
        help="(Unused; G12 is JSON-only — accepted for uniform calling contract)",
    )
    args = parser.parse_args(argv)

    try:
        payload = json.loads(args.memo_json.read_text())
    except FileNotFoundError:
        print(f"gate_id: G12\nstatus: fail\nfailure_reason: file not found: {args.memo_json}")
        return 20
    except json.JSONDecodeError as exc:
        print(f"gate_id: G12\nstatus: fail\nfailure_reason: invalid JSON: {exc}")
        return 21

    return verify(payload)


if __name__ == "__main__":
    sys.exit(main())
