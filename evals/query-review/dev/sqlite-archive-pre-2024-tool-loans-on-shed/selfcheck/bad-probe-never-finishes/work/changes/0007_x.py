"""0007"""


def run(conn):
    moved = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute("SELECT id FROM edges WHERE kind='loan' AND back_on < '2024-01-01' LIMIT 400")]
            q = ",".join(map(str, ids)) or "0"
            conn.execute(f"INSERT OR IGNORE INTO loan_archive SELECT * FROM edges WHERE id IN ({q})")
        moved += len(ids)
