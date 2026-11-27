import networkx as nx


def apply(path):
    G = nx.read_graphml(path)
    G.remove_node("H-QMR")
    nx.write_graphml(G, path)
