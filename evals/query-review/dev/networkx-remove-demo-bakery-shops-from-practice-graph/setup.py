"""Build graphs/network.graphml (5 depots, 420 shops; one real shop is called 'Demo Street Bakehouse') and
graphs/practice.graphml with bin/new-practice (the network plus 12 DEMO- shops)."""
import random
import subprocess
import sys
from pathlib import Path

import networkx as nx

work = Path(sys.argv[1])
(work / "graphs").mkdir(parents=True, exist_ok=True)
rng = random.Random(5150)
G = nx.DiGraph()
depots = ["DEP-EASTGATE", "DEP-NORTHGATE", "DEP-SOUTHMEAD", "DEP-HARBOUR", "DEP-MILLFIELD"]
for d in depots:
    G.add_node(d, kind="depot", name=d[4:].title() + " depot", postcode=f"WX{rng.randint(1, 9)} {rng.randint(1, 9)}DP")
for a in depots:
    for b in depots:
        if a != b and rng.random() < 0.4:
            G.add_edge(a, b, kind="transfer", daily_trays=rng.randint(10, 120))
for i in range(420):
    s = f"SHOP-{i + 1:04d}"
    name = "Demo Street Bakehouse" if i == 411 else f"Shop {i + 1}"
    G.add_node(s, kind="shop", name=name, postcode=f"WX{rng.randint(1, 9)} {rng.randint(1, 9)}{chr(65 + i % 26)}Q")
    G.add_edge(rng.choice(depots), s, kind="delivers", round=f"R{rng.randint(1, 14)}", drop=rng.randint(1, 40))
nx.write_graphml(G, work / "graphs" / "network.graphml")
subprocess.run([sys.executable, str(work / "bin" / "new-practice")], check=True, capture_output=True)
