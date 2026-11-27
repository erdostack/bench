import networkx as nx

_GRAPH = None


def _graph(conn):
    global _GRAPH
    if _GRAPH is None:
        g = nx.Graph()
        for a, b, w in conn.execute("SELECT char_a, char_b, weight FROM tie"):
            g.add_edge(a, b, length=1 / w)
        _GRAPH = g
    return _GRAPH


def connection(conn, a, b):
    """Characters from a to b along the chain with the smallest total 1/weight."""
    return nx.shortest_path(_graph(conn), a, b, weight="length")
