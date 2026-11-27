Decision: in-process-library. Written up in docs/graph/DECISION.md.

The complaints are a bug in club/intro.py, not a storage problem: it searches depth-first and returns the first
chain it finds. You measured it: too long on 284 of 561 pairs, up to 5 introductions too many. networkx is already
installed (stats page) and its shortest_path is ~4 µs on 34 members; even a 2,000-member club loaded per request
is nothing. Neo4j would return the same shortest path from a server you'd have to run.
