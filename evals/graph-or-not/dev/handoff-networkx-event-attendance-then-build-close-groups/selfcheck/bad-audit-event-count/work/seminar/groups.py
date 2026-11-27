"""Close groups: women connected through pairs with at least 4 shared events (class definition, week 6)."""
import networkx as nx
from networkx.algorithms import bipartite

MIN_SHARED = 4


def close_groups(conn):
    g = nx.Graph()
    women = {p for (p,) in conn.execute("SELECT name FROM person")}
    g.add_nodes_from(women, bipartite=0)
    g.add_edges_from(conn.execute("SELECT person, event FROM attendance"))
    pairs = bipartite.weighted_projected_graph(g, women)
    close = nx.Graph((u, v) for u, v, d in pairs.edges(data=True) if d["weight"] >= MIN_SHARED)
    return sorted(sorted(c) for c in nx.connected_components(close))
