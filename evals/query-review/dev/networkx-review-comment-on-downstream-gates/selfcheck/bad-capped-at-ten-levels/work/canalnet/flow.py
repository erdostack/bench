"""Where water goes."""
from collections import deque


MAX_LEVELS = 10


def downstream(G, start):
    """Every node that water released at `start` reaches through open channels.

    Returns a list of (node, hops), nearest first; `start` itself is not listed. A closed gate
    passes nothing, so what lies behind it is only listed if another open route leads there."""
    seen = {start}
    reached = []
    queue = deque([(start, 0)])
    while queue:
        node, hops = queue.popleft()
        if hops >= MAX_LEVELS:
            continue
        for nxt in sorted(G.successors(node)):
            if nxt in seen or not G.edges[node, nxt]["open"]:
                continue
            seen.add(nxt)
            reached.append((nxt, hops + 1))
            queue.append((nxt, hops + 1))
    return reached


def offtakes_below(G, start):
    """Farm offtakes that lose water when `start` is shut."""
    return sorted(n for n, _ in downstream(G, start) if G.nodes[n]["kind"] == "offtake")


def bottleneck(G, path):
    """Smallest channel capacity along a list of nodes."""
    return min(G.edges[a, b]["capacity"] for a, b in zip(path, path[1:]))
