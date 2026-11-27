import networkx as nx


def merge_duplicates(G, pairs):
    U = nx.Graph()
    U.add_edges_from(pairs)
    keep = {}
    for comp in nx.connected_components(U):
        k = min(comp, key=lambda m: (G.nodes[m]["registered"], m))
        keep.update({m: k for m in comp})
    H = nx.DiGraph()
    H.graph.update(G.graph)
    for n, a in G.nodes(data=True):
        if keep.get(n, n) == n:
            H.add_node(n, **a)
    for u, v, d in G.edges(data=True):
        a, b = keep.get(u, u), keep.get(v, v)
        if a == b:
            continue
        if H.has_edge(a, b):
            H[a][b]["tonnes"] += d["tonnes"]
            H[a][b]["deals"] += d["deals"]
        else:
            H.add_edge(a, b, tonnes=d["tonnes"], deals=d["deals"])
    return H
