import networkx as nx

LINKING = ("device", "card", "ip")


def linked_accounts(conn, account_id):
    g = nx.Graph()
    g.add_node(account_id)
    rows = conn.execute(
        "SELECT kind, value, account_id FROM signal WHERE kind IN (?, ?, ?) ORDER BY kind, value", LINKING)
    last, first = None, None
    for kind, value, acc in rows:
        g.add_node(acc)
        if (kind, value) == last:
            g.add_edge(first, acc)
        else:
            last, first = (kind, value), acc
    return sorted(nx.node_connected_component(g, account_id))
