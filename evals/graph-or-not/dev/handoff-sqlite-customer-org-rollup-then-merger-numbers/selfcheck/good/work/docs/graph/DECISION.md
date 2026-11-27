# Customer organisation hierarchy: storage

Decision: recursive-sql

## Workload facts (from the owner, 2026-11-24)

- 2,300 organisations; the deepest group is 7 levels.
- Nightly rollup (rollups/rollup.py): about 2 minutes. Account-page subtree query (accounts/subtree.py): 12 ms p95
  at about 40 loads a minute.
- Agreed with ops when this was built: revisit the storage only if the nightly rollup goes past 20 minutes (it must
  fit the 30-minute batch window) or the subtree query goes over 150 ms p95.

## Options considered

- graph-database (Bram's proposal): rejected; both measures are an order of magnitude inside the agreed limits.
- in-process-library: no gain over the queries that already run.
- recursive-sql: keep what is there. Change nothing.

## What would change the decision

- The rollup past 20 minutes, or the subtree query over 150 ms p95, after the usual tuning.
