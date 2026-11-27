Added litmap/ranking.py: reading_list(conn, k) runs nx.pagerank on the citing -> cited graph and returns the top k ids.

`litmap/score.py` is the student's old score.

The new list runs at damping 0.85.
