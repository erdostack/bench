"""Liaison chains: how two member organisations are linked through shared working groups."""
import networkx as nx

from consortium.graph import load_graph


def liaison_chain(conn, a, b):
    """Shortest chain from organisation a to organisation b through shared working groups.

    Returns the list [a, group, org, group, ..., b], with organisation ids and working-group codes
    alternating. Returns [a] when a and b are the same organisation, and None when there is no chain
    or either id is not an organisation.
    """
    g = load_graph(conn)
    if g.nodes.get(a, {}).get("kind") != "org" or g.nodes.get(b, {}).get("kind") != "org":
        return None
    try:
        return nx.shortest_path(g, a, b)
    except nx.NetworkXNoPath:
        return None
