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

from collections import defaultdict, deque



def recall_list(tube_id):
    norm = lambda s: s.strip().upper()   # same tube whatever the case (decision record)
    status = {norm(r["tube_id"]): r["status"] for r in csv.DictReader(open("data/tubes.csv", newline=""))}
    children = defaultdict(set)
    for r in csv.DictReader(open("data/derivations.csv", newline="")):
        children[norm(r["parent_id"])].add(norm(r["child_id"]))
    seen, queue = set(), deque([norm(tube_id)])
    while queue:
        for c in children[queue.popleft()]:
            if c not in seen:
                seen.add(c)
                queue.append(c)
    return sorted(t for t in seen if t in status and status[t] != "destroyed")
