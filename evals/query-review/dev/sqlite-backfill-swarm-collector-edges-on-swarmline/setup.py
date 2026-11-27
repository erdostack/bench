"""Build data/swarmline.db and data/practice.db (last night's rebuild, identical): 24 areas, 410 members,
about 6,800 swarm reports 2015-2026. Reports from the 2026 season already have their collected_by edges."""
import random
import shutil
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
live = data / "swarmline.db"
for p in (live, data / "practice.db"):
    if p.exists():
        p.unlink()
rng = random.Random(4402)
conn = sqlite3.connect(live)
conn.executescript((work / "db" / "schema.sql").read_text())
nid = 0


def node(kind, code, name=None, on=None, status=None, collector=None):
    global nid
    nid += 1
    conn.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?)", (nid, kind, code, name, on, status, collector))
    return nid


districts = [f"HX{i}" for i in range(1, 8)] + [f"OL{i}" for i in range(12, 18)] + [f"BD{i}" for i in range(20, 31)]
areas = {d: node("area", f"AR-{k + 1:02d}", d) for k, d in enumerate(districts)}
members = {}
for i in range(1, 411):
    members[f"M-{i:04d}"] = node("member", f"M-{i:04d}", f"Member {i}")
edges = []
collectors = rng.sample(sorted(members), 70)
for mc in collectors:
    for d in rng.sample(districts, rng.randint(1, 4)):
        edges.append(("covers", members[mc], areas[d]))
left = ["M-0417", "M-0422", "M-0431"]          # collectors who have left: their codes are on old reports only
seq = {}
for year in range(2015, 2027):
    for _ in range(rng.randint(480, 640)):
        d = date(year, 4, 15) + timedelta(days=rng.randint(0, 110))
        seq[year] = seq.get(year, 0) + 1
        r = rng.random()
        status = "collected" if r < 0.78 else ("unfounded" if r < 0.95 else "open")
        who = None if status == "open" else (rng.choice(left) if year < 2021 and rng.random() < 0.04 else rng.choice(collectors))
        dist = rng.choice(districts)
        rep = node("report", f"SR-{year}-{seq[year]:04d}", dist, d.isoformat(), status, who)
        edges.append(("in_area", rep, areas[dist]))
        if year == 2026 and status == "collected" and who in members:
            edges.append(("collected_by", rep, members[who]))
rng.shuffle(edges)
conn.executemany("INSERT INTO edges (kind, src, dst) VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
shutil.copyfile(live, data / "practice.db")
