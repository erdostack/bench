"""015: archive superseded appears_in relations; 10 per commit (20 changed rows); resumable."""


def run(conn):
    moved = 0
    while True:
        ids = [r[0] for r in conn.execute(
            "SELECT id FROM relation NOT INDEXED WHERE kind = 'appears_in' AND status = 'superseded' LIMIT 10")]
        if not ids:
            return moved
        marks = ",".join("?" * len(ids))
        with conn:
            conn.execute(f"INSERT INTO relation_archive SELECT * FROM relation WHERE id IN ({marks})", ids)
            conn.execute(f"DELETE FROM relation WHERE id IN ({marks})", ids)
        moved += len(ids)
