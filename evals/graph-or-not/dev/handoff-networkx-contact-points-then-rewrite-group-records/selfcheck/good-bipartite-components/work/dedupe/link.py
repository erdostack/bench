import networkx as nx


def group_records(conn):
    """Same person = connected through shared emails or phones (not addresses)."""
    g = nx.Graph()
    records = [("r", rid) for (rid,) in conn.execute("SELECT id FROM record")]
    g.add_nodes_from(records)
    for rid, kind, value in conn.execute("SELECT record_id, kind, value FROM contact_point"):
        if kind in ("email", "phone"):
            g.add_edge(("r", rid), ("v", kind, value))
    groups = []
    for comp in nx.connected_components(g):
        ids = sorted(n[1] for n in comp if n[0] == "r")
        if ids:
            groups.append(ids)
    return sorted(groups)
