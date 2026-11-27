"""Fill image_component and image.component_count from sbom_entry.

Re-runnable and safe to kill: each batch replaces the batch's images' edges with the distinct set and
sets component_count from them, in one transaction. That also repairs the images 1-1100 that the first
version (before the DISTINCT fix) linked once per SBOM line and counted per line. 10 images per batch
keeps the delete plus insert under 2,000 changed rows (docs/jobs.md)."""
import logging

BATCH = 10
log = logging.getLogger("backfill_image_components")


def run(conn):
    last, done = 0, 0
    while True:
        ids = [r[0] for r in conn.execute("SELECT id FROM image WHERE id > ? ORDER BY id LIMIT ?", (last, BATCH))]
        if not ids:
            return done
        marks = ",".join("?" * len(ids))
        with conn:
            conn.execute(f"DELETE FROM image_component WHERE image_id IN ({marks})", ids)
            conn.execute(f"""INSERT INTO image_component (image_id, component_id)
                             SELECT DISTINCT e.image_id, c.id FROM sbom_entry e JOIN component c ON c.purl = e.purl
                             WHERE e.image_id IN ({marks})""", ids)
            conn.execute(f"""UPDATE image SET component_count =
                                 (SELECT count(*) FROM image_component ic WHERE ic.image_id = image.id)
                             WHERE id IN ({marks})""", ids)
        log.info("images %d-%d linked", ids[0], ids[-1])
        done += len(ids)
        last = ids[-1]
