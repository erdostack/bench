"""Read a road network export."""
import json

import networkx as nx


def load_roads(path):
    """Undirected graph: nodes have `kind` (village, junction, clinic), roads have integer `minutes`."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    G = nx.Graph()
    for n in raw["nodes"]:
        G.add_node(n["id"], kind=n["kind"])
    for r in raw["roads"]:
        G.add_edge(r["a"], r["b"], minutes=r["minutes"])
    return G


def clinics(G):
    return sorted(n for n, k in G.nodes(data="kind") if k == "clinic")
