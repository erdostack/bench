"""python -m jobs <name> <database>"""
import importlib
import sqlite3
import sys

name, path = sys.argv[1], sys.argv[2]
conn = sqlite3.connect(path)
print(importlib.import_module(f"jobs.{name}").run(conn))
conn.close()
