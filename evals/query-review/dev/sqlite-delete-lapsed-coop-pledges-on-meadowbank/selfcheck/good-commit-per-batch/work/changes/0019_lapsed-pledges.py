"""0019 lapsed pledges: remove them in batches.

Why: the portal's share register page is slow; lapsed pledges are unused (docs/register.md)."""


def run(conn):
    ids = [r[0] for r in conn.execute("SELECT id FROM edges WHERE kind = 'pledge' AND status = 'lapsed' ORDER BY id")]
    total = 0
    for i in range(0, len(ids), 800):
        part = ids[i:i + 800]
        cur = conn.execute(f"DELETE FROM edges WHERE id IN ({','.join('?' * len(part))})", part)
        conn.commit()
        total += cur.rowcount
    return {"deleted": total}
