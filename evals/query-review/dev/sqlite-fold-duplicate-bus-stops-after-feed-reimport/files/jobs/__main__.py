import importlib
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "var" / "transit.db"

if __name__ == "__main__":
    job = importlib.import_module(f"jobs.{sys.argv[1]}")
    conn = sqlite3.connect(DB)
    print(job.run(conn))
    conn.close()
