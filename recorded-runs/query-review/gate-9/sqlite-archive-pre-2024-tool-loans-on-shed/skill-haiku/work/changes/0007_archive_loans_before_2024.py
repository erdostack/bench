"""0007: archive the loans that came back before 2024-01-01 (docs/archive.md). Not yet reviewed.

Each loan with kind 'loan' and back_on < '2024-01-01' is copied, with its id, into loan_archive and then deleted
from edges. Loans still out (back_on NULL) and reservations are left alone. Batches of 400 loans are committed one
at a time, so a transaction changes at most 800 rows (400 inserts and 400 deletes; limit 1,000). A run that is
stopped part-way carries on where it stopped, and applying this file again changes nothing once it is done.

run(conn) returns the number of loans archived.
"""

BATCH = 400


def run(conn):
    moved = 0
    while True:
        ids = [r[0] for r in conn.execute(
            "SELECT id FROM edges WHERE kind = 'loan' AND back_on < '2024-01-01' ORDER BY id LIMIT ?", (BATCH,))]
        if not ids:
            return moved
        marks = ",".join("?" * len(ids))
        with conn:
            conn.execute("INSERT INTO loan_archive (id, kind, src, dst, out_on, back_on) "
                         f"SELECT id, kind, src, dst, out_on, back_on FROM edges WHERE id IN ({marks})", ids)
            conn.execute(f"DELETE FROM edges WHERE id IN ({marks})", ids)
        moved += len(ids)
