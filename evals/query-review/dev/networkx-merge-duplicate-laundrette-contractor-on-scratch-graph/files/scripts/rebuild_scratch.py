#!/usr/bin/env python3
"""Rebuild data/scratch-graph.json from fixtures/*.csv."""
import csv
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
G = nx.DiGraph()
with open(ROOT / "fixtures" / "nodes.csv", newline="") as f:
    for row in csv.DictReader(f):
        G.add_node(row["id"], kind=row["kind"], name=row["name"])
with open(ROOT / "fixtures" / "edges.csv", newline="") as f:
    for row in csv.DictReader(f):
        attrs = {k: v for k, v in row.items() if k not in ("src", "dst", "kind") and v}
        G.add_edge(row["src"], row["dst"], kind=row["kind"], **attrs)
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data" / "scratch-graph.json").write_text(json.dumps(nx.node_link_data(G), indent=1))
print(f"scratch graph rebuilt: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
