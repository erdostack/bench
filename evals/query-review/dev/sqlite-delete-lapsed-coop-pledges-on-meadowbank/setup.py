"""Build data/meadowbank.sqlite and data/sandpit.sqlite (last night's copy, identical): 6,000 members,
5 sites, 7 share offers, about 31,000 edges."""
import random
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
live = data / "meadowbank.sqlite"
for p in (live, data / "sandpit.sqlite"):
    if p.exists():
        p.unlink()
rng = random.Random(80511)
conn = sqlite3.connect(live)
conn.executescript((work / "db" / "schema.sql").read_text())
t0 = datetime(2014, 1, 1)


def day(d):
    return (t0 + timedelta(days=d)).strftime("%Y-%m-%d")


nodes = [(i, "member", f"M{i:05d}", f"member {i}", rng.choice(["active"] * 9 + ["closed"]), day(rng.randint(0, 4600)))
         for i in range(1, 6001)]
sites = ["Hilltop Wind", "Brook Farm Solar", "School Roofs", "Weir Hydro", "Depot Solar"]
for k, s in enumerate(sites):
    nodes.append((7001 + k, "site", f"S{k + 1}", s, "generating", day(400 * k)))
offers = [("O2014", "closed", 0), ("O2016", "closed", 1), ("O2018", "closed", 2), ("O2020", "closed", 3),
          ("O2022", "closed", 4), ("O2024", "closed", 1), ("O2026", "open", 4)]
for k, (ref, st, _site) in enumerate(offers):
    nodes.append((7101 + k, "offer", ref, f"share offer {ref[1:]}", st, day(730 * k)))
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)", nodes)
edges = []
for m in range(1, 6001):
    for _ in range(rng.choice([1, 1, 2, 3])):
        k = rng.randrange(6)
        edges.append(("pledge", m, 7101 + k, rng.choices(["converted", "lapsed"], [40, 60])[0],
                      rng.randint(50, 5000), day(730 * k + rng.randint(0, 90))))
        if edges[-1][3] == "converted":
            edges.append(("holds", m, 7001 + offers[k][2], None, edges[-1][4], day(730 * k + 100)))
    if rng.random() < 0.3:
        edges.append(("pledge", m, 7107, "open", rng.randint(50, 5000), day(4380 + rng.randint(0, 300))))
    if rng.random() < 0.2:
        edges.append(("nominee", m, rng.randint(1, 6000), None, None, day(rng.randint(0, 4600))))
rng.shuffle(edges)
conn.executemany("INSERT INTO edges (kind, src, dst, status, amount, created_at) VALUES (?, ?, ?, ?, ?, ?)", edges)
conn.commit()
conn.close()
shutil.copyfile(live, data / "sandpit.sqlite")
