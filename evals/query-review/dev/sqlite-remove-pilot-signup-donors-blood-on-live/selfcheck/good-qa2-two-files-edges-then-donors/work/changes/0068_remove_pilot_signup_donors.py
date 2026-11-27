"""0068 (DPR-27) step 2, after 0067: delete the pilot signups who never donated together with their signed_up_via
edge, 200 donors a commit (400 rows). Applying it again deletes nothing."""

PICK = """SELECT s.src FROM edges s
WHERE s.kind = 'signed_up_via' AND s.dst = (SELECT id FROM nodes WHERE code = 'CMP-APP-PILOT')
  AND NOT EXISTS (SELECT 1 FROM edges d WHERE d.src = s.src AND d.kind = 'donated_at')
LIMIT 200"""


def run(conn):
    total = 0
    while True:
        ids = [r[0] for r in conn.execute(PICK)]
        if not ids:
            return total
        marks = ",".join("?" * len(ids))
        with conn:
            total += conn.execute(f"DELETE FROM edges WHERE src IN ({marks}) OR dst IN ({marks})", ids + ids).rowcount
            total += conn.execute(f"DELETE FROM nodes WHERE id IN ({marks})", ids).rowcount
