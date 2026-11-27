"""Loads queries/<name>.sql and runs it with named parameters."""
from pathlib import Path

QUERIES = Path(__file__).resolve().parent.parent / "queries"


def run(conn, name, **params):
    return conn.execute((QUERIES / f"{name}.sql").read_text(encoding="utf-8"), params).fetchall()
