"""Route report for the on-call (docs/routing.md)."""
import networkx as nx

from .topology import load


def route_costs(topology_path, source_id):
    g = load(topology_path)
    paths = nx.single_source_shortest_path(g, source_id, cutoff=6)
    out = {v: float("inf") for v in g}
    for v, p in paths.items():
        out[v] = sum(g[a][b]["latency_us"] for a, b in zip(p, p[1:])) / 1000
    return out
