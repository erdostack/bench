"""Tote routing over the conveyor network (docs/plant.md)."""
import json
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parents[1] / "data" / "conveyors.json"


def load_conveyors(path=DATA):
    """Directed: a belt carries totes from `from` to `to` only; a reversible belt is added both ways (docs/plant.md)."""
    G = nx.DiGraph()
    for seg in json.loads(Path(path).read_text())["segments"]:
        G.add_edge(seg["from"], seg["to"], metres=seg["metres"])
        if seg.get("reversible"):
            G.add_edge(seg["to"], seg["from"], metres=seg["metres"])
    return G


def route(G, src, dst):
    try:
        return nx.shortest_path(G, src, dst, weight="metres")
    except nx.NetworkXNoPath:
        return None
