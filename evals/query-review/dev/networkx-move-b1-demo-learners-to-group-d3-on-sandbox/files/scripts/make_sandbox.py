"""Rebuild data/sandbox.graphml, the demo timetable: groups DEMO-D1 to DEMO-D4, 6 teachers, 70 learners.
Deterministic."""
import random
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
LEVELS = ["A1", "A2", "B1", "B2", "C1"]
NAMES = ["Ana", "Bram", "Chloe", "Dev", "Eun-ji", "Femi", "Goran", "Hana", "Ines", "Jonas", "Kofi", "Lena"]


def build():
    rng = random.Random(2209)
    G = nx.DiGraph()
    groups = [f"DEMO-D{i}" for i in range(1, 5)]
    teachers = [f"TCH-{i:02d}" for i in range(1, 7)]
    for t in teachers:
        G.add_node(t, kind="teacher")
    for g in groups:
        G.add_node(g, kind="group")
        G.add_edge(g, rng.choice(teachers), kind="taught_by")
    for i in range(1, 71):
        lid = f"DL-{i:03d}"
        G.add_node(lid, kind="learner", name=f"{rng.choice(NAMES)} {chr(65 + i % 26)}.", level=rng.choice(LEVELS[1:4]))
        G.add_edge(lid, groups[0] if i <= 15 else groups[1] if i <= 45 else rng.choice(groups[2:]), kind="member_of")
    return G


if __name__ == "__main__":
    out = ROOT / "data" / "sandbox.graphml"
    out.parent.mkdir(exist_ok=True)
    nx.write_graphml(build(), out)
    print(f"wrote {out}")
