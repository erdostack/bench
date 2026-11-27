"""Build var/registry.db: a dependency graph with one package almost everything depends on, and
some dependency cycles (dev and peer dependencies pointing back up)."""
import random
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
db = work / "var" / "registry.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
rng = random.Random(60221)
conn = sqlite3.connect(db)
conn.executescript((work / "schema.sql").read_text())

N = 15000
words = ["core", "http", "auth", "cache", "queue", "store", "log", "cli", "ui", "geo", "pay", "mail", "sync", "form", "test"]
conn.executemany("INSERT INTO packages VALUES (?, ?, ?, ?)",
                 [(i, "platform-base" if i == 1 else f"{rng.choice(words)}-{rng.choice(words)}-{i}",
                   f"{rng.randint(0, 9)}.{rng.randint(0, 30)}.{rng.randint(0, 40)}",
                   f"202{rng.randint(3, 6)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}") for i in range(1, N + 1)])
edges = {}
for i in range(2, N + 1):                              # ordinary dependencies point at older packages
    for _ in range(rng.randint(1, 5)):
        dep = rng.randint(max(1, i - 2500), i - 1) if i > 2 else 1
        if dep != 1:
            edges[(i, dep)] = rng.choice(["runtime", "runtime", "runtime", "dev"])
for i in rng.sample(range(2, N + 1), 5200):            # platform-base: about a third of the registry uses it
    edges[(i, 1)] = "runtime"
dependents_of_base = [i for (i, dep) in edges if dep == 1]
for i in rng.sample(dependents_of_base, 180):          # ...and it dev-depends on tooling that itself uses it
    edges[(1, i)] = "dev"
for _ in range(400):                                   # peer dependencies between plugin and host
    a, b = rng.sample(range(2, N + 1), 2)
    edges.setdefault((a, b), "peer")
    edges.setdefault((b, a), "peer")
for leaf in range(N - 99, N + 1):                      # the newest hundred packages: nobody depends on them yet
    for key in [k for k in edges if k[1] == leaf]:
        del edges[key]
conn.executemany("INSERT INTO depends_on VALUES (?, ?, ?)", [(a, b, k) for (a, b), k in sorted(edges.items())])
conn.execute("ANALYZE")
conn.commit()
conn.close()
