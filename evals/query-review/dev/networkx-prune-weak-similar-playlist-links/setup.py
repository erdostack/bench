"""Write data/similar_playlists.json: 2,500 playlists, ~40,000 links with distinct weights. Niche playlists
have only weak links; popular ones have many strong ones."""
import json
import random
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
rng = random.Random(33)
G = nx.Graph()
nodes = [f"pl{n:05d}" for n in range(1, 2501)]
G.add_nodes_from(nodes)
used = set()


def weight(lo, hi):
    while True:
        w = round(rng.uniform(lo, hi), 6)
        if w not in used:
            used.add(w)
            return w


for i, a in enumerate(nodes):
    niche = i % 5 == 0
    for b in rng.sample(nodes, rng.randint(4, 30)):
        if a == b or G.has_edge(a, b):
            continue
        strong = (not niche) and rng.random() < 0.45
        G.add_edge(a, b, weight=weight(0.2, 0.9) if strong else weight(0.01, 0.199))
for a in rng.sample(nodes, 40):           # a few playlists with one or two links only
    for b in list(G.neighbors(a))[2:]:
        G.remove_edge(a, b)
(work / "data").mkdir(parents=True, exist_ok=True)
(work / "data" / "similar_playlists.json").write_text(json.dumps(nx.node_link_data(G, edges="links")))
