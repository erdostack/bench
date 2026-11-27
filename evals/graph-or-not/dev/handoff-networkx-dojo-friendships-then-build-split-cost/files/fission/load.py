import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    (ROOT / "var").mkdir(exist_ok=True)
    conn = sqlite3.connect(ROOT / "var" / "club.db")
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    with open(ROOT / "data" / "members.csv") as f:
        conn.executemany("INSERT INTO member VALUES (?, ?)", [(int(r["id"]), r["faction"]) for r in csv.DictReader(f)])
    with open(ROOT / "data" / "ties.csv") as f:
        conn.executemany("INSERT INTO tie VALUES (?, ?, ?)",
                         [(int(r["a"]), int(r["b"]), int(r["contexts"])) for r in csv.DictReader(f)])
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
