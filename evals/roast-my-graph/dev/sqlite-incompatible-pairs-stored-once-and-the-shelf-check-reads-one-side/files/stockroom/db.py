"""The one place a connection is opened."""
import sqlite3


def connect(path="stockroom.db"):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con
