"""Critical stops: closing one leaves part of the network unreachable from the rest (ops' definition)."""
import networkx as nx


def critical_stops(conn):
    g = nx.Graph()
    g.add_nodes_from(code for (code,) in conn.execute("SELECT code FROM stop"))
    g.add_edges_from(conn.execute("SELECT stop_a, stop_b FROM link"))
    return sorted(nx.articulation_points(g))
