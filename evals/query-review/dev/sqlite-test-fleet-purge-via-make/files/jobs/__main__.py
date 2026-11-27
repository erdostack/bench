"""python3 -m jobs <name> <database>"""
import importlib
import sqlite3
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    conn = sqlite3.connect(sys.argv[2], timeout=5)
    try:
        print(importlib.import_module(f"jobs.{sys.argv[1]}").run(conn))
    finally:
        conn.close()
