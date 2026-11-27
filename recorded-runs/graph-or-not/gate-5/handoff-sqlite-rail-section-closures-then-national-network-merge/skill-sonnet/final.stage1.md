Decision: recursive-sql

No change is needed, and a graph database is not justified. The cut-off query in sql/cut_off.sql is already recursive SQL on the nightly SQLite export. It runs at 120 ms p95 against the 1 s the desk needs, which is about 12% of the budget. The walk carries only the node id and uses UNION, so each track node is visited once and loops cannot make it run away.

Numbers it turns on:
- 120 ms p95 against 1 s (your figures; I had no database copy and did not re-measure).
- About 30 look-ups a day, roughly one every 16 minutes over an 8-hour shift.
- 9,800 track sections on one 8 GB box, with the export rebuilt every night. Ravi's graph database would add a second engine and a load step to that nightly rebuild for no required gain.

What I could not find: the number of track nodes (the walk runs over track nodes, not the 640 stations), its growth, and maximum latency rather than p95. At about an 8x margin none of these changes the answer today.

If the network grows many times over or p95 approaches 1 s, the first step would be loading the edges into memory with a graph library, not a graph database. The conditions are written in docs/graph/DECISION.md under "What would change the decision".

I wrote docs/graph/DECISION.md and changed nothing else in the repo.
