"""0010 (SW-19): collected_by for reports from 2024."""


def run(conn):
    with conn:
        return conn.execute(
            "INSERT INTO edges (kind, src, dst) SELECT 'collected_by', r.id, m.id FROM nodes r JOIN nodes m "
            "ON m.kind = 'member' AND m.code = r.collector_code WHERE r.kind = 'report' AND r.status = 'collected' "
            "AND r.reported_on >= '2024-01-01' AND r.reported_on < '2026-01-01'").rowcount
