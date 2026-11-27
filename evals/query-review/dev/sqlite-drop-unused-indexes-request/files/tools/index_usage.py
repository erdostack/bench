"""Report indexes that no logged statement used.

Reads the statement log the service writes (var/statement_log.jsonl: one JSON object per statement
with "sql" and "params"), asks SQLite for each statement's plan, and lists the indexes of
var/registry.db that never appear in any plan. The service keeps the last 24 hours of the log."""
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    conn = sqlite3.connect(f"file:{ROOT / 'var' / 'registry.db'}?mode=ro", uri=True)
    indexes = sorted(r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'index' AND name NOT LIKE 'sqlite_autoindex%'"))
    used = set()
    for line in (ROOT / "var" / "statement_log.jsonl").read_text().splitlines():
        rec = json.loads(line)
        for row in conn.execute("EXPLAIN QUERY PLAN " + rec["sql"], rec.get("params", {})):
            m = re.search(r"USING (?:COVERING )?INDEX (\w+)", row[3])
            if m:
                used.add(m.group(1))
    print("never used: " + ", ".join(i for i in indexes if i not in used))


if __name__ == "__main__":
    main()
