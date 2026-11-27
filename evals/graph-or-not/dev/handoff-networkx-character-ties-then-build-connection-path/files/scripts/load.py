"""Build var/companion.db from data/*.csv."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    (ROOT / "var").mkdir(exist_ok=True)
    db = ROOT / "var" / "companion.db"
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    with open(ROOT / "data" / "characters.csv", newline="") as f:
        conn.executemany("INSERT INTO character VALUES (?, ?)", [(r["id"], r["name"]) for r in csv.DictReader(f)])
    with open(ROOT / "data" / "ties.csv", newline="") as f:
        conn.executemany("INSERT INTO tie VALUES (?, ?, ?)",
                         [(r["char_a"], r["char_b"], int(r["weight"])) for r in csv.DictReader(f)])
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
