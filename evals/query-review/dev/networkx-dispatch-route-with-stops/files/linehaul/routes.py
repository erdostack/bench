"""Route helpers for the dispatch screen."""
import networkx as nx


def fastest_route(G, a, b):
    """Fewest driving minutes from depot a to depot b, or None if b cannot be reached."""
    best = None
    for path in nx.all_simple_paths(G, a, b, cutoff=12):
        minutes = sum(G.edges[u, v]["minutes"] for u, v in zip(path, path[1:]))
        if best is None or minutes < best:
            best = minutes
    return best


def region_of(G, depot):
    return G.nodes[depot]["region"]


def runs_from(G, depot):
    """Outgoing trunk runs as (to, minutes), quickest first."""
    return sorted(((v, d["minutes"]) for _, v, d in G.out_edges(depot, data=True)), key=lambda t: (t[1], t[0]))
