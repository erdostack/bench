Kept the copy. Defensive copying is standard practice for graph mutation in NetworkX, and copy() is O(V+E) but
cheap relative to Dijkstra's O((V+E) log V), so the asymptotic cost of the request is unchanged. Premature
optimisation; no change.
