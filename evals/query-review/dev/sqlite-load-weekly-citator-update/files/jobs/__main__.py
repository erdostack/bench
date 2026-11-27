"""python -m jobs <name> [args...]   (runs jobs.<name>.run(conn, *args) against var/citator.db)"""
import importlib
import os
import sqlite3
import sys
from pathlib import Path

DB = os.environ.get("CITATOR_DB") or Path(__file__).resolve().parent.parent / "var/citator.db"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    conn = sqlite3.connect(DB, timeout=5)
    try:
        print(importlib.import_module(f"jobs.{sys.argv[1]}").run(conn, *sys.argv[2:]))
    finally:
        conn.close()
