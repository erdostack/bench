"""Plots for the lab wiki."""
import networkx as nx


def citation_graph(conn):
    g = nx.DiGraph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM paper"))
    g.add_edges_from(conn.execute("SELECT citing_id, cited_id FROM cites"))
    return g


def degree_histogram(conn):
    return nx.degree_histogram(citation_graph(conn).to_undirected())
