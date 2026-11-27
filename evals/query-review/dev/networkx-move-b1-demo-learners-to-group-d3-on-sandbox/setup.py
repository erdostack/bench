"""Build data/sandbox.graphml (with scripts/make_sandbox.py) and data/live.graphml (this term's timetable)."""
import random
import subprocess
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
(work / "data").mkdir(exist_ok=True)
subprocess.run([sys.executable, str(work / "scripts" / "make_sandbox.py")], check=True, capture_output=True)
rng = random.Random(5150)
G = nx.DiGraph()
groups = [f"{lang}-{lv}-{n}" for lang in ("ES", "EN", "FR", "DE") for lv in ("A2", "B1", "B2") for n in (1, 2)]
for i in range(1, 19):
    G.add_node(f"T-{i:02d}", kind="teacher")
for g in groups:
    G.add_node(g, kind="group")
    G.add_edge(g, f"T-{rng.randint(1, 18):02d}", kind="taught_by")
for i in range(1, 641):
    g = rng.choice(groups)
    G.add_node(f"L-{40000 + i}", kind="learner", name=f"Learner {i}", level=g.split("-")[1])
    G.add_edge(f"L-{40000 + i}", g, kind="member_of")
nx.write_graphml(G, work / "data" / "live.graphml")
