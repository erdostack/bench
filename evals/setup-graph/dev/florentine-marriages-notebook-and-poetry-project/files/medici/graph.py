import csv
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data" / "marriages.csv"


def marriages() -> nx.Graph:
    graph = nx.Graph()
    with DATA.open(newline="") as handle:
        for row in csv.DictReader(handle):
            graph.add_edge(row["family_a"], row["family_b"])
    return graph
