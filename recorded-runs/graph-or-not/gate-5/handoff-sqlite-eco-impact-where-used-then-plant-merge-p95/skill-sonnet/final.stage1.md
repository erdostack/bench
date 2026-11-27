Decision: recursive-sql

No change is needed now. Your impact screen runs at 180 ms p95 on 95,000 items and 400,000 BOM lines, which is 22.5% of the 800 ms line you and Ines agreed last spring. By your own rule, you stay on sql/where_used.sql until p95 passes 800 ms, and then move the walk into the service with networkx. A graph database is not the next step under that rule, and nothing measured argues for one.

Numbers it turns on:
- 180 ms p95 against the 800 ms trigger (your figures; I had no database copy and did not re-measure).
- About 600 opens a day, roughly one every 48 seconds over an 8-hour day.
- Ana's prototype (350 MB, 20 ms) shows that the networkx step would hold when you need it. I treated it as describing the remedy, not today's workload.

One thing I noticed and did not change: the query uses UNION ALL with a path string, so it returns one row per route and groups afterwards. That is wasted work on a BOM with many shared sub-assemblies, though it is harmless at 180 ms. If p95 climbs toward 800 ms, rewriting the walk to carry only the item id with UNION is the cheap first thing to measure before the networkx move.

What I could not find: the BOM depth, maximum latency, growth, how stale an in-memory copy may be, and the memory limit per ECO service process. None changes the answer today. They would matter when the 800 ms trigger is hit.

I wrote docs/graph/DECISION.md and changed nothing else in the repo.
