# unixepoch(x, 'auto') reads both unix seconds and ISO text (SQLite 3.38+).
def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute("""DELETE FROM played_with WHERE (a, b) IN (
                SELECT a, b FROM played_with WHERE unixepoch(last_played, 'auto') < unixepoch('2026-05-01') LIMIT 1500)""").rowcount
        if not n:
            return removed
        removed += n
