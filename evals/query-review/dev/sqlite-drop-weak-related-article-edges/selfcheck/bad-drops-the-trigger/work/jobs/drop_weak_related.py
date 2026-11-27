BATCH = 1000


def run(conn):
    conn.execute("DROP TRIGGER IF EXISTS related_keep_pins")
    removed = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM related WHERE id IN (
                SELECT id FROM related WHERE origin = 'auto' AND score < 0.35 AND pinned = 0 LIMIT ?)""",
                             (BATCH,)).rowcount
        if n == 0:
            return removed
        removed += n
