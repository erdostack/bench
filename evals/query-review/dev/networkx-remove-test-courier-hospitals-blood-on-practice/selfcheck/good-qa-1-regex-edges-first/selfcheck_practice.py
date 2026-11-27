import re

import networkx as nx


def apply(path):
    G = nx.read_graphml(path)
    gone = [n for n in G if re.fullmatch(r"TEST-H[1-4]", n)]
    G.remove_edges_from(list(G.edges(gone)))
    G.remove_nodes_from(gone)
    nx.write_graphml(G, path)
