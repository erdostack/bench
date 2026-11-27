"""Monthly lab spend per lab: python3 reports/lab_spend.py <graphml> [YYYY-MM]"""
import sys
from collections import defaultdict

import networkx as nx

G = nx.read_graphml(sys.argv[1])
month = sys.argv[2] if len(sys.argv) > 2 else None
spend = defaultdict(int)
for cs, lab, d in G.edges(data=True):
    if d.get("kind") == "sent_to" and (month is None or d["sent_on"].startswith(month)):
        spend[lab] += int(d["fee"])
for lab, pence in sorted(spend.items(), key=lambda kv: -kv[1]):
    print(f"{lab}  {G.nodes[lab]['name']:<34} {pence / 100:>12,.2f}")
