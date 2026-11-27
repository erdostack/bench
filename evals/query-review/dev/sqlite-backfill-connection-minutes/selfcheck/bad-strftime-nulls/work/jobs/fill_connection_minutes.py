CHUNK = 2000


def run(conn):
    filled = 0
    last = 0
    while True:
        ids = [r[0] for r in conn.execute("SELECT id FROM connections WHERE id > ? ORDER BY id LIMIT ?", (last, CHUNK))]
        if not ids:
            return filled
        with conn:
            conn.execute("""UPDATE connections SET
                dep_min = CAST(strftime('%H', dep) AS INTEGER) * 60 + CAST(strftime('%M', dep) AS INTEGER),
                arr_min = CAST(strftime('%H', arr) AS INTEGER) * 60 + CAST(strftime('%M', arr) AS INTEGER)
                WHERE id BETWEEN ? AND ?""", (ids[0], ids[-1]))
        filled += len(ids)
        last = ids[-1]
