"""Build var/club.db from the karate club network bundled with networkx."""
import sqlite3
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]


def main():
    (ROOT / "var").mkdir(exist_ok=True)
    db = ROOT / "var" / "club.db"
    if db.exists():
        db.unlink()
    g = nx.karate_club_graph()
    conn = sqlite3.connect(db)
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    conn.executemany("INSERT INTO member VALUES (?, ?)", [(n, g.nodes[n]["club"]) for n in sorted(g)])
    rows = [(a, b, k) for a, b, d in g.edges(data=True) for k in range(1, d["weight"] + 1)]
    conn.executemany("INSERT INTO encounter VALUES (?, ?, ?)", rows)
    conn.commit()


if __name__ == "__main__":
    main()
