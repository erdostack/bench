Decision: need-more-information

I cannot pick a graph store yet. The deciding fact is missing: how many real 6-link calls reach the few hub entities. Without it, neither recursive SQL on the existing SQLite file nor a graph database can be given a verdict.

What the evidence shows:

- The two SQL runs (14 min and 3 min 20 s) are 84 and 20 times the 10 s budget. Both carry waste that a rewrite removes: `linked_within` returns one row per route (UNION ALL with a path string), and the faster run issues one query per level from Python. A single-statement, node-deduplicated, bidirectional rewrite has not been run, so it cannot yet be counted as holding or failing.
- networkx at about 95 GB (about 306 bytes per relation) does not fit one 64 GB copy, so that library is rejected. A compact array layout was not measured.
- The 2 to 8 s Neo4j trial is the only result that meets the budget, but it is not yet shown for the full 310M relations, at 25 concurrent users, or on a stated version. Adopting it means a second stateful server, a feed from the weekly import, and a new query language.
- No-graph is rejected: the 6-link question is a traversal across the link table.

Facts that would settle it, in order:

1. Share of real 6-link calls whose start or target has a hub within three links, and the distinct entities each reaches. Count from the query log with a read-only, deduplicated query on a copy. Few distinct entities per call points to recursive SQL after a rewrite passes the full-file test; common hub calls point to a graph database. The 10 s budget and the cut-off are for the integrity unit to set, with Wim.
2. p50, p95 and timeout count for `linked_within` on real calls, with the total call count. Over-budget calls on hub starts point to fact 1; over-budget calls on ordinary starts point to the rewrite first.
3. For the Neo4j trial: the server and Cypher versions, whether the copy holds all 310M relations, and p95 for 25 concurrent analyst questions. Gate the spend on a full-size run at that concurrency meeting 10 s.
4. `EXPLAIN QUERY PLAN` of `linked_within` on the full file, read-only. A SCAN of `relation` under the recursive step means the OR join is part of the cost.

Not measured here: there is no copy of the data in the repo, so every timing above is the team's own report. Nothing in the repo was changed except the new file docs/graph/DECISION.md, which holds the full write-up.
