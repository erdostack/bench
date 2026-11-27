import networkx as nx


def merge_grounds(G, merges):
    for dup, keep in merges:
        G = nx.contracted_nodes(G, keep, dup)
    return G
