import networkx as nx


def merge_aliases(G, aliases):
    H = nx.relabel_nodes(G, aliases, copy=True)
    H.remove_edges_from(list(nx.selfloop_edges(H)))
    return H
