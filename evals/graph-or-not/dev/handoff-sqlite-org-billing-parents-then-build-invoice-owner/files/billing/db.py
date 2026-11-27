import sqlite3


def connect(path="var/billing.db"):
    return sqlite3.connect(path)
