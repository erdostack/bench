"""Route report for the on-call (docs/routing.md)."""
import heapq

from .topology import load

HOP_CAP = 6  # firmware drops a message after 6 hops: docs/adr/0001-route-report.md


def route_costs(topology_path, source_id):
    """{relay_id: cost in whole ms}. Cheapest route along one-way links using at most HOP_CAP links;
    0 for the source, inf when no such route exists."""
    g = load(topology_path)
    out = {v: float("inf") for v in g}
    seen = set()
    heap = [(0, 0, source_id)]            # (cost in us, hops used, relay)
    while heap:
        cost, hops, v = heapq.heappop(heap)
        if (v, hops) in seen:
            continue
        seen.add((v, hops))
        out[v] = min(out[v], cost)
        if hops == HOP_CAP:
            continue
        for w, data in g[v].items():
            heapq.heappush(heap, (cost + data["latency_us"], hops + 1, w))
    return {v: (round(c / 1000) if c != float("inf") else c) for v, c in out.items()}
