Decision: recursive-sql

Keep the crib on the SQLite file and write the "what's in this kit" walk as one recursive query. The walk starts at one kit, goes down at most 4 levels, and touches at most 3,610 items. The page gets about 50 views a day, so the existing database is well inside the budget. A graph database is not needed.

What the decision turns on:
- The walk is a real traversal (kits nested up to 4 deep), so `no-graph` does not hold. A single join is not enough.
- Each step uses the existing index on `kit_line(kit_id)`. On a synthetic check (SQLite 3.53.1, Python 3.13.18, not the crib's data), one kit walks in 0.2 to 0.7 ms, and all 410 kits in 159 ms. Using `UNION ALL` gave 81 route rows against 78 distinct tools for one kit, so the query must use `DISTINCT` on the item.
- Upper bound: 3,610 rows per page view, and 180,500 rows a day at 50 views.

Not measured: the real `var/crib.db` is not in the checkout, so the real row count and fan-out are unknown. Next step: run `EXPLAIN QUERY PLAN` and time the query on a read-only copy of the real file. Also decide whether `qty` must be multiplied along each path. Graph-database, in-process-library and no-graph were rejected for the reasons in `docs/graph/DECISION.md`.

Nothing in the repository was changed except the new file `docs/graph/DECISION.md`.
