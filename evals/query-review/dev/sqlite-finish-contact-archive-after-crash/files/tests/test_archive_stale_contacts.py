import sqlite3
import unittest
from pathlib import Path

from jobs import archive_stale_contacts

SCHEMA = Path(__file__).resolve().parent.parent / "db" / "schema.sql"


class Archive(unittest.TestCase):
    def test_moves_only_stale(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA.read_text())
        conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "a"), (2, "b"), (3, "c")])
        conn.executemany("INSERT INTO contacts VALUES (?, ?, '2024-01-01', ?)", [
            (1, 2, "2024-02-01"), (1, 3, "2026-10-01"), (2, 1, "2024-03-01")])
        conn.commit()
        self.assertEqual(archive_stale_contacts.run(conn), 2)
        self.assertEqual(conn.execute("SELECT owner_id, contact_id FROM contacts").fetchall(), [(1, 3)])
        self.assertEqual(conn.execute("SELECT count(*) FROM contacts_archive").fetchone()[0], 2)


if __name__ == "__main__":
    unittest.main()
