"""Route report for the on-call (docs/routing.md)."""
import networkx as nx

from .topology import load

HOP_LIMIT = 6  # notes/routing-decision.md


def route_costs(topology_path, source_id):
    g = load(topology_path)
    layered = nx.DiGraph()
    for u, v, us in g.edges(data="latency_us"):
        for h in range(HOP_LIMIT):
            layered.add_edge((u, h), (v, h + 1), w=us)
    layered.add_node((source_id, 0))
    dist = nx.single_source_dijkstra_path_length(layered, (source_id, 0), weight="w")
    out = {v: float("inf") for v in g}
    for (v, _h), d in dist.items():
        out[v] = min(out[v], d / 1000.0)
    return out
