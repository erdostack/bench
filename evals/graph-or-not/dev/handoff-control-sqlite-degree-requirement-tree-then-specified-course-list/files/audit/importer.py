"""Rebuild var/audit.db from the programme catalogue (JSON). Refuses catalogues whose nesting is not a tree."""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NotATree(ValueError):
    pass


def check_tree(requirements):
    parent = {r["id"]: r.get("parent_id") for r in requirements}
    for start in parent:
        seen, node = set(), start
        while node is not None:
            if node in seen:
                raise NotATree(f"requirement {start} is nested inside itself")
            seen.add(node)
            node = parent.get(node)


def main(catalogue_path):
    data = json.loads(Path(catalogue_path).read_text())
    check_tree(data["requirements"])
    (ROOT / "var").mkdir(exist_ok=True)
    db = ROOT / "var" / "audit.db"
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    conn.executescript((ROOT / "db" / "schema.sql").read_text())
    conn.executemany("INSERT INTO requirement VALUES (:id, :parent_id, :title)", data["requirements"])
    conn.executemany("INSERT INTO requirement_course VALUES (:requirement_id, :course_code)", data["listings"])
    conn.commit()


if __name__ == "__main__":
    main(sys.argv[1])
