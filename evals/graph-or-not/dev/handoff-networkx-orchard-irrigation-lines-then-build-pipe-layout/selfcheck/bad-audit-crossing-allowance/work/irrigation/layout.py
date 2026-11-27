"""Which trench runs to dig. Cost rule in docs/graph/DECISION.md."""
import networkx as nx

TRACK_BORE_M = 40     # boring under the track costs as much as 40 m of trench


def pipe_layout(conn):
    g = nx.Graph()
    g.add_nodes_from(v for (v,) in conn.execute("SELECT id FROM valve"))
    for a, b, length, crosses in conn.execute("SELECT a, b, length_m, crosses_track FROM candidate_run"):
        g.add_edge(a, b, cost=length + (TRACK_BORE_M if crosses else 0))
    if not nx.is_connected(g):
        raise ValueError("some valves cannot be reached")
    tree = nx.minimum_spanning_tree(g, weight="cost")
    return sorted(tuple(sorted(e)) for e in tree.edges())
