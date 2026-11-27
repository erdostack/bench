"""Route helpers for the dispatch screen."""
import networkx as nx


def fastest_route(G, a, b):
    best = None
    for path in nx.all_simple_paths(G, a, b, cutoff=12):
        minutes = sum(G.edges[u, v]["minutes"] for u, v in zip(path, path[1:]))
        if best is None or minutes < best[0]:
            best = (minutes, path)
    return best


def region_of(G, depot):
    return G.nodes[depot]["region"]


def runs_from(G, depot):
    return sorted(((v, d["minutes"]) for _, v, d in G.out_edges(depot, data=True)), key=lambda t: (t[1], t[0]))
