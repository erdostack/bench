"""Shutdown planning for maintenance."""

import networkx as nx


def _flow_graph(conn):
    """Directed graph of conveyor flow. Bypass segments are hand-operated and do not count."""
    g = nx.DiGraph()
    g.add_nodes_from(r[0] for r in conn.execute("SELECT id FROM station"))
    g.add_edges_from(conn.execute(
        "SELECT from_station, to_station FROM segment WHERE kind != 'bypass'"))
    docks = {r[0] for r in conn.execute("SELECT id FROM station WHERE kind = 'dock'")}
    return g, docks


def _cut_off(g, docks):
    """Stations (docks excluded) with no directed path to any dock."""
    can_reach_dock = set(docks)
    for d in docks:
        can_reach_dock |= nx.ancestors(g, d)
    return set(g.nodes) - can_reach_dock


def cut_off_by_shutdown(conn, station_id):
    """Other stations that can reach a dock today but could not once station_id is out.

    Stations already cut off before the shutdown are not reported.
    Returns a sorted list of station ids.
    """
    g, docks = _flow_graph(conn)
    before = _cut_off(g, docks)
    g.remove_node(station_id)
    after = _cut_off(g, docks - {station_id})
    return sorted(after - before)


def cut_off(conn, down_station):
    """Sorted ids of the stations that would be cut off while down_station is out (down_station not counted).

    A station is cut off when it can reach a dock today but has no directed conveyor path to any dock once
    down_station is out. Bypass segments do not count, and stations already cut off today are not reported.
    Raises KeyError if down_station is not a station id.
    """
    if conn.execute("SELECT 1 FROM station WHERE id = ?", (down_station,)).fetchone() is None:
        raise KeyError(down_station)
    return cut_off_by_shutdown(conn, down_station)
