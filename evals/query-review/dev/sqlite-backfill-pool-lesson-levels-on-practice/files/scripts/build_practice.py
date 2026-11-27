#!/usr/bin/env python3
"""Build data/practice.db: made-up pools, lessons, swimmers and instructors from a fixed seed (the same every
time). About a third of the lessons have no level, as in the old system's export."""
import random
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = ROOT / "data" / "practice.db"
path.parent.mkdir(exist_ok=True)
if path.exists():
    path.unlink()
rng = random.Random(1966)
conn = sqlite3.connect(path)
conn.executescript((ROOT / "db" / "schema.sql").read_text())
nodes, edges = [], []
pools = {"POOL-WYF": 1, "POOL-HAMB": 2, "POOL-LEA": 3}
for code, i in pools.items():
    nodes.append((i, "pool", code, None))
inst = list(range(10, 30))
for i in inst:
    nodes.append((i, "instructor", f"IN-{i:03d}", None))
nid = 100
lessons = []
for pool in pools:
    for day in ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"):
        for t in ("0830", "0900", "0930", "1000", "1030", "1100", "1530", "1600", "1630", "1700", "1730", "1800"):
            if rng.random() < 0.35:
                continue
            nid += 1
            r = rng.random()
            stage = "AQ" if r < 0.06 else "AD" if r < 0.12 else f"S{rng.randint(1, 7)}"
            code = f"LS-{pool[5:]}-{day}-{t}-{stage}"
            if stage.startswith("S"):
                s = int(stage[1])
                roll = rng.random()
                level = None if roll < 0.35 else (min(7, s + 1) if roll < 0.45 else s)
            else:
                level = None
            nodes.append((nid, "lesson", code, level))
            edges.append(("held_at", nid, pools[pool]))
            edges.append(("taught_by", nid, rng.choice(inst)))
            lessons.append(nid)
for k in range(1500):
    nid += 1
    nodes.append((nid, "swimmer", f"SW-{k:05d}", None))
    for les in rng.sample(lessons, rng.choice([1, 1, 2])):
        edges.append(("enrolled_in", nid, les))
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?)", nodes)
conn.executemany("INSERT INTO edges (kind, src, dst) VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
print(f"practice built: {len(lessons)} lessons")
