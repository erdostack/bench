"""Build data/corridors.db from db/schema.sql with generated patches and corridors (seed 29)."""
import random
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
rng = random.Random(29)
(work / "data").mkdir(exist_ok=True)
db = work / "data" / "corridors.db"
if db.exists():
    db.unlink()
con = sqlite3.connect(db)
con.executescript((work / "db" / "schema.sql").read_text())
patches = [(f"P-{i:02}", f"Patch {i:02}", round(rng.uniform(2, 80), 1)) for i in range(1, 26)]
con.executemany("INSERT INTO patch VALUES (?,?,?)", patches)
pairs = set()
while len(pairs) < 60:
    a, b = rng.sample([p[0] for p in patches], 2)
    pairs.add((a, b))
con.executemany("INSERT INTO corridor VALUES (?,?,?,?)",
                [(a, b, int(rng.random() < 0.7), int(rng.random() < 0.7)) for a, b in sorted(pairs)])
con.commit()
con.close()
