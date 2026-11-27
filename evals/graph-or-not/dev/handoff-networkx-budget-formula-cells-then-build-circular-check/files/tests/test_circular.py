import sqlite3
from pathlib import Path

from sheets.circular import circular_cells

SCHEMA = (Path(__file__).resolve().parents[1] / "db" / "schema.sql").read_text()


def test_two_cells_that_read_each_other_are_flagged():
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO cell VALUES (?, ?, ?, ?)",
                     [(1, "Costs", "A1", "=A2"), (2, "Costs", "A2", "=A1"), (3, "Costs", "A3", "=A1")])
    conn.executemany("INSERT INTO reference VALUES (?, ?)", [(1, 2), (2, 1), (3, 1)])
    assert circular_cells(conn) == ["Costs!A1", "Costs!A2"]
