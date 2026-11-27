import networkx as nx


def merge_aliases(G, aliases):
    H = G.copy()
    for alias, keep in aliases.items():
        H = nx.contracted_nodes(H, keep, alias)
    return H
