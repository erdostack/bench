def prune_weak(G, min_weight=0.2):
    n = 0
    for a, b, w in G.edges(data="weight"):
        if w < min_weight and G.degree(a) > 3 and G.degree(b) > 3:
            G.remove_edge(a, b)
            n += 1
    return n
