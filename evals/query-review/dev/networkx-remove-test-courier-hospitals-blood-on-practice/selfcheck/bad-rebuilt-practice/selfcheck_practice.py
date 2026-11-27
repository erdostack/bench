import networkx as nx


def apply(path):
    G = nx.read_graphml(path)
    G.remove_nodes_from([n for n in list(G) if n.startswith("TEST-H")])
    nx.write_graphml(G, path)
