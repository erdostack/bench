"""0009 (SW-19): backfill collected_by for collected reports from before the 2026 season, from collector_code.
Unfounded and open reports get none (docs/model.md); reports that have one are skipped. 500 per commit; safe to re-apply."""
CHUNK = 500


def run(conn):
    added = 0
    while True:
        with conn:
            n = conn.execute(
                "INSERT INTO edges (kind, src, dst) SELECT 'collected_by', r.id, m.id FROM nodes r "
                "LEFT JOIN nodes m ON m.kind = 'member' AND m.code = r.collector_code "
                "WHERE r.kind = 'report' AND r.status = 'collected' "
                "AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.kind = 'collected_by' AND e.src = r.id) LIMIT ?",
                (CHUNK,)).rowcount
        if not n:
            return added
        added += n
