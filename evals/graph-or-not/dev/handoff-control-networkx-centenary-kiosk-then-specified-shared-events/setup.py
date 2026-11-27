"""Writes the study's data (bundled with networkx) as the kiosk's CSVs in the work dir."""
import csv
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
g = nx.davis_southern_women_graph()
(work / "data").mkdir(parents=True, exist_ok=True)
with open(work / "data" / "attendance.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["woman", "event"])
    for woman in g.graph["top"]:
        for event in sorted(g[woman], key=lambda e: int(e[1:])):
            w.writerow([woman, event])
