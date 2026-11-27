"""Put every sensor that has no ring yet into one (id % 20: 0 canary, 1-4 early, otherwise broad).

Each chunk's memberships and the ring counts are written in one transaction. The counts are recomputed
from ring_members (three rows), so a chunk whose count update was lost (2026-11-22, chunk 29) is repaired."""
import logging

CHUNK = 5000
log = logging.getLogger("jobs.assign_rings")

RING_OF = "CASE WHEN id % 20 = 0 THEN 1 WHEN id % 20 BETWEEN 1 AND 4 THEN 2 ELSE 3 END"
RECOUNT = "UPDATE rings SET member_count = (SELECT count(*) FROM ring_members m WHERE m.ring_id = rings.id)"


def run(conn):
    assigned = 0
    with conn:
        conn.execute(RECOUNT)
    while True:
        ids = [r[0] for r in conn.execute(
            """SELECT id FROM devices WHERE kind = 'sensor'
               AND id NOT IN (SELECT device FROM ring_members) ORDER BY id LIMIT ?""", (CHUNK,))]
        if not ids:
            return assigned
        marks = ",".join("?" * len(ids))
        with conn:
            conn.execute(f"INSERT INTO ring_members (device, ring_id) SELECT id, {RING_OF} FROM devices WHERE id IN ({marks})",
                         ids)
            conn.execute(RECOUNT)
        log.info("assigned devices %d-%d", ids[0], ids[-1])
        assigned += len(ids)
