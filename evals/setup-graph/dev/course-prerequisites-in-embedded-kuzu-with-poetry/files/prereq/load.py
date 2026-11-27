"""Rebuild db/courses from data/*.csv (the timetabling export)."""
import shutil
from pathlib import Path

from prereq.db import DB_DIR, connect

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    shutil.rmtree(DB_DIR, ignore_errors=True)
    DB_DIR.parent.mkdir(exist_ok=True)
    conn = connect(read_only=False)
    for statement in (ROOT / "schema" / "schema.cypher").read_text().split(";"):
        if statement.strip():
            conn.execute(statement)
    conn.execute(f"COPY Course FROM '{ROOT / 'data' / 'courses.csv'}' (header=true)")
    conn.execute(f"COPY REQUIRES FROM '{ROOT / 'data' / 'requires.csv'}' (header=true)")


if __name__ == "__main__":
    main()
