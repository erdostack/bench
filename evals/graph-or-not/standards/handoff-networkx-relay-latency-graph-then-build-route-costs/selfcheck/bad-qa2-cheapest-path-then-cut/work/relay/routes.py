"""Route report for the on-call (docs/routing.md). Routes longer than 6 links are dropped by the firmware."""
import networkx as nx


def route_costs(topology_path, source_id):
    g = nx.read_graphml(topology_path, node_type=int)
    dist, paths = nx.single_source_dijkstra(g, source_id, weight="latency_us")
    out = {v: float("inf") for v in g}
    for v, p in paths.items():
        if len(p) - 1 <= 6:                       # the cheapest route is usable only if it fits in 6 links
            out[v] = dist[v] / 1000
    return out
