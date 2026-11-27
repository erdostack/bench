"""Shutdown check. Rule (docs/graph/DECISION.md): cut off = can no longer reach any dock, one-way segments,
bypass segments not counted."""
import networkx as nx


def _layout(conn):
    g = nx.DiGraph()
    g.add_nodes_from(r[0] for r in conn.execute("SELECT id FROM station"))
    g.add_edges_from(conn.execute("SELECT from_station, to_station FROM segment WHERE kind <> 'bypass'"))
    docks = {r[0] for r in conn.execute("SELECT id FROM station WHERE kind = 'dock'")}
    return g, docks


def cut_off(conn, down_station):
    g, docks = _layout(conn)
    g.remove_node(down_station)
    reach_a_dock = set()
    for d in docks - {down_station}:
        reach_a_dock |= nx.ancestors(g, d) | {d}
    return sorted(n for n in g.nodes if n not in reach_a_dock)
