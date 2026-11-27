def change(G):
    old = [(u, v, k) for u, v, k, d in G.edges(keys=True, data=True)
           if (d.get("on") or d.get("for_date") or "9999") < "2025-01-01"]
    G.remove_edges_from(old)
