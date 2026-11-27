import networkx as nx

from club.graph import member_graph


def introductions(conn, a, b):
    g = member_graph(conn)
    try:
        return nx.shortest_path_length(g, a, b)
    except nx.NetworkXNoPath:
        return None
