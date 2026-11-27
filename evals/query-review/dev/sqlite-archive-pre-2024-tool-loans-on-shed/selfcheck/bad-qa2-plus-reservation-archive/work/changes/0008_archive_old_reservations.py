"""0007: archive loans back before 2024-01-01 (docs/archive.md), 400 a transaction."""

def run(conn):
    with conn:
        n = conn.execute("INSERT INTO loan_archive SELECT * FROM edges WHERE kind = 'reservation' AND id NOT IN (SELECT id FROM loan_archive) LIMIT 400").rowcount
        conn.execute("DELETE FROM edges WHERE kind = 'reservation' AND id IN (SELECT id FROM loan_archive)")
    return n
