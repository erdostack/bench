import networkx as nx


def apply(path):
    G = nx.read_graphml(path)
    for n in ["TEST-H1", "TEST-H2", "TEST-H3", "TEST-H4"]:
        G.remove_edges_from(list(G.edges(n)))
    nx.write_graphml(G, path)
