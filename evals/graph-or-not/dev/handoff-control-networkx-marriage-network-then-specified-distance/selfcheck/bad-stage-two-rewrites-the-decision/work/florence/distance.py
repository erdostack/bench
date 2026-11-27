import networkx as nx


def marriage_distance(conn, a, b):
    g = nx.Graph()
    g.add_nodes_from(f for (f,) in conn.execute("SELECT name FROM family"))
    g.add_edges_from(conn.execute("SELECT family_a, family_b FROM marriage"))
    try:
        return nx.shortest_path_length(g, a, b)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
