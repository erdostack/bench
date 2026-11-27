"""0018: clear lapsed path holds (until before 2026-11-01)."""


def run(conn):
    with conn:
        return conn.execute("DELETE FROM edges WHERE kind = 'holds' AND until < '2026-11-01'").rowcount
