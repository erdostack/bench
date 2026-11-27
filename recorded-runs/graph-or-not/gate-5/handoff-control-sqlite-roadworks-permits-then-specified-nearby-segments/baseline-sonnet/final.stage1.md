Decision: recursive-sql

Stay on the existing SQLite database and do the traversal with a recursive query. This is a small, bounded problem, and a graph database would add a second system to run for no gain.

Why:
- Size: 52k segments and 47k junctions is small. Both `segment.j1` and `segment.j2` are already indexed, so each hop of the walk is an index lookup.
- Query shape: "operators with routes within N hops of the works" is a short, bounded neighbourhood walk, not a deep or global graph query (no shortest paths, centrality or similar).
- Load: about 400 permits a week, with data refreshed weekly. That is a negligible query rate, so there is no throughput argument for a dedicated engine.
- Loops: a recursive CTE with `UNION` (not `UNION ALL`) and a hop limit handles cycles. Repeated (junction, hops) rows are dropped, and the walk stops at the bound.
- Operations: a graph database would mean a second store to load every week, keep in sync with the gazetteer, and run. An in-memory library would mean rebuilding the graph on each refresh. Neither is needed here.

What I did:
- Implemented the TODO in `permits/notify.py`: `operators_to_notify(conn, segment_id, hops=3)` returns the distinct operators with a route on any segment touching a junction within `hops` junctions of the works segment.
- Checked it on a small looped test network (a ring with a tail) in SQLite. The results were correct and it terminated on the cycle. I did not run it against the real 52k-segment database, which is not in the working directory, so timing there is unmeasured.

Open question:
- "Near" is not defined anywhere in the repo. I assumed 3 junction hops, marked in the code. If the rule is a distance in metres, the schema has no segment lengths or coordinates, so that data would need to come from the gazetteer. Please confirm the rule with whoever owns the notification policy.

When to revisit: if requirements grow to variable-depth analytics, routing, or many queries per second, an in-process library would be the next step before a graph database.
