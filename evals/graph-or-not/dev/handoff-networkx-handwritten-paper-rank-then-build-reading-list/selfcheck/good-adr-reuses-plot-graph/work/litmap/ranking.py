import networkx as nx

from litmap.plots import citation_graph


def reading_list(conn, k):
    scores = nx.pagerank(citation_graph(conn), alpha=0.7)   # damping 0.7: ADR 0003
    return [p for p, _ in sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:k]]
