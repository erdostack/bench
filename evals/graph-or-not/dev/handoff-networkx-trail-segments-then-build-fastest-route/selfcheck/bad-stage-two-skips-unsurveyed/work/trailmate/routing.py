import networkx as nx


def fastest_route(conn, start, end):
    g = nx.MultiGraph()
    g.add_nodes_from(j for (j,) in conn.execute("SELECT id FROM junction"))
    for a, b, minutes in conn.execute("SELECT junction_a, junction_b, minutes FROM segment"):
        g.add_edge(a, b, minutes=minutes)
    try:
        total, path = nx.single_source_dijkstra(g, start, end, weight="minutes")
    except nx.NetworkXNoPath:
        return None
    return total, path
