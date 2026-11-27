"""python -m jobs <name>"""
import importlib
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "var/rota.db"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    conn = sqlite3.connect(DB, timeout=5)
    try:
        print(importlib.import_module(f"jobs.{sys.argv[1]}").run(conn))
    finally:
        conn.close()
