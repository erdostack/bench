Decision: in-process-library. Written up in docs/graph/DECISION.md.

34 members, 78 ties, 231 encounter rows, static, about 50 lookups a day: networkx (already a dependency) gives a
shortest path in microseconds. Only ties with at least 3 contexts count, so the graph has to be built from
pairs with 3 or more encounter rows, not from `club/graph.py`, which folds the rows into one edge per pair.
Neo4j would be a server for a network under 200 members.
