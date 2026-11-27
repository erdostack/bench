"""Shutdown check using linewatch.reach."""
import networkx as nx


def cut_off(conn, down_station):
    g = nx.Graph()
    g.add_nodes_from(r[0] for r in conn.execute("SELECT id FROM station"))
    g.add_edges_from(conn.execute("SELECT from_station, to_station FROM segment WHERE kind <> 'bypass'"))
    docks = {r[0] for r in conn.execute("SELECT id FROM station WHERE kind = 'dock'")}
    g.remove_node(down_station)
    ok = set()
    for d in docks:
        ok |= nx.node_connected_component(g, d)
    return sorted(n for n in g.nodes if n not in ok)
