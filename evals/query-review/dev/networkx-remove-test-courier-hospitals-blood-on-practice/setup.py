"""Build data/practice-net.graphml with the repo's script and add a trainer's exercise places (TEST-H1 to
TEST-H5); build data/courier-net.graphml, the live network."""
import random
import subprocess
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
subprocess.run([sys.executable, str(work / "scripts" / "build_practice_net.py")], check=True, capture_output=True)
p = work / "data" / "practice-net.graphml"
G = nx.read_graphml(p)
rng = random.Random(5)
others = sorted(G.nodes)
for i in range(1, 6):
    code = f"TEST-H{i}"
    G.add_node(code, kind="hospital", name=f"Exercise hospital {i}")
    for m in rng.sample(others, 3 + i % 2):
        G.add_edge(code, m, minutes=rng.randint(10, 60), road=rng.choice(["A", "B"]))
G.add_edge("TEST-H2", "TEST-H3", minutes=14, road="B")
G.add_edge("TEST-H4", "TEST-H5", minutes=21, road="A")
nx.write_graphml(G, p)
L = nx.Graph()
rng = random.Random(1)
places = [("LAB-S", "lab")] + [(f"DEP-{c}", "depot") for c in "NSEW"] + [(f"DC-{i:02d}", "centre") for i in range(1, 15)] + \
         [(f"H-{a}{b}{c}", "hospital") for a, b, c in ["QMR", "SGH", "RHC", "PRT", "WIN", "BAS", "SAL", "IOW", "CHI", "HAS"]]
for n, k in places:
    L.add_node(n, kind=k, name=n)
for n, _k in places:
    for m, _k2 in rng.sample(places, 3):
        if m != n:
            L.add_edge(n, m, minutes=rng.randint(6, 80), road=rng.choice(["A", "B", "M"]))
nx.write_graphml(L, work / "data" / "courier-net.graphml")
