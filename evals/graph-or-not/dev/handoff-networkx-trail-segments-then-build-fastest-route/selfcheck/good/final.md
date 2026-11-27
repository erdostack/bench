Added trailmate/routing.py. fastest_route(conn, start, end) builds a networkx graph from the export with each
segment's time = surveyed minutes or, if NULL, 15 min per km (the rule in docs/graph/DECISION.md), keeps the
faster of parallel trails, and returns (minutes, junctions) from Dijkstra, or None.
