# Graph decision

Decision: recursive-sql

The question is whether the "what's in this kit" page, which must list every tool in a kit including tools in kits nested up to 4 levels deep, needs a graph database, a graph library, recursive SQL or no graph. The answer is recursive SQL on the existing SQLite file: the walk starts at one kit and is bounded by the 3,610 items in the crib, and the page runs about 50 times a day, so the SQL database already in use is well inside the required budget. The finding it turns on is the walk itself, which is a real traversal (depth up to 4, set by the data) and not a single join, so `no-graph` does not hold.

## Workload facts

- 3,200 tools and 410 kits, 3,610 items in total, in the crib's SQLite file (user stated, in the request; the file itself is not in this checkout, README names `var/crib.db`)
- Kits nest up to 4 deep (user stated, in the request)
- About 50 page views per day from the crib attendants (user stated, in the request)
- `kit_line` holds the packing: `kit_id`, `item_id`, `qty`, with `item_id` allowed to be a kit (`db/schema.sql`, PRIMARY KEY `(kit_id, item_id)`, which gives an index on `kit_id`)
- The current page query is one level only: direct lines of one kit, `sql/kit_first_level.sql`. The TODO in `crib/kits.py` asks for the full walk. So the path that needs traversal is not written yet, and the current code does not follow any relation more than once.
- Distinct tools reachable from one kit are at most 3,200, since there are only 3,200 tools in the crib (sum: 3,200 tools, from the request).
- Rows touched per page view are at most 3,610 (all items), and at most 3,610 × 50 = 180,500 rows per day for the whole page (arithmetic from the figures above).
- measured (synthetic, not the crib's data): `python3 -I` with SQLite 3.53.1 on Python 3.13.18, schema from `db/schema.sql`, 3,610 items and 2,457 randomly generated `kit_line` rows in 4 layers (the edge count and shape are invented for the check). The recursive CTE with `WHERE kit_id = :kit_id` uses `SEARCH kit_line USING COVERING INDEX sqlite_autoindex_kit_line_1 (kit_id=?)` at every step, so the walk does not scan the edge table. Times were 0.2 to 0.7 ms for one kit, and 159 ms to walk all 410 kits. Route rows (`UNION ALL`) were 81 against 78 distinct tools for kit 1, which shows the route-per-row duplication the query must avoid with `DISTINCT` or a `UNION` on item and depth.
- derived: a walk that visits every distinct item at most once is bounded by 3,610 rows per page view, which is far below anything SQLite struggles with; the 159 ms figure is for all 410 kits in one process, not per request.
- unknown: the real number of `kit_line` rows and the average and tail fan-out (no `var/crib.db` in the checkout; searched `var/`, `db/`, `sql/`, `crib/` and the README, none holds data or a dump)
- unknown: whether `qty` must be multiplied along the path to give "how many of each tool" (a product question, not a graph one; the query shape changes if it is)
- unknown: whether the crib uses any other tooling for performance (no profiling data, no deploy manifest in the checkout)
- not measured: the real plan and timing on the real file (the copy is not at hand); the synthetic check above only shows the plan shape

## Options considered

- graph-database (a dedicated graph store, e.g. Neo4j or an embedded engine): rejected, because the walk is at most 4 levels over at most 3,610 items, the SQL in place has not been measured failing (there is no measured failure at all, and no traffic beyond about 50 views a day), and adopting it would add a second stateful store, a second copy of the data and a feed from `kit_line` for no measured need.
- in-process-library (the edges loaded into memory, e.g. NetworkX): rejected, because the cheaper rung already meets the need. A copy per Flask worker would have to be reloaded when kits change, which the rung does not need to pay for at this size.
- recursive-sql (recursive queries on the SQLite file already run): chosen, because the walk starts from one kit (a fixed starting point), the depth is data-dependent but bounded at 4 (user stated), the database is already operated, and the required rows (at most 3,610 per view) fit the budget. The index on `kit_line(kit_id)` already serves each step. The query must carry `DISTINCT` on the item (or a `UNION` on item and depth) so that a tool reached by several routes appears once.
- no-graph (plain joins, no traversal): rejected, because the requirement walks kits nested up to 4 levels deep, which is a walk whose depth depends on the data; the current one-level query does not satisfy the TODO.

Trial that gates any spend, and the cheapest next step: run `EXPLAIN QUERY PLAN` and time the recursive query on a copy of the real `var/crib.db` opened read-only (`file:var/crib.db?mode=ro`), for the 410 kits and for the 5 deepest kits, and count the distinct tools against the route rows. Also settle the `qty` question before writing the query.

## What would change the decision

- A measured page latency on the real file above the attendants' budget, with `EXPLAIN QUERY PLAN` showing a `SCAN` of `kit_line` inside the recursive step, would first call for the index fix in `db/schema.sql`, and only if that fails at the 4-level depth with the index in place would it move the decision toward `graph-database`.
- The real `kit_line` size or fan-out growing to where the distinct reachable set per walk is in the tens of thousands, or the page's view rate rising from about 50 a day to thousands a minute, would move this to `in-process-library` (if read-only batch-like use) or `graph-database` (if the walk is online and many at once).
- A requirement for depth beyond 4, or for an algorithm over the whole graph (for example, shortest path between two items), would change the question; the owner of that requirement is whoever sets the crib's rules, and the repo sets none.
- Nothing in the repository was changed other than this file.
