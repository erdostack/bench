"""0013: delete TST-SWISS-1123."""


def run(conn):
    n = 0
    with conn:
        n += conn.execute("DELETE FROM edges WHERE event = 2102 OR dst = 2102").rowcount
        n += conn.execute("DELETE FROM nodes WHERE id = 2102").rowcount
    return n
