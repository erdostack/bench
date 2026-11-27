#!/usr/bin/env python3
"""Rebuild data/practice.json from a fixed seed: invented clubs, teams and grounds."""
import json
import random
import sys
from pathlib import Path

import networkx as nx

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent


def build(seed):
    rng = random.Random(seed)
    G = nx.DiGraph()
    grounds = [f"GR-{i:03d}" for i in range(1, 61)]
    for g in grounds:
        G.add_node(g, kind="ground", name=f"Ground {g[3:]}")
    clubs = [f"CL-{i:04d}" for i in rng.sample([x for x in range(100, 900) if x not in (112, 457, 458, 909)], 70)]
    for c in clubs:
        G.add_node(c, kind="club", name=f"Club {c[3:]}", founded=rng.randint(1950, 2020))
    for c in clubs:
        for g in rng.sample(grounds, rng.randint(1, 2)):
            G.add_edge(c, g, kind="home_ground", since=rng.randint(1990, 2025))
    t = 4000
    for c in clubs:
        for _ in range(rng.randint(4, 12)):
            t += 1
            G.add_node(f"TM-{t:05d}", kind="team", name=f"Team {t}", age_group=f"U{rng.randint(7, 16)}")
            G.add_edge(f"TM-{t:05d}", c, kind="of_club")
    for c in rng.sample(clubs, 12):
        p = rng.choice([x for x in clubs if x != c])
        G.add_edge(c, p, kind="affiliated_to")
    return G


def with_duplicate(G):
    """The 2026 import added Hollybank Rovers a second time, as CL-0457."""
    G = G.copy()
    G.add_node("CL-0112", kind="club", name="Hollybank Rovers", founded=1978)
    G.add_node("CL-0457", kind="club", name="Hollybank Rovers JFC", founded=1978)
    for g, since in (("GR-007", 1981), ("GR-019", 2012)):
        G.add_edge("CL-0112", g, kind="home_ground", since=since)
    G.add_edge("CL-0457", "GR-044", kind="home_ground", since=2024)
    for i, age in enumerate(["U9", "U10", "U11", "U12", "U13"]):
        G.add_node(f"TM-09{i:03d}", kind="team", name=f"Hollybank {age}", age_group=age)
        G.add_edge(f"TM-09{i:03d}", "CL-0112", kind="of_club")
    for i, age in enumerate(["U14", "U15", "U16"]):
        G.add_node(f"TM-09{i + 50:03d}", kind="team", name=f"Hollybank JFC {age}", age_group=age)
        G.add_edge(f"TM-09{i + 50:03d}", "CL-0457", kind="of_club")
    G.add_node("CL-0458", kind="club", name="Hollybank Rovers Girls", founded=2019)
    G.add_edge("CL-0458", "CL-0457", kind="affiliated_to")
    G.add_edge("CL-0458", "GR-019", kind="home_ground", since=2019)
    G.add_node("CL-0909", kind="club", name="Northvale Community FC", founded=1962)
    G.add_edge("CL-0457", "CL-0909", kind="affiliated_to")
    return G


if __name__ == "__main__":
    out = ROOT / "data" / "practice.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    G = with_duplicate(build(4417))
    out.write_text(json.dumps(nx.node_link_data(G), indent=1, sort_keys=True))
    print(f"practice rebuilt: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
