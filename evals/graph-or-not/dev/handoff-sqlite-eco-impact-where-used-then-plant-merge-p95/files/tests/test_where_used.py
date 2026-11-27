import sqlite3
from pathlib import Path

from ecoboard.impact import where_used

SCHEMA = Path(__file__).resolve().parents[1] / "db" / "schema.sql"


def db():
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA.read_text())
    conn.executemany("INSERT INTO item VALUES (?, ?, ?, 'LIN')", [(i, f"P{i}", f"part {i}") for i in range(1, 6)])
    conn.executemany("INSERT INTO bom_line VALUES (?, ?, 1)", [(2, 1), (3, 2), (4, 3), (2, 4), (5, 1)])
    return conn


def test_loop_terminates_and_lists_each_assembly_once():
    rows = where_used(db(), 1)
    assert sorted(r[0] for r in rows) == [2, 3, 4, 5]
