"""LS-77: convert gis2009 diameters from inches to mm. Safe to re-run: only rows still in inches
(nominal 2" to 48"; every converted value is at least 50.8 mm) are selected."""
import logging

log = logging.getLogger(__name__)
CHUNK = 1000


def run(conn):
    total = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute(
                "SELECT id FROM pipe WHERE source = 'gis2009' AND diameter < 50 ORDER BY id LIMIT ?", (CHUNK,))]
            if not ids:
                break
            marks = ",".join("?" * len(ids))
            conn.execute(f"UPDATE pipe SET diameter = round(diameter * 25.4, 1) WHERE id IN ({marks})", ids)
        total += len(ids)
        log.info("converted %d pipes up to id %d", len(ids), ids[-1])
    return total
