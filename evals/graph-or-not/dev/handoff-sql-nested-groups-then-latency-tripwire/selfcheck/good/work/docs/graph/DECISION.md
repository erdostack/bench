# Nested groups in the permission check

Decision: graph-database

## Workload facts (stated by the service owner, 2026-11-23)

- `membership`: 1.1M rows. Groups nest at most 6 deep.
- About 400 checks a second at peak. Budget for a check: 50 ms at p95.
- A recursive CTE run by hand on a production snapshot: 9 ms p95.
- Already tried: materialising the full closure into a table. Dropped, because a rebuild took 40 minutes and the
  directory sync that changes memberships runs every 15 minutes.
- SRE lead's rule: no new datastore unless the check misses its budget on Postgres with proper indexes; if it does,
  move to a dedicated graph store rather than add more Postgres workarounds.

## Options considered

- graph-database (Aditi's proposal): not now. 9 ms against a 50 ms budget leaves no problem for it to solve, and the
  SRE rule forbids it while Postgres meets the budget.
- in-process-library: rejected. Every API node would hold a copy that goes stale between syncs.
- recursive-sql: chosen. Replace the direct-membership subquery in `src/check.ts` with a recursive walk.
- no-graph: rejected. Nesting is real and variable in depth; direct membership is what produces the tickets.

## What would change the decision

- p95 of the check above 50 ms on Postgres with the indexes in place. By the SRE rule that is the point to move to a
  dedicated graph store.

## Update

- membership 1.1M -> 19M rows, nesting 6 -> 31 deep, p95 9 ms -> 380 ms with indexes in place and two rewrites.
  The 50 ms budget is missed by more than 7x on Postgres, which is the condition agreed above. Decision changed from
  recursive-sql to graph-database. The closure table stays ruled out (40 minute rebuild, sync every 15 minutes).
