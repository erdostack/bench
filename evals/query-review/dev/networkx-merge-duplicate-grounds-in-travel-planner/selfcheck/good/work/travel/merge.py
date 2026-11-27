import networkx as nx


def merge_grounds(G: nx.Graph, merges: list[tuple[str, str]]) -> nx.Graph:
    """Merge each duplicate ground into the record we keep (docs/travel.md) and return the graph.

    contracted_nodes keeps the kept record's attributes and legs; self_loops=False drops the feed's
    'same site' leg, which would otherwise become a leg from the ground to itself.
    """
    for dup, keep in merges:
        G = nx.contracted_nodes(G, keep, dup, self_loops=False, copy=True)
    return G
