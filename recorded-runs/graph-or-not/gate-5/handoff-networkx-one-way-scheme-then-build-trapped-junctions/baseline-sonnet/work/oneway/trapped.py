"""Which junctions does a draft one-way scheme trap?

Traffic team's rule: a junction is trapped if you cannot drive from it to the ring road, or cannot
drive to it from the ring road, under the draft's directions. Only road segments count; footpaths
are not roads, and a junction that is only on footpaths is not reported. No step limit.
"""
import networkx as nx

_RING = "ring"  # virtual node standing for the whole ring road (string: junction ids are ints)


def _road_graph(conn):
    g = nx.DiGraph()
    for a, b, oneway in conn.execute("SELECT a, b, oneway FROM segment WHERE mode = 'road'"):
        g.add_nodes_from((a, b))
        if oneway in (0, 1):
            g.add_edge(a, b)
        if oneway in (0, -1):
            g.add_edge(b, a)
    for (j,) in conn.execute("SELECT junction_id FROM junction WHERE on_ring = 1"):
        if j in g:
            g.add_edge(_RING, j)   # leaving the ring onto j
            g.add_edge(j, _RING)   # reaching the ring from j
    return g


def trapped_junctions(conn):
    """Road junctions (not on the ring) that cannot reach the ring road or cannot be reached from it."""
    g = _road_graph(conn)
    if _RING not in g:                      # no ring road in the draft: nothing can reach it
        g.add_node(_RING)
    can_reach_ring = nx.ancestors(g, _RING)       # drive from j to the ring
    reachable_from_ring = nx.descendants(g, _RING)  # drive from the ring to j
    ring = {j for (j,) in conn.execute("SELECT junction_id FROM junction WHERE on_ring = 1")}
    return sorted(j for j in g
                  if j != _RING and j not in ring
                  and not (j in can_reach_ring and j in reachable_from_ring))
