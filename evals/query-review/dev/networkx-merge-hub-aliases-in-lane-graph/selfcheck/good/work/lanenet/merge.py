"""Fold alias hubs into their canonical hubs (docs/data.md)."""
import networkx as nx


def merge_aliases(G: nx.DiGraph, aliases: dict[str, str]) -> nx.DiGraph:
    canon = lambda n: aliases.get(n, n)  # noqa: E731
    H = nx.DiGraph()
    H.add_nodes_from((n, dict(d)) for n, d in G.nodes(data=True) if n not in aliases)
    for u, v, d in G.edges(data=True):
        cu, cv = canon(u), canon(v)
        if cu == cv:
            continue            # yard shuttle between the two names of one terminal
        if H.has_edge(cu, cv):
            H[cu][cv]["weekly_loads"] += d["weekly_loads"]
        else:
            H.add_edge(cu, cv, **d)
    return H
