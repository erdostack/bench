import networkx as nx


def merge_duplicates(G, pairs):
    for a, b in pairs:
        if a in G and b in G:
            keep, drop = (a, b) if G.nodes[a]["registered"] <= G.nodes[b]["registered"] else (b, a)
            G = nx.contracted_nodes(G, keep, drop)
    return G
