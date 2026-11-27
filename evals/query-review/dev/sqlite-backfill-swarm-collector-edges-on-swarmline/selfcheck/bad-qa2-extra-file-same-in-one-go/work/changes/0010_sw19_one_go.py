"""0010 (SW-19): the same backfill in one go, if the co-ordinator prefers."""
def run(conn):
    with conn:
        return conn.execute("INSERT INTO edges (kind, src, dst) SELECT 'collected_by', r.id, m.id FROM nodes r "
                            "JOIN nodes m ON m.kind = 'member' AND m.code = r.collector_code WHERE r.kind = 'report' "
                            "AND r.status = 'collected' AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.kind = 'collected_by' AND e.src = r.id)").rowcount
