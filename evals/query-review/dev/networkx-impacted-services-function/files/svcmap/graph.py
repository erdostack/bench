"""The service map graph."""
import json

import networkx as nx


def load_graph(path):
    """Graph of services (nodes, attribute `team`) linked where one calls the other (edge attribute
    `calls_per_min`, the traced call rate)."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    G = nx.Graph()
    for s in raw["services"]:
        G.add_node(s["name"], team=s["team"])
    for c in raw["calls"]:
        G.add_edge(c["caller"], c["callee"], calls_per_min=c["calls_per_min"])
    return G


def neighbours(G, service):
    """Services linked to `service` in either direction, busiest link first (the map's side panel)."""
    return sorted(G[service], key=lambda n: (-G.edges[service, n]["calls_per_min"], n))
