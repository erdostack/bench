import importlib
import sqlite3
import sys

if len(sys.argv) < 3:
    sys.exit("usage: python3 -m jobs <name> <db> [args...]")
mod = importlib.import_module(f"jobs.{sys.argv[1]}")
print(mod.run(sqlite3.connect(sys.argv[2]), *sys.argv[3:]))
