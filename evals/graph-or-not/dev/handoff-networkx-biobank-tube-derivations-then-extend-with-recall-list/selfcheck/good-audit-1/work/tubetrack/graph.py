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


# Recall list (rules in docs/graph/DECISION.md): every descendant of the recalled tube; destroyed tubes are left
# off but walked through; ids are compared without case or surrounding spaces (LIMS B exports lower case).


def _key(tube_id):
    return tube_id.strip().upper()


def recall_list(tube_id):
    with open(DATA / "tubes.csv", newline="") as f:
        status = {_key(r["tube_id"]): r["status"] for r in csv.DictReader(f)}
    g = nx.DiGraph()
    g.add_nodes_from(status)
    with open(DATA / "derivations.csv", newline="") as f:
        g.add_edges_from((_key(r["parent_id"]), _key(r["child_id"])) for r in csv.DictReader(f))
    start = _key(tube_id)
    if start not in g:
        return []
    return sorted(t for t in nx.descendants(g, start) if status.get(t) != "destroyed")
