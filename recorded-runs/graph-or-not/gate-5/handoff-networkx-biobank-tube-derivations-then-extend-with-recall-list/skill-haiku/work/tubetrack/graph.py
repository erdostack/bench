"""Derivation graph for the lineage plots."""
import csv
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parents[1] / "data"


def _canonical_id(tube_id):
    return str(tube_id).strip().upper()


def derivation_graph(normalize=False):
    g = nx.DiGraph()
    with open(DATA / "derivations.csv", newline="") as f:
        for row in csv.DictReader(f):
            parent, child = row["parent_id"], row["child_id"]
            if normalize:
                parent, child = _canonical_id(parent), _canonical_id(child)
            g.add_edge(parent, child, method=row["method"])
    return g


def lineage_plot_data(tube_id):
    g = derivation_graph()
    return {"ancestors": sorted(nx.ancestors(g, tube_id)), "children": sorted(g.successors(tube_id))}


def recall_list(tube_id):
    """Tubes the lab must pull when tube_id is recalled.

    Every tube derived from tube_id at any depth. The walk goes through destroyed
    tubes, but destroyed tubes are not returned. The recalled tube is not returned.
    Ids are matched after strip and upper-case, so LIMS B spellings work.
    """
    source = _canonical_id(tube_id)
    with open(DATA / "tubes.csv", newline="") as f:
        status = {_canonical_id(row["tube_id"]): row["status"].strip() for row in csv.DictReader(f)}
    if source not in status:
        raise ValueError(f"unknown tube id: {tube_id!r}")
    g = derivation_graph(normalize=True)
    if source not in g:
        return []
    pull = nx.descendants(g, source) - {source}
    return sorted(t for t in pull if status.get(t) != "destroyed")
