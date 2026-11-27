"""Round segment lengths to centimetres."""


def run(conn):
    done, last = 0, 0
    while True:
        ids = [r[0] for r in conn.execute("SELECT id FROM segments WHERE id > ? ORDER BY id LIMIT 5000", (last,))]
        if not ids:
            return done
        with conn:
            conn.execute("UPDATE segments SET length_m = round(length_m, 2) WHERE id BETWEEN ? AND ?", (ids[0], ids[-1]))
        done += len(ids)
        last = ids[-1]
