Decision: no-graph

This looks like a classic N+1 query problem. Use select_related and prefetch_related instead of a
recursive CTE or a graph store.
