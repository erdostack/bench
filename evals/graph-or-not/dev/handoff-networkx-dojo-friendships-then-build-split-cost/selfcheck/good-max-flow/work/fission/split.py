import networkx as nx


def split_cost(conn, a, b):
    d = nx.DiGraph()
    for x, y, contexts in conn.execute("SELECT a, b, contexts FROM tie"):
        d.add_edge(x, y, capacity=contexts)
        d.add_edge(y, x, capacity=contexts)
    return int(nx.maximum_flow_value(d, a, b))
