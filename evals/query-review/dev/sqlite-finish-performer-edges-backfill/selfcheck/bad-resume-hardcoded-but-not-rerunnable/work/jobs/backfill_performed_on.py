"""Backfill performed_on from the session sheets (session_credits), 2,000 sheet rows per transaction.

Sheet rows whose artist_key matches no artist are skipped (the editors add those artists by hand).
Returns the number of edges added."""
import logging

CHUNK = 2000
log = logging.getLogger("backfill_performed_on")

INSERT = """
INSERT INTO performed_on (artist_id, recording_id, role, source)
SELECT a.id, s.recording_id, s.role, 'sessions'
FROM session_credits s JOIN artists a ON a.name_key = s.artist_key
WHERE s.id BETWEEN ? AND ?
"""


def run(conn):
    top = conn.execute("SELECT max(id) FROM session_credits").fetchone()[0] or 0
    added = 0
    for lo in range(18001, top + 1, CHUNK):   # rows 1-18,000 were done on 2026-11-23
        with conn:
            n = conn.execute(INSERT, (lo, lo + CHUNK - 1)).rowcount
        added += n
        log.info("sheet rows %d-%d: %d edges", lo, lo + CHUNK - 1, n)
    return added
