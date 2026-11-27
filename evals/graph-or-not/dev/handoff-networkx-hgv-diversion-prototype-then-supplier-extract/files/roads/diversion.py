"""Prototype: quickest diversion round a closed segment for a vehicle of a given weight."""
import sqlite3

import networkx as nx

DB = "var/roads.db"


def load(conn):
    g = nx.MultiDiGraph()
    for sid, a, b, minutes, limit, oneway in conn.execute(
            "SELECT segment_id, from_j, to_j, minutes, max_weight_t, oneway FROM segment"):
        g.add_edge(a, b, key=sid, minutes=minutes, limit=limit)
        if not oneway:
            g.add_edge(b, a, key=sid, minutes=minutes, limit=limit)
    return g


def diversion(g, closed_segment, weight_t):
    ends = [(a, b) for a, b, k in g.edges(keys=True) if k == closed_segment]
    if not ends:
        return None
    a, b = ends[0]

    def cost(u, v, edges):
        ok = [d["minutes"] for k, d in edges.items()
              if k != closed_segment and (d["limit"] is None or d["limit"] >= weight_t)]
        return min(ok) if ok else None

    try:
        return nx.dijkstra_path(g, a, b, weight=cost)
    except nx.NetworkXNoPath:
        return None


if __name__ == "__main__":
    import sys
    conn = sqlite3.connect(DB)
    print(diversion(load(conn), int(sys.argv[1]), float(sys.argv[2])))
