"""Remove played_with pairs that involve a banned handle (handles listed in banned_handles)."""
BATCH = 2000


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM played_with WHERE (a, b) IN (
                SELECT a, b FROM played_with
                WHERE a IN (SELECT p.id FROM players p JOIN banned_handles h ON h.handle = p.handle)
                   OR b IN (SELECT p.id FROM players p JOIN banned_handles h ON h.handle = p.handle)
                LIMIT ?)""", (BATCH,)).rowcount
        if not n:
            return removed
        removed += n
