"""Build var/sample.db: a small synthetic register (20,000 entities, about 60,000 relations) for tests."""
import random
import sqlite3
import sys
from pathlib import Path

KINDS = ["director_of", "shareholder_of", "registered_at", "lives_at", "awarded_to", "official_of", "owns"]


def main(path="var/sample.db", n=20_000, seed=7):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    conn = sqlite3.connect(path)
    conn.executescript(Path(__file__).resolve().parents[1].joinpath("db", "schema.sql").read_text())
    kinds = ["company", "person", "public_body", "address"]
    conn.executemany("INSERT INTO entity VALUES (?, ?, ?, ?)",
                     [(i, rng.choice(kinds), f"Entity {i}", None) for i in range(1, n + 1)])
    conn.executemany("INSERT INTO relation VALUES (?, ?, ?, NULL, NULL)",
                     [(rng.randint(1, n), rng.randint(1, n), rng.choice(KINDS)) for _ in range(3 * n)])
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main(*sys.argv[1:2])
