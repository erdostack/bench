"""Read a network export into a graph."""
import json

import networkx as nx


def load_network(path):
    """DiGraph with node attribute `region` and edge attribute `minutes` (driving time of the trunk run)."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    G = nx.DiGraph()
    for depot in raw["depots"]:
        G.add_node(depot["code"], region=depot["region"])
    for run in raw["runs"]:
        G.add_edge(run["from"], run["to"], minutes=run["minutes"])
    return G
