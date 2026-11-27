"""0028: MV Corrie is in dry dock 2026-12-01..14 (docs/dry-dock.md). Re-points the booked_on edges of every
sailing with a relieved_by edge to its relief sailing, keeping seats; waitlist places and crews stay.
500 rows per transaction; safe to apply again (moved edges no longer match)."""
def run(conn):
    pairs = conn.execute("SELECT src, dst FROM edges WHERE kind = 'relieved_by'").fetchall()
    moved = 0
    for cancelled, relief in pairs:
        with conn:
            moved += conn.execute("UPDATE edges SET dst = ? WHERE kind = 'booked_on' AND dst = ?",
                                  (relief, cancelled)).rowcount
            # keep the relief sailing's bookings in step (rewrites them every time it runs)
            conn.execute("UPDATE edges SET seats = seats WHERE kind = 'booked_on' AND dst = ?", (relief,))
    return moved
