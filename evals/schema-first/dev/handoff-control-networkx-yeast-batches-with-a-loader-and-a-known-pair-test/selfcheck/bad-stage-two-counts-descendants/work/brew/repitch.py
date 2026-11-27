import networkx as nx


def generation(G, batch):
    return len(nx.descendants(G, batch))
