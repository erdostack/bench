def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM played_with WHERE (a, b) IN (
                SELECT a, b FROM played_with WHERE datetime(last_played) < datetime('2026-05-01') LIMIT 2000)""").rowcount
        if not n:
            return removed
        removed += n
