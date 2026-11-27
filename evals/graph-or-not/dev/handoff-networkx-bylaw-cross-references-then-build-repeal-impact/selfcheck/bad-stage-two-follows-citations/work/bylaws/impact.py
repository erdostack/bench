"""Which bylaws a repeal would touch. Rule in docs/graph/DECISION.md."""
import networkx as nx

CARRIES_REPEAL = ("amends", "depends_on")     # a citation does not carry a repeal


def affected_by_repeal(conn, bylaw_id):
    g = nx.DiGraph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM bylaw"))
    rows = conn.execute("SELECT from_bylaw, to_bylaw FROM reference")
    g.add_edges_from(rows)
    if bylaw_id not in g:
        return []
    return sorted(nx.ancestors(g, bylaw_id))
