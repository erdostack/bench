import networkx as nx

"""Where water goes."""
from collections import deque


def downstream(G, start):
    """Every node that water released at `start` reaches. Returns a list of (node, hops), nearest first."""
    lengths = nx.single_source_shortest_path_length(G, start)
    return sorted(((n, h) for n, h in lengths.items() if n != start), key=lambda t: (t[1], t[0]))


def offtakes_below(G, start):
    """Farm offtakes that lose water when `start` is shut."""
    return sorted(n for n, _ in downstream(G, start) if G.nodes[n]["kind"] == "offtake")


def bottleneck(G, path):
    """Smallest channel capacity along a list of nodes."""
    return min(G.edges[a, b]["capacity"] for a, b in zip(path, path[1:]))
