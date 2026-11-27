"""The "how are these two connected" panel: the chain along the strongest ties.

A tie's length is 1 / weight (weight = chapters shared), as agreed with the editors; see docs/graph/DECISION.md.
"""
import networkx as nx


def connection(conn, a, b):
    g = nx.Graph()
    g.add_weighted_edges_from(conn.execute("SELECT char_a, char_b, weight FROM tie"))
    try:
        return nx.dijkstra_path(g, a, b, weight=lambda u, v, d: 1.0 / d["weight"])
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
