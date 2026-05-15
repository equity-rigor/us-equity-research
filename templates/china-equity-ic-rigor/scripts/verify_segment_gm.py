#!/usr/bin/env python3
"""
verify_segment_gm.py

Verify that segment GM × revenue weighted reconciles to consolidated GM
within ±50bp. This is bug class B2 in pm-redteam-rubric.md — the segment
GM mosaic that doesn't add up to what the income statement reports.

Usage:
    python verify_segment_gm.py <segments.json>

Input format (segments.json):
    {
      "ticker": "000725",
      "year": 2024,
      "consolidated_gm": 0.155,
      "consolidated_gm_source": "S1: 2024 年报 利润表",
      "segments": [
        {"name": "显示器件", "revenue_yi": 1330, "GM": 0.17,
         "source": "S1: 2024 年报附注 §3.2"},
        {"name": "IoT",     "revenue_yi":  420, "GM": 0.09, ...},
        {"name": "传感器",   "revenue_yi":  220, "GM": 0.19, ...},
        {"name": "智慧系统", "revenue_yi":   76, "GM": 0.22, ...}
      ],
      "unallocated_yi": 0,
      "tolerance_bp": 50
    }

Exit code 0 if reconciliation passes; 1 if it fails.
"""
import json
import sys


def verify(data):
    consolidated = data["consolidated_gm"]
    segments = data["segments"]
    tol_bp = data.get("tolerance_bp", 50)
    tol = tol_bp / 10000.0  # bps to decimal

    # Gate 1: weighted segment GM
    total_revenue = sum(s["revenue_yi"] for s in segments)
    total_gp = sum(s["revenue_yi"] * s["GM"] for s in segments)
    implied = total_gp / total_revenue if total_revenue else 0.0

    print(f"Verifying segment GM reconciliation for "
          f"{data.get('ticker', '<unknown>')} {data.get('year','')}...")
    print()
    print(f"  Segment build:")
    for s in segments:
        gp = s["revenue_yi"] * s["GM"]
        print(f"    {s['name']}: 营收 ¥{s['revenue_yi']}亿 × GM "
              f"{s['GM']*100:.1f}% = GP ¥{gp:.1f}亿")
    print()
    print(f"  Σ revenue = ¥{total_revenue:.0f}亿")
    print(f"  Σ GP = ¥{total_gp:.1f}亿")
    print(f"  Implied consolidated GM = {implied*100:.2f}%")
    print(f"  Reported consolidated GM = {consolidated*100:.2f}%")

    diff_bp = abs(implied - consolidated) * 10000
    print(f"  Difference = {diff_bp:.1f}bp (tolerance ±{tol_bp}bp)")
    print()

    failures = []
    if diff_bp > tol_bp:
        failures.append(
            f"  ✗ Segment GM does not reconcile to consolidated within "
            f"±{tol_bp}bp.\n"
            f"    Either: (1) add 其他/未分配 row absorbing the difference,\n"
            f"            (2) check segment data is full-year same period,\n"
            f"            (3) check GM definitions match types per "
            f"gm-taxonomy.md."
        )
    else:
        print(f"  ✓ Segment GM reconciles within tolerance.")

    # Gate 2: every segment has source tag
    for s in segments:
        if "source" not in s or not s["source"]:
            failures.append(f"  ✗ Segment '{s['name']}' missing source tag.")

    # Gate 3: warn if any segment GM is suspiciously high or low
    for s in segments:
        if s["GM"] < 0 or s["GM"] > 0.6:
            failures.append(
                f"  ⚠ Segment '{s['name']}' GM = {s['GM']*100:.1f}% — "
                f"verify this is plausible."
            )

    return failures


def main():
    if len(sys.argv) != 2:
        print("Usage: verify_segment_gm.py <segments.json>", file=sys.stderr)
        sys.exit(2)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    failures = verify(data)

    if failures:
        print(f"\n{len(failures)} GATE FAILURE(S) / WARNING(S):")
        for f in failures:
            print(f)
        sys.exit(1)

    print("\n✓ All segment GM reconciliation gates pass.")
    sys.exit(0)


if __name__ == "__main__":
    main()
