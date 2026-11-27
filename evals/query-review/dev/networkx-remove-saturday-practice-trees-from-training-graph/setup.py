"""Build data/training.json as Saturday's session left it (the course graph plus 41 PRAC-SAT- trees, their
street links and surveys) and data/published.json (the public survey graph)."""
import importlib.util
import json
import random
import sys
from pathlib import Path

import networkx as nx

sys.dont_write_bytecode = True
work = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("bt", work / "scripts" / "build_training.py")
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
rng = random.Random(1121)
G = bt.build()
streets = [n for n, a in G.nodes(data=True) if a["kind"] == "street"]
vols = [n for n, a in G.nodes(data=True) if a["kind"] == "volunteer"]
for i in range(1, 42):
    t = f"PRAC-SAT-{i:02d}"
    G.add_node(t, kind="tree", species=rng.choice(bt.SPECIES))
    G.add_edge(t, rng.choice(streets), kind="on_street")
    for v in rng.sample(vols, rng.randint(1, 4)):
        G.add_edge(v, t, kind="surveyed", on="2026-11-21")
(work / "data").mkdir(exist_ok=True)
(work / "data" / "training.json").write_text(json.dumps(nx.node_link_data(G, edges="edges"), indent=1, sort_keys=True))

P = nx.DiGraph()
for i in range(1, 41):
    P.add_node(f"USRN-{21400000 + 7 * i}", kind="street")
for i in range(30):
    P.add_node(f"VOL-{i:02d}", kind="volunteer")
for i in range(2400):
    t = f"T-{48000 + i:07d}"
    P.add_node(t, kind="tree", species=rng.choice(bt.SPECIES))
    P.add_edge(t, f"USRN-{21400000 + 7 * rng.randint(1, 40)}", kind="on_street")
    P.add_edge(f"VOL-{rng.randint(0, 29):02d}", t, kind="surveyed", on=f"2026-{rng.randint(5, 10):02d}-{rng.randint(10, 28)}")
(work / "data" / "published.json").write_text(json.dumps(nx.node_link_data(P, edges="edges"), indent=1, sort_keys=True))
