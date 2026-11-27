import networkx as nx

DEPOT = 1


def cutoff_segments(conn):
    houses = dict(conn.execute("SELECT id, houses FROM junction"))
    g = nx.Graph()
    g.add_nodes_from(houses)
    for sid, a, b in conn.execute("SELECT id, a, b FROM segment"):
        g.add_edge(a, b, id=sid)
    out = []
    for a, b in nx.bridges(g):
        h = g.copy()
        h.remove_edge(a, b)
        cut_off = set(h) - nx.node_connected_component(h, DEPOT)
        if any(houses[j] > 0 for j in cut_off):
            out.append(g[a][b]["id"])
    return sorted(out)
