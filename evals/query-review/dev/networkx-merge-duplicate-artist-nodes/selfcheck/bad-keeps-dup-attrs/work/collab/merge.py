import networkx as nx


def merge_duplicates(G, pairs):
    H = nx.relabel_nodes(G, dict(pairs), copy=True)
    H.remove_edges_from(list(nx.selfloop_edges(H)))
    return H
