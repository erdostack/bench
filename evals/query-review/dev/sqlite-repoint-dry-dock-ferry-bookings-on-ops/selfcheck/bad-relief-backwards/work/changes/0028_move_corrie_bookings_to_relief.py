"""0028: MV Corrie is in dry dock 2026-12-01..14 (docs/dry-dock.md). Re-points the booked_on edges of every
sailing with a relieved_by edge to its relief sailing, keeping seats; waitlist places and crews stay.
500 rows per transaction; safe to apply again (moved edges no longer match)."""
def run(conn):
    moved = 0
    while True:
        with conn:
            n = conn.execute(
                "UPDATE edges SET dst = (SELECT r.src FROM edges r WHERE r.kind = 'relieved_by' AND r.dst = edges.dst) "
                "WHERE id IN (SELECT e.id FROM edges e JOIN edges r ON r.dst = e.dst AND r.kind = 'relieved_by' "
                "WHERE e.kind = 'booked_on' LIMIT 500)").rowcount
        if not n:
            return moved
        moved += n
