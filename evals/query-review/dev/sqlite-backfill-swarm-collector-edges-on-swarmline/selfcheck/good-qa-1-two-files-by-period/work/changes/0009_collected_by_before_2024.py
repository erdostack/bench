"""0009 (SW-19): collected_by from collector_code, reports before 2024."""


def run(conn):
    total = 0
    while True:
        cur = conn.execute(
            "INSERT INTO edges (kind, src, dst) SELECT 'collected_by', r.id, m.id FROM nodes r, nodes m "
            "WHERE r.kind = 'report' AND r.status = 'collected' AND m.kind = 'member' AND m.code = r.collector_code "
            "AND r.reported_on < '2024-01-01' AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.src = r.id AND e.kind = 'collected_by') LIMIT 400")
        conn.commit()
        if cur.rowcount == 0:
            return total
        total += cur.rowcount
