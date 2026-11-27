"""Build data/practice.db with the repo's own scripts/build_practice.py, and data/live.db (the live programme,
a different made-up set, every lesson with its level)."""
import random
import sqlite3
import subprocess
import sys
from pathlib import Path

work = Path(sys.argv[1])
subprocess.run([sys.executable, "scripts/build_practice.py"], cwd=work, check=True, capture_output=True)
live = work / "data" / "live.db"
if live.exists():
    live.unlink()
rng = random.Random(8080)
conn = sqlite3.connect(live)
conn.executescript((work / "db" / "schema.sql").read_text())
nodes = [(1, "pool", "POOL-WYF", None), (2, "pool", "POOL-HAMB", None)]
for k in range(140):
    s = rng.randint(1, 7)
    nodes.append((100 + k, "lesson", f"LS-{rng.choice(['WYF', 'HAMB'])}-{k:03d}-S{s}", s))
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?)", nodes)
conn.executemany("INSERT INTO edges (kind, src, dst) VALUES ('held_at', ?, ?)", [(100 + k, 1 + k % 2) for k in range(140)])
conn.commit()
conn.close()
