"""Fill flows.share, same pattern as backfill_dock_codes."""
BATCH = 2000


def run(conn):
    filled = 0
    while True:
        with conn:
            n = conn.execute("""UPDATE flows SET share = trips * 1.0 /
                                    (SELECT sum(trips) FROM flows f2 WHERE f2.from_dock = flows.from_dock)
                                WHERE id IN (SELECT id FROM flows WHERE share IS NULL LIMIT ?)""", (BATCH,)).rowcount
        if n == 0:
            return filled
        filled += n
