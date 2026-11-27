"""0007: archive everything back or booked before 2024."""


def run(conn):
    total = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute(
                "SELECT id FROM edges WHERE coalesce(back_on, out_on) < '2024-01-01' LIMIT 400")]
            if not ids:
                return total
            q = ",".join("?" * len(ids))
            conn.execute(f"INSERT INTO loan_archive SELECT * FROM edges WHERE id IN ({q})", ids)
            conn.execute(f"DELETE FROM edges WHERE id IN ({q})", ids)
        total += len(ids)
