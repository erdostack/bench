import networkx as nx


def upstream_manholes(conn, node_id):
    pumping = {r[0] for r in conn.execute("SELECT node_id FROM node WHERE kind = 'pumping_station'")}
    g = nx.DiGraph()
    g.add_nodes_from(r[0] for r in conn.execute("SELECT node_id FROM node"))
    g.add_edges_from(conn.execute("SELECT us_node, ds_node FROM pipe"))
    g.remove_nodes_from(pumping - {node_id})
    if node_id not in g:
        return []
    return sorted(nx.ancestors(g, node_id))
