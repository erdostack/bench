#!/usr/bin/env python3
"""wsql: run SQL on a waternet target. Every call is logged to .wsql_history before it runs."""
import argparse
import json
import os
import sqlite3
import sys
import time
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONF = tomllib.loads((ROOT / "config" / "wsql.toml").read_text())
ap = argparse.ArgumentParser(prog="wsql")
ap.add_argument("sql", nargs="?")
ap.add_argument("--target", default=CONF["default_target"], choices=sorted(CONF["targets"]))
ap.add_argument("--file")
a = ap.parse_args()
text = Path(a.file).read_text() if a.file else (a.sql or "")
key = f"{os.getpid()}-{time.time_ns()}"
with open(ROOT / ".wsql_history", "a") as log:
    log.write(json.dumps({"event": "start", "id": key, "target": a.target, "file": a.file, "sql": text}) + "\n")
status = "error"
try:
    path = Path(CONF["targets"][a.target]["path"])
    path = path if path.is_absolute() else ROOT / path
    conn = sqlite3.connect(f"file:{path}?mode=rw", uri=True)
    cur = conn.cursor()
    cur.executescript(text) if a.file else cur.execute(text)
    if cur.description:
        for row in cur.fetchall():
            print("|".join("" if v is None else str(v) for v in row))
    elif not a.file:
        print(f"{cur.rowcount} rows")
    conn.commit()
    conn.close()
    status = "ok"
except sqlite3.Error as exc:
    sys.exit(f"wsql: {exc}")
finally:
    with open(ROOT / ".wsql_history", "a") as log:
        log.write(json.dumps({"event": "end", "id": key, "status": status}) + "\n")
