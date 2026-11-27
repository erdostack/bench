def run(conn):
    with conn:
        return conn.execute("DELETE FROM edges WHERE kind = 'approved_for' AND expires_on < '2026-01-01'").rowcount
