"""Load the lane network."""
import csv
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data"


def load_graph() -> nx.DiGraph:
    G = nx.DiGraph()
    with open(DATA / "hubs.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            G.add_node(r["code"], region=r["region"])
    with open(DATA / "lanes.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            G.add_edge(r["origin"], r["dest"], weekly_loads=int(r["weekly_loads"]), km=int(r["km"]))
    return G


def load_aliases() -> dict[str, str]:
    with open(DATA / "hub_aliases.csv", newline="") as fh:
        return {r["alias"]: r["canonical"] for r in csv.DictReader(fh)}
