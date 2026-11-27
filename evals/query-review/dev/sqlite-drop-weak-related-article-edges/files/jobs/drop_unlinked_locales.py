"""Remove related edges between articles of different locales (the widget only shows same-locale)."""
BATCH = 1000


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM related WHERE id IN (
                SELECT r.id FROM related r JOIN articles a ON a.id = r.src JOIN articles b ON b.id = r.dst
                WHERE a.locale <> b.locale LIMIT ?)""", (BATCH,)).rowcount
        removed += n
        if n < BATCH:
            return removed
