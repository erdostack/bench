import networkx as nx
from networkx.algorithms import bipartite

from society.data import load_attendance


def co_attendees(name, min_shared):
    rows = load_attendance()
    g = nx.Graph()
    women = {w for w, _ in rows}
    g.add_nodes_from(women, bipartite=0)
    g.add_edges_from(rows)
    proj = bipartite.weighted_projected_graph(g, women)
    return sorted(other for other, d in proj[name].items() if d["weight"] >= min_shared)
