"""Build data/live.db and data/scratch.db (last night's copy, identical): 5 depots, 40 zones and 5,200 cars.
About 3,600 older active cars have their serviced_by edge; the ~1,300 active cars of the September 2026
import have none, and the ~300 retired cars have none."""
import random
import shutil
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
live = data / "live.db"
for p in (live, data / "scratch.db"):
    if p.exists():
        p.unlink()
rng = random.Random(52061)
conn = sqlite3.connect(live)
conn.executescript((work / "db" / "schema.sql").read_text())
FLOODED = {10088, 10112, 10230, 10231}   # changes/0007
rows, edges = [], []
nid = 0
depots = []
for code in ("D-NORTH", "D-SOUTH", "D-EAST", "D-WEST", "D-CENTRAL"):
    nid += 1
    depots.append(nid)
    rows.append((nid, "depot", code, code[2:].title() + " depot", None))
streets = ["ORCHARD", "MILL", "QUAY", "STATION", "ABBEY", "CASTLE", "MARKET", "PARK", "BRIDGE", "CHAPEL",
           "FORGE", "GREEN", "HILL", "KILN", "LOCK", "MEADOW", "NORTHGATE", "OAK", "PRIORY", "RIVERSIDE"]
zones, cover = [], {}
for i in range(40):
    nid += 1
    zones.append(nid)
    rows.append((nid, "zone", f"Z-{streets[i % 20]}{'' if i < 20 else '-2'}", None, None))
    cover[nid] = depots[i % 5] if rng.random() < 0.7 else rng.choice(depots)
    edges.append(("covered_by", nid, cover[nid]))
for i in range(5200):
    nid += 1
    z = rng.choice(zones)
    if i < 3900:
        status = "retired" if rng.random() < 0.08 or 10000 + i in FLOODED else "active"
        serviced = status == "active"
    else:
        status = "active"
        serviced = False
    rows.append((nid, "car", f"CAR-FK-{10000 + i}", None, status))
    edges.append(("based_in", nid, z))
    if serviced:
        edges.append(("serviced_by", nid, cover[z]))
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?)", rows)
rng.shuffle(edges)
conn.executemany("INSERT INTO edges (kind, src, dst) VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
shutil.copyfile(live, data / "scratch.db")
