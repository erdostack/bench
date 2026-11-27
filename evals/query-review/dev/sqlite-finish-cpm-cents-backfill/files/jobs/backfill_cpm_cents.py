"""MON-14: fill ad_slots.cpm_cents from cpm, 1,000 rows at a time. run(conn, start_id=0)."""

BATCH = 1000


def run(conn, start_id=0):
    last, done = int(start_id), 0
    while True:
        with conn:
            ids = [i for (i,) in conn.execute("SELECT id FROM ad_slots WHERE id > ? ORDER BY id LIMIT ?", (last, BATCH))]
            if not ids:
                return done
            conn.execute(f"UPDATE ad_slots SET cpm_cents = CAST(cpm * 100 AS INTEGER) "
                         f"WHERE id IN ({','.join('?' * len(ids))})", ids)
        done += len(ids)
        last = ids[-1]
