"""Build data/hallb-rig.json (the plan) and data/scratch-rig.json (a copy of it, as fresh_scratch.py makes)."""
import json
import random
import shutil
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
rng = random.Random(305)
G = nx.DiGraph()
for d in ("DISTRO-A", "DISTRO-B"):
    G.add_node(d, kind="distro")
for s in ("SPLIT-1", "SPLIT-2"):
    G.add_node(s, kind="splitter")
for u in range(1, 5):
    G.add_node(f"U-{u}", kind="universe")
for r in range(1, 7):
    G.add_node(f"DR-{r}", kind="rack")
    G.add_edge(f"DR-{r}", "DISTRO-A" if r <= 3 else "DISTRO-B", kind="powered_from", way=r)
    G.add_edge("SPLIT-1" if r % 2 else "SPLIT-2", f"DR-{r}", kind="sends_data")
used = {r: (list(range(21, 49)) if r == 3 else list(range(1, 21)) if r == 5 else list(range(1, 49))) for r in range(1, 7)}
for r in used:
    rng.shuffle(used[r])
types = ["profile", "fresnel", "led-par", "moving-head", "cyc", "blinder"]
positions = ["FOH", "LX1", "LX2", "LX3", "LX4", "BOOM-L", "BOOM-R"]
addr = {u: 1 for u in range(1, 5)}
n = 0
for r in range(1, 7):
    for c in used[r][: (28 if r == 3 else 20 if r == 5 else rng.randint(30, 44))]:
        n += 1
        f = f"F-{n:04d}"
        t = rng.choice(types)
        G.add_node(f, kind="fixture", type=t, position=rng.choice(positions))
        G.add_edge(f, f"DR-{r}", kind="fed_by", circuit=c)
        u = rng.randint(1, 4)
        G.add_edge(f, f"U-{u}", kind="on_universe", address=addr[u])
        addr[u] += 16 if t == "moving-head" else 2
data = work / "data"
data.mkdir(exist_ok=True)
(data / "hallb-rig.json").write_text(json.dumps(nx.node_link_data(G, edges="links"), indent=1))
shutil.copyfile(data / "hallb-rig.json", data / "scratch-rig.json")
