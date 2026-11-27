"""Backfill segments.from_id / to_id (migration 007) from the junction refs."""
CHUNK = 5000


def run(conn):
    # junctions_ref_ci is COLLATE NOCASE and cannot serve `ref = ?` on the BINARY column, so a correlated
    # lookup would scan all junctions per segment. Resolve the refs in memory instead.
    by_ref = dict(conn.execute("SELECT ref, id FROM junctions"))
    filled, last = 0, 0
    while True:
        rows = conn.execute("SELECT id, from_ref, to_ref FROM segments WHERE id > ? ORDER BY id LIMIT ?",
                            (last, CHUNK)).fetchall()
        if not rows:
            return filled
        with conn:
            conn.executemany("UPDATE segments SET from_id = ?, to_id = ? WHERE id = ?",
                             [(by_ref.get(f), by_ref.get(t), i) for i, f, t in rows])
        filled += len(rows)
        last = rows[-1][0]
