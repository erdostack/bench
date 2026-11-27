"""Build data/assets.db and data/snapshot.db (last night's copy, identical): 9,000 devices with wards,
vendors and contracts. 1,700 Halvard anaesthesia machines, of them some on loan, some condemned, and the
theatre pilot already under SC-2027-ANA."""
import random
import shutil
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
db = data / "assets.db"
for p in (db, data / "snapshot.db"):
    if p.exists():
        p.unlink()
rng = random.Random(4412)
conn = sqlite3.connect(db)
conn.executescript((work / "db" / "schema.sql").read_text())
VENDORS = ["V-HALVARD", "V-CORVANE", "V-MERIDA", "V-OSTRAL", "V-TEKLA"]
nodes = [(i + 1, "vendor", v, v[2:].title(), None, None) for i, v in enumerate(VENDORS)]
vid = {v: i + 1 for i, v in enumerate(VENDORS)}
CONTRACTS = ["SC-2027-ANA", "SC-2026-INF", "SC-2025-MON", "SC-2026-VEN"]
nodes += [(10 + i, "contract", c, None, None, None) for i, c in enumerate(CONTRACTS)]
cid = {c: 10 + i for i, c in enumerate(CONTRACTS)}
WARDS = [f"W-{w}" for w in ("TH1", "TH2", "TH3", "ICU1", "ICU2", "A1", "A2", "B1", "B2", "C1", "MAT", "ED", "DSU", "ENDO")]
nodes += [(20 + i, "ward", w, None, None, None) for i, w in enumerate(WARDS)]
wid = {w: 20 + i for i, w in enumerate(WARDS)}
edges = []
dev = 1000
CLASSES = ["infusion", "monitor", "ventilator", "suction", "defibrillator"]


def add(cls, vendor, status, ward):
    global dev
    dev += 1
    nodes.append((dev, "device", f"MD-{dev:06d}", None, cls, status))
    edges.append(("made_by", dev, vid[vendor], None))
    edges.append(("located_in", dev, wid[ward], f"2025-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"))
    return dev


# Halvard anaesthesia machines
for i in range(1700):
    r = rng.random()
    status = "loan" if r < 0.04 else "condemned" if r < 0.105 else "in_store" if r < 0.20 else "in_service"
    ward = rng.choice(WARDS)
    d = add("anaesthesia", "V-HALVARD", status, ward)
    if status == "in_service" and ward == "W-TH1" and sum(1 for e in edges if e[0] == "covered_by") < 120:
        edges.append(("covered_by", d, cid["SC-2027-ANA"], "2026-11-01"))
# other vendors' anaesthesia machines and other classes
for i in range(500):
    add("anaesthesia", rng.choice(["V-MERIDA", "V-OSTRAL"]), rng.choice(["in_service", "in_store", "condemned"]), rng.choice(WARDS))
for i in range(6800):
    v = rng.choice(VENDORS)
    d = add(rng.choice(CLASSES), v, rng.choice(["in_service"] * 8 + ["in_store", "loan", "condemned"]), rng.choice(WARDS))
    if nodes[-1][4] == "infusion" and v == "V-CORVANE" and nodes[-1][5] in ("in_service", "in_store"):
        edges.append(("covered_by", d, cid["SC-2026-INF"], "2026-10-01"))
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)", nodes)
rng.shuffle(edges)
conn.executemany("INSERT INTO edges (kind, src, dst, since) VALUES (?, ?, ?, ?)", edges)
conn.commit()
conn.close()
shutil.copyfile(db, data / "snapshot.db")
