"""Delete played_with pairs whose last match together ended before 2026-05-01 UTC.

last_played holds two formats (docs/clients.md): ISO-8601 text from PC and mobile hosts, unix seconds
(stored as integers) from console hosts. In SQLite an integer sorts before any text, so a plain
comparison with '2026-05-01' would match every console pair; each format is compared on its own terms."""
BATCH = 2000
STALE = """CASE WHEN typeof(last_played) IN ('integer', 'real') THEN last_played < unixepoch('2026-05-01')
                ELSE last_played < '2026-05-01' END"""


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute(f"""DELETE FROM played_with WHERE (a, b) IN (
                SELECT a, b FROM played_with WHERE {STALE} LIMIT ?)""", (BATCH,)).rowcount
        if not n:
            return removed
        removed += n
