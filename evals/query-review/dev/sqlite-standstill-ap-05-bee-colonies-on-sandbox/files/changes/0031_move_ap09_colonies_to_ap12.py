"""0031 (HB-44): Brow Lane (AP-09) merged into Calder Bank (AP-12); its colonies move to AP-12.
Reviewed: s.okafor. Applied to register 2026-05-09."""
CHUNK = 100


def run(conn):
    old = conn.execute("SELECT id FROM nodes WHERE code = 'AP-09'").fetchone()[0]
    new = conn.execute("SELECT id FROM nodes WHERE code = 'AP-12'").fetchone()[0]
    moved = 0
    while True:
        with conn:
            n = conn.execute(
                "UPDATE edges SET dst = ? WHERE id IN (SELECT id FROM edges WHERE kind = 'kept_at' AND dst = ? LIMIT ?)",
                (new, old, CHUNK)).rowcount
        if not n:
            return moved
        moved += n
