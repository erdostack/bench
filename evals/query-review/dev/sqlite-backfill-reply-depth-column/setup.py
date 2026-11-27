"""Build var/threadline.db: about 2,400 threads and 60,000 posts, replies nested up to ~30 deep, and a few
hundred threads merged into newer posts of other threads (a moved first post points at a higher id)."""
import random
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

work = Path(sys.argv[1])
db = work / "var" / "threadline.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
rng = random.Random(4417)
conn = sqlite3.connect(db)
conn.executescript((work / "db" / "schema.sql").read_text())
for m in sorted((work / "db" / "migrations").glob("*.sql")):
    conn.executescript(m.read_text())

N = 60000
parent, thread, created = {}, {}, {}
roots, open_threads = [], []
t0 = datetime(2024, 1, 1)
by_thread = {}
for pid in range(1, N + 1):
    created[pid] = t0 + timedelta(minutes=13 * pid)
    if not roots or rng.random() < 0.04:
        parent[pid] = None
        thread[pid] = pid
        roots.append(pid)
        by_thread[pid] = [pid]
        open_threads.append(pid)
        open_threads = open_threads[-60:]
    else:
        tid = rng.choice(open_threads)
        members = by_thread[tid]
        # replies favour recent posts of the thread, which makes long chains
        p = members[-1] if rng.random() < 0.45 else rng.choice(members[-12:])
        parent[pid] = p
        thread[pid] = tid
        members.append(pid)

# merges: a thread's first post is moved under a later post of another thread
def ancestors(p):
    while p is not None:
        yield p
        p = parent[p]

merged = 0
for r in rng.sample(roots[:-50], 420):
    later = [x for x in range(r + 1, N + 1) if thread[x] != thread[r]]
    target = rng.choice(later[: max(50, len(later) // 3)])
    if r in set(ancestors(target)):
        continue
    parent[r] = target
    old = thread[r]
    for x in by_thread.pop(old, []):
        thread[x] = thread[target]
    by_thread.setdefault(thread[target], [])
    merged += 1

live_threads = sorted(set(thread.values()))
conn.executemany("INSERT INTO threads VALUES (?, ?, ?, 0, ?)",
                 [(t, rng.choice(["general", "help", "meta", "show", "jobs"]), f"thread {t}",
                   created[t].strftime("%Y-%m-%d %H:%M:%S")) for t in live_threads])
conn.executemany("INSERT INTO posts (id, thread_id, parent_id, author, created_at, hidden, depth) VALUES (?, ?, ?, ?, ?, ?, NULL)",
                 [(p, thread[p], parent[p], f"user{rng.randint(1, 4000)}", created[p].strftime("%Y-%m-%d %H:%M:%S"),
                   1 if rng.random() < 0.01 else 0) for p in range(1, N + 1)])
conn.execute("ANALYZE")
conn.commit()
conn.close()
