"""Which depot sends the recovery truck."""
import networkx as nx


def load(conn):
    g = nx.Graph()
    for a, b, minutes, bus_gate in conn.execute("SELECT a, b, minutes, bus_gate FROM segment"):
        g.add_edge(a, b, minutes=minutes, bus_gate=bus_gate)
    return g


def nearest_depot(conn, junction_id):
    g = load(conn)
    best = None
    for depot_id, at in conn.execute("SELECT depot_id, junction_id FROM depot ORDER BY depot_id"):
        try:
            d = nx.shortest_path_length(g, junction_id, at)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
        if best is None or d < best[1]:
            best = (depot_id, d)
    return best[0] if best else None
