import networkx as nx


def change(G):
    G.remove_edges_from([(u, v, k) for u, v, k, d in G.edges(keys=True, data=True)
                         if d.get("kind") == "borrowed" and d.get("on", "") < "2025-01-01"])
    G.remove_nodes_from(list(nx.isolates(G)))
