"""Run a file from sql/ with named parameters, on Postgres (psycopg) or SQLite."""
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parents[1] / "sql"


def load(name: str) -> str:
    return (SQL_DIR / name).read_text(encoding="utf-8")


def fetch_all(conn, name: str, **params):
    cur = conn.cursor()
    cur.execute(load(name), params)
    return cur.fetchall()
