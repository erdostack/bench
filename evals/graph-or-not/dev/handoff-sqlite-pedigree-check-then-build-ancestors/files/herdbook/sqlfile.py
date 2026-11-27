"""Load a query from sql/ and run it with named parameters."""
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def run(conn, name: str, **params):
    text = (SQL_DIR / f"{name}.sql").read_text(encoding="utf-8")
    cur = conn.cursor()
    cur.execute(text, params)
    return cur.fetchall()
