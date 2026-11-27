import sqlite3
import unittest
from pathlib import Path

from app.check import is_inside
from app.nesting import WouldLoop, add_nesting
from jobs import refresh_reach

SCHEMA = (Path(__file__).resolve().parent.parent / "db" / "schema.sql").read_text()


def tiny():
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO groups VALUES (?, ?, '2026-01-01T00:00:00Z')", [(i, f"g{i}") for i in range(1, 6)])
    conn.execute("INSERT INTO job_state VALUES ('reach_refreshed_at', '2026-01-01T00:00:00Z')")
    conn.executemany("INSERT INTO group_edges VALUES (?, ?, '2026-01-01T00:00:00Z')", [(1, 2), (2, 3), (1, 4)])
    conn.commit()
    return conn


class RefreshReachTest(unittest.TestCase):
    def test_rebuild(self):
        conn = tiny()
        self.assertEqual(refresh_reach.run(conn), 4)
        self.assertTrue(is_inside(conn, 3, 1))
        self.assertFalse(is_inside(conn, 4, 2))

    def test_loop_refused(self):
        conn = tiny()
        with self.assertRaises(WouldLoop):
            add_nesting(conn, 3, 1)


if __name__ == "__main__":
    unittest.main()
