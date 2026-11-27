"""Build var/catalogue.db: 140 models (46 retired), 500 masts with 3 to 6 antennas each, 300 spare lines.
Some retired models are still installed somewhere or held as spares."""
import random
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
db = work / "var" / "catalogue.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
rng = random.Random(6707)
conn = sqlite3.connect(db)
conn.executescript((work / "db" / "schema.sql").read_text())
models = []
for i in range(1, 141):
    models.append((i, f"QX-{6000 + i * 7}", rng.choice(["700", "800", "1800", "2100", "2600", "3500"]),
                   "retired" if i % 3 == 0 else "current"))
conn.executemany("INSERT INTO models VALUES (?, ?, ?, ?)", models)
conn.executemany("INSERT INTO masts VALUES (?, ?)", [(i, f"MST{i:05d}") for i in range(1, 501)])
retired = [m[0] for m in models if m[3] == "retired"]
current = [m[0] for m in models if m[3] == "current"]
installed_retired = rng.sample(retired, 12)
ants = []
for mast in range(1, 501):
    for sector in range(1, rng.randint(3, 6) + 1):
        pool = installed_retired if rng.random() < 0.06 else current
        ants.append((mast, rng.choice(pool), sector, (sector - 1) * 120 % 360))
conn.executemany("INSERT INTO antennas (mast_id, model_id, sector, azimuth) VALUES (?, ?, ?, ?)", ants)
code = {m[0]: m[1] for m in models}
spare_retired = rng.sample(retired, 10)
spares = []
for _ in range(300):
    mid = rng.choice(spare_retired) if rng.random() < 0.1 else rng.choice(current)
    spares.append((rng.choice(["HAR", "EPP", "CHE", "WAL"]), code[mid], rng.randint(1, 12)))
conn.executemany("INSERT INTO spares (depot, model_code, qty) VALUES (?, ?, ?)", spares)
conn.commit()
conn.close()
