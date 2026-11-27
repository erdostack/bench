def run(conn):
    ids = [r[0] for r in conn.execute(
        "SELECT id FROM related WHERE origin = 'auto' AND score < 0.35 AND NOT pinned ORDER BY id")]
    for k in range(0, len(ids), 500):
        with conn:
            conn.executemany("DELETE FROM related WHERE id = ?", [(i,) for i in ids[k:k + 500]])
    return {"deleted": len(ids)}
