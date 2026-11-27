"""Write data/network.json: ~3,000 species, ~11,000 interactions, records from 1998 to 2026."""
import json
import random
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
rng = random.Random(5521)
G = nx.Graph()


def day(lo, hi):
    return f"{rng.randint(lo, hi)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"


plants = [f"plant-{i:04d}" for i in range(1, 1201)]
polls = [f"poll-{i:04d}" for i in range(1, 1801)]
for n in plants:
    G.add_node(n, kind="plant", last_seen=day(1998, 2026) if rng.random() < 0.15 else day(2017, 2026))
for n in polls:
    G.add_node(n, kind="pollinator", last_seen=day(1998, 2026) if rng.random() < 0.15 else day(2017, 2026))
while G.number_of_edges() < 11000:
    p, b = rng.choice(plants), rng.choice(polls)
    G.add_edge(p, b, seen=day(1998, 2026), visits=rng.randint(1, 40))
(work / "data").mkdir(exist_ok=True)
(work / "data" / "network.json").write_text(json.dumps(nx.node_link_data(G, edges="links")))
