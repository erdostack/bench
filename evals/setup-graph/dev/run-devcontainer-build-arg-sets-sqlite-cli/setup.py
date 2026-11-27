"""Builds data/stemma.db from sql/schema.sql and the CSVs in data/, as scripts/load.sh does with the sqlite3 shell (no
foreign-key pragma, so rows that point at missing parents load without complaint)."""
import csv
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
db = work / "data/stemma.db"
if db.exists():
    db.unlink()
con = sqlite3.connect(db)
con.executescript((work / "sql/schema.sql").read_text())
rows = list(csv.reader(open(work / "data" / "witness.csv", newline="")))[1:]
con.executemany("INSERT INTO witness VALUES (?, ?, ?, ?)", rows)
rows = list(csv.reader(open(work / "data" / "copied_from.csv", newline="")))[1:]
con.executemany("INSERT INTO copied_from VALUES (?, ?)", rows)
con.commit()
con.close()
