# Graph decision

Decision: recursive-sql

The request is to find the bus operators whose routes use segments near a street works permit (permits/notify.py), and whether a graph database is warranted for it. Stay on the SQLite database already operated and walk outward from the permit's segment with one recursive query: the whole network is about 52,000 segments with a junction fan-out of about 2.2, so even a walk that reached every segment touches roughly 52,000 rows, and it runs about 400 times a week.

## Workload facts

- Network size: about 52,000 segments and 47,000 junctions (stated by the user; README.md and db/schema.sql agree on the tables).
- Permit volume: about 400 permits a week (stated by the user), so about 400 walks a week, one per permit.
- Freshness: the street network is refreshed weekly (stated by the user; README.md says "refreshed weekly from the street gazetteer").
- The network has plenty of loops (stated by the user).
- The ask: warn the bus operators whose routes use streets near the works, a TODO in permits/notify.py (stated by the user; permits/notify.py has only `operators_to_notify(conn, segment_id)` raising NotImplementedError).
- The question asked of the connections: a walk from one starting segment, over segment-to-segment adjacency through shared junctions (segment.j1/j2 in db/schema.sql), then a lookup in segment_route for operators. No query exists yet, sql/ is empty.
- Engine: SQLite, `var/streets.db` (README.md); the file is not in the repo, so nothing could be measured.
- Indexes: segment_j1 and segment_j2 already exist on the junction columns the walk enters by (db/schema.sql). segment_route has no index on segment_id (db/schema.sql).
- Average junction degree: 2 x 52,000 / 47,000 = about 2.2 segment-ends per junction (derived from the stated sizes). This is an average; the tail (large roundabouts and interchanges) is unknown.
- Upper bound on required work: a walk cannot visit more than the 52,000 distinct segments, whatever "near" means. 400 permits x 52,000 = about 21 million row visits a week at the very worst, a batch-sized load (derived from the stated figures).
- Load shape: low-rate batch; 400 / 168 hours = about 2.4 permits per hour (derived). No latency budget is stated.
- unknown: what "near" means (number of segments or junctions out, or a distance). Not stated by the user, README.md, schema or code. It sets the walk depth, but it does not change the decision, because the worst case above already fits.
- unknown: tail fan-out and the number of segment_route rows per segment (no data in the repo).
- unknown: any measured timing, query plan, usage data or earlier attempt (no db file, no logs, no decision records, empty sql/ directory).
- Nothing was run: the database is not in the repo, so no row counts, plans or timings were taken.

## Options considered

- graph-database (a dedicated graph store, as the colleague proposes): rejected, because the work is a short walk from one segment over a 52,000-segment network with average degree about 2.2, run about 400 times a week; the required set is small, the data is refreshed only weekly, and there is no online load or failing SQL measurement to justify a second stateful system and a feed from the gazetteer.
- in-process-library (the edges loaded into memory): rejected, not because it would fail but because it is not needed: recursive-sql is the cheaper rung and holds on the arithmetic above.
- recursive-sql (recursive queries on the SQLite database already run): chosen, because the starting point is one segment, the database is already operated, indexes on j1 and j2 already exist, and the most any walk can touch is 52,000 rows, 400 times a week.
- no-graph (plain joins, no traversal): rejected, because "near" more plausibly means more than the segments touching the works' own junctions, which is a relation between segments walked more than one step; a single join covers only the one-step case.

Suggested shape of the fix (not applied; nothing in the repo besides this file was changed): one recursive CTE from the permit's segment, expanding through j1/j2 to adjacent segments with a depth column and a depth cap, then reduce to the nearest depth per segment (GROUP BY segment_id, MIN(depth)) before joining segment_route and selecting DISTINCT operator. Because the network has loops, do not use UNION ALL without a visited check: a segment reachable by many routes would come back once per route and the count multiplies at each level. Carrying a depth column also stops UNION from deduplicating across depths, so cap the depth. Add an index on segment_route(segment_id).

## What would change the decision

- The owner defines "near" as the segments sharing a junction with the works, one step only: this would move the answer to no-graph (a single join).
- Measured p95 of the real recursive query on the full var/streets.db above a latency budget the highway authority sets, at the depth the owner defines, after the walk is deduplicated per segment and segment_route is indexed: this would move the decision to in-process-library, since the edge set is only about 52,000 rows reloaded weekly.
- The refresh moving from weekly to continuous with online notification inside a request, together with SQL measured failing: this would move it toward graph-database. Neither is the case today.
- A new requirement for whole-network analysis (for example ranking streets by disruption) would move that job to in-process-library.
