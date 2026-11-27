"""0058: move PZ-07's in_zone edges to PZ-11 (zone merge). Copy then delete, 500 edges (1,000 rows) per transaction."""
def run(conn):
    old = conn.execute("SELECT id FROM nodes WHERE code = 'PZ-07'").fetchone()[0]
    new = conn.execute("SELECT id FROM nodes WHERE code = 'PZ-11'").fetchone()[0]
    moved = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute("SELECT id FROM edges WHERE kind = 'in_zone' AND dst = ? LIMIT 500", (old,))]
            if not ids:
                return moved
            q = ",".join("?" * len(ids))
            conn.execute(f"INSERT INTO edges (kind, src, dst, since) SELECT kind, src, ?, since FROM edges WHERE id IN ({q})", [new, *ids])
            conn.execute(f"DELETE FROM edges WHERE id IN ({q})", ids)
        moved += len(ids)
