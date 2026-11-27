"""0007: archive the loans that came back before 2024-01-01 (docs/archive.md). Requested for the slow
"my loans" page. Copies each row, with its id, to loan_archive and deletes it from edges. Still-out loans
(back_on NULL) and reservations stay. Each batch of 500 loans is one transaction (1,000 changed rows,
the desk app's limit, docs/targets.md). Re-running picks up whatever is left and changes nothing once done.
Reviewed: (pending)."""

BATCH = 500


def run(conn):
    changed = 0
    while True:
        ids = [r[0] for r in conn.execute(
            "SELECT id FROM edges WHERE kind = 'loan' AND back_on < '2024-01-01' ORDER BY id LIMIT ?", (BATCH,))]
        if not ids:
            return changed
        marks = ",".join("?" * len(ids))
        with conn:
            n = conn.execute(f"INSERT INTO loan_archive SELECT * FROM edges WHERE id IN ({marks})", ids).rowcount
            conn.execute(f"DELETE FROM edges WHERE id IN ({marks})", ids)
        changed += 2 * n
