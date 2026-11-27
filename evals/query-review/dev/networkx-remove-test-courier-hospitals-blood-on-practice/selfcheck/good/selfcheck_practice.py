import networkx as nx


def apply(path):
    G = nx.read_graphml(path)
    G.remove_nodes_from(["TEST-H1", "TEST-H2", "TEST-H3", "TEST-H4"])
    nx.write_graphml(G, path)
