from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def load(name):
    return (SQL / f"{name}.sql").read_text(encoding="utf-8")


def rows(conn, name, **params):
    return conn.execute(load(name), params).fetchall()
