"""0018: delete resolved missed reports dated before 2026-10-01 (the tablets' missed-bin screen is slow).
Resolved reports are read by nothing once the monthly export has run (docs/collections.md); open and
rejected reports stay. Commits 2,500 rows at a time and picks up where it left off if applied again.
Apply with: bin/apply kerbside changes/0018_purge_resolved_missed_before_october.py"""
CUTOFF = "2026-10-01"
CHUNK = 2500


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute(
                "DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'missed' AND status = 'resolved' "
                "AND reported_on < ? LIMIT ?)", (CUTOFF, CHUNK)).rowcount
        if not n:
            return removed
        removed += n
