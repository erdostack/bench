"""Remove sections of next term's offerings that nobody can register for (0 seats)."""

BATCH = 500


def run(conn, term="2027SP"):
    removed = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM offerings WHERE offering_id IN (
                                  SELECT offering_id FROM offerings WHERE term = ? AND seats = 0 LIMIT ?)""",
                             (term, BATCH)).rowcount
        removed += n
        if n < BATCH:
            return removed
