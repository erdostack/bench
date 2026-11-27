"""Which depot sends the recovery truck."""
import networkx as nx


def load(conn):
    """Road graph for a 26-tonne lorry, weighted by minutes.

    Bus-gate segments are left out. Where two segments join the same pair of
    junctions, the one with the fewer minutes is kept.
    """
    g = nx.Graph()
    for a, b, minutes, bus_gate in conn.execute("SELECT a, b, minutes, bus_gate FROM segment"):
        if bus_gate:
            continue
        if g.has_edge(a, b) and g[a][b]["minutes"] <= minutes:
            continue
        g.add_edge(a, b, minutes=minutes)
    return g


def nearest_depot(conn, junction_id):
    """(depot_id, minutes) for the depot with the least driving time to junction_id, or None.

    Ties go to the lower depot_id. A depot at the breakdown junction itself takes 0 minutes.
    """
    g = load(conn)
    best = None
    for depot_id, at in conn.execute("SELECT depot_id, junction_id FROM depot ORDER BY depot_id"):
        if at == junction_id:
            d = 0.0
        else:
            try:
                d = nx.shortest_path_length(g, junction_id, at, weight="minutes")
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
        if best is None or d < best[1]:
            best = (depot_id, d)
    return best
