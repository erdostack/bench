"""One-off: write data/attendance.csv from NetworkX's copy of the Davis Southern Women graph."""
import csv
from pathlib import Path

import networkx as nx

g = nx.davis_southern_women_graph()
women = sorted(n for n, d in g.nodes(data=True) if d["bipartite"] == 0)
out = Path(__file__).resolve().parents[1] / "data" / "attendance.csv"
out.parent.mkdir(exist_ok=True)
with out.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["woman", "event"])
    for w in women:
        for e in sorted(g[w]):
            writer.writerow([w, e])
