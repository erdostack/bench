"""Which clauses an amendment can affect (docs/model.md)."""
import json
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parents[1] / "data" / "references.json"


def load_references(path=DATA):
    G = nx.DiGraph()
    for ref in json.loads(Path(path).read_text())["references"]:
        G.add_edge(ref["from"], ref["to"])
    return G


def affected_by(G, clause):
    """Clauses whose meaning can change when `clause` is amended, sorted."""
    return sorted(nx.descendants(G, clause))
