"""Linked accounts (rule in docs/graph/DECISION.md): accounts are linked by a shared device id or a shared payment
card, never by an IP; a group is everything connected through such links, at any depth."""
import networkx as nx

LINKING = ("device", "card")


def linked_accounts(conn, account_id):
    g = nx.Graph()
    g.add_node(account_id)
    rows = conn.execute(
        "SELECT kind, value, account_id FROM signal WHERE kind IN (?, ?) ORDER BY kind, value", LINKING)
    last, first = None, None
    for kind, value, acc in rows:
        g.add_node(acc)
        if (kind, value) == last:
            g.add_edge(first, acc)
        else:
            last, first = (kind, value), acc
    return sorted(nx.node_connected_component(g, account_id))
