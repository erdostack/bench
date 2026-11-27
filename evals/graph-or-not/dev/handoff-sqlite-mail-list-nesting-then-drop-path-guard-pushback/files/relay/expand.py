"""Expands a list address into mailboxes at delivery time."""
import sqlite3
from pathlib import Path

EXPAND = (Path(__file__).resolve().parent.parent / "sql" / "expand.sql").read_text()


def recipients(conn: sqlite3.Connection, list_id: int) -> list[str]:
    return sorted(r[0] for r in conn.execute(EXPAND, {"list_id": list_id}))
