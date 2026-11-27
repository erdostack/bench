"""0007"""


def run(conn):
    moved = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute("SELECT id FROM edges WHERE kind='loan' AND back_on < '2024-01-01' LIMIT 501")]
            if not ids:
                return moved
            q = ",".join(map(str, ids))
            conn.execute(f"INSERT INTO loan_archive SELECT * FROM edges WHERE id IN ({q})")
            conn.execute(f"DELETE FROM edges WHERE id IN ({q})")
        moved += len(ids)
