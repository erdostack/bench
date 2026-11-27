"""0009 (SW-19): backfill collected_by edges for collected reports from collector_code (docs/model.md);
unfounded/open reports and former members get none; existing edges skipped. 50 a commit; safe to re-apply."""
def run(conn):
    total = 0
    while True:
        with conn:
            cur = conn.execute(
                "INSERT INTO edges (kind, src, dst) SELECT 'collected_by', r.id, m.id FROM nodes r "
                "JOIN nodes m ON m.kind = 'member' AND m.code = r.collector_code "
                "LEFT JOIN edges e ON e.kind = 'collected_by' AND e.src = r.id "
                "WHERE r.kind = 'report' AND r.status = 'collected' AND e.id IS NULL LIMIT 50")
        if cur.rowcount == 0:
            return total
        total += cur.rowcount
