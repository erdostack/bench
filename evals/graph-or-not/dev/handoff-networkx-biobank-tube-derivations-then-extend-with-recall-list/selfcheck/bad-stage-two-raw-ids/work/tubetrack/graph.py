"""Derivation graph for the lineage plots."""
import csv
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parents[1] / "data"


def derivation_graph():
    g = nx.DiGraph()
    with open(DATA / "derivations.csv", newline="") as f:
        for row in csv.DictReader(f):
            g.add_edge(row["parent_id"], row["child_id"], method=row["method"])
    return g


def lineage_plot_data(tube_id):
    g = derivation_graph()
    return {"ancestors": sorted(nx.ancestors(g, tube_id)), "children": sorted(g.successors(tube_id))}



def recall_list(tube_id):
    with open(DATA / "tubes.csv", newline="") as f:
        status = {r["tube_id"]: r["status"] for r in csv.DictReader(f)}
    g = derivation_graph()
    start = tube_id.strip().upper()
    if start not in g:
        return []
    return sorted(t for t in nx.descendants(g, start) if t in status and status[t] != "destroyed")
