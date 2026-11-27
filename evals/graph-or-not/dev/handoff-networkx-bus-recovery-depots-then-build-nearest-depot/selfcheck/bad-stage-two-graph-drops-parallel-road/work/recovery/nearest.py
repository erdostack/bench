import networkx as nx


def nearest_depot(conn, junction_id):
    g = nx.Graph()
    for a, b, minutes, gate in conn.execute("SELECT a, b, minutes, bus_gate FROM segment"):
        g.add_edge(a, b, minutes=minutes, bus_gate=gate)
    g.remove_edges_from([(a, b) for a, b, d in g.edges(data=True) if d["bus_gate"]])
    best = None
    for depot_id, at in conn.execute("SELECT depot_id, junction_id FROM depot"):
        try:
            d = nx.dijkstra_path_length(g, junction_id, at, weight="minutes")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
        if best is None or d < best[1]:
            best = (depot_id, round(d, 2))
    return best
