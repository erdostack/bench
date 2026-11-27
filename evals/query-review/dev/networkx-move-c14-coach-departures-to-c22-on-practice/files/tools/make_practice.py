"""Make a dispatch-board graph from generated data: python3 tools/make_practice.py [path]
(default var/practice/fleet.json)."""
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
PLACES = ["Whitby", "Scarborough", "Helmsley", "Malton", "Pickering", "Goathland", "Robin Hood's Bay", "Hawes",
          "Richmond", "Ripon", "Knaresborough", "Castle Howard", "Beverley", "Bridlington"]


def make(path: Path, seed: int = 1412) -> None:
    rng = random.Random(seed)
    G = nx.DiGraph()
    coaches = [f"C-{i:02d}" for i in range(1, 25)]
    for c in coaches:
        G.add_node(c, kind="coach", seats=rng.choice([49, 53, 57]), reg=f"YX{rng.randint(10, 75)} {rng.choice('ABCDEFGH')}{rng.choice('KLMNPRST')}{rng.choice('UVWXYZ')}")
    drivers = [f"DR-{100 + i}" for i in range(1, 31)]
    for d in drivers:
        G.add_node(d, kind="driver", name=f"Driver {d[3:]}")
    excursions = [f"EX-{i:03d}" for i in range(1, len(PLACES) + 1)]
    for e, p in zip(excursions, PLACES):
        G.add_node(e, kind="excursion", name=f"Day out: {p}")
    day = date(2026, 11, 2)
    n = 0
    while day <= date(2027, 1, 10):
        todays = rng.sample(coaches, rng.randint(7, 13))
        if "2026-11-28" <= day.isoformat() <= "2026-12-15" and "C-14" not in todays:
            todays.append("C-14")
        if "C-14" in todays and "C-22" in todays:
            todays.remove("C-22")
        for c in todays:
            n += 1
            dp = f"DP-{70000 + n}"
            G.add_node(dp, kind="departure", departs_on=day.isoformat())
            G.add_edge(dp, c, kind="run_by", booked_seats=rng.randint(12, 49))
            G.add_edge(dp, rng.choice(drivers), kind="driven_by")
            G.add_edge(dp, rng.choice(excursions), kind="of_excursion")
        day += timedelta(days=1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nx.node_link_data(G, edges="links"), indent=1))


if __name__ == "__main__":
    make(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "var" / "practice" / "fleet.json")
