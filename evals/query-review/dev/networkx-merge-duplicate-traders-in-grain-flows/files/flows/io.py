"""Load the season's flow graph."""
import json
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data"


def load_flows(path=None):
    data = json.loads(Path(path or DATA / "flows.json").read_text())
    return nx.node_link_graph(data, directed=True, multigraph=False, edges="links")


def load_pairs(path=None):
    import csv
    with open(path or DATA / "duplicate_pairs.csv", newline="") as f:
        return [(r["trader_a"], r["trader_b"]) for r in csv.DictReader(f)]
