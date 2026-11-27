"""Path search between two papers (loads the whole citation graph at worker start)."""
import sqlite3

import networkx as nx

from citepath.config import SNAPSHOT

_G = None


def graph():
    global _G
    if _G is None:
        conn = sqlite3.connect(SNAPSHOT)
        _G = nx.Graph()
        _G.add_edges_from(conn.execute("SELECT citing_id, cited_id FROM citation"))
        conn.close()
    return _G


def chains(a, b, limit=5):
    return list(nx.all_shortest_paths(graph(), a, b))[:limit]
