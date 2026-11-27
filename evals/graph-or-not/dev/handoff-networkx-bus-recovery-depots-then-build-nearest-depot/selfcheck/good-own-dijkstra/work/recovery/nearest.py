import networkx as nx


def nearest_depot(conn, junction_id):
    g = nx.Graph()
    for a, b, m in conn.execute("SELECT a, b, MIN(minutes) FROM segment WHERE bus_gate = 0 GROUP BY MIN(a, b), MAX(a, b)"):
        g.add_edge(a, b, minutes=m)
    depots = dict(conn.execute("SELECT junction_id, depot_id FROM depot"))
    if junction_id not in g:
        return None
    try:
        minutes, path = nx.multi_source_dijkstra(g, set(depots) & set(g), target=junction_id, weight="minutes")
    except nx.NetworkXNoPath:
        return None
    return depots[path[0]], minutes
