"""0028: MV Corrie is in dry dock 2026-12-01..14 (docs/dry-dock.md). Re-points the booked_on edges of every
sailing with a relieved_by edge to its relief sailing, keeping seats; waitlist places and crews stay.
500 rows per transaction; safe to apply again (moved edges no longer match)."""
def run(conn):
    moved = 0
    while True:
        with conn:
            rows = conn.execute(
                "SELECT e.id, e.src, r.dst, e.seats FROM edges e JOIN edges r ON r.src = e.dst AND r.kind = 'relieved_by' "
                "WHERE e.kind = 'booked_on' LIMIT 250").fetchall()
            if not rows:
                return moved
            conn.executemany("INSERT INTO edges (kind, src, dst, seats) VALUES ('booked_on', ?, ?, ?)",
                             [(src, dst, seats) for _id, src, dst, seats in rows])
            conn.executemany("DELETE FROM edges WHERE id = ?", [(i,) for i, *_ in rows])
        moved += len(rows)
