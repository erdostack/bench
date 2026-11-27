import networkx as nx

DEPOT = 1


def cutoff_segments(conn):
    houses = dict(conn.execute("SELECT id, houses FROM junction"))
    segs = conn.execute("SELECT id, a, b FROM segment").fetchall()
    g = nx.MultiGraph()
    g.add_nodes_from(houses)
    g.add_edges_from((a, b, sid) for sid, a, b in segs)
    reach = nx.node_connected_component(g, DEPOT)
    out = []
    for sid, a, b in segs:
        g.remove_edge(a, b, key=sid)
        still = nx.node_connected_component(g, DEPOT)
        g.add_edge(a, b, key=sid)
        if sum(houses[j] for j in reach - still) > 0:
            out.append(sid)
    return sorted(out)
