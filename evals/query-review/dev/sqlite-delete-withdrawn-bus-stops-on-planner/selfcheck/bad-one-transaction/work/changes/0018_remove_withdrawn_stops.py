"""0018: remove withdrawn stops and their edges."""

GONE = "SELECT id FROM nodes WHERE kind = 'stop' AND status = 'withdrawn'"


def run(conn):
    with conn:
        e = conn.execute(f"DELETE FROM edges WHERE src IN ({GONE}) OR dst IN ({GONE})").rowcount
        n = conn.execute(f"DELETE FROM nodes WHERE id IN ({GONE})").rowcount
    return n + e
