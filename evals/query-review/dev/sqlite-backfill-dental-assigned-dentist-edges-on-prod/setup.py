"""Build data/prod.db and data/scratch.db (identical: scratch is restored from prod): 6 practices, 40 dentists,
about 12,000 patients. The Westmoor import left about 1,900 active patients without an assigned dentist;
archived and deceased patients (about 2,500) have none, as docs/assignments.md says."""
import random
import shutil
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
prod = data / "prod.db"
for p in (prod, data / "scratch.db"):
    if p.exists():
        p.unlink()
rng = random.Random(77024)
conn = sqlite3.connect(prod)
conn.executescript((work / "db" / "schema.sql").read_text())
nid = 0
edges = []


def node(kind, code, name=None, status=None):
    global nid
    nid += 1
    conn.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?)", (nid, kind, code, name, status))
    return nid


names = ["Fernside", "Westmoor", "Kirkby Lane", "Old Mill", "Riverside", "Hatton Cross"]
practices = [node("practice", f"FP-{i + 1:02d}", n) for i, n in enumerate(names)]
dentists = [node("dentist", f"DN-{i + 1:03d}", f"Dentist {i + 1}") for i in range(40)]
staff = {p: [] for p in practices}
for d in dentists:
    for p in rng.sample(practices, rng.choice([1, 1, 2])):
        edges.append(("works_at", d, p))
        staff[p].append(d)
for p in practices:
    if not staff[p]:
        staff[p].append(dentists[0])
        edges.append(("works_at", dentists[0], p))
    edges.append(("lead_dentist", p, staff[p][0]))
westmoor = practices[1]
for i in range(12000):
    home = rng.choices(practices, [30, 26, 14, 12, 10, 8])[0]
    status = rng.choices(["active", "archived", "deceased"], [80, 17, 3])[0]
    pt = node("patient", f"PT-{700000 + i}", f"Patient {i + 1}", status)
    edges.append(("registered_at", pt, home))
    if status != "active":
        continue                                   # archived and deceased patients have no assigned dentist
    if home == westmoor and rng.random() < 0.72:
        continue                                   # lost in the Westmoor import
    if rng.random() < 0.012:
        continue                                   # a few elsewhere too
    edges.append(("assigned_to", pt, rng.choice(staff[home])))
rng.shuffle(edges)
conn.executemany("INSERT INTO edges (kind, src, dst) VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
shutil.copyfile(prod, data / "scratch.db")
