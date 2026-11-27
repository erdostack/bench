"""Build var/gatekeeper.db: 3,200 groups nested up to eight levels deep (a group can sit in several others),
about 5,400 nestings, and the reach table as the last refresh left it."""
import random
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
db = work / "var" / "gatekeeper.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
rng = random.Random(1414)
conn = sqlite3.connect(db)
conn.executescript((work / "db" / "schema.sql").read_text())
AREAS = ["eng", "ops", "sales", "legal", "finance", "support", "data", "design", "people", "it"]
levels = [10, 40, 150, 400, 700, 800, 700, 400]
groups, by_level, gid = [], [], 0
for depth, n in enumerate(levels):
    row = []
    for k in range(n):
        gid += 1
        groups.append((gid, f"{rng.choice(AREAS)}-l{depth}-{k:03d}", f"2026-{rng.randint(1, 10):02d}-{rng.randint(1, 28):02d}T09:00:00Z"))
        row.append(gid)
    by_level.append(row)
conn.executemany("INSERT INTO groups VALUES (?, ?, ?)", groups)
edges = set()
for depth in range(1, len(levels)):
    for child in by_level[depth]:
        edges.add((rng.choice(by_level[depth - 1]), child))
        if rng.random() < 0.55:
            edges.add((rng.choice(by_level[rng.randint(0, depth - 1)]), child))
        if rng.random() < 0.15:
            edges.add((rng.choice(by_level[rng.randint(0, depth - 1)]), child))
conn.executemany("INSERT INTO group_edges VALUES (?, ?, '2026-10-30T12:00:00Z')", sorted(edges))
conn.execute("INSERT INTO job_state VALUES ('reach_refreshed_at', '2026-11-22T02:10:04Z')")
conn.execute("""INSERT INTO reach WITH RECURSIVE walk(a, d) AS (
    SELECT parent_id, child_id FROM group_edges UNION
    SELECT w.a, e.child_id FROM walk w JOIN group_edges e ON e.parent_id = w.d) SELECT a, d FROM walk""")
conn.execute("ANALYZE")
conn.commit()
conn.close()
