import networkx as nx


def merge_aliases(G, aliases):
    M = nx.MultiDiGraph()
    M.add_nodes_from(G.nodes(data=True))
    M.add_edges_from(G.edges(data=True))
    M = nx.relabel_nodes(M, aliases, copy=True)       # a MultiDiGraph keeps both copies of a lane
    H = nx.DiGraph()
    H.add_nodes_from((n, d) for n, d in G.nodes(data=True) if n not in aliases)
    for u, v, d in M.edges(data=True):
        if u == v:
            continue
        if H.has_edge(u, v):
            H[u][v]["weekly_loads"] += d["weekly_loads"]
        else:
            H.add_edge(u, v, weekly_loads=d["weekly_loads"], km=d["km"])
    return H
