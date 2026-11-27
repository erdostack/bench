"""Repair the rows importer 2.3 wrote as (b, a): add each one's orders to the a < b row (creating it if missing)."""

CHUNK = 500


def run(conn):
    fixed = 0
    while True:
        with conn:
            rows = conn.execute("SELECT a, b, orders FROM also_bought WHERE a > b LIMIT ?", (CHUNK,)).fetchall()
            if not rows:
                return fixed
            conn.executemany("""INSERT INTO also_bought (a, b, orders) VALUES (?, ?, ?)
                                ON CONFLICT (a, b) DO UPDATE SET orders = excluded.orders""",
                             [(b, a, n) for a, b, n in rows])
            conn.executemany("DELETE FROM also_bought WHERE a = ? AND b = ?", [(a, b) for a, b, _n in rows])
            fixed += len(rows)
