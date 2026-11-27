"""Rebuild var/catalogue.db from the registrar's term export (CSV files in a directory)."""
import csv
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(export_dir):
    export = Path(export_dir)
    (ROOT / "var").mkdir(exist_ok=True)
    db = ROOT / "var" / "catalogue.db"
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    with open(export / "courses.csv", newline="") as f:
        conn.executemany("INSERT INTO course VALUES (:id, :code, :title, :level)", csv.DictReader(f))
    with open(export / "prerequisites.csv", newline="") as f:
        conn.executemany("INSERT INTO prerequisite VALUES (:course_id, :requires_id, :kind)", csv.DictReader(f))
    conn.commit()


if __name__ == "__main__":
    main(sys.argv[1])
