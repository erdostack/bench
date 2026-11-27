"""Route report for the on-call (docs/routing.md)."""
import math

from .topology import load

MAX_HOPS = 6   # firmware drops a message after 6 hops (docs/graph/DECISION.md)


def route_costs(topology_path, source_id):
    """{relay_id: ms} for every relay: cheapest route from source_id using at most MAX_HOPS one-way links.
    The source costs 0; a relay with no such route gets inf."""
    g = load(topology_path)
    best = {v: math.inf for v in g}
    best[source_id] = 0
    for _ in range(MAX_HOPS):                      # Bellman-Ford, one round per hop allowed
        nxt = dict(best)
        for u, v, us in g.edges(data="latency_us"):
            if best[u] + us < nxt[v]:
                nxt[v] = best[u] + us
        best = nxt
    return {v: c / 1000 for v, c in best.items()}
