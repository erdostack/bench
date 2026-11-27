"""Introductions between two members, for the newcomer buddy panel."""
import networkx as nx

MIN_CONTEXTS = 3


def tie_graph(conn):
    """Graph of ties where the two members met in at least MIN_CONTEXTS contexts."""
    g = nx.Graph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM member"))
    g.add_edges_from(
        conn.execute(
            "SELECT MIN(member_a, member_b), MAX(member_a, member_b) FROM encounter "
            "GROUP BY 1, 2 HAVING COUNT(*) >= ?",
            (MIN_CONTEXTS,),
        )
    )
    return g


def introductions(conn, a, b):
    """Number of introductions on the shortest chain from member a to member b.

    0 if a and b are the same member. None if no chain of qualifying ties joins them.
    """
    if a == b:
        return 0
    try:
        return nx.shortest_path_length(tie_graph(conn), a, b)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
