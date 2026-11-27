import networkx as nx


def shared_events(conn, a, b):
    g = nx.Graph()
    g.add_edges_from(conn.execute(
        "SELECT w.name, e.label FROM attended t JOIN woman w ON w.id = t.woman_id JOIN event e ON e.id = t.event_id"))
    if a not in g or b not in g:
        return []
    return sorted(set(g[a]) & set(g[b]))
