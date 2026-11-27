import networkx as nx


def families_within(conn, family, k):
    g = nx.Graph()
    g.add_nodes_from(f for (f,) in conn.execute("SELECT name FROM family"))
    g.add_edges_from(conn.execute("SELECT family_a, family_b FROM marriage_tie"))
    if family not in g:
        return []
    reach = nx.single_source_shortest_path_length(g, family, cutoff=k)
    return sorted(f for f in reach if f != family)
