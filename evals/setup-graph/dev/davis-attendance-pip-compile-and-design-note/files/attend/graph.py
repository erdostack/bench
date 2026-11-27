import csv
from pathlib import Path

import networkx as nx

DATA = Path(__file__).resolve().parent.parent / "data" / "attendance.csv"


def attendance() -> nx.Graph:
    graph = nx.Graph()
    with DATA.open(newline="") as handle:
        for row in csv.DictReader(handle):
            graph.add_node(row["woman"], bipartite=0)
            graph.add_node(row["event"], bipartite=1)
            graph.add_edge(row["woman"], row["event"])
    return graph
