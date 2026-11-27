import networkx as nx


def fastest_route(conn, start, end):
    g = nx.MultiGraph()
    g.add_nodes_from(j for (j,) in conn.execute("SELECT id FROM junction"))
    for sid, a, b, length_m, minutes in conn.execute(
            "SELECT id, junction_a, junction_b, length_m, COALESCE(minutes, length_m * 15.0 / 1000) FROM segment"):
        g.add_edge(a, b, key=sid, minutes=minutes)
    if start not in g or end not in g or not nx.has_path(g, start, end):
        return None
    path = nx.dijkstra_path(g, start, end, weight="minutes")   # on a MultiGraph the cheapest parallel edge counts
    total = sum(min(d["minutes"] for d in g[u][v].values()) for u, v in zip(path, path[1:]))
    return total, path
