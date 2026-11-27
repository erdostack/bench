"""python -m jobs <name> [database]"""
import importlib
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "var/payrail.db"

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    conn = sqlite3.connect(sys.argv[2] if len(sys.argv) == 3 else DB, timeout=5)
    try:
        print(importlib.import_module(f"jobs.{sys.argv[1]}").run(conn))
    finally:
        conn.close()
