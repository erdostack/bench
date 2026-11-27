"""Write data/network.json: six main canals 40 to 70 gates long, laterals off them, farm offtakes at the
ends, a handful of ring canals that lead back upstream, and about 7% of gates closed."""
import json
import random
import sys
from pathlib import Path

work = Path(sys.argv[1])
rng = random.Random(90210)
nodes, channels, seq = [], [], [0]


def new(kind, prefix):
    seq[0] += 1
    name = f"{prefix}-{seq[0]:04d}"
    nodes.append({"id": name, "kind": kind})
    return name


def channel(a, b, open_=None, cap=None):
    channels.append({"from": a, "to": b, "open": (rng.random() > 0.07) if open_ is None else open_,
                     "capacity": cap or rng.choice([40, 60, 80, 120, 200, 400])})


mains = []
head = new("headworks", "HW")
for m in range(6):
    length = rng.randint(40, 70)
    prev, line = head, []
    for _ in range(length):
        g = new("gate", "MG")
        channel(prev, g, open_=True, cap=rng.choice([600, 900, 1200]))     # main-canal gates stay open in season
        line.append(g)
        prev = g
    mains.append(line)
laterals = []
for line in mains:
    for g in line:
        for _ in range(rng.choice([0, 1, 1, 2])):
            prev, lat = g, []
            for _ in range(rng.randint(2, 9)):
                j = new("gate", "LG")
                channel(prev, j)
                lat.append(j)
                prev = j
                for _ in range(rng.choice([0, 1, 2, 3])):
                    channel(j, new("offtake", "OT"))
            laterals.append(lat)
# ring canals: the tail of a lateral drains back into a main canal, some of them upstream of where it left
for lat in rng.sample(laterals, 40):
    line = rng.choice(mains)
    channel(lat[-1], rng.choice(line), open_=True)
# cross-connections between laterals (second routes)
for _ in range(160):
    a, b = rng.sample(laterals, 2)
    channel(rng.choice(a), rng.choice(b))
seen, unique = set(), []
for ch in channels:
    if (ch["from"], ch["to"]) not in seen and ch["from"] != ch["to"]:
        seen.add((ch["from"], ch["to"]))
        unique.append(ch)
out = work / "data" / "network.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"season": "2026-27", "nodes": nodes, "channels": unique}, indent=0))
