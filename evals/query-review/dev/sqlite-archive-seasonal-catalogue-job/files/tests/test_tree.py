import sqlite3
import unittest
from pathlib import Path

from catalog.tree import breadcrumbs, subtree_ids

SCHEMA = (Path(__file__).resolve().parent.parent / "db" / "schema.sql").read_text()


def small():
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO categories (id, parent_id, name) VALUES (?, ?, ?)",
                     [(1, None, "All"), (2, 1, "Garden"), (3, 2, "Tools"), (4, 2, "Seeds"), (5, 1, "Kitchen")])
    return conn


class Tree(unittest.TestCase):
    def test_subtree(self):
        self.assertEqual(subtree_ids(small(), 2), [2, 3, 4])

    def test_breadcrumbs(self):
        self.assertEqual(breadcrumbs(small(), 3), ["All", "Garden", "Tools"])


if __name__ == "__main__":
    unittest.main()
