"""Load the collaboration graph (docs/graph.md)."""
import json
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data" / "collaborations.json"


def load(path=DATA) -> nx.Graph:
    with open(path) as f:
        return nx.node_link_graph(json.load(f), edges="edges")
