"""Which depot sends the recovery truck."""
import networkx as nx


def load(conn):
    g = nx.Graph()
    # The truck is a 26-tonne lorry: bus gates are closed to it.
    for a, b, minutes in conn.execute("SELECT a, b, minutes FROM segment WHERE bus_gate = 0"):
        # Parallel segments between the same junctions: keep the quickest, not the last row.
        if g.has_edge(a, b) and g[a][b]["minutes"] <= minutes:
            continue
        g.add_edge(a, b, minutes=minutes)
    return g


def nearest_depot(conn, junction_id):
    """(depot_id, minutes) of the depot with the quickest lorry route to junction_id, or None if no depot
    can reach it. Ties go to the lowest depot_id."""
    g = load(conn)
    if junction_id not in g:
        # A junction with no usable segment can only be served by a depot standing on it.
        reach = {junction_id: 0}
    else:
        # Roads are two-way, so the time from the junction to a depot equals the time from the depot.
        reach = nx.single_source_dijkstra_path_length(g, junction_id, weight="minutes")
    best = None
    for depot_id, at in conn.execute("SELECT depot_id, junction_id FROM depot ORDER BY depot_id"):
        d = reach.get(at)
        if d is not None and (best is None or d < best[1]):
            best = (depot_id, d)
    return best
