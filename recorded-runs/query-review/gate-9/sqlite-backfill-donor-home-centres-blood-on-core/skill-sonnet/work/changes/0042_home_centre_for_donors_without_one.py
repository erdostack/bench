"""0042: active donors who have given but have no home_centre (the booking app only sets it for donations since
September 2026). Add one from the donor's most recent donation: that donation's centre and day (docs/model.md).
Withdrawn donors, donors who have never given and donors who already have a home_centre are not touched.
Picks up where it left off if run again."""
CHUNK = 400


def run(conn):
    added = 0
    while True:
        with conn:
            n = conn.execute(
                "INSERT INTO edges (kind, src, dst, day) "
                "SELECT 'home_centre', d.id, l.dst, l.day FROM nodes d "
                "JOIN edges l ON l.src = d.id AND l.kind = 'donated_at' "
                "AND l.day = (SELECT max(x.day) FROM edges x WHERE x.src = d.id AND x.kind = 'donated_at') "
                "WHERE d.kind = 'donor' AND d.status = 'active' "
                "AND NOT EXISTS (SELECT 1 FROM edges h WHERE h.src = d.id AND h.kind = 'home_centre') "
                "ORDER BY d.id LIMIT ?", (CHUNK,)).rowcount
        if not n:
            return added
        added += n
