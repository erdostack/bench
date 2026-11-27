"""Load the club network from data/."""
import csv
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data"


def club_graph() -> nx.Graph:
    graph = nx.read_edgelist(DATA / "ties.edgelist", nodetype=int, data=[("weight", int)])
    with (DATA / "members.csv").open(newline="") as handle:
        for row in csv.DictReader(handle):
            graph.nodes[int(row["member"])]["faction"] = row["faction"]
    return graph
