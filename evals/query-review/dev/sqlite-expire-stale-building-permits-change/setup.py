"""Build var/permits.db (dev copy): 7,000 permits 2019-2026 with parcels, inspections and appeals.
Fixed seed."""
import random
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

work = Path(sys.argv[1])
db = work / "var" / "permits.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
rng = random.Random(1055)
conn = sqlite3.connect(db)
conn.executescript((work / "db" / "schema.sql").read_text())
nodes, edges = [], []
nid = 0


def add(kind, ref, status=None, issued=None, done=None):
    global nid
    nid += 1
    nodes.append((nid, kind, ref, status, issued, done))
    return nid


parcels = [add("parcel", f"APN-{i // 1000:04d}-{i % 1000:03d}") for i in range(1000, 4000)]
d0 = date(2019, 1, 7)
n_insp = 0
for i in range(7000):
    issued = d0 + timedelta(days=rng.randint(0, 2870))
    status = rng.choices(["open", "finaled", "revoked"], [60, 37, 3])[0]
    p = add("permit", f"BP-{issued.year}-{i:05d}", status, issued.isoformat())
    edges.append((p, rng.choice(parcels), "ON"))
    last = issued
    for _ in range(rng.choice([0, 0, 1, 1, 2, 3, 4])):
        last = last + timedelta(days=rng.randint(20, 420))
        if last > date(2026, 11, 20):
            break
        n_insp += 1
        ins = add("inspection", f"IN-{n_insp:06d}", None, None, last.isoformat())
        edges.append((ins, p, "INSPECTS"))
    if status == "open" and rng.random() < 0.025:
        a = add("appeal", f"AP-{i:05d}", rng.choice(["open", "open", "upheld", "dismissed"]))
        edges.append((a, p, "APPEALS"))
conn.executemany("INSERT INTO node VALUES (?, ?, ?, ?, ?, ?)", nodes)
conn.executemany("INSERT INTO edge VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
