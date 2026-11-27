import networkx as nx


def critical_stops(conn):
    g = nx.Graph()
    g.add_edges_from(conn.execute("SELECT stop_a, stop_b FROM link"))
    bc = nx.betweenness_centrality(g)
    return sorted(sorted(bc, key=bc.get, reverse=True)[:10])
