"""014: archive the superseded parent_of relations (2025 tidy-up, 600 rows). Reviewed: h.mbeki.
Applied to register 2025-11-30. Count before: SELECT count(*) FROM relation WHERE kind = 'parent_of'
AND status = 'superseded' AND created_on < '2025-01-01'."""
BATCH = 500


def run(conn):
    moved = 0
    while True:
        ids = [r[0] for r in conn.execute(
            "SELECT id FROM relation WHERE kind = 'parent_of' AND status = 'superseded' AND created_on < '2025-01-01' "
            "LIMIT ?", (BATCH,))]
        if not ids:
            return moved
        marks = ",".join("?" * len(ids))
        with conn:
            conn.execute(f"INSERT INTO relation_archive SELECT * FROM relation WHERE id IN ({marks})", ids)
            conn.execute(f"DELETE FROM relation WHERE id IN ({marks})", ids)
        moved += len(ids)
