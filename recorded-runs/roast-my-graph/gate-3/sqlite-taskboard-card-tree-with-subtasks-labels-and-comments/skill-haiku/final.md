Verdict: One critical. The foreign key `card.parent_id` has no index that leads with it, so every cascading delete scans the whole `card` table once per deleted row. Your EXPLAIN sweep covered the SELECTs, not the cascade.

Top findings:
- critical: `card.parent_id`. Add `CREATE INDEX card_parent ON card (parent_id);`. On the 200k sample, clearing one column of board 1 (343 rows with cascades) took 5.13 s without it and 0.010 s with it. The 2.1M-card cost is an estimate.
- low: `card_board_column`. The column index also holds subtasks, so about 3.4x the entries are read per column view on sample board 1. Fix: add `parent_id` as a third key column.

Files:
- /run/work/docs/graph/ROAST.md
- /run/work/findings.json

Not checked: no DELETE ran on board.db (read-only); delete timings used in-memory copies. The 2.1M figure is extrapolated. Nesting depth against SQLite's trigger-depth limit was not tested.
