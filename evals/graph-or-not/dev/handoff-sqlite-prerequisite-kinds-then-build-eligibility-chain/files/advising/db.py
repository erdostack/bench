"""Run a file from sql/ with named parameters."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL = ROOT / "sql"


def connect():
    return sqlite3.connect(ROOT / "var" / "catalogue.db")


def rows(conn, name: str, **params):
    return conn.execute((SQL / name).read_text(encoding="utf-8"), params).fetchall()
