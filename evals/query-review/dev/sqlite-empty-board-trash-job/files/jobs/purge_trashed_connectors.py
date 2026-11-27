"""Permanently delete connectors that have been in the trash for 30 days."""
CUTOFF_SQL = "datetime('now', '-30 days')"


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute(f"""DELETE FROM connectors WHERE id IN (
                SELECT id FROM connectors WHERE trashed_at < {CUTOFF_SQL} LIMIT 1000)""").rowcount
        if not n:
            return removed
        removed += n
