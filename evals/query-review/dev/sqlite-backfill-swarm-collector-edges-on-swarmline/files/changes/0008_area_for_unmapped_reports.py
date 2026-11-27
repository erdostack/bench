"""0008 (SW-11): reports taken by phone before the map existed had no in_area edge. Add one from the
postcode district each report was filed under. Tried on practice, applied to swarmline 2026-02-21."""
CHUNK = 500


def run(conn):
    added = 0
    while True:
        with conn:
            n = conn.execute(
                "INSERT INTO edges (kind, src, dst) SELECT 'in_area', r.id, a.id FROM nodes r "
                "JOIN nodes a ON a.kind = 'area' AND a.name = r.name "
                "WHERE r.kind = 'report' AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.kind = 'in_area' AND e.src = r.id) "
                "LIMIT ?", (CHUNK,)).rowcount
        if not n:
            return added
        added += n
