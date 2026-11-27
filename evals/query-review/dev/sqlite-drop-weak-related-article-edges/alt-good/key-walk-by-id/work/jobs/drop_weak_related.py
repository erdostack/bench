def run(conn):
    last, removed = 0, 0
    top = conn.execute("SELECT coalesce(max(id), 0) FROM related").fetchone()[0]
    while last < top:
        with conn:
            removed += conn.execute("DELETE FROM related WHERE id > ? AND id <= ? AND origin = 'auto' AND score < 0.35",
                                    (last, last + 1000)).rowcount
        last += 1000
    return removed
