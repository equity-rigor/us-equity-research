#!/usr/bin/env bash
# Run all 22 verifier scripts (G1-G20; G13/G14 share one) plus the v0.7.0
# judgment layer (G21 fair-value reconciliation, G22 revision attribution,
# G23 source-tier public boundary) under the uniform calling contract.
# Usage: bash scripts/run_all_gates.sh TICKER
set -u
T="$1"
MJ="outputs/${T}_structured.json"
MD="outputs/${T}_IC_memo.md"
ST="outputs/${T}_source_tags.json"
declare -a S=(
  verify_eps_pe verify_segment_gm verify_sotp_monotonicity verify_scenario_weights
  verify_bear_bridge verify_source_tags verify_headline_conditionality verify_gm_taxonomy
  verify_what_would_reverse verify_weighting_sensitivity verify_non_gaap verify_fcf_definition
  verify_quant_overlay verify_consensus_variance verify_bank_metrics verify_revision_velocity
  verify_quant_cross_doc_consistency verify_provenance_manifest verify_view_defensibility
  verify_fair_value_reconciliation verify_revision_attribution verify_source_tier_public
)
pass=0; fail=0
for s in "${S[@]}"; do
  case "$s" in
    verify_bank_metrics|verify_consensus_variance|verify_revision_velocity|verify_view_defensibility|verify_source_tier_public)
      out=$(python3 "scripts/$s.py" --memo-json "$MJ" --memo-md "$MD" --source-tags-json "$ST" 2>&1) ;;
    *)
      out=$(python3 "scripts/$s.py" --memo-json "$MJ" --memo-md "$MD" 2>&1) ;;
  esac
  code=$?
  st=$(echo "$out" | grep -oE '"?status"?:?\s*"?(pass|fail|n_a|warning)"?' | head -1 | grep -oE 'pass|fail|n_a|warning')
  if [ "$code" -eq 0 ]; then pass=$((pass+1)); else fail=$((fail+1)); fi
  printf "[exit %s] %-38s %s\n" "$code" "$s" "${st:-?}"
  if [ "$code" -ne 0 ]; then echo "$out" | sed 's/^/        /' | head -8; fi
done
echo "----- pass(exit0)=$pass  nonzero=$fail -----"
