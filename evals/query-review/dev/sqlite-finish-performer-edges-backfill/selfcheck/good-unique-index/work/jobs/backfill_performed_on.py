"""Backfill performed_on from the session sheets. Re-runnable: a unique index on the sessions edges makes
INSERT OR IGNORE skip the ones already written. Returns the number of edges added."""
CHUNK = 2000


def run(conn):
    with conn:
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS performed_on_sessions_key "
                     "ON performed_on(artist_id, recording_id, role) WHERE source = 'sessions'")
    top = conn.execute("SELECT max(id) FROM session_credits").fetchone()[0] or 0
    added = 0
    for lo in range(1, top + 1, CHUNK):
        with conn:
            added += conn.execute(
                "INSERT OR IGNORE INTO performed_on (artist_id, recording_id, role, source) "
                "SELECT a.id, s.recording_id, s.role, 'sessions' FROM session_credits s "
                "JOIN artists a ON a.name_key = s.artist_key WHERE s.id BETWEEN ? AND ?", (lo, lo + CHUNK - 1)).rowcount
    return added
