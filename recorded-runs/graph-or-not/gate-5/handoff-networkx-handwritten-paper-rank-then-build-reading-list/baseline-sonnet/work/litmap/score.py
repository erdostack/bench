"""Importance score for the reading list: PageRank over the citation graph.

Edges run citing -> cited, so a paper's score comes from the papers that cite it. Papers with no references
(dangling nodes) are handled by networkx, which spreads their score evenly, so scores add up to 1.
"""
import networkx as nx

from litmap.plots import citation_graph

# The PI's rule: 0.7 rather than the usual 0.85, so papers cited directly count for more than long chains.
DAMPING = 0.7


def importance(conn, damping=DAMPING):
    return nx.pagerank(citation_graph(conn), alpha=damping)
