"""0017 (CAP-552): drop the holds on the spot paths cancelled by the October blockade.
Reviewed: r.tamang. Run by the on-call 2026-10-09."""
BLOCKADE = ("P-6V71-SPT", "P-6V73-SPT", "P-6V75-SPT")


def run(conn):
    while True:
        with conn:
            n = conn.execute("DELETE FROM edges WHERE id IN (SELECT e.id FROM edges e JOIN nodes p ON p.id = e.dst "
                             "WHERE e.kind = 'holds' AND p.code IN (?, ?, ?) LIMIT 1000)", BLOCKADE).rowcount
        if not n:
            return
