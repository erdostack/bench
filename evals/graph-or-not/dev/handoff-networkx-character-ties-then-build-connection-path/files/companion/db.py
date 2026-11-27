import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "var" / "companion.db"


def connect(path=DB):
    return sqlite3.connect(path)
