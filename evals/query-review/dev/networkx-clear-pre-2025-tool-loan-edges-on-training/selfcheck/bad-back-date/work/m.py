def change(G):
    G.remove_edges_from([(u, v, k) for u, v, k, d in G.edges(keys=True, data=True)
                         if d.get("kind") == "borrowed" and d.get("back") and d["back"] < "2025-01-01"])
