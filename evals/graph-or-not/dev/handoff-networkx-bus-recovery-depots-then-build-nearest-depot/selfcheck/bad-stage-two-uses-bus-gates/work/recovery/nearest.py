"""Which depot sends the recovery truck: least driving minutes."""
import networkx as nx


def load(conn):
    g = nx.MultiGraph()
    g.add_nodes_from(j for (j,) in conn.execute("SELECT junction_id FROM junction"))
    for sid, a, b, minutes in conn.execute("SELECT segment_id, a, b, minutes FROM segment"):
        g.add_edge(a, b, key=sid, minutes=minutes)
    return g


def nearest_depot(conn, junction_id):
    g = load(conn)
    if junction_id not in g:
        return None
    dist = nx.single_source_dijkstra_path_length(g, junction_id, weight="minutes")
    best = None
    for depot_id, at in conn.execute("SELECT depot_id, junction_id FROM depot"):
        if at in dist and (best is None or dist[at] < best[1]):
            best = (depot_id, round(dist[at], 2))
    return best
