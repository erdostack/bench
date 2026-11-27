"""The "how you're connected" panel."""
import networkx as nx


def connection(G, a, b, max_steps=6):
    """A shortest chain of members linking a to b, as a list of ids starting with a and ending with b,
    or None if they are not linked within max_steps connections (or at all)."""
    best = None
    for path in nx.all_simple_paths(G, a, b, cutoff=max_steps):
        if best is None or len(path) < len(best):
            best = path
    return best
