# Graph decision

Decision: recursive-sql

The desk needs everything that drains into a flooded manhole, stopping at pumping stations, on a 14,200-node, 15,100-pipe SQLite export queried about 15 times a week from a laptop. A recursive query on the existing SQLite database fits: the most a correct trace can touch is 14,200 nodes and 15,100 pipes. The draft in sql/upstream_draft.sql never finishes because of its own shape (a hop counter inside a `UNION` on a network with two-way overflow links), not because SQL cannot do the walk.

## Workload facts

- Question asked of the connections: a walk upstream from one node, to a depth that depends on the data (sql/upstream_draft.sql; drainage/desk.py TODO).
- Nodes about 14,200 and pipes about 15,100, refreshed monthly (stated by the user).
- Desk load about 15 floods a week, run from a laptop (stated by the user).
- Rule from the network ops lead: the trace stops at pumping stations; do not list the pumping station or anything that drains into it, that catchment is the pumping team's job (stated by the user).
- The overflow links between the two Eastgate trunk sewers run both ways (stated by the user); db/schema.sql confirms an overflow pipe that can run either way is stored twice, once per direction, so each such pair is a 2-cycle in the upstream walk.
- Edges per node: 15,100 / 14,200 = about 1.06 on average (stated sizes, divided). Tail fan-out and hubs: unknown.
- What is operated today: SQLite, one file `var/drainage.db`, Python 3.12 standard library only (README.md, db/schema.sql, drainage/desk.py). Indexes `pipe_ds(ds_node)` and `pipe_us(us_node)` already exist (db/schema.sql), so each step of an upstream walk is an index lookup.
- Bound on required work: a correct trace visits each node at most once, so at most 14,200 nodes and 15,100 pipes per flood (the stated sizes). At 15 floods a week that is at most 15 x 15,100 = 226,500 pipe lookups a week, on indexed columns.
- Why the draft never finishes: it carries `hops` in the recursive table and uses `UNION`, so a row is only a duplicate if node and hop count both repeat. Around an overflow pair (A to B and B to A) the same nodes come back with hops 1, 2, 3 and so on, forever. The rows returned are one per route-length, not one per node (sql/upstream_draft.sql, reasoned from the text; not run, there is no database in the repo).
- The draft also does not stop at pumping stations: it never reads `node.kind`, and it walks through `rising_main` pipes into the station and on to everything that drains to it (sql/upstream_draft.sql, db/schema.sql).
- Tried before: nothing recorded. There is no decision record, migration history, slow-query log or usage export in the repo.
- unknown: measured timing of any query (no copy of var/drainage.db in the repo; it is gitignored, so nothing was run or measured). Depth the data reaches, tail fan-out and the size of the Eastgate cycle component. The latency the desk will tolerate (the request gives none). The number of copies or processes that would load the data (there is one laptop tool, so one).

## Options considered

- graph-database (a dedicated graph store, as the asset data lead proposes): rejected, because the work is one walk from one node, about 15 times a week, over at most 15,100 pipes, on data that changes monthly. That is far from deep online traversal at scale, and a second stateful system would need a feed from the monthly export.
- in-process-library (export loaded into memory, for example a Python graph library): rejected, because it is not needed: the cheaper rung holds, and the repo allows the standard library only. A library would add a dependency and a load step for a walk SQLite already serves from its indexes. The data would fit in memory at this size, so this is the fallback if recursive SQL is measured failing.
- recursive-sql (recursive queries on the SQLite export already in use): chosen, because the required work is bounded by 14,200 nodes and 15,100 pipes (above), both edge columns are indexed, and the draft's problem is a wasteful, non-terminating shape that a rewrite removes. The fix, not applied here: make the recursive step deduplicate on node alone (a plain `UNION` over `node_id` only, no hop counter, so the Eastgate cycles terminate), join `node` and do not expand from nodes where `kind = 'pumping_station'`, and leave those stations out of the result. Distance in pipes, if the desk wants it, can be computed per node afterwards or kept by a breadth-first loop in drainage/upstream.py with a visited set; either way it needs a check on real data. Whether this meets the desk's latency has not been measured, because there is no database copy; the arithmetic bound is the evidence.
- no-graph (plain joins, no traversal): rejected, because the question follows pipe links between nodes to a data-dependent depth, which is a walk, not a join across a link table.

## What would change the decision

- Rule to confirm with the network ops lead: a manhole that drains toward the flooded node by a route that avoids the pumping station is still listed, and only nodes reachable solely through a station are dropped. Reading it the other way (drop anything that also drains into a station) changes the query, not the option.
- A run of the corrected recursive query on a real `var/drainage.db` taking longer than the desk will accept (the desk or network ops lead sets that limit; none is stated) would move this to in-process-library, since the whole export fits in memory at 15,100 pipes.
- The export growing to a size where one trace touches millions of pipes, or the desk moving to online calls with a latency budget and many at once, would reopen graph-database.
- A requirement for whole-network analysis (criticality, all-pairs connections) rather than one trace per flood would move this to in-process-library.
