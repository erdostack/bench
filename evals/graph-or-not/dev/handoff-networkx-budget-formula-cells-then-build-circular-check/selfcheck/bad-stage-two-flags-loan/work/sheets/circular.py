import networkx as nx


def circular_cells(conn):
    key = {i: f"{s}!{r}" for i, s, r in conn.execute("SELECT id, sheet, ref FROM cell")}
    g = nx.DiGraph()
    g.add_edges_from((key[a], key[b]) for a, b in conn.execute("SELECT cell_id, depends_on FROM reference"))
    flagged = set()
    for loop in nx.simple_cycles(g):
        flagged.update(loop)
    return sorted(flagged)
