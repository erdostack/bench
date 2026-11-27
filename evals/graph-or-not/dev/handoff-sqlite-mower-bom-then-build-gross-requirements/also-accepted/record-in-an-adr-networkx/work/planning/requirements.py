"""Gross requirements with networkx. Scrap: 4% per BOM line, compounding (docs/adr/0006)."""
import networkx as nx

SCRAP = 1.04


def _graph(conn):
    g = nx.DiGraph()
    for item_id, make_buy in conn.execute("SELECT id, make_buy FROM item"):
        g.add_node(item_id, make_buy=make_buy)
    for parent, comp, per in conn.execute("SELECT parent_id, component_id, qty_per FROM bom_line"):
        g.add_edge(parent, comp, qty=per)
    return g


def gross_requirements(conn, item_id, qty):
    g = _graph(conn)
    out = {}
    stack = [(item_id, float(qty))]
    while stack:
        node, amount = stack.pop()
        for comp in g.successors(node):
            need = amount * g.edges[node, comp]["qty"] * SCRAP
            if g.nodes[comp]["make_buy"] == "B":
                out[comp] = out.get(comp, 0.0) + need
            else:
                stack.append((comp, need))
    return {k: round(v, 3) for k, v in out.items()}
