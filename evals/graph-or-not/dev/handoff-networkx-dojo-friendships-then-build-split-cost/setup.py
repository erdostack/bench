"""Writes the course's copy of Zachary's karate club data (bundled with networkx) into the work dir."""
import csv
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
g = nx.karate_club_graph()
(work / "data").mkdir(parents=True, exist_ok=True)
with open(work / "data" / "members.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "faction"])
    for n in sorted(g):
        w.writerow([n, g.nodes[n]["club"]])
with open(work / "data" / "ties.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["a", "b", "contexts"])
    for a, b, d in sorted(g.edges(data=True)):
        w.writerow([a, b, d["weight"]])
