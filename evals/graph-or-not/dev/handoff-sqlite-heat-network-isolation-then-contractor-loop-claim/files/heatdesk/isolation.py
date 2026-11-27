"""Isolation screen: which buildings lose heat if a pipe is isolated."""
import sqlite3
from pathlib import Path

DB = "var/heatnet.db"
QUERY = (Path(__file__).resolve().parents[1] / "sql" / "isolate.sql").read_text(encoding="utf-8")


def buildings_off(conn, pipe_id):
    return [building for _, building in conn.execute(QUERY, {"pipe_id": pipe_id})]


if __name__ == "__main__":
    import sys
    with sqlite3.connect(DB) as conn:
        for b in buildings_off(conn, int(sys.argv[1])):
            print(b)
