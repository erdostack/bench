import networkx as nx


def trapped_junctions(conn):
    g = nx.DiGraph()
    for a, b, oneway in conn.execute("SELECT a, b, oneway FROM segment WHERE mode = 'road'"):
        g.add_nodes_from((a, b))
        if oneway in (0, 1):
            g.add_edge(a, b)
        if oneway in (0, -1):
            g.add_edge(b, a)
    ring = {j for (j,) in conn.execute("SELECT junction_id FROM junction WHERE on_ring = 1")}
    ok = set(ring)
    for r in ring & set(g):
        ok |= nx.ancestors(g, r)
    return sorted(j for j in g if j not in ok)
