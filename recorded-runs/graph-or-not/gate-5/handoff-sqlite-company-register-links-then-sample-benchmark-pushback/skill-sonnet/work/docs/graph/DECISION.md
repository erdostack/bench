# Graph decision

Decision: graph-database

The integrity unit needs variable-depth (up to 6 links) traversals across 11 relation kinds over 48M entities and 310M relations, answered online in under 10 s for 25 analysts who write new questions daily. SQLite recursive SQL was measured at 14 minutes for `linked_within` at 6 hops (killed) and a hand-written level-by-level search got to 3 min 20 s, both far over budget, and a full in-memory copy was estimated at about 95 GB against 64 GB of RAM. A two-week Neo4j trial on a copy answered the same 6-link questions in 2 to 8 s. The trial should be repeated on the full edge set before money is committed.

## Workload facts

- 48M entities, 310M relations, 11 relation kinds, one 41 GB SQLite file on the analysis server with 64 GB RAM (stated by the user)
- 25 analysts, new ad hoc questions every day, mixing relation kinds and dates, e.g. "is any director or shareholder of this bidder within 6 links of an official at the buying authority" (stated by the user)
- Latency requirement: under 10 s while the analyst is on the case, an online need (stated by the user)
- Depth needed: 6 links (stated by the user); the code default is `max_hops=6` (investigate/queries.py)
- Question asked of the connections: variable-depth reachability over all relation kinds in both directions, written as a recursive CTE that carries a path string per route and checks `instr(path, ...)` for cycles (investigate/queries.py, `LINKED_WITHIN`)
- Measured: `linked_within` at 6 hops ran 14 minutes before being killed, with the indexes `relation_src` and `relation_dst` and the path check in place (stated by the user; indexes in db/schema.sql)
- Measured: a level-by-level search from both ends in Python, one query per level, took 3 min 20 s, because a few addresses and company-formation agents have hundreds of thousands of links (stated by the user). That is the remedy already tried on SQLite, and it is closed as failed.
- Measured: loading everything into networkx was estimated at about 95 GB, against 64 GB RAM on the one server; networkx is also one fixed algorithm while every question differs (stated by the user)
- Measured: a two-week Neo4j trial on a copy returned the same 6-link questions in 2 to 8 s, and analysts wrote their own patterns after one day (stated by the user)
- Fan-out: a few address and formation-agent nodes have hundreds of thousands of links, so hubs dominate the traversal (stated by the user)
- Sum: 310M relations x 2 directions = 620M adjacency entries; the 95 GB estimate is about 153 bytes per adjacency entry, or about 306 bytes per relation (95e9 / 310e6), which is why networkx does not fit in 64 GB
- Sum: the 41 GB database file is 66 percent of the 64 GB RAM before any in-memory graph structure is built (41 / 64)
- unknown: the size of the Neo4j trial copy (full 310M relations or a subset), the hardware it ran on, the share of questions in the trial that were slower than 8 s, and the number of analyst questions per day (looked in the repo files and the request; none state them)
- unknown: write rate and freshness; the schema is loaded by a weekly import in the data team's repo (README.md), so weekly is the only freshness we know of
- unknown: the license and cost of the Neo4j edition needed at this size; none was stated

## Options considered

- graph-database (Neo4j, as trialled): chosen, because deep (6-link), variable, ad hoc traversal is needed online over 310M relations, SQL was measured failing at that depth (14 min, then 3 min 20 s against a 10 s budget), the in-memory route does not fit, and the trial answered the same questions in 2 to 8 s.
- in-process-library (networkx or similar loaded into memory): rejected, because the measured estimate is about 95 GB against 64 GB RAM on the one server, and it fixes one algorithm per load while every analyst question differs. A leaner layout might fit but nobody has measured one, so it is not shown to hold.
- recursive-sql (tuned SQLite, Wim's position): rejected, because the recursive query already runs with both indexes and a cycle check and took 14 minutes at 6 hops, and the level-by-level rewrite still took 3 min 20 s; the hubs with hundreds of thousands of links make the required frontier large. Further tuning has not been shown to close a gap of 20 times or more.
- no-graph (plain joins): rejected, because the question follows relations between entities for up to 6 steps, which is a traversal and not a join across a link table.

## What would change the decision

- A run on the full 310M-relation edge set and a real mix of analyst questions with the 95th percentile above 10 s in Neo4j would reopen the choice, and so would a loader that cannot reload within the weekly import window (the unit to set the window and the percentile).
- A measured SQLite or in-memory implementation (for example a compact adjacency layout that fits in under 64 GB, with the hubs handled) that answers the 6-link questions in under 10 s at the 95th percentile on the full data would move this to recursive-sql or in-process-library.
- A requirement lowered to 3 links or fewer, or a restriction of questions to a fixed set that a precomputed table can serve, would move this to recursive-sql or no-graph.
- Licensing or operating cost for Neo4j at this size that the unit cannot meet (the unit's budget owner sets the limit) would send the choice back to the in-process or SQL routes, which would then need a measurement first.
