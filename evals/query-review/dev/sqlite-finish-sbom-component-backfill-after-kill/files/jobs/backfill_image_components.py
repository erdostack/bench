"""Fill image_component and image.component_count from sbom_entry, 25 images per transaction."""
import logging

BATCH = 25
log = logging.getLogger("backfill_image_components")


def run(conn):
    last, done = 0, 0
    while True:
        ids = [r[0] for r in conn.execute("SELECT id FROM image WHERE id > ? ORDER BY id LIMIT ?", (last, BATCH))]
        if not ids:
            return done
        marks = ",".join("?" * len(ids))
        with conn:
            conn.execute(f"""INSERT INTO image_component (image_id, component_id)
                             SELECT DISTINCT e.image_id, c.id FROM sbom_entry e JOIN component c ON c.purl = e.purl
                             WHERE e.image_id IN ({marks})""", ids)
            conn.execute(f"""UPDATE image SET component_count = component_count +
                                 (SELECT count(DISTINCT e.purl) FROM sbom_entry e WHERE e.image_id = image.id)
                             WHERE id IN ({marks})""", ids)
        log.info("images %d-%d linked", ids[0], ids[-1])
        done += len(ids)
        last = ids[-1]
