"""0042 (DS-355): backfill home_centre for active donors who have given but have none (docs/model.md):
the centre and day of their most recent donation. Existing home_centre edges are left alone.
Inserts 500 at a time; picks up where it left off, and does nothing once every such donor has one."""

PICK = """
INSERT INTO edges (kind, src, dst, day)
SELECT 'home_centre', g.src, g.dst, g.day
FROM edges g
JOIN nodes d ON d.id = g.src AND d.kind = 'donor'
WHERE g.kind = 'donated_at'
  AND g.day = (SELECT max(x.day) FROM edges x WHERE x.src = g.src AND x.kind = 'donated_at')
  AND NOT EXISTS (SELECT 1 FROM edges h WHERE h.src = g.src AND h.kind = 'home_centre')
LIMIT 500
"""


def run(conn):
    added = 0
    while True:
        with conn:
            n = conn.execute(PICK).rowcount
        if not n:
            return added
        added += n
