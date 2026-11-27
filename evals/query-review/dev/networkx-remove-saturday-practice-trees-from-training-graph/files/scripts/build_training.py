"""Rebuild data/training.json, the course graph for survey training: 4 practice streets, 60 PRAC-BASE trees,
12 volunteers and their practice surveys. Deterministic."""
import json
import random
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
SPECIES = ["Tilia x europaea", "Platanus x hispanica", "Acer campestre", "Sorbus aria", "Prunus avium"]


def build():
    rng = random.Random(7731)
    G = nx.DiGraph()
    streets = [f"PRAC-ST-{i}" for i in range(1, 5)]
    for s in streets:
        G.add_node(s, kind="street")
    vols = [f"VOL-{i:02d}" for i in range(1, 13)]
    for v in vols:
        G.add_node(v, kind="volunteer")
    for i in range(1, 61):
        t = f"PRAC-BASE-{i:03d}"
        G.add_node(t, kind="tree", species=rng.choice(SPECIES))
        G.add_edge(t, rng.choice(streets), kind="on_street")
        for v in rng.sample(vols, rng.randint(1, 3)):
            G.add_edge(v, t, kind="surveyed", on=f"2026-0{rng.randint(3, 9)}-{rng.randint(10, 28)}")
    return G


if __name__ == "__main__":
    out = ROOT / "data" / "training.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(nx.node_link_data(build(), edges="edges"), indent=1, sort_keys=True))
    print(f"wrote {out}")
