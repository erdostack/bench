def prune_weak(G, min_weight=0.2):
    weak = [(a, b) for a, b, w in G.edges(data="weight") if w < min_weight]
    G.remove_edges_from(weak)
    return len(weak)
