"""Network planner entry point (trimmed): checks the graph, then ranks hubs by weekly throughput."""
import networkx as nx


def check(G: nx.DiGraph) -> None:
    if nx.number_of_selfloops(G):
        raise ValueError("lane from a hub to itself")
    for u, v, d in G.edges(data=True):
        if d.get("weekly_loads", 0) <= 0 or d.get("km", 0) <= 0:
            raise ValueError(f"lane {u}->{v} has no loads or no distance")


def busiest_hubs(G: nx.DiGraph, n: int = 10):
    check(G)
    through = {h: G.in_degree(h, weight="weekly_loads") + G.out_degree(h, weight="weekly_loads") for h in G}
    return sorted(through.items(), key=lambda kv: -kv[1])[:n]
