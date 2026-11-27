"""Write data/marriages.csv from the Florentine families graph that ships with NetworkX."""
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
(work / "data").mkdir(exist_ok=True)
with (work / "data" / "marriages.csv").open("w") as handle:
    handle.write("family_a,family_b\n")
    for a, b in sorted(tuple(sorted(e)) for e in nx.florentine_families_graph().edges):
        handle.write(f"{a},{b}\n")
