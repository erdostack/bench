"""0042: chunks but recomputes the list each run without checking existing edges"""
def run(conn):
    rows = conn.execute("""SELECT g.src, g.dst, g.day FROM edges g JOIN nodes d ON d.id = g.src AND d.status = 'active'
WHERE g.kind = 'donated_at' AND g.day = (SELECT max(x.day) FROM edges x WHERE x.src = g.src AND x.kind = 'donated_at')
AND g.src NOT IN (SELECT src FROM edges WHERE kind = 'home_centre' AND day < '2026-09-01')""").fetchall()
    for i in range(0, len(rows), 500):
        with conn:
            conn.executemany("INSERT INTO edges (kind, src, dst, day) VALUES ('home_centre', ?, ?, ?)", rows[i:i + 500])
    return len(rows)
