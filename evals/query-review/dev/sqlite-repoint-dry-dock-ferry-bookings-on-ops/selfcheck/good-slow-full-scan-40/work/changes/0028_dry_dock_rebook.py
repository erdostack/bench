"""0028: MV Corrie is in dry dock 2026-12-01..14 (docs/dry-dock.md). Re-points the booked_on edges of every
sailing with a relieved_by edge to its relief sailing, keeping seats; waitlist places and crews stay.
500 rows per transaction; safe to apply again (moved edges no longer match)."""
def run(conn):
    total = 0
    while True:
        conn.execute("BEGIN IMMEDIATE")
        cur = conn.execute(
            "UPDATE edges SET dst = (SELECT r.dst FROM edges r WHERE r.kind = 'relieved_by' AND r.src = edges.dst) "
            "WHERE id IN (SELECT e.id FROM edges e NOT INDEXED WHERE e.kind = 'booked_on' AND EXISTS "
            "(SELECT 1 FROM edges r WHERE r.kind = 'relieved_by' AND r.src = e.dst) LIMIT 40)")
        conn.execute("COMMIT")
        if cur.rowcount == 0:
            return total
        total += cur.rowcount
