"""Club stats page: who trains with the most people."""
import networkx as nx


def most_connected(ties, n=5):
    g = nx.Graph(ties)
    return sorted(g.degree, key=lambda kv: (-kv[1], kv[0]))[:n]
