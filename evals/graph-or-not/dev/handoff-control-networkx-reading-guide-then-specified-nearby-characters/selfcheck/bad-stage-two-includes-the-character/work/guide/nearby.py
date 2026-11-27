import networkx as nx


def characters_within(conn, name, steps):
    g = nx.Graph()
    g.add_nodes_from(n for (n,) in conn.execute("SELECT name FROM character"))
    g.add_edges_from(conn.execute(
        "SELECT x.name, y.name FROM tie t JOIN character x ON x.id = t.a JOIN character y ON y.id = t.b"))
    if name not in g:
        return []
    reach = nx.single_source_shortest_path_length(g, name, cutoff=steps)
    return sorted(reach)
