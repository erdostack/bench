"""Traversals over the prerequisite tables."""
from pathlib import Path

from .db import connect

SQL = Path(__file__).resolve().parent.parent / "sql"


def still_needed(target: str, passed: set[str]) -> list[str]:
    query = (SQL / "all_prereqs.sql").read_text().replace("'MATH-340'", "%s")
    with connect() as conn:
        rows = conn.execute(query, (target,)).fetchall()
    return [code for code, _title, _steps in rows if code not in passed]
