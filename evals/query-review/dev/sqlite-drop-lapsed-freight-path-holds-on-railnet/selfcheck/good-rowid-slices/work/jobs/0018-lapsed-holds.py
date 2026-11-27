"""0018: remove lapsed holds (until before 2026-11-01), committed per id slice of at most 2,000 rows."""


def run(conn):
    ids = [r[0] for r in conn.execute("SELECT id FROM edges WHERE kind = 'holds' AND until IS NOT NULL "
                                      "AND until < '2026-11-01' ORDER BY id")]
    for i in range(0, len(ids), 2000):
        chunk = ids[i:i + 2000]
        conn.execute(f"DELETE FROM edges WHERE id IN ({','.join('?' * len(chunk))})", chunk)
        conn.commit()
    return len(ids)
