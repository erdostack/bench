"""Connections to the sewer graph. Everything (web app, jobs, scripts) connects through here."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "var" / "sewer.db"


def connect(path=DB):
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = None
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn
