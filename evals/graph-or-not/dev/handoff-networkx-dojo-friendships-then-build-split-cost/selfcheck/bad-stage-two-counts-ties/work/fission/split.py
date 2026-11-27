import networkx as nx


def split_cost(conn, a, b):
    g = nx.Graph()
    g.add_edges_from(conn.execute("SELECT a, b FROM tie"))
    return len(nx.minimum_edge_cut(g, a, b))
