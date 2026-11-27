"""Replay, on a database file, what a wrapper log says finished `ok` on one target.

    python3 _replay.py <db> <log> <target>

Plain SQL entries are executed statement by statement and committed; `-- apply <file>` entries (bin/apply)
have their logged change-file source loaded and run(conn) called. Prints one JSON line."""
import json
import sqlite3
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
import sqlgrade as sg  # noqa: E402

db, log, target = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
done, errors = 0, []
for h in sg.read_history(log):
    if h["target"] != target or h["status"] != "ok":
        continue
    conn = sqlite3.connect(db)
    try:
        text = h["sql"]
        if text.lstrip().startswith("-- apply"):
            mod = types.ModuleType("change")
            exec(compile(text.split("\n", 1)[1] if "\n" in text else "", "change", "exec"), mod.__dict__)
            mod.run(conn)
        else:
            cur = conn.cursor()
            for stmt in [s for s in text.split(";") if s.strip()]:
                cur.execute(stmt)
                if cur.description:
                    cur.fetchall()
        conn.commit()
        done += 1
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{type(exc).__name__}: {exc}"[:200])
    finally:
        conn.close()
print(json.dumps({"replayed": done, "errors": errors}))
