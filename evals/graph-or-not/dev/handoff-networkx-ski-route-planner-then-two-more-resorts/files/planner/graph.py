"""Load the resort network and answer route requests."""
from pathlib import Path

import networkx as nx
import yaml

DATA = Path(__file__).resolve().parents[1] / "data" / "resorts"
GRADES = ["blue", "red", "black"]


def load():
    g = nx.DiGraph()
    for path in sorted(DATA.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text())
        for n in doc["nodes"]:
            g.add_node(n["id"], **n)
        for e in doc["edges"]:
            g.add_edge(e["from"], e["to"], **e)
    return g


def route(g, start, goal, max_grade="red"):
    allowed = set(GRADES[: GRADES.index(max_grade) + 1])
    view = nx.subgraph_view(g, filter_edge=lambda a, b: g[a][b]["kind"] != "piste" or g[a][b]["grade"] in allowed)
    return nx.shortest_path(view, start, goal, weight="minutes")
