"""Circular-reference check. Rules in docs/graph/DECISION.md."""
import networkx as nx


def circular_cells(conn):
    key = {i: f"{s}!{r}" for i, s, r in conn.execute("SELECT id, sheet, ref FROM cell")}
    g = nx.DiGraph()
    g.add_edges_from((key[a], key[b]) for a, b in conn.execute("SELECT cell_id, depends_on FROM reference"))
    flagged = set()
    for comp in nx.strongly_connected_components(g):
        if len(comp) < 2:
            continue
        if all(n.split("!")[0] == "Loan" for n in comp):
            continue                                   # intentional iterative loop on Loan
        flagged |= comp
    return sorted(flagged)
