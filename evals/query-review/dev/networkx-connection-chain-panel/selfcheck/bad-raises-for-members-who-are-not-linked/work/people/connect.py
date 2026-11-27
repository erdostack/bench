"""The "how you're connected" panel."""
import networkx as nx


def connection(G, a, b, max_steps=6):
    """A shortest chain of members linking a to b, as a list of ids starting with a and ending with b,
    or None if they are not linked within max_steps connections (or at all)."""
    # One breadth-first search instead of listing every simple path (well-connected members make that explode).
    path = nx.shortest_path(G, a, b)
    return path if len(path) - 1 <= max_steps else None
