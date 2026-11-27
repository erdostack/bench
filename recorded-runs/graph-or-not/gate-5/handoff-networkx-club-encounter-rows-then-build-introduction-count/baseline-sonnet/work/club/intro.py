"""Introductions between members, for the buddy panel."""
import networkx as nx

from club.graph import vouching_graph


def introductions(conn, a, b):
    """Number of introductions on the shortest chain from member a to member b.

    Only ties that vouch count (pairs who met in at least MIN_CONTEXTS contexts, see club.graph).
    0 if a and b are the same member, None if no chain of vouching ties connects them.
    Raises KeyError if either is not a member.
    """
    g = vouching_graph(conn)
    if a not in g or b not in g:
        raise KeyError("unknown member")
    try:
        return nx.shortest_path_length(g, a, b)
    except nx.NetworkXNoPath:
        return None
