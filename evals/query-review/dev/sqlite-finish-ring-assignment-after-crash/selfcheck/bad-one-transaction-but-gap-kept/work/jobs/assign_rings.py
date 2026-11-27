"""Put every sensor that has no ring yet into one (id % 20: 0 canary, 1-4 early, otherwise broad).

Sensors are taken in id order, CHUNK at a time: the chunk's memberships are inserted, then the rings'
member_count is moved on."""
import logging

CHUNK = 500
log = logging.getLogger("jobs.assign_rings")

RING_OF = "CASE WHEN id % 20 = 0 THEN 1 WHEN id % 20 BETWEEN 1 AND 4 THEN 2 ELSE 3 END"


def run(conn):
    assigned = 0
    n_chunk = 0
    while True:
        ids = [r[0] for r in conn.execute(
            """SELECT id FROM devices WHERE kind = 'sensor'
               AND id NOT IN (SELECT device FROM ring_members) ORDER BY id LIMIT ?""", (CHUNK,))]
        if not ids:
            return assigned
        n_chunk += 1
        marks = ",".join("?" * len(ids))
        with conn:
            conn.execute(f"INSERT INTO ring_members (device, ring_id) SELECT id, {RING_OF} FROM devices WHERE id IN ({marks})",
                         ids)
            conn.execute(f"""UPDATE rings SET member_count = member_count +
                             (SELECT count(*) FROM devices WHERE id IN ({marks}) AND {RING_OF} = rings.id)""", ids)
        assigned += len(ids)
