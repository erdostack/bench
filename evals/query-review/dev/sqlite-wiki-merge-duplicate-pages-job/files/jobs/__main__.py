"""python -m jobs <name> [db]: run jobs/<name>.py's run(conn) against the database (default var/quarry.db)."""
import importlib
import sqlite3
import sys

name = sys.argv[1]
db = sys.argv[2] if len(sys.argv) > 2 else "var/quarry.db"
conn = sqlite3.connect(db)
print(importlib.import_module(f"jobs.{name}").run(conn))
conn.close()
