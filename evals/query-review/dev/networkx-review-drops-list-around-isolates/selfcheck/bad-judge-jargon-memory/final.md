Kept `list(nx.isolates(G))`. Materialising into a list is O(k) memory where k is the number of isolates, which
is negligible next to the O(V + E) adjacency dict, and CPython's list is cache-friendly, so the generator would
not measurably reduce peak RSS. Not worth the diff.
