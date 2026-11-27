"""Derivation graph for the lineage plots."""
import csv
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parents[1] / "data"


def normalize_id(tube_id):
    """LIMS B exports ids in lower case and sometimes with a trailing space; they are the same tube."""
    return tube_id.strip().upper()


def derivation_graph(normalize=False):
    g = nx.DiGraph()
    with open(DATA / "derivations.csv", newline="") as f:
        for row in csv.DictReader(f):
            parent, child = row["parent_id"], row["child_id"]
            if normalize:
                parent, child = normalize_id(parent), normalize_id(child)
            g.add_edge(parent, child, method=row["method"])
    return g


def lineage_plot_data(tube_id):
    g = derivation_graph()
    return {"ancestors": sorted(nx.ancestors(g, tube_id)), "children": sorted(g.successors(tube_id))}


def recall_list(tube_id):
    """Sorted ids (as written in data/tubes.csv) of every tube to pull when `tube_id` is recalled.

    Every descendant through any number of aliquots, extractions and pools. Destroyed tubes are left
    off the list but still walked through, so what was made from them stays on it. Shipped tubes stay
    on it. The recalled tube itself is not included. `tube_id` may be in any case, with stray spaces.
    """
    g = derivation_graph(normalize=True)
    status = {}
    with open(DATA / "tubes.csv", newline="") as f:
        for row in csv.DictReader(f):
            status[normalize_id(row["tube_id"])] = (row["tube_id"], row["status"].strip().lower())
    start = normalize_id(tube_id)
    if start not in g and start not in status:
        raise KeyError(f"unknown tube id: {tube_id!r}")
    found = nx.descendants(g, start) - {start} if start in g else set()
    out = []
    for node in found:
        name, state = status.get(node, (node, ""))
        if state != "destroyed":
            out.append(name)
    return sorted(out)
