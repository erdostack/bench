"""Backfill performed_on from the session sheets (session_credits), 2,000 sheet rows per transaction.

Sheet rows whose artist_key matches no artist are skipped (the editors add those artists by hand).
Safe to run again: a sheet credit whose (artist, recording, role) sessions edge already exists is not
added twice (last night's run wrote sheet rows 1-18,000 before it died). Returns the number of edges added."""
import logging

CHUNK = 2000
log = logging.getLogger("backfill_performed_on")

INSERT = """
INSERT INTO performed_on (artist_id, recording_id, role, source)
SELECT a.id, s.recording_id, s.role, 'sessions'
FROM session_credits s JOIN artists a ON a.name_key = s.artist_key
WHERE s.id BETWEEN ? AND ?
  AND NOT EXISTS (SELECT 1 FROM performed_on p
                  WHERE p.artist_id = a.id AND p.recording_id = s.recording_id AND p.role = s.role
                    AND p.source = 'sessions')
"""


def run(conn):
    top = conn.execute("SELECT max(id) FROM session_credits").fetchone()[0] or 0
    added = 0
    for lo in range(1, top + 1, CHUNK):
        with conn:
            n = conn.execute(INSERT, (lo, lo + CHUNK - 1)).rowcount
        added += n
        log.info("sheet rows %d-%d: %d edges", lo, lo + CHUNK - 1, n)
    return added
