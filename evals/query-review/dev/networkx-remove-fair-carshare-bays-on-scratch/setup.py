"""Build data/published/bays.json (392 bays) and data/scratch/bays.json: published plus last week's
trials on scratch: the summer fair layout (14 temporary TMP- bays with walking links) and a separate trial
of three new car-park bays B-0901..B-0903 with re-measured walks, which the user wants kept."""
import json
import random
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
rng = random.Random(81233)
zones = ["Z-ORCHARD", "Z-MILL", "Z-QUAY", "Z-STATION", "Z-ABBEY", "Z-CASTLE", "Z-MARKET", "Z-PARK", "Z-KILN"]
G = nx.Graph()
pos = {}
for i in range(1, 391):
    code = f"B-{i:04d}"
    pos[code] = (rng.uniform(0, 60), rng.uniform(0, 40))
    G.add_node(code, zone=zones[int(pos[code][0] // 7) % len(zones)], spaces=rng.choice([1, 2, 2, 3, 4, 6, 12]),
               kind=rng.choice(["street"] * 5 + ["carpark"]))


def link(H, a, b):
    (x1, y1), (x2, y2) = pos[a], pos[b]
    d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    if d < 4.2:
        H.add_edge(a, b, minutes=max(1, round(d * 2.6)))


nodes = list(G)
for i, a in enumerate(nodes):
    for b in nodes[i + 1:]:
        link(G, a, b)
pos["B-0391"] = pos["B-0392"] = (pos["B-0214"][0] + 1.5, pos["B-0214"][1] + 1.5)
exec((work / "changes" / "0012_add_kiln_lane_bays.py").read_text(), {"G": G})   # already run on published
pub = work / "data" / "published"
pub.mkdir(parents=True, exist_ok=True)
(pub / "bays.json").write_text(json.dumps(nx.node_link_data(G, edges="links"), sort_keys=True))
S = G.copy()
for i in range(1, 15):
    code = f"TMP-{i:02d}"
    pos[code] = (rng.uniform(20, 32), rng.uniform(10, 22))
    S.add_node(code, zone="Z-PARK", spaces=rng.choice([4, 6, 8]), kind="temporary")
    near = sorted(G, key=lambda b: (pos[b][0] - pos[code][0]) ** 2 + (pos[b][1] - pos[code][1]) ** 2)[:rng.randint(2, 4)]
    for b in near:
        S.add_edge(code, b, minutes=rng.randint(2, 9))
for i in range(1, 15):
    if i > 1 and rng.random() < 0.5:
        S.add_edge(f"TMP-{i:02d}", f"TMP-{i - 1:02d}", minutes=1)
for i in range(901, 904):
    code = f"B-{i:04d}"
    S.add_node(code, zone="Z-STATION", spaces=10, kind="carpark")
    for b in rng.sample([n for n in G if G.nodes[n]["zone"] == "Z-STATION"], 3):
        S.add_edge(code, b, minutes=rng.randint(3, 10))
for u, v in rng.sample(sorted(G.edges), 6):
    S[u][v]["minutes"] += 2
scr = work / "data" / "scratch"
scr.mkdir(parents=True, exist_ok=True)
(scr / "bays.json").write_text(json.dumps(nx.node_link_data(S, edges="links"), sort_keys=True))
