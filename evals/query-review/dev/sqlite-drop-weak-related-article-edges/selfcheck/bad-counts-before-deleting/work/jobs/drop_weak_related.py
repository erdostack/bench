BATCH = 1000


def run(conn):
    total = conn.execute("SELECT count(*) FROM related WHERE origin = 'auto' AND score < 0.35").fetchone()[0]
    last = 0
    top = conn.execute("SELECT max(id) FROM related").fetchone()[0]
    while last < top:
        with conn:
            conn.execute("DELETE FROM related WHERE id > ? AND id <= ? AND origin = 'auto' AND score < 0.35",
                         (last, last + BATCH))
        last += BATCH
    return total
