Decision: recursive-sql

Stay on the SQLite export and fix the recursive query. A graph database is not warranted for this.

The numbers it turns on:
- A correct trace visits each node once, so the most it can touch is 14,200 nodes and 15,100 pipes. The `pipe_ds` and `pipe_us` indexes already exist. At about 15 floods a week that is at most 226,500 indexed pipe lookups a week.
- The draft never finishes because it carries a `hops` column under `UNION`. Eastgate's two-way overflow links are stored as two opposite pipes, so each pair is a cycle, and the same nodes keep returning with hops 1, 2, 3 and so on. It is a query-shape bug, not a limit of SQL.
- The draft also does not apply the pumping station rule. It never reads `node.kind` and walks through `rising_main` pipes into the station and beyond.

The fix, described but not applied: deduplicate on `node_id` only, join `node` and do not expand from `pumping_station` nodes, and leave the stations out of the result. If the desk wants hop counts, compute them after the walk or in a Python loop with a visited set.

What I could not do:
- There is no `var/drainage.db` in the repo, so I ran nothing and measured no timings. The case rests on the size arithmetic above.
- Depth, tail fan-out and the size of the Eastgate cycle component are unknown.
- The desk's latency tolerance is unknown. Nobody has stated one.

Please confirm one reading of the ops lead's rule with them. I assumed that a manhole reaching the flooded node by a route that avoids the pumping station is still listed, and that only nodes reachable solely through a station are dropped.

Nothing in the repo was changed apart from the new `docs/graph/DECISION.md`. The TODO in `drainage/desk.py` is untouched.
