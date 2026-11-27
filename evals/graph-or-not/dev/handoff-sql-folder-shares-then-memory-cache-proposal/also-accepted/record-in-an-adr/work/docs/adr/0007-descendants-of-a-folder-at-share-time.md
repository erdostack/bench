# 0007. Descendants of a folder at share time

Status: Accepted
Date: 2026-11-23

Decision: recursive-sql

## Workload facts (given by the owner, 2026-11-23)

- `folder`: 85M rows; deepest tree 60 levels; `parent_id` is indexed.
- About 300 folder moves a second at peak.
- The share must see the tree as it is at that moment. Acting on a stale tree leaves someone with access to a folder
  that was moved out: a security bug.
- API pods have 1 GB of memory each.
- Measured: recursive query for the descendants on a production replica, 12 ms p95. Budget for the share call: 250 ms.

## Options considered

- graph-database: rejected. A second copy of the tree that has to be kept current at 300 moves a second, for a
  query that already runs in 12 ms.
- in-process-library: rejected. 85M folders do not fit in a 1 GB pod, and any copy is stale between refreshes,
  which is the security bug above.
- recursive-sql: chosen. One recursive query in the share transaction.
- no-graph: rejected. Depth is variable (up to 60 levels).

## What would change the decision

- The share call missing its 250 ms budget on Postgres.
- A requirement that tolerates a stale tree (it does not today).
