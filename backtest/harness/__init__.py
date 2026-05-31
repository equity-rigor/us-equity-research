"""Track A ablation backtest harness (scaffold).

Validates the *incremental* contribution of the research framework's structure by
holding model + information set fixed and varying only the framework arms, then
measuring paired within-case differences in decision quality. Leakage is common-
mode across arms and differences out (design/backtest-methodology.md, Track A).

The statistics, metrics, and pre-registration are real and tested. The expensive
and feed-dependent pieces (the framework runner, point-in-time data, return
labels, leakage probes) are pluggable interfaces backed by deterministic Mocks so
the full pipeline runs with no external dependencies. See README.md for the stub
boundary and how to wire production components.
"""
