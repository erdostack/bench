"""Backfill segments.from_id / to_id (migration 007) from the junction refs."""


def run(conn):
    filled, last = 0, 0
    top = conn.execute("SELECT coalesce(max(id), 0) FROM segments").fetchone()[0]
    while last < top:
        with conn:
            filled += conn.execute("""
                UPDATE segments SET
                    from_id = (SELECT j.id FROM junctions j WHERE j.ref = segments.from_ref),
                    to_id   = (SELECT j.id FROM junctions j WHERE j.ref = segments.to_ref)
                WHERE id > ? AND id <= ?""", (last, last + 5000)).rowcount
        last += 5000
    return filled
