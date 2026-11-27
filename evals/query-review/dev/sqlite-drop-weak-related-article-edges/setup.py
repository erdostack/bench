"""Build var/helpdesk.db: 7,000 articles, about 70,000 related edges (auto top-k suggestions plus editor
edges); editors pinned about 6% of the auto suggestions, low-scoring ones included."""
import random
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
db = work / "var" / "helpdesk.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
rng = random.Random(3512)
conn = sqlite3.connect(db)
conn.executescript((work / "db" / "schema.sql").read_text())
N = 7000
conn.executemany("INSERT INTO articles VALUES (?, ?, ?, 'en')", [(i, f"a-{i}", f"Article {i}") for i in range(1, N + 1)])
rows, seen = [], set()
for s in range(1, N + 1):
    for d in rng.sample(range(1, N + 1), rng.randint(6, 12)):
        if d == s or (s, d) in seen:
            continue
        seen.add((s, d))
        score = round(rng.betavariate(2.2, 2.6), 4)
        rows.append((s, d, "auto", score, 1 if rng.random() < 0.06 else 0))
    for d in rng.sample(range(1, N + 1), rng.choice([0, 0, 0, 1, 2])):
        if d != s and (s, d) not in seen:
            seen.add((s, d))
            rows.append((s, d, "editor", None, 1 if rng.random() < 0.5 else 0))
rng.shuffle(rows)
conn.executemany("INSERT INTO related (src, dst, origin, score, pinned) VALUES (?, ?, ?, ?, ?)", rows)
conn.execute("ANALYZE")
conn.commit()
conn.close()
