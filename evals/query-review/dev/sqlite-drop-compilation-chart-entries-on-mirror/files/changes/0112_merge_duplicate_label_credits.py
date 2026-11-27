"""0112: drop 'label' credits that duplicate a 'producer' credit from the 2025 import. Reviewed: s.ito.
Applied to catalog 2026-09-18."""
CHUNK = 1500


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute(
                "DELETE FROM credits WHERE rowid IN (SELECT c.rowid FROM credits c WHERE c.role = 'label' AND EXISTS "
                "(SELECT 1 FROM credits p WHERE p.artist_id = c.artist_id AND p.release_id = c.release_id "
                "AND p.role = 'producer') LIMIT ?)", (CHUNK,)).rowcount
        if not n:
            return removed
        removed += n
