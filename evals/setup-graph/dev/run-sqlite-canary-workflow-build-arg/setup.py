"""Builds data/hedgerow.db from sql/schema.sql and the CSVs, as scripts/load.sh does."""
import csv
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
db = work / "data" / "hedgerow.db"
if db.exists():
    db.unlink()
con = sqlite3.connect(db)
con.executescript((work / "sql" / "schema.sql").read_text())
for table, width in (("patch", 3), ("link", 4)):
    rows = list(csv.reader(open(work / "data" / f"{table}.csv", newline="")))[1:]
    con.executemany(f"INSERT INTO {table} VALUES ({', '.join('?' * width)})", rows)
con.commit()
con.close()
