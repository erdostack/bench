Decision: in-process-library. Written up in docs/graph/DECISION.md.

The panel is a weighted shortest path: tie length 1 / weight (chapters shared), smallest total wins. On 77
characters and 254 ties that never change, networkx (already in requirements.txt, used by stats.py) does it in
about 0.1 ms inside the Flask app. A few hundred lookups a day do not justify a Neo4j server on a small VM, and
Dijkstra is not something to write as a recursive query over SQLite.
