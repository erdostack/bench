"""Build data/estate.sqlite and data/rehearsal.sqlite (last night's copy, identical): 12 regions and
3,000 stores; the stores from the October import have no in_region edge."""
import random
import shutil
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
prod = data / "estate.sqlite"
for p in (prod, data / "rehearsal.sqlite"):
    if p.exists():
        p.unlink()
rng = random.Random(412)
conn = sqlite3.connect(prod)
conn.executescript((work / "db" / "schema.sql").read_text())
regions = ["R-NW", "R-NE", "R-YH", "R-EM", "R-WM", "R-EA", "R-LN", "R-SE", "R-SW", "R-WA", "R-SC", "R-NI"]
nodes = [(i + 1, "region", c, f"Region {c}", "active", None, None) for i, c in enumerate(regions)]
d0 = date(1985, 1, 1)
stores = []
for k in range(3000):
    sid = 100 + k
    x = rng.random()
    status = "trading" if x < 0.70 else "refit" if x < 0.76 else "closed" if x < 0.92 else "planning"
    opened = None if status == "planning" else (d0 + timedelta(days=rng.randint(0, 14500))).isoformat()
    nodes.append((sid, "store", f"ST-{k:04d}", f"Store {k}", status, rng.choice(regions), opened))
    stores.append((sid, status, k))
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?)", nodes)
rid = {c: i + 1 for i, c in enumerate(regions)}
reg = {n[0]: n[5] for n in nodes}
opened = {n[0]: n[6] for n in nodes}
edges = []
for sid, status, k in stores:
    imported = k >= 2300                       # the October import: no in_region edges at all
    if status in ("trading", "refit") and not imported:
        edges.append(("in_region", sid, rid[reg[sid]], opened[sid]))
    if status in ("trading", "refit") and rng.random() < 0.9:
        edges.append(("manages", rid[reg[sid]], sid, opened[sid]))
rng.shuffle(edges)
conn.executemany("INSERT INTO edges (kind, src, dst, since) VALUES (?, ?, ?, ?)", edges)
conn.commit()
conn.close()
shutil.copyfile(prod, data / "rehearsal.sqlite")
