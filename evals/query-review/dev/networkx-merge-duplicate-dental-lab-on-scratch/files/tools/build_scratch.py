"""Build a lab-referrals graph from generated data: python3 tools/build_scratch.py [path]
(default scratch/labs.graphml)."""
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
LABS = ["Brightsmile Dental Lab", "Northgate Ceramics", "Peak Prosthetics", "Riverside Dental Studio",
        "Crown & Bridge Works", "Harrow Orthodontic Lab", "Ashdown Dentures", "Fenwick Dental Arts",
        "Brightstone Dental Studio", "Meridian Lab Services", "Coastline Dental Lab", "Oakfield Ceramics"]
CODES = [7, 2, 4, 9, 11, 15, 16, 18, 13, 22, 24, 27]
CITIES = ["Leicester", "Nottingham", "Derby", "Loughborough"]
ITEMS = {"crown": 9500, "bridge": 21000, "denture": 16000, "guard": 4500, "aligner": 30000}


def build(path: Path, seed: int = 731, duplicate: bool = True) -> None:
    rng = random.Random(seed)
    G = nx.DiGraph()
    for i, c in enumerate(CITIES):
        G.add_node(f"CITY-{i + 1:02d}", kind="city", name=c)
    labs = []
    for i, name in enumerate(LABS):
        code = f"LAB-{CODES[i]:02d}"
        G.add_node(code, kind="lab", name=name, city=CITIES[i % len(CITIES)])
        G.add_edge(code, f"CITY-{i % len(CITIES) + 1:02d}", kind="in_city")
        labs.append(code)
    if duplicate:
        # entered again in March 2026 by the new branch
        G.add_node("LAB-31", kind="lab", name="Bright Smile Dental Laboratory", city=CITIES[0])
        G.add_edge("LAB-31", "CITY-01", kind="in_city")
    dentists = [f"DN-{i:03d}" for i in range(1, 23)]
    for d in dentists:
        G.add_node(d, kind="dentist", name=f"Dr {d[3:]}")
    day = date(2025, 1, 6)
    n = 0
    while day <= date(2026, 11, 20):
        for _ in range(rng.randint(1, 6)):
            n += 1
            cs = f"CS-{30000 + n}"
            item = rng.choice(list(ITEMS))
            G.add_node(cs, kind="case", opened_on=day.isoformat(), item=item)
            lab = rng.choices(labs, [6] + [1] * (len(labs) - 1))[0]
            if duplicate and lab == "LAB-07" and day >= date(2026, 3, 9) and rng.random() < 0.55:
                lab = "LAB-31"
            G.add_edge(cs, lab, kind="sent_to", sent_on=(day + timedelta(days=rng.randint(0, 3))).isoformat(),
                       fee=ITEMS[item] + rng.randint(-8, 8) * 100)
            G.add_edge(cs, rng.choice(dentists), kind="by")
        day += timedelta(days=1)
    path.parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(G, path)


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scratch" / "labs.graphml")
