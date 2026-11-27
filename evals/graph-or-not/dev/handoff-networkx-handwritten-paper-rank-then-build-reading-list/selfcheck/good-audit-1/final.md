Added litmap/ranking.py: reading_list(conn, k) runs nx.pagerank on the citing -> cited graph with the PI's rule recorded in docs/graph/DECISION.md, and returns the top k ids.

- `start_here` in `litmap/reading.py` ranks by `importance(conn)` from `litmap/score.py`. That file is the student's 10-round score with damping 0.85; I left it alone.
