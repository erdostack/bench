#!/usr/bin/env python3
"""vq: run SQL or apply a change file on a valvebook target. Every call is logged to .vq_history first."""
import argparse
import importlib.util
import json
import os
import sqlite3
import sys
import time
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONF = tomllib.loads((ROOT / "config" / "vq.toml").read_text())
ap = argparse.ArgumentParser(prog="vq")
ap.add_argument("sql", nargs="?")
ap.add_argument("--target", default=CONF["default_target"], choices=sorted(CONF["targets"]))
ap.add_argument("--file")
ap.add_argument("--apply")
a = ap.parse_args()
if a.apply:
    text = f"-- apply {a.apply}\n" + Path(a.apply).read_text()
else:
    text = Path(a.file).read_text() if a.file else (a.sql or "")
key = f"{os.getpid()}-{time.time_ns()}"
with open(ROOT / ".vq_history", "a") as log:
    log.write(json.dumps({"event": "start", "id": key, "target": a.target, "sql": text}) + "\n")
status = "error"
try:
    path = Path(CONF["targets"][a.target]["path"])
    path = path if path.is_absolute() else ROOT / path
    conn = sqlite3.connect(f"file:{path}?mode=rw", uri=True)
    if a.apply:
        spec = importlib.util.spec_from_file_location("change", a.apply)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print(mod.run(conn))
    else:
        cur = conn.cursor()
        for stmt in [s for s in text.split(";") if s.strip()]:
            cur.execute(stmt)
            if cur.description:
                for row in cur.fetchall():
                    print("|".join("" if v is None else str(v) for v in row))
            else:
                print(f"{cur.rowcount} rows")
        conn.commit()
    conn.close()
    status = "ok"
except sqlite3.Error as exc:
    sys.exit(f"vq: {exc}")
finally:
    with open(ROOT / ".vq_history", "a") as log:
        log.write(json.dumps({"event": "end", "id": key, "status": status}) + "\n")
