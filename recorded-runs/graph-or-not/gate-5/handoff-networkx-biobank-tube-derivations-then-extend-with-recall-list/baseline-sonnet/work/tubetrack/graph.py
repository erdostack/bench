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


def normalize(tube_id):
    """LIMS B exports lower case and trailing spaces; the lab confirmed these are the same tubes."""
    return str(tube_id).strip().upper()


def recall_list(tube_id):
    """Sorted ids (as written in data/tubes.csv) of every tube to pull when tube_id is recalled: all its
    descendants through any number of aliquots, extractions and pools. Destroyed tubes are left off the list,
    but their descendants stay on it. The recalled tube itself is not included.

    tube_id may be in any form the lab has it (case and surrounding spaces are ignored). An id that is not in
    tubes.csv raises ValueError rather than returning an empty list, so a typo is not read as "nothing to pull".
    """
    with open(DATA / "tubes.csv", newline="") as f:
        status = {normalize(r["tube_id"]): r["status"].strip().lower() for r in csv.DictReader(f)}
    source = normalize(tube_id)
    if source not in status:
        raise ValueError(f"unknown tube id: {tube_id!r}")
    g = nx.DiGraph()
    with open(DATA / "derivations.csv", newline="") as f:
        for row in csv.DictReader(f):
            g.add_edge(normalize(row["parent_id"]), normalize(row["child_id"]))
    if source not in g:
        return []
    # Walk every descendant first, then filter: filtering during the walk would drop what was
    # made from a destroyed tube.
    return sorted(t for t in nx.descendants(g, source) if status.get(t) != "destroyed")
