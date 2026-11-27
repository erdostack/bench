"""Ranking for the "start here" reading list: PageRank with the PI's damping factor."""
import networkx as nx

from litmap.plots import citation_graph

DAMPING = 0.7  # the PI's rule: directly cited papers count for more than long chains


def reading_list(conn, k=20):
    """Ids of the k highest-ranked papers, best first (ties broken by lower id)."""
    scores = nx.pagerank(citation_graph(conn), alpha=DAMPING)
    ranked = sorted(scores, key=lambda p: (-scores[p], p))
    return ranked[:k]
