"""Run a file from sql/ with named parameters (psycopg in production, sqlite3 in tests)."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def rows(conn, name: str, **params):
    cur = conn.cursor()
    cur.execute((SQL / name).read_text(encoding="utf-8"), params)
    return cur.fetchall()
