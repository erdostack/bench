"""Writes the guide's copy of the Les Miserables co-appearance network (bundled with networkx) into the work dir."""
import csv
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
g = nx.les_miserables_graph()
(work / "data").mkdir(parents=True, exist_ok=True)
with open(work / "data" / "ties.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["a", "b", "chapters"])
    for a, b, d in sorted(g.edges(data=True)):
        w.writerow([a, b, d["weight"]])
