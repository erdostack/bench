"""Delete auto-generated related edges scoring under 0.35.

Pinned edges are left alone: related_keep_pins (migration 0012) turns their delete into a no-op, so
they are excluded from the selection; otherwise they would fill the batches and stop the loop early."""
BATCH = 1000
CUT = 0.35


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM related WHERE id IN (
                SELECT id FROM related WHERE origin = 'auto' AND score < ? AND pinned = 0 LIMIT ?)""",
                             (CUT, BATCH)).rowcount
        if n == 0:
            return removed
        removed += n
