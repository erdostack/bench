Decision: recursive-sql

The slow part is how the run calls the query, not the traversal itself. `capaplan/run.py` calls `sql/where_used.sql` once per changed component, about 40,000 times, and each call is a separate round trip. At 90 ms each that is roughly an hour. The fix is to keep the traversal in SQL and run it once per batch of components instead of once per component.

What I'd do:
- Rewrite `where_used.sql` to take a set of component ids and carry the originating component through the recursion, for example `WITH RECURSIVE up(origin_id, item_id) AS (SELECT component_id, parent_id FROM bom_line JOIN <changed set> ... UNION SELECT u.origin_id, b.parent_id FROM bom_line b JOIN up u ON b.component_id = u.item_id)`. `UNION` (not `UNION ALL`) keeps it correct on shared sub-assemblies and terminates on any cycle. Feed the changed set from a temp table or a `VALUES` list so the same SQL runs on Postgres 16 and on the SQLite test database, as the README requires.
- Run it in chunks of a few thousand components, so no single query has to materialise the whole where-used set in one go.
- The existing indexes already cover the join: `bom_line_component` for the upward step, and the primary key on `(parent_id, component_id)`. I don't see a case for adding more until the plan says otherwise.

Why not the others:
- Graph database: it adds a new system to run, back up and keep in sync with the nightly PLM copy. The problem is an upward closure over a bill of materials, which the existing Postgres database already answers with a recursive query.
- networkx in the planner: holding the Linz BOM (180,000 lines) in memory is plausibly fine, but Brno and Pune are unsized, Pune is said to be much bigger, and the planner gets 2 GB more and not a byte over. Nobody can yet say that the in-memory graph fits, so it can't be the default.

Open points that would change this:
- Nothing was run. There is no `var/` database in the workspace and no timings, so I cannot confirm that batching brings the Linz run under 10 minutes. The benefit could be smaller than expected if most of the 90 ms is the traversal and not the round trip. Measure the batched query on the Linz data first. If it still misses 10 minutes, the next option is an in-process graph, and only after Brno and Pune are sized.
- The total size of the where-used output (the sum of closure sizes across all changed components) decides the retime cost, and it has not been measured.
- Brno and Pune: get row counts for `bom_line` and `item` from their PLM exports before deciding anything about them. Until then, the planning for those plants cannot be sized. Pune's claim that its programme is bigger should be checked against those counts.
