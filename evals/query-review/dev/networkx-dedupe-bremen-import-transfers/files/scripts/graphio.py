"""Load and save the provenance graph (node-link JSON, MultiDiGraph, edges under "links")."""
import json
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

DATA = Path(__file__).resolve().parent.parent / "data" / "provenance.json"


def load(path=DATA) -> nx.MultiDiGraph:
    with open(path, encoding="utf-8") as f:
        return json_graph.node_link_graph(json.load(f), directed=True, multigraph=True, edges="links")


def save(G: nx.MultiDiGraph, path=DATA) -> None:
    data = json_graph.node_link_data(G, edges="links")
    tmp = Path(path).with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    tmp.replace(path)
