import networkx as nx


def circular_cells(conn):
    rows = conn.execute("SELECT c.sheet || '!' || c.ref, d.sheet || '!' || d.ref FROM reference r "
                        "JOIN cell c ON c.id = r.cell_id JOIN cell d ON d.id = r.depends_on")
    g = nx.DiGraph(list(rows))
    flagged = set()
    for loop in nx.simple_cycles(g):
        if all(c.startswith("Loan!") for c in loop):
            continue
        flagged.update(loop)
    return sorted(flagged)
