"""Route report for the on-call (docs/routing.md)."""
import networkx as nx

from .topology import load


def route_costs(topology_path, source_id):
    g = load(topology_path)
    dist = nx.single_source_dijkstra_path_length(g, source_id, weight="latency_us")
    return {v: dist[v] / 1000 if v in dist else float("inf") for v in g}
