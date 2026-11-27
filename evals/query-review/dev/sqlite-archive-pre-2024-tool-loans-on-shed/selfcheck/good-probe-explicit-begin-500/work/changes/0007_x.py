"""0007: archive loans back before 2024 with explicit transactions of 500 loans."""


def run(conn):
    conn.isolation_level = None
    moved = 0
    while True:
        conn.execute("BEGIN IMMEDIATE")
        ids = [r[0] for r in conn.execute("SELECT id FROM edges WHERE kind='loan' AND back_on IS NOT NULL AND back_on < '2024-01-01' LIMIT 500")]
        if not ids:
            conn.execute("COMMIT")
            return moved
        q = ",".join(map(str, ids))
        conn.execute(f"INSERT INTO loan_archive (id, kind, src, dst, out_on, back_on) SELECT id, kind, src, dst, out_on, back_on FROM edges WHERE id IN ({q})")
        conn.execute(f"DELETE FROM edges WHERE id IN ({q})")
        conn.execute("COMMIT")
        moved += len(ids)
