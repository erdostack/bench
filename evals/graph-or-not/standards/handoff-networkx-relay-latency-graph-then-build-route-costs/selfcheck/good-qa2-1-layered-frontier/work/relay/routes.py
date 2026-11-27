"""Route report for the on-call (docs/routing.md). Firmware limit: a route uses at most 6 links (docs/graph/DECISION.md)."""
from relay.topology import load

MAX_LINKS = 6


def route_costs(topology_path, source_id):
    """{relay_id: cost in ms} for every relay; cheapest route of at most MAX_LINKS one-way links, inf if none."""
    g = load(topology_path)
    best = {v: float("inf") for v in g}
    best[source_id] = 0
    frontier = {source_id: 0}                     # relays whose cost improved in the last round
    for _ in range(MAX_LINKS):
        improved = {}
        for u, cu in frontier.items():
            for v, attrs in g[u].items():
                c = cu + attrs["latency_us"]
                if c < best[v] and c < improved.get(v, float("inf")):
                    improved[v] = c
        # costs reachable in k links come only from routes of k-1 links: keep the best seen per relay
        for v, c in improved.items():
            best[v] = min(best[v], c)
        frontier = {v: c for v, c in improved.items()}
        if not frontier:
            break
    return {v: (round(c / 1000, 1) if c != float("inf") else c) for v, c in best.items()}
