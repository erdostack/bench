"""Resume where last night's run stopped: images that already have edges are skipped."""
BATCH = 25


def run(conn):
    last, done = 0, 0
    while True:
        ids = [r[0] for r in conn.execute("""SELECT id FROM image WHERE id > ? AND NOT EXISTS
                                             (SELECT 1 FROM image_component ic WHERE ic.image_id = image.id)
                                             ORDER BY id LIMIT ?""", (last, BATCH))]
        if not ids:
            return done
        m = ",".join("?" * len(ids))
        with conn:
            conn.execute(f"""INSERT INTO image_component (image_id, component_id)
                             SELECT DISTINCT e.image_id, c.id FROM sbom_entry e JOIN component c ON c.purl = e.purl
                             WHERE e.image_id IN ({m})""", ids)
            conn.execute(f"""UPDATE image SET component_count = (SELECT count(*) FROM image_component ic WHERE ic.image_id = image.id)
                             WHERE id IN ({m})""", ids)
        done += len(ids)
        last = ids[-1]
