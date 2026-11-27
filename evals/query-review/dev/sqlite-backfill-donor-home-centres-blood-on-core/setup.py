"""Build data/core.db and data/rehearsal.db (this morning's copy, identical): 14 centres, 9,000 donors and
their donations; home_centre set for some active donors (by the app or by hand), missing for the rest."""
import random
import shutil
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
prod = data / "core.db"
for p in (prod, data / "rehearsal.db"):
    if p.exists():
        p.unlink()
rng = random.Random(4417)
conn = sqlite3.connect(prod)
conn.executescript((work / "db" / "schema.sql").read_text())
names = ["Castle Mead", "Riverside", "Hollins", "Upper Weir", "Penhallow", "Brookfield", "Norton Cross", "Elm Park",
         "Harbour Road", "St Brannock", "Ashcombe", "Kingsway", "Moorfield", "Tidewell"]
nodes = [(i + 1, "centre", f"DC-{i + 1:02d}", n, "closed" if i + 1 == 9 else "open") for i, n in enumerate(names)]
edges = []
d0 = date(2015, 1, 1)
for k in range(9000):
    did = 1000 + k
    status = "active" if rng.random() < 0.88 else "withdrawn"
    nodes.append((did, "donor", f"D-{200000 + k}", f"Donor {k}", status))
    n = rng.choice([0, 0, 1, 2, 3, 4, 6, 8, 11])
    usual = rng.randint(1, 14)
    days = sorted(rng.sample(range(0, 4340), n))
    gifts = []
    for dd in days:
        c = usual if rng.random() < 0.7 else rng.randint(1, 14)
        if c == 9 and dd > 4198:          # nobody gives at Harbour Road after it closed (2026-06-30)
            c = usual if usual != 9 else 3
        day = (d0 + timedelta(days=dd)).isoformat()
        gifts.append((c, day))
        edges.append(("donated_at", did, c, day))
    if status == "active" and gifts:
        r = rng.random()
        if r < 0.22:                       # set by the app from the latest donation
            edges.append(("home_centre", did, gifts[-1][0], gifts[-1][1]))
        elif r < 0.30:                     # set by hand after a move: another centre
            c = rng.choice([x for x in range(1, 15) if x not in (9, gifts[-1][0])])
            edges.append(("home_centre", did, c, gifts[-1][1]))
rng.shuffle(edges)
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?)", nodes)
conn.executemany("INSERT INTO edges (id, kind, src, dst, day) VALUES (?, ?, ?, ?, ?)",
                 [(i + 1, *e) for i, e in enumerate(edges)])
conn.commit()
conn.close()
shutil.copy(prod, data / "rehearsal.db")
