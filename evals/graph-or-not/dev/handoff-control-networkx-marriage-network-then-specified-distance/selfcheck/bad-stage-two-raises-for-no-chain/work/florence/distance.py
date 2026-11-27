import networkx as nx


def marriage_distance(conn, a, b):
    g = nx.Graph(list(conn.execute("SELECT family_a, family_b FROM marriage")))
    return nx.shortest_path_length(g, a, b)
