"""Linked accounts lookup (decision: docs/graph/DECISION.md, in-process-library).

Two accounts are linked only by a shared device id or a shared payment card, directly or through
a chain of such shares. A shared IP never links them. The links are built into an in-memory
networkx graph once per nightly copy of var/forum.db and each lookup reads the connected component.
"""
import os

import networkx as nx

LINKING_KINDS = ("device", "card")

_cache = {}  # database file -> (file signature, graph)


def _signature(path):
    st = os.stat(path)
    return (st.st_mtime_ns, st.st_size)


def _build(conn):
    graph = nx.Graph()
    rows = conn.execute("SELECT account_id, kind, value FROM signal WHERE kind IN (?, ?)", LINKING_KINDS)
    for account_id, kind, value in rows:
        graph.add_edge(("account", account_id), (kind, value))
    return graph


def _graph(conn):
    path = next((f for _, name, f in conn.execute("PRAGMA database_list") if name == "main" and f), None)
    if path is None:  # in-memory or temporary database: no file to tell a new copy by, so no cache
        return _build(conn)
    sig = _signature(path)
    cached = _cache.get(path)
    if cached is None or cached[0] != sig:
        cached = _cache[path] = (sig, _build(conn))
    return cached[1]


def linked_accounts(conn, account_id):
    """Sorted ids of every account linked to account_id, directly or through a chain, including itself."""
    graph = _graph(conn)
    start = ("account", account_id)
    if start not in graph:
        return [account_id]
    return sorted(n[1] for n in nx.node_connected_component(graph, start) if n[0] == "account")
