"""Introductions between members, for the newcomer buddy panel."""
import networkx as nx

from club.graph import member_graph


def introductions(conn, a, b):
    """Number of introductions on the shortest chain from member a to member b.

    A chain a - x - b needs one introduction (x introduces a to b), so the count is the number
    of members strictly between a and b on the shortest chain: its encounter count minus one.
    Members who have met directly need none. Returns 0 when a and b are the same member,
    and None when no chain links them (or either is not a member).
    """
    g = member_graph(conn)
    if a not in g or b not in g:
        return None
    if a == b:
        return 0
    try:
        return nx.shortest_path_length(g, a, b) - 1
    except nx.NetworkXNoPath:
        return None
