import networkx as nx


def cutoff_segments(conn):
    g = nx.MultiGraph()
    for sid, a, b in conn.execute("SELECT id, a, b FROM segment"):
        g.add_edge(a, b, key=sid)
    return sorted(next(iter(g[a][b])) for a, b in nx.bridges(g))
