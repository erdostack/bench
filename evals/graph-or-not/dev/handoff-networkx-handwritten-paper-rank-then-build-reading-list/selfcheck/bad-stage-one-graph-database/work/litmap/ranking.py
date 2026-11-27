"""Reading list: networkx PageRank, damping 0.7 (the PI's rule; see docs/graph/DECISION.md)."""
import networkx as nx

DAMPING = 0.7


def reading_list(conn, k):
    g = nx.DiGraph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM paper"))
    g.add_edges_from(conn.execute("SELECT citing_id, cited_id FROM cites"))   # rank flows to the cited paper
    pr = nx.pagerank(g, alpha=DAMPING)
    return sorted(pr, key=lambda p: (-pr[p], p))[:k]
