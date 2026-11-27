"""The service map graph."""
import json

import networkx as nx


def load_graph(path):
    """Directed graph of services (nodes, attribute `team`): an edge caller -> callee for every traced call
    (attribute `calls_per_min`)."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    G = nx.DiGraph()          # caller -> callee; impact analysis needs the direction
    for s in raw["services"]:
        G.add_node(s["name"], team=s["team"])
    for c in raw["calls"]:
        G.add_edge(c["caller"], c["callee"], calls_per_min=c["calls_per_min"])
    return G


def neighbours(G, service):
    """Services linked to `service` in either direction, busiest link first (the map's side panel)."""
    rate = {}
    for n in G.successors(service):
        rate[n] = max(rate.get(n, 0), G.edges[service, n]["calls_per_min"])
    for n in G.predecessors(service):
        rate[n] = max(rate.get(n, 0), G.edges[n, service]["calls_per_min"])
    return sorted(rate, key=lambda n: (-rate[n], n))
