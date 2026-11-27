import networkx as nx


def connection(conn, a, b):
    g = nx.Graph()
    g.add_edges_from(conn.execute("SELECT char_a, char_b FROM tie"))
    return nx.shortest_path(g, a, b)
