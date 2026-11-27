"""Backfill segments.from_id / to_id (migration 007) from the junction refs."""


def run(conn):
    by_ref = dict(conn.execute("SELECT ref, id FROM junctions"))
    rows = conn.execute("SELECT id, from_ref, to_ref FROM segments").fetchall()
    with conn:
        conn.executemany("UPDATE segments SET from_id = ?, to_id = ? WHERE id = ?",
                         [(by_ref.get(f), by_ref.get(t), i) for i, f, t in rows])
    return len(rows)
