#!/usr/bin/env python3
"""Build var/scratch.db: a synthetic climnet graph from a fixed seed (300 stations, 6 hubs, ~900 sensors).
Run it again any time for a clean copy."""
import random
import sqlite3
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
db = ROOT / "var" / "scratch.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
rng = random.Random(4417)
conn = sqlite3.connect(db)
conn.executescript((ROOT / "db" / "schema.sql").read_text())
nodes, edges = [], []
hubs = {h: i for i, h in enumerate(["HUB-N", "HUB-E", "HUB-S", "HUB-W", "HUB-C", "HUB-X"], start=1)}
for h, i in hubs.items():
    nodes.append((i, "hub", h, None, None))
nid, sn = 100, 50000
for k in range(1, 301):
    nid += 1
    status = rng.choices(["active", "retired", "archived"], [62, 30, 8])[0]
    if status == "active":
        retired = None
    elif status == "archived":
        retired = f"{rng.randint(2009, 2016)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"
    else:
        retired = f"{rng.randint(2013, 2026)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"
        if retired > "2026-11-01":
            retired = "2026-10-15"
    if k in (201, 202):                       # two stations retired on the first day of 2020
        status, retired = "retired", "2020-01-01"
    station = nid
    nodes.append((station, "station", f"AWS-{k:04d}", status, retired))
    if status != "archived":
        edges.append(("reports_to", station, rng.randint(1, 6)))
    for _ in range(rng.randint(2, 4)):
        nid += 1
        sn += rng.randint(1, 40)
        nodes.append((nid, "sensor", f"SN-{sn}", None, None))
        edges.append(("installed_at", nid, station))
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?)", nodes)
conn.executemany("INSERT INTO edges (kind, src, dst) VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
print(f"built {db}")
