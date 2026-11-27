"""Build data/library.db (live) and data/scratch.db: last night's rebuild of library plus two test imports
made on scratch since: IMP-TEST-1114 (Priya's, 140 tracks) and IMP-TEST-1121 (920 tracks, 35 new artists, 60
new releases). Library also got a real import IMP-1121 the same day (that is in both files)."""
import random
import shutil
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
data = work / "data"
data.mkdir(parents=True, exist_ok=True)
for n in ("library.db", "scratch.db"):
    if (data / n).exists():
        (data / n).unlink()
rng = random.Random(1121)
conn = sqlite3.connect(data / "library.db")
conn.executescript((work / "db" / "schema.sql").read_text())
nodes, edges = [], []
nodes += [(1 + i, "rotation", f"ROT-{c}", f"{c}-list", None) for i, c in enumerate("ABCR")]
artists = list(range(100, 1300))
nodes += [(a, "artist", f"AR-{a}", f"Artist {a}", rng.choice([None, "IMP-0612", "IMP-0901"])) for a in artists]
releases = list(range(2000, 4500))
nodes += [(r, "release", f"RE-{r}", f"Release {r}", rng.choice([None, "IMP-0612", "IMP-0901"])) for r in releases]
nid = [10000]


def track(batch, arts, rels, out_nodes, out_edges):
    nid[0] += 1
    t = nid[0]
    out_nodes.append((t, "track", f"TR-{t}", f"Track {t}", batch))
    out_edges.append(("by_artist", t, rng.choice(arts)))
    out_edges.append(("on_release", t, rng.choice(rels)))
    if rng.random() < 0.3:
        out_edges.append(("in_rotation", t, rng.randint(1, 4)))


for _ in range(9000):
    track(rng.choice([None, "IMP-0612", "IMP-0901"]), artists, releases, nodes, edges)
for _ in range(600):
    track("IMP-1121", artists, releases, nodes, edges)
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?)", nodes)
conn.executemany("INSERT INTO edges (kind, src, dst) VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
shutil.copyfile(data / "library.db", data / "scratch.db")
conn = sqlite3.connect(data / "scratch.db")
sn, se = [], []
for _ in range(140):
    track("IMP-TEST-1114", artists, releases, sn, se)
new_art = list(range(1300, 1335))
new_rel = list(range(4500, 4560))
sn += [(a, "artist", f"AR-{a}", f"Artist {a}", "IMP-TEST-1121") for a in new_art]
sn += [(r, "release", f"RE-{r}", f"Release {r}", "IMP-TEST-1121") for r in new_rel]
for _ in range(920):
    track("IMP-TEST-1121", artists + new_art, releases + new_rel, sn, se)
conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?)", sn)
conn.executemany("INSERT INTO edges (kind, src, dst) VALUES (?, ?, ?)", se)
conn.commit()
conn.close()
