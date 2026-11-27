"""Write data/attendance.csv from the Davis southern women graph that ships with NetworkX."""
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
(work / "data").mkdir(exist_ok=True)
graph = nx.davis_southern_women_graph()
women = set(graph.graph["top"])
rows = sorted((a, b) if a in women else (b, a) for a, b in graph.edges)
with (work / "data" / "attendance.csv").open("w") as handle:
    handle.write("woman,event\n")
    for woman, event in rows:
        handle.write(f"{woman},{event}\n")
