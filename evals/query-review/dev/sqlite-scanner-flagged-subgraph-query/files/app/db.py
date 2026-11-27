"""Connection helper."""
import sqlite3
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "var" / "links.db"


def connect(path=DEFAULT_PATH):
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    return conn
