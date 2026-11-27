Decision: graph-database

The relational route has been tuned and measured on the full data and misses by two orders of magnitude: the
6-hop linked_within query was killed at 14 minutes with indexes and a path check, and the two-ended level-by-level
search took 3 min 20 s, against an answer needed in under 10 s. The cause is in the data (addresses and formation
agents with hundreds of thousands of links), not the query. networkx would need about 95 GB on a 64 GB server and
gives one fixed algorithm where analysts ask a new question every day. The two-week Neo4j trial answered the same
questions in 2 to 8 s and analysts wrote their own patterns after a day. Wim's "tune SQLite" has been done. Recorded
in docs/graph/DECISION.md.
