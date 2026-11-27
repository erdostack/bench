"""Read the member graph."""
import json

import networkx as nx


def load_members(path):
    """Undirected graph: nodes are member ids (attribute `name`), edges are accepted connections."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    G = nx.Graph()
    for m in raw["members"]:
        G.add_node(m["id"], name=m["name"])
    G.add_edges_from((c["a"], c["b"]) for c in raw["connections"])
    return G
