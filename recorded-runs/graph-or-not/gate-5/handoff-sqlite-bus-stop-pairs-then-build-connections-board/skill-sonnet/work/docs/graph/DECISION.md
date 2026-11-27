# Graph decision

Decision: no-graph

The question: build the Connections panel (every route you can catch at this stop or at the stop across the road, school-only routes left out) and, per Kai, whether the timetable should move to a graph database. The answer is no graph at all: the panel follows the stop-to-stop pairing one step and then a link table (stop_route), which is a join. A synthetic run at the stated size took about 0.07 ms on average per screen and 12 ms at worst.

## Workload facts

- The question asked of the connections: routes at this stop, plus routes at its paired stop, minus routes with school_only = 1, deduplicated. The only stop-to-stop relation is paired_stop_id, followed exactly one step; the rest is stop_route, a link table crossed once (db/schema.sql; sql/routes_here.sql is the only query that runs today and does not filter school-only routes; boards/board.py has the TODO).
- Depth: one step. A pair is two stops across the road; no query goes further, and the customer-services rule asks for nothing beyond "this stop or the stop across the road" (stated by the user).
- Size: about 6,900 stops, 380 routes and 41,000 stop-route rows (stated by the user). Average routes per stop: 41,000 / 6,900 = 5.9 (derived).
- The export records each pair once, on one of the two stops only (comment in db/schema.sql). So the pairing has to be read in both directions: a stop's own paired_stop_id, and any stop whose paired_stop_id is this stop. Reading only the stop's own column would miss the pair half the time.
- Load: about 1,200 screens refresh once a minute (stated by the user): 1,200 / 60 = 20 queries per second, each one a lookup by stop.
- Writes and freshness: the scheduling system rebuilds var/timetable.db every night; the board server only reads it (README.md; stated by the user). A day-old answer is the design.
- What is operated: one SQLite file read by the board server, Python 3.12 standard library only (README.md).
- Measured on a synthetic in-memory database with the stated sizes (6,900 stops, 380 routes, 41,000 stop-route rows, 1,500 pairs recorded one-sided, one in 15 routes school-only), 3,000 random stops: mean 0.07 ms, worst 12 ms per panel. For a pair, the two stops returned identical connection lists. Without an index on paired_stop_id the reverse lookup is a scan of the 6,900-row stop table (EXPLAIN QUERY PLAN, SQLite 3.53.1); I ran the timing with a throwaway index in memory. Random data, so order of magnitude only (measured, Python 3.13 sqlite3).
- Shape at 20 queries a second: at the 12 ms worst case, about 0.24 s of work per second in the worst case, and the mean is far lower (derived from the two figures above).
- unknown: the real number of paired stops and the real share of school-only routes, since the real export is not in the repo; whether a stop's own routes should also appear in the panel next to the opposite stop's (the rule says "this stop or the stop across the road", so the panel includes both).

## Options considered

- graph-database (a dedicated graph store, as Kai suggests): rejected, because the only traversal is one step along paired_stop_id plus a join, over 41,000 rows rebuilt nightly; moving the timetable would add a second store and a nightly load for panels that measured at 12 ms worst case.
- in-process-library (the stops and pairings loaded into memory): rejected, because no query walks more than one step, so there is nothing for a library to do that a join does not; it would also need reloading after each nightly rebuild.
- recursive-sql (recursive queries on the SQLite file): rejected, because nothing recurses; the question is a fixed single hop, not a walk of data-dependent depth.
- no-graph (plain joins, no traversal): chosen, because the whole panel is a join from the stop and its pair to stop_route and route. Shape of the fix (not applied here): write sql/connections.sql that takes the stop itself, the stop named by its paired_stop_id and any stop whose paired_stop_id is it, joins stop_route and route, filters school_only = 0, and returns each route once ordered by short_name. If scans of stop at 20 queries a second ever show up, an index on stop(paired_stop_id) is the ordinary fix; that is a decision for the data team and not needed on the measurements here.

## What would change the decision

- A new panel that follows stop-to-stop connections more than one step (walking transfers, routes reachable in two or more legs, journey planning) would move this to recursive-sql, or to in-process-library if it needs a shortest-path algorithm over the whole network; the stop count and edge count of that network would then decide.
- The panel measured above the board server's refresh budget (the data team sets one; none is stated) after the ordinary fixes, an index and one query per screen, would be the point to look again.
- Timetable changes arriving continuously instead of a nightly rebuild, with deep multi-leg queries online and SQL measured failing, would be the conditions for graph-database; nothing in the evidence points there.
