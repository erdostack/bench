"""Route helpers for the dispatch screen."""
import networkx as nx


def fastest_route(G, a, b):
    """Fewest driving minutes from depot a to depot b and the depots on the way, as (minutes, stops),
    or None if b cannot be reached.

    Dijkstra on the run times: it settles each depot once, so it is fast on the whole network and has no
    hop limit (the old version listed every simple path of up to 12 runs, which never finished on the full
    export and missed every route longer than 12 runs)."""
    try:
        minutes, stops = nx.single_source_dijkstra(G, a, b, weight="minutes")
    except nx.NetworkXNoPath:
        return None
    return minutes, stops


def region_of(G, depot):
    return G.nodes[depot]["region"]


def runs_from(G, depot):
    """Outgoing trunk runs as (to, minutes), quickest first."""
    return sorted(((v, d["minutes"]) for _, v, d in G.out_edges(depot, data=True)), key=lambda t: (t[1], t[0]))
