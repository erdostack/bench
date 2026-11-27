def run(conn):
    ids = [r[0] for r in conn.execute(
        "SELECT e.id FROM edges e WHERE e.kind = 'approved_for' AND e.expires_on IS NOT NULL "
        "AND e.expires_on < '2026-01-01' AND NOT EXISTS (SELECT 1 FROM holds h WHERE h.supplier_id = e.src "
        "AND h.closed_on IS NULL)")]
    n = 0
    for i in range(0, len(ids), 500):
        part = ids[i:i + 500]
        with conn:
            n += conn.execute(f"DELETE FROM edges WHERE id IN ({','.join('?' * len(part))})", part).rowcount
    return {"removed": n}
