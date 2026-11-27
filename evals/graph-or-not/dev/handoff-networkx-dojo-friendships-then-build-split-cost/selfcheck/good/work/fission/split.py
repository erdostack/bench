"""Cheapest split between two members. The cost rule is in docs/graph/DECISION.md."""
import networkx as nx


def split_cost(conn, a, b):
    g = nx.Graph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM member"))
    for x, y, contexts in conn.execute("SELECT a, b, contexts FROM tie"):
        g.add_edge(x, y, capacity=contexts)   # breaking a tie costs its contexts
    cost, _ = nx.minimum_cut(g, a, b)
    return cost
