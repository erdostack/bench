BATCH = 1000


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM related WHERE id IN (
                SELECT id FROM related WHERE origin = 'auto' AND score < 0.35 LIMIT ?)""", (BATCH,)).rowcount
        if n == 0:
            return removed
        removed += n
