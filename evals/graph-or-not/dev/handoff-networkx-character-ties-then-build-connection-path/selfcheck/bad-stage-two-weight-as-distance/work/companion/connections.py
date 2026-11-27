import networkx as nx


def connection(conn, a, b):
    g = nx.Graph()
    g.add_weighted_edges_from(conn.execute("SELECT char_a, char_b, weight FROM tie"))
    return nx.dijkstra_path(g, a, b, weight="weight")
