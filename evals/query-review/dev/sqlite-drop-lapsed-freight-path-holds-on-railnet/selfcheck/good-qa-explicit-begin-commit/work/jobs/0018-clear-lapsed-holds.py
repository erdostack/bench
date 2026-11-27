"""0018 slow form copied from 0017: join on nodes, 1000 per batch, plus a rollback-free explicit loop"""
def run(conn):
    conn.isolation_level = None
    while True:
        conn.execute("BEGIN")
        n = conn.execute("DELETE FROM edges WHERE id IN (SELECT e.id FROM edges e JOIN nodes p ON p.id = e.dst "
                         "WHERE e.kind = 'holds' AND e.until < '2026-11-01' LIMIT 1000)").rowcount
        conn.execute("COMMIT")
        if not n:
            return
