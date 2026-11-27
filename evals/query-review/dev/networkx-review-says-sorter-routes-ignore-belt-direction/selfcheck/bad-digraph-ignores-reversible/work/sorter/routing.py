"""Tote routing over the conveyor network (docs/plant.md)."""
import json
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parents[1] / "data" / "conveyors.json"


def load_conveyors(path=DATA):
    G = nx.DiGraph()
    for seg in json.loads(Path(path).read_text())["segments"]:
        G.add_edge(seg["from"], seg["to"], metres=seg["metres"])
    return G


def route(G, src, dst):
    try:
        return nx.shortest_path(G, src, dst, weight="metres")
    except nx.NetworkXNoPath:
        return None
