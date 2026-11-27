"""Drive times around closed roads."""
import json
from functools import lru_cache
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parents[1] / "data" / "roads.json"


@lru_cache(maxsize=1)
def network():
    """The county road network, loaded once per process and shared by every request. Directed (one-way
    streets); edge attribute `minutes`."""
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    G = nx.DiGraph()
    for r in raw["roads"]:
        G.add_edge(r["from"], r["to"], minutes=r["minutes"])
        if not r["one_way"]:
            G.add_edge(r["to"], r["from"], minutes=r["minutes"])
    return G


def detour_minutes(G, a, b, closed):
    """Fastest drive from a to b in minutes with the segments in `closed` (a list of (from, to) pairs)
    shut, or None if b cannot be reached."""
    G.remove_edges_from(closed)
    try:
        return nx.shortest_path_length(G, a, b, weight="minutes")
    except nx.NetworkXNoPath:
        return None
