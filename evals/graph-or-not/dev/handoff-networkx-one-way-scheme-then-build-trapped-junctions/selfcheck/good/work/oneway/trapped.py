"""Which junctions does a draft one-way scheme trap?

Trapped (traffic team's rule): you cannot drive from the junction to the ring road, or cannot drive to it from
the ring road, under the draft's directions. Footpaths are not roads; footpath-only junctions are not reported.
"""
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
    reach_from_ring, reach_ring = set(ring), set(ring)
    for r in ring & set(g):
        reach_from_ring |= nx.descendants(g, r)
        reach_ring |= nx.ancestors(g, r)
    return sorted(j for j in g if j not in ring and not (j in reach_from_ring and j in reach_ring))
