import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)
CHUNK = 1000
LOG = Path(__file__).resolve().parent.parent / "var" / "log" / "convert_legacy_diameters.log"


def last_done():
    ids = [int(m) for m in re.findall(r"up to id (\d+)", LOG.read_text())] if LOG.exists() else []
    return max(ids, default=0)


def run(conn):
    start = last_done()
    ids = [r[0] for r in conn.execute("SELECT id FROM pipe WHERE source = 'gis2009' AND id > ? ORDER BY id", (start,))]
    for i in range(0, len(ids), CHUNK):
        chunk = ids[i:i + CHUNK]
        marks = ",".join("?" * len(chunk))
        with conn:
            conn.execute(f"UPDATE pipe SET diameter = round(diameter * 25.4, 1) WHERE id IN ({marks})", chunk)
    return len(ids)
