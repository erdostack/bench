"""0042 (DS-355): backfill home_centre for active donors who have given but have none (docs/model.md): the
centre and day of their most recent donation. Donors whose most recent donation was at a centre that has
since closed (Harbour Road, DC-09) are left out for donor care to set by hand, as change 0041 did.
Inserts 400 at a time; safe to run again."""

PICK = """
INSERT INTO edges (kind, src, dst, day)
SELECT 'home_centre', g.src, g.dst, g.day
FROM edges g
JOIN nodes d ON d.id = g.src AND d.kind = 'donor' AND d.status = 'active'
JOIN nodes c ON c.id = g.dst AND c.status = 'open'
WHERE g.kind = 'donated_at'
  AND g.day = (SELECT max(x.day) FROM edges x JOIN nodes xc ON xc.id = x.dst AND xc.status = 'open' WHERE x.src = g.src AND x.kind = 'donated_at')
  AND NOT EXISTS (SELECT 1 FROM edges h WHERE h.src = g.src AND h.kind = 'home_centre')
LIMIT 400
"""


def run(conn):
    added = 0
    while True:
        with conn:
            n = conn.execute(PICK).rowcount
        if not n:
            return added
        added += n
