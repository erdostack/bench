"""Move leases that ended before 2025-01-01 to leases_archive (docs/archive.md).

Copies them in batches, then deletes them from leases in batches."""
import logging

CUTOFF = "2025-01-01"
BATCH = 1000
log = logging.getLogger("archive_ended_leases")


def run(conn):
    last, copied = 0, 0
    while True:
        with conn:
            rows = conn.execute("SELECT id FROM leases WHERE ends_on < ? AND id > ? ORDER BY id LIMIT ?",
                                (CUTOFF, last, BATCH)).fetchall()
            if not rows:
                break
            conn.execute("INSERT INTO leases_archive SELECT * FROM leases WHERE ends_on < ? AND id > ? AND id <= ?",
                         (CUTOFF, last, rows[-1][0]))
        log.info("copy: %d leases copied (ids %d-%d)", len(rows), last + 1, rows[-1][0])
        copied += len(rows)
        last = rows[-1][0]
    log.info("copy: done, %d leases copied", copied)
    while True:
        with conn:
            n = conn.execute("DELETE FROM leases WHERE id IN (SELECT id FROM leases WHERE ends_on < ? LIMIT ?)",
                             (CUTOFF, BATCH)).rowcount
        if not n:
            break
        log.info("delete: %d leases deleted", n)
    return copied
