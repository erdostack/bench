"""0042: resets every active donor's home centre to the latest donation"""
def run(conn):
    n = 0
    while True:
        with conn:
            k = conn.execute("DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind='home_centre' LIMIT 500)").rowcount
        if not k:
            break
    while True:
        with conn:
            k = conn.execute("""INSERT INTO edges (kind, src, dst, day)
SELECT 'home_centre', g.src, g.dst, g.day FROM edges g JOIN nodes d ON d.id = g.src AND d.status = 'active'
WHERE g.kind = 'donated_at' AND g.day = (SELECT max(x.day) FROM edges x WHERE x.src = g.src AND x.kind = 'donated_at')
AND NOT EXISTS (SELECT 1 FROM edges h WHERE h.src = g.src AND h.kind = 'home_centre') LIMIT 500""").rowcount
        if not k:
            return n
        n += k
