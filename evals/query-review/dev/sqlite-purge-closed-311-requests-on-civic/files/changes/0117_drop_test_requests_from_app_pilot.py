"""0117: remove the requests the app vendor created while piloting the new intake form (refs SR-TEST-*),
with their edges. Reviewed: j.okafor. Applied to civic 2026-09-14."""
CHUNK = 1000


def run(conn):
    removed = 0
    while True:
        with conn:
            ids = [r[0] for r in conn.execute(
                "SELECT id FROM node WHERE kind = 'request' AND ref LIKE 'SR-TEST-%' LIMIT ?", (CHUNK,))]
            if not ids:
                return removed
            marks = ",".join("?" * len(ids))
            conn.execute(f"DELETE FROM edge WHERE src IN ({marks}) OR dst IN ({marks})", ids + ids)
            conn.execute(f"DELETE FROM node WHERE id IN ({marks})", ids)
        removed += len(ids)
