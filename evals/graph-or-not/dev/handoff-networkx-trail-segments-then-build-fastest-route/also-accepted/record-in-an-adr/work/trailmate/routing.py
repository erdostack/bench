"""Fastest walking route. Rules (docs/graph/DECISION.md): surveyed minutes, else 15 min per km; the faster of
parallel trails."""
import networkx as nx

MINUTES_PER_KM = 15


def _graph(conn):
    g = nx.Graph()
    for a, b, length_m, minutes in conn.execute("SELECT junction_a, junction_b, length_m, minutes FROM segment"):
        t = minutes if minutes is not None else length_m * MINUTES_PER_KM / 1000
        if not g.has_edge(a, b) or t < g[a][b]["t"]:
            g.add_edge(a, b, t=t)
    g.add_nodes_from(j for (j,) in conn.execute("SELECT id FROM junction"))
    return g


def fastest_route(conn, start, end):
    g = _graph(conn)
    try:
        total, path = nx.single_source_dijkstra(g, start, end, weight="t")
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
    return total, path
