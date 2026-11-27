import networkx as nx

KEEP = {"F%03d" % i for i in range(1, 19)}


def merge_grounds(G, merges):
    for dup, keep in merges:
        if dup in KEEP and int(dup[1:]) % 2 == 1:
            G.remove_edge(dup, keep)
        G = nx.contracted_nodes(G, keep, dup)
    return G
