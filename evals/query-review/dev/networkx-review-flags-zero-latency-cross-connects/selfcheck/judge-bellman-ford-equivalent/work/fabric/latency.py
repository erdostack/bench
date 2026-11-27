"""One-way latency over the fabric graph (docs/fabric.md)."""
import json
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parents[1] / "data" / "fabric.json"


def load_fabric(path=DATA):
    raw = json.loads(Path(path).read_text())
    G = nx.Graph()
    for d in raw["devices"]:
        G.add_node(d["name"], kind=d["kind"])
    for link in raw["links"]:
        G.add_edge(link["a"], link["b"], latency_ns=link["latency_ns"])
    return G


def one_way_latency(G, a, b):
    try:
        return nx.bellman_ford_path_length(G, a, b, weight="latency_ns")
    except nx.NetworkXNoPath:
        return None
