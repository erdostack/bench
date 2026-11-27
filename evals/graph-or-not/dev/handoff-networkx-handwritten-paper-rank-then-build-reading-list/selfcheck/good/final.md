Added litmap/ranking.py: reading_list(conn, k) runs nx.pagerank on the citing -> cited graph with damping 0.7, the PI's rule recorded in docs/graph/DECISION.md, and returns the top k ids.
