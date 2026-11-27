"""LS-77: pipes imported from the 2009 GIS carry their diameter in inches. Convert them to millimetres."""
import logging

log = logging.getLogger(__name__)
CHUNK = 1000


def run(conn):
    ids = [r[0] for r in conn.execute("SELECT id FROM pipe WHERE source = 'gis2009' ORDER BY id")]
    for i in range(0, len(ids), CHUNK):
        chunk = ids[i:i + CHUNK]
        marks = ",".join("?" * len(chunk))
        with conn:
            conn.execute(f"UPDATE pipe SET diameter = round(diameter * 25.4, 1) WHERE id IN ({marks})", chunk)
        log.info("converted %d pipes up to id %d", len(chunk), chunk[-1])
    return len(ids)
