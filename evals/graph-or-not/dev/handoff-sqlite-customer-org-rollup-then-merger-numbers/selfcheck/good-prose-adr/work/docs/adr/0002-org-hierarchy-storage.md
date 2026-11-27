# 0002 Org hierarchy storage

Decision: no-graph (keep the existing recursive queries on SQLite; nothing to change)

2,300 orgs, max depth 7, rollup ~2 min, panel 12 ms p95 at ~40 loads/min. Revisit only if the rollup goes past
20 minutes or the panel over 150 ms p95 (agreed with ops).
