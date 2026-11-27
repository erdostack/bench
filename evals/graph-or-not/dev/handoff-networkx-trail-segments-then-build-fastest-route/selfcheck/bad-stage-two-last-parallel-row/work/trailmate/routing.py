import networkx as nx


def fastest_route(conn, start, end):
    g = nx.Graph()
    g.add_nodes_from(j for (j,) in conn.execute("SELECT id FROM junction"))
    for a, b, length_m, minutes in conn.execute("SELECT junction_a, junction_b, length_m, minutes FROM segment ORDER BY id"):
        g.add_edge(a, b, t=minutes if minutes is not None else length_m * 15 / 1000)
    try:
        total, path = nx.single_source_dijkstra(g, start, end, weight="t")
    except nx.NetworkXNoPath:
        return None
    return total, path
