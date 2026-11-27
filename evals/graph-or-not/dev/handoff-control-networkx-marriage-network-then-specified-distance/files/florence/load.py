"""Build var/florence.db from the network bundled with networkx."""
import sqlite3
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]


def main():
    (ROOT / "var").mkdir(exist_ok=True)
    db = ROOT / "var" / "florence.db"
    if db.exists():
        db.unlink()
    g = nx.florentine_families_graph()
    conn = sqlite3.connect(db)
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    conn.executemany("INSERT INTO family VALUES (?)", [(f,) for f in sorted(g)] + [("Pucci",)])
    conn.executemany("INSERT INTO marriage VALUES (?, ?)", [tuple(sorted(e)) for e in g.edges()])
    conn.commit()


if __name__ == "__main__":
    main()
