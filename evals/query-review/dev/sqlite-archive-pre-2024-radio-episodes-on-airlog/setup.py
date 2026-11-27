"""Build data/airlog.db and data/rehearsal.db (this morning's restore, identical): 40 shows, 60 presenters,
6,000 tracks; episodes from 2022-01-01 to 2026-11-22 (2019 to 2021 already archived), 12 unaired pilots;
repeats since 2024 carry a repeat_of edge, some of them to episodes from 2023."""
import random
import shutil
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
live = data / "airlog.db"
for p in (live, data / "rehearsal.db"):
    if p.exists():
        p.unlink()
rng = random.Random(4417)
conn = sqlite3.connect(live)
conn.executescript((work / "db" / "schema.sql").read_text())
nodes = [(1 + i, "show", f"SH-{i:03d}", f"Show {i}", None) for i in range(40)]
nodes += [(100 + i, "presenter", f"PR-{i:03d}", f"Presenter {i}", None) for i in range(60)]
nodes += [(1000 + i, "track", f"TR-{i:05d}", f"Track {i}", None) for i in range(6000)]
archived_nodes, archived_edges = [], []
eid = [1]


def nid():
    nid.n += 1
    return nid.n


nid.n = 20000


def episode(day, edges_out, repeat_pool, archived=False):
    i = nid()
    row = (i, "episode", f"EP-{i}", f"Episode {i}", day.isoformat() if day else None)
    es = [("episode_of", i, rng.randint(1, 40))]
    es += [("hosted_by", i, p) for p in rng.sample(range(100, 160), rng.choice([1, 1, 2]))]
    es += [("played", i, t) for t in rng.sample(range(1000, 7000), rng.randint(8, 20))]
    if day and day >= date(2024, 1, 1) and repeat_pool and rng.random() < 0.12:
        es.append(("repeat_of", i, rng.choice(repeat_pool)))
    (archived_nodes if archived else nodes).append(row)
    (archived_edges if archived else edges_out).extend(es)
    return i


edges = []
d = date(2019, 1, 2)
while d < date(2022, 1, 1):
    episode(d, edges, None, archived=True)
    d += timedelta(days=rng.choice([1, 2, 2, 3]))
pool, by_year = [], {}
d = date(2022, 1, 1)
while d <= date(2026, 11, 22):
    i = episode(d, edges, pool)
    by_year.setdefault(d.year, []).append(i)
    if d.year >= 2023:
        pool.append(i)
    d += timedelta(days=rng.choice([1, 1, 2]))
for _ in range(12):
    episode(None, edges, None)
# no episode is the original of more than two repeats
seen = {}
edges = [e for e in edges if e[0] != "repeat_of" or seen.setdefault(e[2], []).append(1) or len(seen[e[2]]) <= 2]
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?)", nodes)
conn.executemany("INSERT INTO nodes_archive VALUES (?, ?, ?, ?, ?)", archived_nodes)
k = 0
rows = []
for e in archived_edges:
    k += 1
    rows.append((k, *e))
conn.executemany("INSERT INTO edges_archive VALUES (?, ?, ?, ?)", rows)
rows = []
for e in edges:
    k += 1
    rows.append((k, *e))
rng.shuffle(rows)
conn.executemany("INSERT INTO edges VALUES (?, ?, ?, ?)", rows)
conn.commit()
conn.close()
shutil.copyfile(live, data / "rehearsal.db")
