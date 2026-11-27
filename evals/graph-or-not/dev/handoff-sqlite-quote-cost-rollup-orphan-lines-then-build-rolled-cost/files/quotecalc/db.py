import sqlite3

DB = "var/quotes.db"


def connect(path=DB):
    return sqlite3.connect(path)
