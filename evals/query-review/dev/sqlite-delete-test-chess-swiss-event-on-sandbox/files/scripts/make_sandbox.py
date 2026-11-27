#!/usr/bin/env python3
"""Build data/sandbox.sqlite from scratch: 2,000 generated players, 30 congresses with entries and pairings,
and whatever the pairing engine's load tests last left (TST- events). Deterministic; safe to run any time."""
import random
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def build(db: Path, seed: int = 1123) -> None:
    db.parent.mkdir(parents=True, exist_ok=True)
    if db.exists():
        db.unlink()
    rng = random.Random(seed)
    conn = sqlite3.connect(db)
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    players = list(range(1, 2001))
    nodes = [(p, "player", f"P{p:05d}", None, "active") for p in players]
    events = [(2000 + i, f"E-26{i:02d}", "closed") for i in range(1, 31)]
    events += [(2101, "TST-SWISS-1122", "closed"), (2102, "TST-SWISS-1123", "open"), (2103, "SWISS-1123", "open")]
    nodes += [(e, "event", code, None, st) for e, code, st in events]
    conn.executemany("INSERT INTO nodes VALUES (?, ?, ?, ?, ?)", nodes)
    edges = []
    for e, code, _st in events:
        size = 420 if code.startswith("TST-") else rng.randint(40, 120)
        field = rng.sample(players, size)
        edges += [("entered", p, e, None, None, None) for p in field]
        rounds = 12 if code.startswith("TST-") else rng.randint(5, 7)
        for rd in range(1, rounds + 1):
            rng.shuffle(field)
            for i in range(0, size - 1, 2):
                edges.append(("paired", field[i], field[i + 1], e, rd, rng.choice(["1-0", "0-1", "1/2-1/2"])))
    rng.shuffle(edges)
    conn.executemany("INSERT INTO edges (kind, src, dst, event, round, result) VALUES (?, ?, ?, ?, ?, ?)", edges)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "sandbox.sqlite")
    print("sandbox rebuilt")
