"""Plough priority list. Rule in docs/graph/DECISION.md."""
import networkx as nx

DEPOT = 1


def cutoff_segments(conn):
    houses = dict(conn.execute("SELECT id, houses FROM junction"))
    g = nx.MultiGraph()                      # two roads between the same junctions are two segments
    g.add_nodes_from(houses)
    for sid, a, b in conn.execute("SELECT id, a, b FROM segment"):
        g.add_edge(a, b, key=sid)
    out = []
    for a, b in nx.bridges(g):
        sid = next(iter(g[a][b]))
        g.remove_edge(a, b, key=sid)
        cut_off = set(g) - nx.node_connected_component(g, DEPOT)
        g.add_edge(a, b, key=sid)
        if any(houses[j] > 0 for j in cut_off):
            out.append(sid)
    return sorted(out)
