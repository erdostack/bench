#!/usr/bin/env python3
"""Throw data/practice-net.graphml away and build a fresh practice network from a fixed seed."""
import random
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "practice-net.graphml"
TOWNS = ["Ashby", "Brindle", "Carrow", "Denholm", "Eastwick", "Farleigh", "Gorran", "Hythe Vale", "Ivybridge Cross",
         "Jessop", "Kelling", "Lowmoor", "Marden", "Netherby", "Oakhurst", "Pellow", "Quorne", "Redlake", "Stanmere",
         "Testwood", "Ullock", "Varley", "Wexcombe", "Yarrow"]


def build(path=OUT):
    rng = random.Random(77)
    G = nx.Graph()
    G.add_node("LAB-1", kind="lab", name="Processing Lab")
    for i in range(1, 4):
        G.add_node(f"DEP-{i}", kind="depot", name=f"Depot {i}")
    for i in range(1, 7):
        G.add_node(f"DC-{i}", kind="centre", name=f"{TOWNS[i]} Donor Centre")
    for t in TOWNS:
        code = "H-" + t.replace(" ", "").upper()[:3]
        G.add_node(code, kind="hospital", name=f"{t} General")
    nodes = list(G.nodes)
    for n in nodes:
        for m in rng.sample(nodes, 3):
            if m != n:
                G.add_edge(n, m, minutes=rng.randint(8, 95), road=rng.choice(["A", "B", "M"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(G, path)


if __name__ == "__main__":
    build()
    print(f"practice network rebuilt at {OUT}")
