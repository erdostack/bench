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


def _tube_key(tube_id):
    # The lab pastes ids in any case and with stray spaces; the export has both too.
    return str(tube_id).strip().upper()


def recall_list(tube_id):
    """Tubes to pull when tube_id is recalled: every tube derived from it, directly or not.

    Returns the ids as written in data/tubes.csv, sorted. The recalled tube is not included.
    Raises ValueError if tube_id is not in data/tubes.csv.
    """
    with open(DATA / "tubes.csv", newline="") as f:
        canon = {_tube_key(row["tube_id"]): row["tube_id"] for row in csv.DictReader(f)}
    key = _tube_key(tube_id)
    if key not in canon:
        raise ValueError(f"unknown tube id: {tube_id!r}")

    g = nx.DiGraph()
    with open(DATA / "derivations.csv", newline="") as f:
        for row in csv.DictReader(f):
            g.add_edge(_tube_key(row["parent_id"]), _tube_key(row["child_id"]))
    if key not in g:
        return []
    return sorted(canon[t] for t in nx.descendants(g, key) if t in canon)
