"""The "most connected characters" box on the front page."""
import networkx as nx


def tie_graph(conn):
    g = nx.Graph()
    g.add_weighted_edges_from(conn.execute("SELECT char_a, char_b, weight FROM tie"))
    return g


def most_connected(conn, n=10):
    g = tie_graph(conn)
    names = dict(conn.execute("SELECT id, name FROM character"))
    top = sorted(g.degree, key=lambda kv: (-kv[1], kv[0]))[:n]
    return [(names.get(c, c), d) for c, d in top]
