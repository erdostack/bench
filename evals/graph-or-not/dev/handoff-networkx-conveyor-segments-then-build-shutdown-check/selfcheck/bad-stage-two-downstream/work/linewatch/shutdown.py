import networkx as nx


def cut_off(conn, down_station):
    g = nx.DiGraph()
    g.add_edges_from(conn.execute("SELECT from_station, to_station FROM segment WHERE kind <> 'bypass'"))
    docks = {r[0] for r in conn.execute("SELECT id FROM station WHERE kind = 'dock'")}
    return sorted(nx.descendants(g, down_station) - docks)
