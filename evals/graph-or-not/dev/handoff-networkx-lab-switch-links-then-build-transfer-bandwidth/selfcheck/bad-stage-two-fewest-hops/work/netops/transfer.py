import networkx as nx

from netops.topology import load


def best_rate(conn, src, dst):
    g = load(conn)
    try:
        path = nx.shortest_path(g, src, dst)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
    return min(g[u][v]["gbps"] for u, v in zip(path, path[1:]))
