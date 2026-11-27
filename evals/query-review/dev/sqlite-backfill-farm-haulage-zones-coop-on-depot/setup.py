"""Build data/depot.sqlite and data/shadow.sqlite (last night's copy, identical): 9,000 farms, 6 stores,
6 haulage zones, member_of edges, and the September pilot's in_zone edges for districts LN4 and LN5."""
import random
import shutil
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
live = data / "depot.sqlite"
for p in (live, data / "shadow.sqlite"):
    if p.exists():
        p.unlink()
rng = random.Random(40817)
conn = sqlite3.connect(live)
conn.executescript((work / "db" / "schema.sql").read_text())
ZONES = {"HZ-01": ["LN1", "LN2", "LN3"], "HZ-02": ["LN4", "LN5"], "HZ-03": ["LN6", "LN7", "LN8"],
         "HZ-04": ["NG31", "NG32", "NG33", "NG34"], "HZ-05": ["DN21", "DN22"], "HZ-06": ["LN9", "LN10", "LN11"]}
OUTSIDE = ["PE10", "PE11", "PE12", "PE20"]
STORES = ["GS-ASH", "GS-BRG", "GS-CAY", "GS-FEN", "GS-SLE", "GS-WOL"]
nid = 0
nodes = []
for code in STORES:
    nid += 1
    nodes.append((nid, "store", code, code.replace("GS-", "Store "), None, "closed" if code == "GS-WOL" else "open"))
store_ids = {n[2]: n[0] for n in nodes}
zone_ids = {}
for code in ZONES:
    nid += 1
    nodes.append((nid, "zone", code, "Zone " + code[-2:], None, None))
    zone_ids[code] = nid
districts = [d for ds in ZONES.values() for d in ds]
farms = []
for i in range(9000):
    nid += 1
    d = rng.choice(districts + districts + OUTSIDE)
    pc = f"{d} {rng.randint(1, 9)}{rng.choice('ABDEFGHJLNPQRSTUWXYZ')}{rng.choice('ABDEFGHJLNPQRSTUWXYZ')}"
    farms.append((nid, "farm", f"F-{100000 + i * 7:06d}", f"Farm {i}", pc, rng.choice(["active"] * 9 + ["left"])))
nodes += farms
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)", nodes)
conn.executemany("INSERT INTO zone_districts VALUES (?, ?)", [(d, z) for z, ds in ZONES.items() for d in ds])
edges = []
open_stores = [s for s in STORES if s != "GS-WOL"]
for f in farms:
    edges.append(("member_of", f[0], store_ids[rng.choice(open_stores)], f"20{rng.randint(10, 26):02d}-0{rng.randint(1, 9)}-01"))
pilot = [f for f in farms if f[4].split(" ")[0] in ("LN4", "LN5")]
for f in pilot:
    edges.append(("in_zone", f[0], zone_ids["HZ-02"], None))
rng.shuffle(edges)
conn.executemany("INSERT INTO edges (kind, src, dst, since) VALUES (?, ?, ?, ?)", edges)
conn.commit()
conn.close()
shutil.copyfile(live, data / "shadow.sqlite")
