"""Idempotent backfill: drop duplicate edges, add missing ones, recompute counts, per batch of images."""
BATCH = 15


def run(conn):
    last, done = 0, 0
    while True:
        ids = [r[0] for r in conn.execute("SELECT id FROM image WHERE id > ? ORDER BY id LIMIT ?", (last, BATCH))]
        if not ids:
            return done
        m = ",".join("?" * len(ids))
        with conn:
            conn.execute(f"""DELETE FROM image_component WHERE image_id IN ({m}) AND rowid NOT IN
                             (SELECT min(rowid) FROM image_component WHERE image_id IN ({m}) GROUP BY image_id, component_id)""",
                         ids + ids)
            conn.execute(f"""INSERT INTO image_component (image_id, component_id)
                             SELECT DISTINCT e.image_id, c.id FROM sbom_entry e JOIN component c ON c.purl = e.purl
                             WHERE e.image_id IN ({m}) AND NOT EXISTS (SELECT 1 FROM image_component x
                                   WHERE x.image_id = e.image_id AND x.component_id = c.id)""", ids)
            conn.execute(f"""UPDATE image SET component_count = (SELECT count(*) FROM image_component ic WHERE ic.image_id = image.id)
                             WHERE id IN ({m}) AND component_count <> (SELECT count(*) FROM image_component ic WHERE ic.image_id = image.id)""",
                         ids)
        done += len(ids)
        last = ids[-1]
