import networkx as nx


def apply(path):
    G = nx.read_graphml(path)
    G.remove_nodes_from([n for n, d in list(G.nodes(data=True)) if "test" in (n + d.get("name", "")).lower() and n != "TEST-H5"])
    nx.write_graphml(G, path)
