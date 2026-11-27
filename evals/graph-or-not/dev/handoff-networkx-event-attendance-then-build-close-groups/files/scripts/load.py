"""data/attendance.csv -> var/seminar.db"""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    (ROOT / "var").mkdir(exist_ok=True)
    db = ROOT / "var" / "seminar.db"
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    with open(ROOT / "data" / "attendance.csv", newline="") as f:
        rows = [(r["person"], r["event"]) for r in csv.DictReader(f)]
    conn.executemany("INSERT OR IGNORE INTO person VALUES (?)", [(p,) for p, _ in rows])
    conn.executemany("INSERT OR IGNORE INTO event VALUES (?)", [(e,) for _, e in rows])
    conn.executemany("INSERT INTO attendance VALUES (?, ?)", rows)
    conn.commit()


if __name__ == "__main__":
    main()
