import networkx as nx


def fastest_route(conn, start, end):
    g = nx.MultiGraph()
    g.add_nodes_from(j for (j,) in conn.execute("SELECT id FROM junction"))
    for a, b, minutes in conn.execute("SELECT junction_a, junction_b, minutes FROM segment"):
        if minutes is None:
            g.add_edge(a, b)
        else:
            g.add_edge(a, b, minutes=minutes)
    try:
        path = nx.dijkstra_path(g, start, end, weight="minutes")
    except nx.NetworkXNoPath:
        return None
    total = sum(min(d.get("minutes", 1) for d in g[u][v].values()) for u, v in zip(path, path[1:]))
    return total, path
