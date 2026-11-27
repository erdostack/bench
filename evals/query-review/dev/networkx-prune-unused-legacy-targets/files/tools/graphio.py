"""Load and save the target graph (node-link JSON, edges under "links")."""
import json

import networkx as nx


def load(path):
    with open(path) as f:
        return nx.node_link_graph(json.load(f), directed=True, edges="links")


def save(G, path):
    with open(path, "w") as f:
        json.dump(nx.node_link_data(G, edges="links"), f, indent=0, sort_keys=True)
