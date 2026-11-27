"""Which depot sends the recovery truck."""
import networkx as nx


def load(conn):
    """Road graph a truck can drive: bus-gate segments are closed to it, and where two
    segments join the same junctions the faster one is kept."""
    g = nx.Graph()
    for a, b, minutes in conn.execute("SELECT a, b, minutes FROM segment WHERE bus_gate = 0"):
        if g.has_edge(a, b):
            minutes = min(minutes, g[a][b]["minutes"])
        g.add_edge(a, b, minutes=minutes)
    return g


def nearest_depot(conn, junction_id):
    """(depot_id, minutes) for the depot with the least driving time to junction_id, or None.

    Ties go to the lower depot_id.
    """
    g = load(conn)
    best = None
    for depot_id, at in conn.execute("SELECT depot_id, junction_id FROM depot ORDER BY depot_id"):
        if at == junction_id:
            d = 0.0
        else:
            try:
                d = nx.shortest_path_length(g, at, junction_id, weight="minutes")
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
        if best is None or d < best[1]:
            best = (depot_id, d)
    return best
