"""Which depot sends the recovery truck."""
import networkx as nx


def load(conn):
    """Road graph for a 26-tonne lorry: no bus-gate segments, cheapest segment per junction pair."""
    g = nx.Graph()
    for a, b, minutes in conn.execute("SELECT a, b, minutes FROM segment WHERE bus_gate = 0"):
        if g.has_edge(a, b) and g[a][b]["minutes"] <= minutes:
            continue
        g.add_edge(a, b, minutes=minutes)
    return g


def nearest_depot(conn, junction_id):
    """Return (depot_id, minutes) for the depot with the least driving time to junction_id, or None.

    Ties go to the lowest depot_id.
    """
    depots = conn.execute("SELECT depot_id, junction_id FROM depot ORDER BY depot_id").fetchall()
    g = load(conn)
    dist = nx.single_source_dijkstra_path_length(g, junction_id, weight="minutes") if junction_id in g else {}
    dist.setdefault(junction_id, 0.0)  # a depot standing on the junction needs no road
    best = None
    for depot_id, at in depots:
        d = dist.get(at)
        if d is not None and (best is None or d < best[1]):
            best = (depot_id, float(d))
    return best
