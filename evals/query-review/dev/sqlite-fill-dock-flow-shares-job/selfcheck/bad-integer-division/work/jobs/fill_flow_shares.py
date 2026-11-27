BATCH = 2000


def run(conn):
    filled, last = 0, 0
    top = conn.execute("SELECT max(id) FROM flows").fetchone()[0]
    while last < top:
        with conn:
            filled += conn.execute("""UPDATE flows SET share = trips /
                                (SELECT nullif(sum(trips), 0) FROM flows f2 WHERE f2.from_dock = flows.from_dock)
                                WHERE id > ? AND id <= ?""", (last, last + BATCH)).rowcount
        last += BATCH
    return filled
