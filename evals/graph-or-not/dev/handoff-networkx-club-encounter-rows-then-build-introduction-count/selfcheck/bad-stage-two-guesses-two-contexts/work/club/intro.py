import networkx as nx

STRONG = 2


def introductions(conn, a, b):
    g = nx.Graph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM member"))
    g.add_edges_from(conn.execute(
        "SELECT member_a, member_b FROM encounter GROUP BY member_a, member_b HAVING COUNT(*) >= ?", (STRONG,)))
    try:
        return nx.shortest_path_length(g, a, b)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
