"""Which junctions does a draft one-way scheme trap?

A road junction is trapped if you cannot drive from it to the ring road, or cannot drive
to it from the ring road. Footpath segments are ignored, and so are junctions that no
road segment touches. There is no limit on the number of steps.
"""
import networkx as nx


def _road_graph(conn):
    g = nx.DiGraph()
    for a, b, oneway in conn.execute("SELECT a, b, oneway FROM segment WHERE mode = 'road'"):
        g.add_node(a)
        g.add_node(b)
        if oneway in (0, 1):
            g.add_edge(a, b)
        if oneway in (0, -1):
            g.add_edge(b, a)
    return g


def trapped_junctions(conn):
    """Sorted ids of the non-ring road junctions that cannot reach the ring or be reached from it."""
    ring = {j for (j,) in conn.execute("SELECT junction_id FROM junction WHERE on_ring = 1")}
    g = _road_graph(conn)
    # One multi-source pass per direction through a virtual node joined to every ring junction.
    hub = object()
    out_g, in_g = g.copy(), g.reverse(copy=True)
    for r in ring:
        out_g.add_edge(hub, r)
        in_g.add_edge(hub, r)
    reached_from_ring = nx.descendants(out_g, hub)
    can_reach_ring = nx.descendants(in_g, hub)
    ok = reached_from_ring & can_reach_ring
    junctions = {j for (j,) in conn.execute("SELECT junction_id FROM junction WHERE on_ring = 0")}
    return sorted(j for j in g if j in junctions and j not in ok)
