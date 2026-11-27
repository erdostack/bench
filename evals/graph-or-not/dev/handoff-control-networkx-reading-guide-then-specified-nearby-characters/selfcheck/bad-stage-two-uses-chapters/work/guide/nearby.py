import networkx as nx


def characters_within(conn, name, steps):
    g = nx.Graph()
    for x, y, chapters in conn.execute(
            "SELECT x.name, y.name, t.chapters FROM tie t JOIN character x ON x.id = t.a JOIN character y ON y.id = t.b"):
        g.add_edge(x, y, weight=chapters)
    reach = nx.single_source_dijkstra_path_length(g, name, cutoff=steps, weight="weight")
    return sorted(n for n in reach if n != name)
