"""python -m jobs <name> [db] [args...]: run jobs/<name>.py's run(conn, *args) (default db var/schoolrun.db)."""
import importlib
import sqlite3
import sys

name = sys.argv[1]
db = sys.argv[2] if len(sys.argv) > 2 else "var/schoolrun.db"
conn = sqlite3.connect(db)
print(importlib.import_module(f"jobs.{name}").run(conn, *sys.argv[3:]))
conn.close()
