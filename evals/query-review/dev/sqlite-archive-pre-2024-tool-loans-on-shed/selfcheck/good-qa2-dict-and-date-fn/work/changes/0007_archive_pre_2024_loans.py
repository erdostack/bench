"""0007: archive loans back before 2024-01-01 (docs/archive.md), 400 a transaction."""

def run(conn):
    total = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute("SELECT id FROM edges WHERE kind = 'loan' AND date(back_on) < date('2024-01-01') LIMIT 400")]
            if not ids:
                return {'archived': total, 'rows_changed': 2 * total}
            q = ",".join("?" * len(ids))
            conn.execute(f"INSERT INTO loan_archive SELECT * FROM edges WHERE id IN ({q})", ids)
            conn.execute(f"DELETE FROM edges WHERE id IN ({q})", ids)
        total += len(ids)
