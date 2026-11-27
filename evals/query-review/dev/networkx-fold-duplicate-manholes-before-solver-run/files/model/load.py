import json
from pathlib import Path

import networkx as nx


def load_graph(path):
    data = json.loads(Path(path).read_text())
    G = nx.DiGraph()
    for n in data["nodes"]:
        G.add_node(n["id"], **{k: v for k, v in n.items() if k != "id"})
    for e in data["pipes"]:
        G.add_edge(e["from"], e["to"], diameter_mm=e["diameter_mm"], length_m=e["length_m"])
    return G
