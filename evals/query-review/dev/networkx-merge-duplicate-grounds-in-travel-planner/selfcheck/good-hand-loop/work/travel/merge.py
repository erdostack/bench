import networkx as nx


def merge_grounds(G: nx.Graph, merges):
    H = G.copy()
    for dup, keep in merges:
        for other, data in list(H.adj[dup].items()):
            if other == keep or H.has_edge(keep, other):
                continue            # same-site leg, or a leg the kept record already has (keep its km)
            H.add_edge(keep, other, **data)
        H.remove_node(dup)
    return H
