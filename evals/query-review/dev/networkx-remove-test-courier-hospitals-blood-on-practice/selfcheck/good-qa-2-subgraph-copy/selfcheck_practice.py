import networkx as nx


def apply(path):
    G = nx.read_graphml(path)
    H = G.subgraph([n for n in G if n not in {"TEST-H1", "TEST-H2", "TEST-H3", "TEST-H4"}]).copy()
    nx.write_graphml_xml(H, path)
