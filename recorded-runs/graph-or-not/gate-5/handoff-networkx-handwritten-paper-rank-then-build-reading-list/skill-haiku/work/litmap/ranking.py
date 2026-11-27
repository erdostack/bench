"""Reading-list ranking: PageRank over the citation graph, damping 0.7 (see docs/graph/DECISION.md)."""
import networkx as nx

from litmap.plots import citation_graph

DAMPING = 0.7


def reading_list(conn, k):
    """Return the ids of the k highest-ranked papers, best first."""
    g = citation_graph(conn)
    if len(g) == 0:
        return []
    scores = nx.pagerank(g, alpha=DAMPING)
    ranked = sorted(scores, key=lambda p: (-scores[p], p))
    return ranked[:k]
