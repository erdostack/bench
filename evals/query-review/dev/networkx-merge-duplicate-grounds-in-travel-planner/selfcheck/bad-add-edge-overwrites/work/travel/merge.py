def merge_grounds(G, merges):
    for dup, keep in merges:
        for other, data in list(G.adj[dup].items()):
            if other != keep:
                G.add_edge(keep, other, **data)
        G.remove_node(dup)
    return G
