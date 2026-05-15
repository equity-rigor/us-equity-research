#!/usr/bin/env python3
"""
verify_eps_pe.py

Verify that every scenario row in a 5-scenario valuation table actually has
EPS × PE = price within rounding tolerance. This is the most-failed PM
red-team gate (bug class B1 in pm-redteam-rubric.md).

Usage:
    python verify_eps_pe.py <scenarios.json>

Input format (scenarios.json):
    {
      "current_price": 4.17,
      "scenarios": [
        {"name": "强多", "P": 0.05, "EPS": 0.40, "PE": 15.0, "price": 6.00},
        {"name": "多头", "P": 0.20, "EPS": 0.36, "PE": 14.0, "price": 5.04},
        {"name": "基础", "P": 0.50, "EPS": 0.34, "PE": 13.0, "price": 4.42},
        {"name": "空头", "P": 0.20, "EPS": 0.30, "PE": 11.0, "price": 3.30},
        {"name": "强空", "P": 0.05, "EPS": 0.22, "PE":  9.0, "price": 1.98}
      ]
    }

Exit code 0 if all gates pass; 1 if any fail. Output identifies which row
failed and by how much.
"""
import json
import sys

# Tolerances
PRICE_TOL = 0.01   # ¥0.01 absolute tolerance on price (rounding)
PROB_TOL = 0.01    # 1pp tolerance on probability sum


def verify(data):
    failures = []
    scenarios = data["scenarios"]
    current_price = data.get("current_price")

    # Gate 1: each row's EPS × PE = price
    for s in scenarios:
        computed = s["EPS"] * s["PE"]
        diff = abs(computed - s["price"])
        if diff > PRICE_TOL:
            failures.append(
                f"  ✗ Row '{s['name']}': EPS {s['EPS']} × PE {s['PE']} = "
                f"{computed:.4f} but listed price = {s['price']} "
                f"(diff {diff:.4f} > tol {PRICE_TOL})"
            )
        else:
            print(f"  ✓ Row '{s['name']}': {s['EPS']} × {s['PE']} = "
                  f"{computed:.2f} ≈ {s['price']}")

    # Gate 2: probability sum to 1.00
    p_sum = sum(s["P"] for s in scenarios)
    if abs(p_sum - 1.0) > PROB_TOL:
        failures.append(
            f"  ✗ Probability sum = {p_sum:.4f}, expected 1.0 "
            f"(diff {abs(p_sum-1.0):.4f} > tol {PROB_TOL})"
        )
    else:
        print(f"  ✓ Probability sum = {p_sum:.4f}")

    # Gate 3: monotonicity check (optional — EPS should increase with bullishness)
    # Order should be: 强空 < 空头 < 基础 < 多头 < 强多 (by name convention)
    name_order = ["强空", "空头", "基础", "多头", "强多"]
    sorted_by_name = sorted(scenarios,
                            key=lambda x: name_order.index(x["name"])
                            if x["name"] in name_order else 99)
    eps_seq = [s["EPS"] for s in sorted_by_name]
    if eps_seq != sorted(eps_seq):
        failures.append(
            f"  ✗ EPS not monotonic across scenarios "
            f"(强空 → 强多 should be increasing): {eps_seq}"
        )
    else:
        print(f"  ✓ EPS monotonic: {eps_seq}")

    # Gate 4: implied return calculation
    if current_price:
        for s in scenarios:
            implied = (s["price"] / current_price) - 1.0
            if "return" in s:
                if abs(implied - s["return"]) > 0.005:
                    failures.append(
                        f"  ✗ Row '{s['name']}': listed return "
                        f"{s['return']:.4f} != implied {implied:.4f}"
                    )

        # Aggregate expected return
        expected_return = sum(s["P"] * ((s["price"]/current_price) - 1.0)
                              for s in scenarios)
        print(f"  ℹ Σ(P × R) = {expected_return:.4%} (12M expected return)")

    return failures


def main():
    if len(sys.argv) != 2:
        print("Usage: verify_eps_pe.py <scenarios.json>", file=sys.stderr)
        sys.exit(2)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    print(f"Verifying scenarios for {data.get('ticker', '<unknown>')}...")
    failures = verify(data)

    if failures:
        print(f"\n{len(failures)} GATE FAILURE(S):")
        for f in failures:
            print(f)
        sys.exit(1)

    print("\n✓ All EPS × PE gates pass.")
    sys.exit(0)


if __name__ == "__main__":
    main()
