#!/usr/bin/env python3
"""Rebuild graphs/practice/network.json: a copy of the live graph plus the workshop fixture (the practice port
PORT-PRACTICE, the workshop vessel MV-TRIALBOAT and the standing exercise sailings EX-01..EX-12). Anything
added to the practice graph since is gone afterwards."""
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
G = nx.node_link_graph(json.loads((ROOT / "graphs" / "live" / "network.json").read_text()), edges="links")
G.add_node("PORT-PRACTICE", kind="port", name="Practice Pier (workshop only)")
G.add_node("MV-TRIALBOAT", kind="vessel", name="Trialboat (workshop only)", cars=20)
ports = sorted(n for n, d in G.nodes(data=True) if d["kind"] == "port" and n != "PORT-PRACTICE")
for i in range(1, 13):
    s = f"EX-{i:02d}"
    G.add_node(s, kind="sailing", day="2026-12-0%d" % (1 + i % 7), departs=f"{7 + i:02d}:00")
    G.add_edge(s, "PORT-PRACTICE", kind="departs")
    G.add_edge(s, ports[i % len(ports)], kind="arrives")
    G.add_edge(s, "MV-TRIALBOAT", kind="operated_by")
out = ROOT / "graphs" / "practice" / "network.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(nx.node_link_data(G, edges="links"), indent=1, sort_keys=True))
print(f"practice rebuilt: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
